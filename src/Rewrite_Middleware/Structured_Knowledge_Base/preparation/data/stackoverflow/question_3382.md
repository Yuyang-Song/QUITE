# Convert GROUP BY in MySQL to Snowflake when SELECT includes more fields than in GROUP BY
[Link to question](https://stackoverflow.com/questions/77984696/convert-group-by-in-mysql-to-snowflake-when-select-includes-more-fields-than-in)
**Creation Date:** 1707777813
**Score:** -1
**Tags:** sql, snowflake-cloud-data-platform
## Question Body
<p>I'm currently working through a project where I'm converting queries that were written to execute on a MySQL database to Snowflake. One query is particular has really stumped me. I've pasted the MySQL query below and afterwards identify where I'm running into issues with its conversation for Snowflake.</p>
<pre><code>select 
  st.split_test_id,
  st.analytics_id,
  st.test,
  st.value,
  st.market_id,
  created_at,
  u.id,
  u.email,
  u.lead,
  u.created_at as user_created_at
from split_test st
left join user_analytics ua on ua.analytics_id = st.analytics_id
left join users u on u.id = ua.user_id
where 
((u.email NOT LIKE '%@picmonic.com%' and u.email NOT LIKE '%@truelearn.com%') OR u.email IS NULL)
  AND st.analytics_id not in(select user_analytics.analytics_id from app_v2.user_analytics join app_v2.users on user_analytics.user_id = users.id where email like '%@picmonic.com' or email like '%@truelearn.com%')
AND st.test = 'free_premium_trial_medicine_24q1'
group by coalesce(u.id, st.analytics_id)
</code></pre>
<p>The part about this query that is throwing me for a curve is how to convert the GROUP BY in the last line of the query. MySQL seems to allow you to use a GROUP BY without requiring you to include all of the non-aggregate fields in the GROUP BY. Specifically, the GROUP BY in this query is only grouping by u.id and st.analytics but the SELECT includes other non-aggregate fields, such as st.test and u.email. Snowflake does not support this behavior - all of the non-aggregate fields must be included in the GROUP BY or the query does not execute.</p>
<p>I tried rewriting the query to this form in Snowflake:</p>
<pre><code>SELECT
    COALESCE(u.id::string, st.analytics_id::string) AS id,
    st.split_test_id,
    st.analytics_id,
    u.id,
    st.test,
    st.value,
    st.market_id,
    st.created_at
FROM dq.dq_pm__split_test AS st
-- FROM mysql_picmonic_reporting_app_v2.split_test AS st
LEFT JOIN dq.dq_pm__user_analytics ua ON ua.analytics_id = st.analytics_id
-- LEFT JOIN mysql_picmonic_reporting_app_v2.user_analytics AS ua ON ua.analytics_id = st.analytics_id
LEFT JOIN dq.dq_pm__users u ON u.id = ua.user_id
-- LEFT JOIN mysql_picmonic_reporting_app_v2.users u ON u.id = ua.user_id
WHERE st.test = 'free_premium_trial_medicine_24q1'
AND ((u.email NOT ILIKE '%@picmonic.com%' AND u.email NOT ILIKE '%@truelearn.com%') OR u.email IS NULL)
AND st.analytics_id NOT IN (
    SELECT user_analytics.analytics_id 
    FROM dq.dq_pm__user_analytics AS user_analytics 
    JOIN dq.dq_pm__users AS users ON user_analytics.user_id = users.id 
    WHERE email ILIKE '%@picmonic.com' OR email ILIKE '%@truelearn.com%'
)
GROUP BY ALL
;
</code></pre>
<p>Specifically, I moved the COALESCE out of the GROUP BY into the SELECT and then tried to GROUP BY ALL (all fields). Unfortunately, this produces a different row count. The original MySQL query returns about 1,000 rows fewer than my Snowflake conversion.</p>

## Answers
### Answer ID: 77985106
<p>I suggest you turn on ONLY_FULL_GROUP_BY in MySQL which will prohibit you from falling into a trap that MySQL regrettably permits when that option is off. I recommend reading <a href="https://dev.mysql.com/doc/refman/8.0/en/group-by-handling.html" rel="nofollow noreferrer">MySQL Handling of GROUP BY</a>.</p>
<blockquote>
<p>If ONLY_FULL_GROUP_BY is disabled, ... , the server <strong>is
free to choose any value from each group</strong> [and] <strong>the values chosen
are nondeterministic</strong></p>
</blockquote>
<p><em>In short: the result can be misleading (aka &quot;nondeterministic&quot;).</em></p>
<p>If ONLY_FULL_GROUP_BY was on, then your existing MySQL query would need to look like the following (with every &quot;non-aggregating&quot; column repeated in the group by clause) - and this will produce many more rows than your existing query that is only valid if ONLY_FULL_GROUP_BY is off.</p>
<pre><code>SELECT
      st.split_test_id
    , st.analytics_id
    , st.test
    , st.value
    , st.market_id
    , created_at
    , u.id
    , u.email
    , u.lead
    , u.created_at AS user_created_at
FROM split_test st
LEFT JOIN user_analytics ua ON ua.analytics_id = st.analytics_id
LEFT JOIN users u ON u.id = ua.user_id AND (u.email NOT LIKE '%@picmonic.com%' OR u.email NOT LIKE '%@truelearn.com%')
WHERE st.test = 'free_premium_trial_medicine_24q1'
AND  st.analytics_id NOT IN (
        SELECT user_analytics.analytics_id
        FROM app_v2.user_analytics
        INNER JOIN app_v2.users ON user_analytics.user_id = users.id
        WHERE email LIKE '%@picmonic.com' OR email LIKE '%@truelearn.com%'
        ) 
GROUP BY
      st.split_test_id
    , st.analytics_id
    , st.test
    , st.value
    , st.market_id
    , created_at
    , u.id
    , u.email
    , u.lead
    , u.created_at
</code></pre>
<p>If you really only want to <code>group by coalesce(u.id, st.analytics_id)</code> then you have to decide what to do each of the other columns by applying an aggregation function to that column - OR - expanding the the columns in the group by clause - OR - exclude some columns from the result. e.g.</p>
<pre><code>SELECT
      coalesce(u.id, st.analytics_id) as identifer
    , max(st.test) as test
    , max(st.value) as value
    , max(st.market_id) as market_id
    , max(created_at) as created_at
    , max(u.email) as email
    , max(u.lead) as lead
    , max(u.created_at) AS user_created_at
FROM split_test st
LEFT JOIN user_analytics ua ON ua.analytics_id = st.analytics_id
LEFT JOIN users u ON u.id = ua.user_id AND (u.email NOT LIKE '%@picmonic.com%' OR u.email NOT LIKE '%@truelearn.com%')
WHERE st.test = 'free_premium_trial_medicine_24q1'
AND  st.analytics_id NOT IN (
        SELECT user_analytics.analytics_id
        FROM app_v2.user_analytics
        INNER JOIN app_v2.users ON user_analytics.user_id = users.id
        WHERE email LIKE '%@picmonic.com' OR email LIKE '%@truelearn.com%'
        ) 
GROUP BY
      coalesce(u.id, st.analytics_id)
</code></pre>
<p>An alternative approach might be to use <code>row_number() over(partition by ... order by ...)</code>. By using this technique you can control which rows you display raher than having MIN or MAX values calculated. e.g.</p>
<pre><code>SELECT 
    *
FROM (
    SELECT
          st.split_test_id
        , st.analytics_id
        , st.test
        , st.value
        , st.market_id
        , st.created_at
        , u.id
        , u.email
        , u.lead
        , u.created_at AS user_created_at
        , row_number() over(partition by coalesce(u.id, st.analytics_id) 
                            order by coalesce(st.created_at,st.created_at) DESC
                            ) as rn
    FROM split_test st
    LEFT JOIN user_analytics ua ON ua.analytics_id = st.analytics_id
    LEFT JOIN users u ON u.id = ua.user_id AND (u.email NOT LIKE '%@picmonic.com%' OR u.email NOT LIKE '%@truelearn.com%')
    WHERE st.test = 'free_premium_trial_medicine_24q1'
    AND  st.analytics_id NOT IN (
            SELECT user_analytics.analytics_id
            FROM app_v2.user_analytics
            INNER JOIN app_v2.users ON user_analytics.user_id = users.id
            WHERE email LIKE '%@picmonic.com' OR email LIKE '%@truelearn.com%'
            )
    ) derived
WHERE rn = 1
</code></pre>
<p>Here you get to choose in a &quot;row-wise&quot; fashion - here I have used the created_at dates (descending) to get &quot;the most recent&quot; rows.</p>

