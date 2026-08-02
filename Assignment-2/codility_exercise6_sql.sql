-- Solutions to Codility Exercise 6 - SQL: SqlSum, SqlEventsDelta, SqlWorldCup.
-- Written and tested against SQLite; also valid on PostgreSQL (Codility supports
-- both engines for this exercise). Each query is preceded by the table schema
-- it targets, per the task statement, so it can be pasted straight into the
-- Codility editor.

-- ===========================================================================
-- 1. SqlSum -- "elementary": return the sum of column v in table `elements`.
-- ===========================================================================
-- create table elements (
--     v integer not null
-- );

SELECT SUM(v) AS total
FROM elements;


-- ===========================================================================
-- 2. SqlEventsDelta -- "easy": for each event_type seen more than once,
-- return (latest value - second latest value), ordered by event_type asc.
-- ===========================================================================
-- create table events (
--     event_type integer not null,
--     value integer not null,
--     time timestamp not null,
--     unique(event_type, time)
-- );

WITH ranked_events AS (
    SELECT
        event_type,
        value,
        ROW_NUMBER() OVER (PARTITION BY event_type ORDER BY time DESC) AS recency_rank,
        COUNT(*) OVER (PARTITION BY event_type) AS event_count
    FROM events
)
SELECT
    event_type,
    MAX(CASE WHEN recency_rank = 1 THEN value END)
        - MAX(CASE WHEN recency_rank = 2 THEN value END) AS value_delta
FROM ranked_events
WHERE event_count > 1 AND recency_rank <= 2
GROUP BY event_type
ORDER BY event_type;


-- ===========================================================================
-- 3. SqlWorldCup -- "medium": total league points per team (3 win / 1 draw /
-- 0 loss), including teams that haven't played, ordered by points desc then
-- team_id asc.
-- ===========================================================================
-- create table teams (
--     team_id integer not null,
--     team_name varchar(30) not null,
--     unique(team_id)
-- );
-- create table matches (
--     match_id integer not null,
--     host_team integer not null,
--     guest_team integer not null,
--     host_goals integer not null,
--     guest_goals integer not null,
--     unique(match_id)
-- );

WITH match_points AS (
    SELECT
        host_team AS team_id,
        CASE
            WHEN host_goals > guest_goals THEN 3
            WHEN host_goals = guest_goals THEN 1
            ELSE 0
        END AS points
    FROM matches

    UNION ALL

    SELECT
        guest_team AS team_id,
        CASE
            WHEN guest_goals > host_goals THEN 3
            WHEN guest_goals = host_goals THEN 1
            ELSE 0
        END AS points
    FROM matches
)
SELECT
    t.team_id,
    t.team_name,
    COALESCE(SUM(mp.points), 0) AS num_points
FROM teams AS t
LEFT JOIN match_points AS mp ON mp.team_id = t.team_id
GROUP BY t.team_id, t.team_name
ORDER BY num_points DESC, t.team_id ASC;
