-- Validate the data landed by the tap-checkly -> target-duckdb smoke test.
--
-- Usage: duckdb -bail output/wh.duckdb < tests/smoke/validate.sql
--
-- Prints a Markdown report of every assertion, suitable for a GitHub job summary.
-- If any of them fail, the last statement raises an error so the CLI exits with
-- a non-zero status.

.mode markdown
USE dev_checkly;

CREATE TEMP TABLE assertions AS
-- Streams that always have data in the smoke test account
SELECT 'checks is not empty' AS assertion, (SELECT count(*) > 0 FROM checks) AS passed
UNION ALL
SELECT 'locations is not empty', (SELECT count(*) > 0 FROM locations)
UNION ALL
SELECT 'runtimes is not empty', (SELECT count(*) > 0 FROM runtimes)
UNION ALL
SELECT 'locations include us-east-1', (SELECT count(*) = 1 FROM locations WHERE region = 'us-east-1')
-- The heartbeat check pinged at the end of the smoke test workflow
UNION ALL
SELECT 'checks include a heartbeat check', (SELECT count(*) > 0 FROM checks WHERE checktype = 'HEARTBEAT')

-- Primary keys are present and unique
UNION ALL
SELECT 'checks.id is unique and not null', (SELECT count(*) = count(DISTINCT id) AND count(id) = count(*) FROM checks)
UNION ALL
SELECT 'locations.region is unique and not null', (SELECT count(*) = count(DISTINCT region) AND count(region) = count(*) FROM locations)
UNION ALL
SELECT 'runtimes.name is unique and not null', (SELECT count(*) = count(DISTINCT name) AND count(name) = count(*) FROM runtimes)
UNION ALL
SELECT 'variables.key is unique and not null', (SELECT count(*) = count(DISTINCT key) AND count(key) = count(*) FROM variables)
UNION ALL
SELECT 'heartbeat_events.id is unique and not null', (SELECT count(*) = count(DISTINCT id) AND count(id) = count(*) FROM heartbeat_events)

-- Child stream records point at a parent check of the right type
UNION ALL
SELECT 'heartbeat_events belong to heartbeat checks', (
    SELECT count(*) = 0
    FROM heartbeat_events AS e
    LEFT JOIN checks AS c ON c.id = e.checkid AND c.checktype = 'HEARTBEAT'
    WHERE c.id IS NULL
)

-- Replication keys are loaded as timestamps, not strings
UNION ALL
SELECT 'replication keys are timestamps', (
    SELECT count(*) = 2 AND bool_and(data_type = 'TIMESTAMP')
    FROM information_schema.columns
    WHERE table_schema = 'dev_checkly'
        AND (table_name, column_name) IN (
            ('check_alerts', 'created_at'),
            ('heartbeat_events', 'timestamp')
        )
);

.print '## Smoke test: landed data'
.print ''
SELECT
    CASE WHEN passed THEN '✅' ELSE '❌' END AS status,
    assertion
FROM assertions;

.print ''
SELECT
    count(*) FILTER (WHERE passed) AS passed,
    count(*) FILTER (WHERE NOT passed) AS failed
FROM assertions;

-- Discard the (empty) result of the final check, so it doesn't end up in the report
.output /dev/null
SELECT error('Smoke test assertions failed: ' || string_agg(assertion, '; '))
FROM assertions
WHERE NOT passed
HAVING count(*) > 0;
