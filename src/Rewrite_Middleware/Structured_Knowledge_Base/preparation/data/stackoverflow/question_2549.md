# UPDATE with SELECT subquery runs extremely slowly on MySQL 5.7 (but was fine on 5.5)
[Link to question](https://stackoverflow.com/questions/39482198/update-with-select-subquery-runs-extremely-slowly-on-mysql-5-7-but-was-fine-on)
**Creation Date:** 1473824835
**Score:** 3
**Tags:** mysql, sql, mysql-5.7, mysql-dependent-subquery, query-planner
## Question Body
<p>Thank you all in advance. I have encountered an issue in upgrading my database from MySQL 5.5 to 5.7 that has me completely and totally confounded. The upgrade was not done using mysqldump or similar, but as a rebuild from several tab separated input files using several very long SQL scripts. One seemingly innocuous query in particular (inside a stored procedure) has been giving me trouble and I cannot work out why:</p>

<pre><code>UPDATE liverpool.master_person mp 
SET Link_Count = ( SELECT count(*) FROM liverpool.person_record pr
WHERE mp.Master_Person_ID = pr.Master_Person_ID ) - 1;
</code></pre>

<p>This seems fairly simple, but the EXPLAIN from this query shows that some serious row scanning is going on:</p>

<pre><code># id | select_type          | table | partitions | type    | possible_keys | key                    | key_len | ref  | rows      | filtered | Extra
========================================================================================================================================================================
'1'  | 'UPDATE'             | 'mp'  | NULL       | 'index' | NULL          | 'PRIMARY'              | '4'     | NULL | '1198100' | '100.00' | NULL
------------------------------------------------------------------------------------------------------------------------------------------------------------------------
'2'  | 'DEPENDENT SUBQUERY' | 'pr'  | NULL       | 'index' | NULL          | 'Master_Person_ID_IDX' | '17'    | NULL | '1200537' | '100.00' | 'Using where; Using index'
</code></pre>

<p>The important thing seems to be the rows column, which is 1198100 for the UPDATE and 1200537 for the SELECT subquery. Both of these numbers are pretty close to the total number of rows in both of the referenced tables (1207744 for both). So it seems to be doing a full row for row scan of both, and I can't see why. Precisely the same query worked fine in MySQL 5.5. I was hopeful that <a href="https://stackoverflow.com/questions/37733946/query-extremely-slow-after-migration-to-mysql-5-7">this</a> solution would help, but passed 'derived_merge=off' to the optimizer_switch and restarting the server did not help. </p>

<p>I certainly don't expect this query to be super fast. It doesn't have to be. It wasn't exactly speedy before (a few minutes on a 7200rpm spinning disk), but since the upgrade to MySQL 5.7 it seems like it wouldn't complete anytime before the heat death of the universe, and I'd rather not wait that long. Does anyone out there have any ideas? Whether query rewrites, or my.ini settings or anything at all?</p>

<p>Also, please let me know if I have breached protocol in any way or if I can improve my question. As I said above, it is my first post here.</p>

<p>Thank you for your time.</p>

<p>EDIT: I thought for a moment that <a href="https://stackoverflow.com/questions/21074717/mysql-not-in-query-much-slower-after-mysql-upgrade?rq=1">this</a> solution looked promising. Apparently tables with differing charsets/collations can't properly read each others indexes. I was <em>pretty</em> sure everything was in <code>latin1</code>, but figured it was worth making sure. So I explicitly added <code>DEFAULT CHARSET=latin1</code> to all of my <code>CREATE TABLE</code> statements and added <code>CHARACTER SET latin1</code> to my <code>LOAD DATA INFILE</code> statements. Sadly, no change.</p>

## Answers
### Answer ID: 39485800
<p>Try to rewrite query as:</p>

<pre><code>UPDATE liverpool.master_person mp
  JOIN (SELECT Master_Person_ID, count(*) as cnt
          FROM liverpool.person_record
         GROUP BY Master_Person_ID)
       ) pr
    ON mp.Master_Person_ID = pr.Master_Person_ID
   SET mp.Link_Count = pr.cnt - 1
</code></pre>

