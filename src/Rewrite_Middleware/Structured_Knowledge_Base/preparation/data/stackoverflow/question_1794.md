# Optimize query in sql server
[Link to question](https://stackoverflow.com/questions/8257038/optimize-query-in-sql-server)
**Creation Date:** 1322137633
**Score:** 0
**Tags:** sql-server, optimization, indexing
## Question Body
<p>I have a query in Sql Server that I will like to optimize. </p>

<pre><code>SELECT user_type_name = CASE user_type_id 
                          WHEN 1 THEN 'Admin' 
                          WHEN 5 THEN 'Super Admin' 
                          WHEN 3 THEN 'Writer' 
                          WHEN 4 THEN 'Reader' 
                        END, 
       user_can_log = CASE user_inactive 
                        WHEN 1 THEN 'No' 
                        ELSE 'Yes' 
                      END, 
       (SELECT COUNT(*) 
        FROM   t_fthread 
        WHERE  fthread_creator_userid = user_id)         AS number_tickets, 
       (SELECT COUNT(*) 
        FROM   t_email 
        WHERE  email_to LIKE '%' + user_email + '%' 
                OR email_cc LIKE '%' + user_email + '%') AS number_emails, 
       * 
FROM   t_user 
       LEFT JOIN t_organisation 
         ON user_org_id = organisation_id 
WHERE  user_org_id = 42 
ORDER  BY user_last_name, 
          user_first_name 
</code></pre>

<p>The query takes too much time to run. thanks to query analyzer, I've identified the part in the query that takes too much time,
It's this section:</p>

<pre><code>(select count(*) from t_email where email_to like '%'+user_email+'%' or email_cc like '%'+user_email+'%') as number_emails.
</code></pre>

<p>I'm trying to rewrite the query to still get the number_emails but in every case, it's still very slow. </p>

<p>I've tried to create the indexes, but it's impossible to create index on user_email and user_cc. Both columns are ntext types and on sql server 2000, it's not possible to create index on theses columns.
I've run analyze the query with Database Engine Tune Advisor and I've run the recommendations provided by the tools.</p>

<pre><code>CREATE NONCLUSTERED INDEX [_dta_index_t_fthread_15_2073058421__K5] ON [dbo].[t_fthread]
(
[fthread_creator_userid] ASC
)

CREATE STATISTICS [_dta_stat_1365579903_4_3] ON [dbo].[t_user]([user_last_name], [user_first_name])

CREATE STATISTICS [_dta_stat_1365579903_1_5] ON [dbo].[t_user]([user_id], [user_org_id])

CREATE NONCLUSTERED INDEX [_dta_index_t_user_15_1365579903__K5_K1] ON [dbo].[t_user]
(
[user_org_id] ASC,
[user_id] ASC
)
</code></pre>

<p>But the query still takes lot of time to finish the execution.</p>

## Answers
### Answer ID: 8257396
<p>Your query indicates bad design. You should either </p>

<ul>
<li>normalize your database if all users from to and cc are in your database, or</li>
<li>keep a track of number of emails sent</li>
</ul>

<h2>Normalize your database</h2>

<p>Requirement: all users from to and cc are in your database (no emails sent to email addresses out of organization)</p>

<p>Instead of storing emails in <code>to</code> and <code>cc</code>, create new tables and store email id as well as user_ids from to and cc.</p>

<h2>Keep a track of number of emails sent</h2>

<p>Add two columns (<code>Number_To, Number_CC</code>) in <code>t_user</code> table and increment them as needed (when sending emails, storing it to <code>t_email</code> table, ...). If You decide to go this way, watch out for concurrency, it is best to do <code>UPDATE t_user SET Number_To = Number_To + 1</code> instead of selecting current <code>Number_To</code> value and then updating to new value.</p>

### Answer ID: 8257280
<p>Try this query once. Also, try <code>=</code> operator instead <code>LIKE</code></p>

<pre><code>SELECT tu.*,

(case when  user_type_id = 1 then 'Admin' 
       when user_type_id = 5 then 'Super Admin' 
       when user_type_id = 3 then 'Writer' 
       when user_type_id = 4 then  'Reader'
       else 'somethingelse' 
       end) as user_type_name, 

    (case when user_inactive = 1 then 'No'
     else 'Yes' end) as user_can_log,

    (select count(*) as number_tickets from  t_fthread where
    fthread_creator_userid=user_id()),

    (select count(*) as number_emails from  t_email where email_to like '%abc@xyz.com%'
  or email_cc like '%abc@xyz.com%') 

   FROM t_user tu left join t_organisation torg on tu.user_org_id=
  torg.organisation_id   where tu.user_org_id = 42  order by tu.user_last_name, 
  tu.user_first_name 
</code></pre>

### Answer ID: 8257350
<p>Well, you could do the following for the email:</p>

<pre><code>    SELECT COUNT(*) 
    FROM   t_email 
    WHERE  
       (
            PATINDEX('%' + user_email + '%', email_to) != 0
            OR PATINDEX('%' + user_email + '%', email_cc) != 0
       )
</code></pre>

### Answer ID: 8257174
<p>Is it possible to do the search using:</p>

<pre><code> email_to like user_email+'%' 
</code></pre>

<p>, or even code all alternatives?
Or, even better, store the user email (that will being searched for later) in a "cleansed" form in the database?</p>

<p>The wildcard in front of user_email is the evil one: textual searches starting with '%' will always be slow, because they're unpredictable, and you'll never know where in the string the search text will be found.</p>

<p>For example, consider the text:</p>

<pre><code>kakaka@mailblahblah.youknowka@this.text
</code></pre>

<p>While this is a relatively small string, the search for the text "ka@this.text" will go like this</p>

<ul>
<li>"k" found on position one</li>
<li>match still on position two</li>
<li>mismatch on position three</li>
</ul>

<p>this goes two times on, and the third time the ''@'' is found. Then mismatch at position four.</p>

<p>Only after about 36 comparison-operations, SQL Server knows the string matches. And that is for one row only.. So try to avoid wildcards at the beginning of string comparisons.</p>

