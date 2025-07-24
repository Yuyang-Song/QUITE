# SQL Query returning too many results
[Link to question](https://stackoverflow.com/questions/16658731/sql-query-returning-too-many-results)
**Creation Date:** 1369085435
**Score:** 0
**Tags:** mysql
## Question Body
<p>I have an sql query that is almost right but when a user has more than 1 aircraft in the database they end up with multiple row listings in the results returned from:</p>

<pre><code>SELECT  a.this_pay, 
    u.username, 
    u.user_id, 
    c.type_id,
    c.is_primary, 
    x.typename, 
    p.pf_city, 
    p.pf_state, 
    n.username AS non_username, 
    n.user_id AS non_user_id, 
    n.pf_city AS non_pf_city, 
    n.pf_state AS non_pf_state 
    FROM (((((jowner_event_attendees a 
    LEFT JOIN jowner_users u ON a.user_id = u.user_id) 
    LEFT JOIN jowner_aircraft c ON a.user_id = c.user_id) 
    LEFT JOIN jowner_aircraft_types x ON x.id = c.type_id) 
    LEFT JOIN jowner_profile_fields_data p ON a.user_id = p.user_id) 
    LEFT JOIN jowner_not_users n ON a.user_id = n.user_id) 
    WHERE a.event_id = 28 ORDER BY COALESCE(u.username,non_username);
</code></pre>

<p>I end up with a list that has multiple entries for anyone with multiple aircraft, I only want 1 entry returned no matter how many aircraft entries they have in the 'jowner_aircraft' table.</p>

<p>I also would prefer to not change this query drastically as other parts of the app rely on it, obviously it needs the revision I am asking for, but please try to answer it without a complete rewrite.</p>

## Answers
### Answer ID: 16658965
<p>You should just need to add another where clause to eliminate all but the record where is_primary is true.</p>

<pre><code>SELECT  a.this_pay, 
u.username, 
u.user_id, 
c.type_id,
c.is_primary, 
x.typename, 
p.pf_city, 
p.pf_state, 
n.username AS non_username, 
n.user_id AS non_user_id, 
n.pf_city AS non_pf_city, 
n.pf_state AS non_pf_state 
FROM jowner_event_attendees a 
LEFT JOIN jowner_users u ON a.user_id = u.user_id
LEFT JOIN jowner_aircraft c ON a.user_id = c.user_id 
LEFT JOIN jowner_aircraft_types x ON x.id = c.type_id
LEFT JOIN jowner_profile_fields_data p ON a.user_id = p.user_id
LEFT JOIN jowner_not_users n ON a.user_id = n.user_id 
WHERE a.event_id = 28 
AND c.is_primary = 1
ORDER BY COALESCE(u.username,non_username);
</code></pre>

<p>Substituting whatever the correct value for "true" is for is_primary.</p>

### Answer ID: 16658863
<p>Would a</p>

<pre><code>SELECT
a.this_pay, 
u.username, 
u.user_id, 
c.type_id, 
x.typename, 
p.pf_city, 
p.pf_state, 
n.username AS non_username, 
n.user_id AS non_user_id, 
n.pf_city AS non_pf_city, 
n.pf_state AS non_pf_state 
FROM (((((jowner_event_attendees a 
LEFT JOIN jowner_users u ON a.user_id = u.user_id) 
LEFT JOIN jowner_aircraft c ON a.user_id = c.user_id) 
LEFT JOIN jowner_aircraft_types x ON x.id = c.type_id) 
LEFT JOIN jowner_profile_fields_data p ON a.user_id = p.user_id) 
LEFT JOIN jowner_not_users n ON a.user_id = n.user_id) 
WHERE a.event_id = 28 ORDER BY COALESCE(u.username,non_username)
LIMIT 1;
</code></pre>

<p>be out of the question?</p>

<p>A bit of clarification would help, such as what this query is ultimately designed to do. If it was originally designed to return multiple rows and you're needing it to serve another purpose, it stands to reason you should give it a nice clean overhaul.</p>

### Answer ID: 16658933
<pre><code>SELECT  a.this_pay, 
    u.username, 
    u.user_id, 
    c.type_id, 
    x.typename, 
    p.pf_city, 
    p.pf_state, 
    n.username AS non_username, 
    n.user_id AS non_user_id, 
    n.pf_city AS non_pf_city, 
    n.pf_state AS non_pf_state 
    FROM (((((jowner_event_attendees a 
    LEFT JOIN jowner_users u ON a.user_id = u.user_id) 
    LEFT JOIN jowner_aircraft c ON a.user_id = c.user_id AND c.is_primary=1) 
    LEFT JOIN jowner_aircraft_types x ON x.id = c.type_id) 
    LEFT JOIN jowner_profile_fields_data p ON a.user_id = p.user_id) 
    LEFT JOIN jowner_not_users n ON a.user_id = n.user_id) 
    WHERE a.event_id = 28 ORDER BY COALESCE(u.username,non_username);
</code></pre>

