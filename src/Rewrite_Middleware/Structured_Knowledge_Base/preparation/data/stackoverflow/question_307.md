# Fast Refresh on commit of materialized view
[Link to question](https://stackoverflow.com/questions/20103190/fast-refresh-on-commit-of-materialized-view)
**Creation Date:** 1384969700
**Score:** 11
**Tags:** oracle-database, materialized-views
## Question Body
<p>I just created tables DEPT and EMP like follow :</p>

<pre><code>create table DEPT
( dept_no number , dept_name varchar(32) , dept_desc varchar(32),
  CONSTRAINT dept_pk Primary Key (dept_no) );

create table EMP
( emp_no number, dept_no number, CONSTRAINT emp_pk Primary Key (emp_no,dept_no));

insert into dept values (10,'it','desc1');
insert into dept values (20,'hr','desc2');

insert into emp values (1,10);
insert into emp values (2,20);
</code></pre>

<p>I created materialized view logs on these tables with rowid and materialized views as follows:</p>

<pre><code>create materialized view log on emp with rowid;
create materialized view log on dept with rowid;

create materialized view empdept_mv refresh fast on commit as
select a.rowid dept_rowid, b.rowid emp_rowid, a.dept_no,b.emp_no
from dept a, emp b
where a.dept_no=b.dept_no ;

select * from emp;
    EMP_NO    DEPT_NO
  ---------- ----------
     1         10
     2         20
     3         30

select * from dept;
   DEPT_NO DEPT_NAME                        DEPT_DESC
---------- -------------------------------- --------------------------------
    10 it                               desc1
    20 hr                               desc2
    30 it                               desc3

select * from empdept_mv;

DEPT_ROWID         EMP_ROWID             DEPT_NO     EMP_NO
------------------ ------------------ ---------- ----------
AAAli5AABAAAPZ6AAA AAAli7AABAAAQs6AAA         10          1
AAAli5AABAAAPZ6AAB AAAli7AABAAAQs6AAB         20          2
</code></pre>

<p>I inserted a new record and did COMMIT; ..but still when i check the materialized view, the new record is not shown in the materialized view.</p>

<pre><code>insert into dept values (30,'it','desc3');
commit;
insert into emp values (3,30);
commit;

select * from empdept_mv;

DEPT_ROWID         EMP_ROWID             DEPT_NO     EMP_NO
------------------ ------------------ ---------- ----------
AAAli5AABAAAPZ6AAA AAAli7AABAAAQs6AAA         10          1
AAAli5AABAAAPZ6AAB AAAli7AABAAAQs6AAB         20          2
</code></pre>

<p>Now, when I run the procedure for Fast and complete refresh as <a href="http://docs.oracle.com/cd/E16655_01/server.121/e17749/refresh.htm#DWHSG8366%20" rel="noreferrer">per</a>, The Fast refresh does not update the Mview but the complete refresh does. ( Note: <strong>But the Mview is still REFRESH ON COMMIT</strong>)</p>

<pre><code>execute DBMS_MVIEW.REFRESH('empdept_mv', 'F', '', TRUE, FALSE, 0,0,0,FALSE, FALSE);
PL/SQL procedure successfully completed.

DEPT_ROWID         EMP_ROWID             DEPT_NO     EMP_NO
------------------ ------------------ ---------- ----------
AAAli5AABAAAPZ6AAA AAAli7AABAAAQs6AAA         10          1
AAAli5AABAAAPZ6AAB AAAli7AABAAAQs6AAB         20          2


execute DBMS_MVIEW.REFRESH('test_mview2', 'C', '', TRUE, FALSE, 0,0,0,FALSE, FALSE);
PL/SQL procedure successfully completed.

DEPT_ROWID         EMP_ROWID             DEPT_NO     EMP_NO
------------------ ------------------ ---------- ----------
AAAli5AABAAAPZ6AAA AAAli7AABAAAQs6AAA         10          1
AAAli5AABAAAPZ6AAB AAAli7AABAAAQs6AAB         20          2
AAAli5AABAAAPZ6AAC AAAli7AABAAAQs6AAC         30          3
</code></pre>

<p>The DBMS_MVIEW.EXPLAIN_MVIEW output is as shown : (capability_name --Possible-- msgtxt)</p>

<ol>
<li>PCT --N--</li>
<li>REFRESH_COMPLETE --Y--</li>
<li>REFRESH_FAST --Y--</li>
<li>REWRITE --N--</li>
<li>PCT_TABLE --N-- Oracle error: see RELATED_NUM and RELATED_TEXT for
details</li>
<li>REFRESH_FAST_AFTER_INSERT --Y--</li>
<li>REFRESH_FAST_AFTER_ONETAB_DML --Y--</li>
<li>REFRESH_FAST_AFTER_ANY_DML --Y--</li>
<li>REFRESH_FAST_PCT --N-- PCT is not possible on any of the detail
tables in the mater</li>
<li>REWRITE_FULL_TEXT_MATCH --N-- Oracle error: see RELATED_NUM and
 RELATED_TEXT for details</li>
<li>REWRITE_FULL_TEXT_MATCH --N-- query rewrite is disabled on the
 materialized view</li>
<li>REWRITE_PARTIAL_TEXT_MATCH --N-- materialized view cannot support
 any type of query rewrite</li>
<li>REWRITE_PARTIAL_TEXT_MATCH --N-- query rewrite is disabled on the
 materialized view</li>
<li>REWRITE_GENERAL --N-- materialized view cannot support any type of
 query rewrite</li>
<li>REWRITE_GENERAL --N-- query rewrite is disabled on the materialized
 view</li>
<li>REWRITE_PCT --N-- general rewrite is not possible or PCT is not
 possible on an</li>
<li>PCT_TABLE_REWRITE --N-- Oracle error: see RELATED_NUM and
 RELATED_TEXT for details</li>
</ol>

<p><strong>How can I achieve Fast Refresh On Commit ?</strong><br>
The Oracle Version details are as follows:<br>
NLSRTL                  10.2.0.4.0  Production<br>
Oracle Database 10g     10.2.0.4.0  64bit Production<br>
PL/SQL              10.2.0.4.0  Production<br>
TNS for Linux:          10.2.0.4.0  Production  </p>

## Answers
### Answer ID: 24950138
<p>I don't know if the problem still persists, but as I took a look at the artice you provided, I noticed something (which might just be the solution here):</p>

<p><strong>ON COMMIT Refresh</strong></p>

<p>A materialized view can be refreshed automatically using the ON COMMIT method. Therefore, whenever a transaction commits which has updated the tables on which a materialized view is defined, those changes are automatically reflected in the materialized view. The advantage of using this approach is you never have to remember to refresh the materialized view. <strong>The only disadvantage is the time required to complete the commit will be slightly longer because of the extra processing involved.</strong> However, in a data warehouse, this should not be an issue because there is unlikely to be concurrent processes trying to update the same table.</p>

<ul>
<li><em>Notice the bold line.</em></li>
</ul>

<p>Then we have:</p>

<p><strong>Table 7-1 ON DEMAND Refresh Methods</strong></p>

<p>Refresh Option  Parameter   Description
<strong>COMPLETE</strong>        C           <strong>Refreshes by recalculating the defining query</strong> of the materialized view.</p>

<p><strong>FAST</strong>            F           <strong>Refreshes by incrementally applying changes to the materialized view</strong>. For local materialized views, it chooses the refresh method which is estimated by optimizer to be most efficient. The refresh methods considered are log-based FAST and FAST_PCT.</p>

<p><strong>FAST_PCT</strong>        P           Refreshes by recomputing the rows in the materialized view affected by changed partitions in the detail tables.</p>

<p><strong>FORCE</strong>           ?           Attempts a fast refresh. If that is not possible, it does a complete refresh.
For local materialized views, it chooses the refresh method which is estimated by optimizer to be most efficient. The refresh methods considered are log based FAST, FAST_PCT, and COMPLETE.</p>

<ul>
<li><em>Notice the bold lines.</em></li>
<li><em>I personally prefer the FORCE Option.</em></li>
</ul>

<p>Could you please tell, if this occurs again after some time (depending of the parameters of the DB and the machine it runs on, so I can't even hint you how much)?</p>

<p><strong>When Fast Refresh is Possible</strong></p>

<p><strong>Not all materialized views may be fast refreshable.</strong> Therefore, use the package <em>DBMS_MVIEW.EXPLAIN_MVIEW</em> to determine what refresh methods are available for a materialized view.</p>

<p>If you are not sure how to make a materialized view fast refreshable, you can use the <em>DBMS_ADVISOR.TUNE_MVIEW</em> procedure, which provides a script containing the statements required to create a fast refreshable materialized view.</p>

<p>Cheers</p>

### Answer ID: 20693204
<p>I see that you created the materialized view logs with ROWID, which is not really required as both tables have a primary key so you could try without the ROWID.</p>

<p>create materialized view log on emp;
create materialized view log on dept;</p>

<p>Additionally, if you create the materialized view log with ROWID you should create the materialized view with rowid.</p>

<p>create materialized view empdept_mv refresh fast on commit WITH ROWID as
select a.rowid dept_rowid, b.rowid emp_rowid, a.dept_no,b.emp_no
from dept a, emp b
where a.dept_no=b.dept_no ;</p>

<p>You could try those changes and see if the materialized views fast refresh on commit. </p>

