# postgres, how to efficienctly calculate statistics over a series of intervals with multiple columns
[Link to question](https://stackoverflow.com/questions/67014079/postgres-how-to-efficienctly-calculate-statistics-over-a-series-of-intervals-wi)
**Creation Date:** 1617933335
**Score:** 0
**Tags:** postgresql, query-optimization
## Question Body
<p>I've been trying to find ways to optimize my query for the following problem. For a given plant, it contains a set of production lines that are either in production or marked in downtime, and over a set time period I need to find the availability as a percentage(%) calculated in the following form</p>
<pre><code>availability = (production_time - down_time) /  (production_time)
</code></pre>
<p>The set time period can be sliced into intervals of x by y , where x is an integer and y is a type of interval, ie 'Hour', 'Day', 'Week', 'Month', etc.</p>
<p>I have written a solution, but as the selected time period gets larger and the interval slices get smaller it starts to slows down and I'm not sure what else to optimize or whether I need to rewrite the solution all together into smaller components. Deconstructing the function and plugging values into the parameters and then analyzing it, the primary culprit is partitioning function thats windowing  over three columns two of which are not indexed:</p>
<pre><code>SUM(COALESCE(ac.unplanned_downtime_in_seconds, 0)) OVER (PARTITION BY ac.interval_ts,  ac.&quot;PLI_cID&quot;, production_shift ) downtime_sum,
                 SUM(ac.production_time - COALESCE(ac.planned_downtime_in_seconds, 0))  OVER (PARTITION BY ac.interval_ts,  ac.&quot;PLI_cID&quot;, production_shift ) AS production_sum,
</code></pre>
<p>Of course I don't expect a solution in milliseconds as I feel like the solution does require sorting in order to aggregate data in buckets of intervals, production lines(PLI_cID column) and by shifts but I have a suspicion that my way is the naîve way.</p>
<p><strong>My solution</strong></p>
<pre class="lang-sql prettyprint-override"><code>CREATE get_availabilities_by_interval_for_production_line(_client_id uuid,
_production_line_ids uuid[],
_shifts character varying[],
_start_timestamp timestamp without time zone,
_end_timestamp timestamp without time zone,
 _intervaltime integer,
 _intervaltype character varying)
    returns TABLE(production_line_id uuid, production_line_name character varying, startingtime timestamp without time zone, endtime timestamp without time zone, shift character varying, availability double precision)
    language plpgsql
as
$$
BEGIN
    RETURN QUERY
        WITH prods as (
            SELECT * 
                FROM (
                    SELECT generate_series(_start_timestamp,_end_timestamp- (_intervaltime || _intervaltype) :: interval, (_intervaltime || _intervaltype):: interval) interval_ts,
                           generate_series(_start_timestamp +  (_intervaltime || _intervaltype):: interval ,_end_timestamp,  (_intervaltime || _intervaltype):: interval) interval_ts_end
                    ) intervals  
                CROSS JOIN(
                    SELECT d.start_timestamp_utc at time zone 'utc' at time zone prod_lines.time_zone as dt_start1 ,
                           d.start_timestamp_utc at time zone 'utc' at time zone prod_lines.time_zone as dt_start,
                           d.end_timestamp_utc at time zone 'utc' at time zone prod_lines.time_zone as dt_end,
                           p.start_timestamp_utc at time zone 'utc' at time zone prod_lines.time_zone as p_start,
                           p.end_timestamp_utc at time zone 'utc' at time zone prod_lines.time_zone as p_end,
                           d.&quot;BPA_cID&quot;,
                           p.shift as production_shift,
                           d.is_planned,
                           d.&quot;PLB_cID&quot;,
                           d.is_deleted,
                           d.downtime_duration_seconds,
                           p.&quot;PLI_cID&quot;,
                           prod_lines.production_line_name,
                           prod_lines.time_zone
                    FROM productions p
                        LEFT JOIN production_lines prod_lines ON  p.&quot;PLI_cID&quot; = prod_lines.&quot;PLI_cID&quot;
                        LEFT JOIN downtimes d ON d.&quot;PLB_cID&quot; = p.&quot;PLB_cID&quot; AND d.is_deleted = 0
                    WHERE p.start_timestamp_utc at time zone 'utc' at time zone prod_lines.time_zone &lt;= _end_timestamp
                      AND p.end_timestamp_utc  at time zone 'utc' at time zone prod_lines.time_zone &gt;= _start_timestamp
                      AND p.&quot;PLI_cID&quot; = ANY(_production_line_ids)
                      AND p.&quot;CLI_cID&quot; = _client_id
                      AND p.is_deleted = 0
                      AND (_shifts IS NULL OR p.shift = ANY(_shifts))
                      AND (
                          d.start_timestamp_utc  at time zone 'utc' at time zone prod_lines.time_zone &gt;= p.start_timestamp_utc  at time zone 'utc' at time zone prod_lines.time_zone
                          AND d.end_timestamp_utc  at time zone 'utc' at time zone prod_lines.time_zone&lt;= p.end_timestamp_utc at time zone 'utc' at time zone prod_lines.time_zone
                        )
                    ) productions_and_dt 
            WHERE  &quot;PLI_cID&quot; IS NOT NULL
            ),

    /*
    *   We use a control table that contains a set of a possible time intervals (hour/day/week/month) within a given period of time
    *   It is entirely possible that part of a downtime falls in  the range of a interval but is not completely contained with in it
    *  so it will need to be bucketed into two seperate bins.
    *  Example:
    *  Bin           1    2    3    4    5    6    7    8    9   10   11   12
    *  Start time [ -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- | -- ] End time
    *  Downtimes      D    DDDD     DD
    *  The second one will be referenced by bin 2 and 3.
    *  Perform a downtime calculation based on the current frame(bin) of time it is currently in.
    */

             availabilities_components AS (
                 SELECT p2.dt_end,
                        p2.dt_start,
                        p2.p_end,
                        p2.p_start,
                        p2.interval_ts,
                        p2.interval_ts_end,
                        p2.&quot;PLI_cID&quot;,
                        p2.production_shift,
                        p2.production_line_name,
                        p2.&quot;PLB_cID&quot;,
                        EXTRACT (EPOCH FROM (p2.interval_ts_end - p2.interval_ts)) AS max_time_in_seconds,
                        COALESCE(
                            EXTRACT(
                                EPOCH FROM(
                                    CASE WHEN p2.p_end IS NOT NULL AND p2.p_end &lt;= p2.interval_ts_end
                                        THEN p2.p_end
                                        ELSE p2.interval_ts_end
                                        END
                                        -
                            CASE WHEN p2.p_start &lt; p2.interval_ts
                                THEN p2.interval_ts
                                ELSE p2.p_start
                                END
                                    )
                                ),0
                            ) AS production_time,
                        CASE WHEN p2.is_planned = 0
                            THEN COALESCE (
                                EXTRACT(
                                    EPOCH FROM (
                                        CASE WHEN p2.interval_ts_end &lt;= COALESCE(p2.dt_end, p2.interval_ts_end )
                                            THEN p2.interval_ts_end
                                            WHEN COALESCE(p2.p_end , NOW())&lt; COALESCE(p2.dt_end, NOW())
                                                THEN COALESCE(p2.p_end , p2.interval_ts_end )
                                            ELSE
                                                COALESCE(p2.dt_end, p2.interval_ts_end )
                                            END
                                            -
                                        CASE WHEN p2.interval_ts &gt; p2.dt_start
                                            THEN p2.interval_ts
                                            ELSE p2.dt_start
                                            END
                                        )
                                    ),0
                                )
                            ELSE 0
                            END AS unplanned_downtime_in_seconds,
                        CASE WHEN p2.is_planned = 1
                            THEN COALESCE (
                                EXTRACT(
                                    EPOCH FROM (
                                        CASE WHEN p2.interval_ts_end  &lt;= COALESCE(p2.dt_end, p2.interval_ts_end)
                                            THEN p2.interval_ts_end
                                            WHEN COALESCE(p2.p_end, NOW())&lt; COALESCE(p2.dt_end, NOW())
                                                THEN COALESCE(p2.p_end, p2.interval_ts_end )
                                            ELSE COALESCE(p2.dt_end, p2.interval_ts_end )
                                            END
                                            -
                                        CASE WHEN p2.interval_ts  &gt; p2.dt_start
                                            THEN p2.interval_ts
                                            ELSE p2.dt_start
                                            END
                                        )
                                    ),0
                                )
                            ELSE 0
                            END
                            AS planned_downtime_in_seconds,
                        CASE WHEN p2.&quot;BPA_cID&quot; IS NULL
                            THEN 0
                            ELSE 1
                            END
                            AS has_a_production
                 FROM prods p2
                 ),

             cleaned_availability_components AS(
                 SELECT ac2.&quot;PLI_cID&quot;,
                        ac2.interval_ts,
                        ac2.interval_ts_end,
                        ac2.dt_end,
                        ac2.dt_start,
                        ac2.p_end,
                        ac2.p_start,
                        ac2.production_shift,
                        ac2.production_line_name,
                        ac2.&quot;PLB_cID&quot;,
                        -- the production time falls outside of the interval and is invalid for calculations
                        CASE WHEN  ac2.production_time BETWEEN 0 AND ac2.max_time_in_seconds
                            THEN ac2.production_time
                            END as production_time,
                        CASE WHEN ac2.unplanned_downtime_in_seconds BETWEEN 0 AND ac2.max_time_in_seconds
                            THEN ac2.unplanned_downtime_in_seconds
                            END as unplanned_downtime_in_seconds,
                        CASE WHEN ac2.planned_downtime_in_seconds BETWEEN 0 AND ac2.max_time_in_seconds
                            THEN ac2.planned_downtime_in_seconds
                            END AS planned_downtime_in_seconds
                 FROM availabilities_components ac2
                 ),

      availabilities_variables_dirty AS(
          SELECT row_number() over (PARTITION BY ac.interval_ts, &quot;PLI_cID&quot;, production_shift ) as row_num,
                 SUM(COALESCE(ac.unplanned_downtime_in_seconds, 0)) OVER (PARTITION BY ac.interval_ts,  ac.&quot;PLI_cID&quot;, production_shift ) downtime_sum,
                 SUM(ac.production_time - COALESCE(ac.planned_downtime_in_seconds, 0))  OVER (PARTITION BY ac.interval_ts,  ac.&quot;PLI_cID&quot;, production_shift ) AS production_sum,
                 *
          FROM cleaned_availability_components ac
          order by ac.interval_ts, ac.&quot;PLI_cID&quot;, ac.production_shift
         ),

     availabilities_variables_cleaned AS (
         SELECT CASE WHEN av.production_sum = 0
             THEN 0
             ELSE (production_sum - downtime_sum) / production_sum
             END AS availability,
                *
         FROM availabilities_variables_dirty av
     )

        SELECT av.&quot;PLI_cID&quot;,
               av.production_line_name,
               av.interval_ts,
               av.interval_ts_end,
               av.production_shift,
               av.availability
        FROM availabilities_variables_cleaned av
        WHERE av.row_num = 1;
     END
$$;
</code></pre>
<p>Currently, the database holds the following three tables</p>
<p><strong>Downtime table</strong></p>
<pre><code>
COLUMN NAME             |   is_nullable         |   data_type                   |   character_maximum_length    | is_pk?
------------------------------------------------------------------------------------------------------------------------
BPA_cID                 |   NO                  |   uuid                        |   NULL                        | YES
CLI_cID                 |   NO                  |   uuid                        |   NULL                        | NO
start_timestamp_utc     |   NO                  |   timestamp without time zone |   NULL                        | NO
end_timestamp_utc       |   YES                 |   timestamp without time zone |   NULL                        | NO
PLB_cID                 |   YES                 |   uuid                        |   NULL                        | NO
is_planned              |   NO                  |   integer                     |   NULL                        | NO
is_deleted              |   NO                  |   integer                     |   NULL                        | NO

</code></pre>
<p>Indicies in use for downtimes</p>
<pre><code>&quot;CREATE UNIQUE INDEX downtimes_pkey ON dw_staging_v1.downtimes USING btree (&quot;&quot;BPA_cID&quot;&quot;, &quot;&quot;CLI_cID&quot;&quot;)&quot;
CREATE INDEX downtimes_start_timestamp_utc_idx ON dw_staging_v1.downtimes USING btree (start_timestamp_utc DESC)
CREATE INDEX downtimes_end_timestamp_utc_idx ON dw_staging_v1.downtimes USING btree (end_timestamp_utc DESC)
&quot;CREATE INDEX &quot;&quot;downtimes_CLI_cID_idx&quot;&quot; ON dw_staging_v1.downtimes USING btree (&quot;&quot;CLI_cID&quot;&quot;)&quot;
CREATE INDEX downtimes_is_deleted_idx ON dw_staging_v1.downtimes USING btree (is_deleted)
CREATE INDEX downtimes_production_line_name_idx ON dw_staging_v1.downtimes USING btree (production_line_name)

</code></pre>
<p><strong>Production table</strong></p>
<pre><code>COLUMN NAME             |   is_nullable         |   data_type                   |   character_maximum_length    | is_pk?
------------------------------------------------------------------------------------------------------------------------

PLB_cID                 |   NO                  |   uuid                        |   NULL                        | YES
start_timestamp_utc     |   NO                  |   timestamp without time zone |   NULL                        | NO
end_timestamp_utc       |   YES                 |   timestamp without time zone |   NULL                        | NO
is_deleted              |   NO                  |   integer                     |   NULL                        | NO
PLI_cID                 |   NO                  |   uuid                        |   NULL                        | NO

</code></pre>
<p>Indices in use for the production table</p>
<pre><code>&quot;CREATE UNIQUE INDEX productions_pkey ON dw_staging_v1.productions USING btree (&quot;&quot;PLB_cID&quot;&quot;, &quot;&quot;CLI_cID&quot;&quot;)&quot;
CREATE INDEX productions_start_timestamp_utc_idx ON dw_staging_v1.productions USING btree (start_timestamp_utc DESC)
CREATE INDEX productions_end_timestamp_utc_idx ON dw_staging_v1.productions USING btree (end_timestamp_utc DESC)
&quot;CREATE INDEX &quot;&quot;productions_CLI_cID_idx&quot;&quot; ON dw_staging_v1.productions USING btree (&quot;&quot;CLI_cID&quot;&quot;)&quot;
CREATE INDEX productions_is_deleted_idx ON dw_staging_v1.productions USING btree (is_deleted)
&quot;CREATE INDEX &quot;&quot;productions_PLI_cID_idx&quot;&quot; ON dw_staging_v1.productions USING btree (&quot;&quot;PLI_cID&quot;&quot;)&quot;

</code></pre>
<p><strong>Production lines table</strong></p>
<pre><code>COLUMN NAME             |   is_nullable         |   data_type                   |   character_maximum_length    | is_pk?
------------------------------------------------------------------------------------------------------------------------

PLI_cID                 |   NO                  |   uuid                        |   NULL                        | YES
start_timestamp_utc     |   NO                  |   timestamp without time zone |   NULL                        | NO
end_timestamp_utc       |   YES                 |   timestamp without time zone |   NULL                        | NO
is_deleted              |   NO                  |   integer                     |   NULL                        | NO
pli_dtdeleted           |   YES                 |   timestamp without time zone |   NULL                        | NO
time_zone               |   NO                  |   character varying           |   50                          | NO
production_line_name    |   YES                 |   character varying           |   50                          | NO
CLI_cID                 |   NO                  |   uuid                        |   NULL                        | NO
</code></pre>
<p>Indices in use for the production lines table</p>
<pre><code>&quot;CREATE UNIQUE INDEX production_lines_pkey ON dw_staging_v1.production_lines USING btree (&quot;&quot;PLI_cID&quot;&quot;, &quot;&quot;CLI_cID&quot;&quot;)&quot;
&quot;CREATE INDEX &quot;&quot;production_lines_CLI_cID_idx&quot;&quot; ON dw_staging_v1.production_lines USING btree (&quot;&quot;CLI_cID&quot;&quot;)&quot;
</code></pre>

