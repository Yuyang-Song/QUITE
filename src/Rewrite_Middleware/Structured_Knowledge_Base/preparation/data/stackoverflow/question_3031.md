# Real time copy of data from one table to another table in same schema in oracle
[Link to question](https://stackoverflow.com/questions/62992346/real-time-copy-of-data-from-one-table-to-another-table-in-same-schema-in-oracle)
**Creation Date:** 1595236914
**Score:** 0
**Tags:** oracle-database
## Question Body
<p>Ours is a transnational database and due to this pandemic our data has increased exponentially which is causing performance issue.we have tried all kinds of performance tuning , rewriting queries etc but nothing is helping.
The scenario is that same table (<strong>Table A</strong> )is used to write data from the staging area and also
reporting application (Cognos) is reading the data from the same table.
Our plan is to create another duplicate table (say <strong>Table B</strong>)in the same schema in the same DB (we do not want to make any major changes to the reporting part) but the issue is can we replicate the data from table A to table B real time and how can we achieve this. In another 6 months we are migrating to 19C.</p>

## Answers
### Answer ID: 62993042
<p>For your scenario I would create a MATERIALIZE VIEW with LOG and refresh fast on commit, but obviously the refresh is something you need to evaluate for yourself depending on when you want the data available in TABLE B respect to TABLE A</p>
<p>Test case</p>
<pre><code>SQL&gt; create table my_test ( c1 number , c2 number ) ;

Table created.

SQL&gt; alter table my_test add primary key (c1) ;

Table altered.

SQL&gt; declare
begin
for i in 1 .. 100000
loop
insert into my_test values ( i, i );
end loop;
commit;
end;
/  2    3    4    5    6    7    8    9

PL/SQL procedure successfully completed.


SQL&gt; create MATERIALIZED VIEW LOG ON  my_test with primary key including new values ;

Materialized view log created.

SQL&gt; create materialized view my_test_replica nologging cache build immediate refresh fast on commit
  2  as select * from my_test ;

Materialized view created.

SQL&gt; select count(*) from my_test ;

  COUNT(*)
----------
    100000

SQL&gt; select count(*) from my_test_replica ;

  COUNT(*)
----------
    100000

 declare
  2  begin
  3  for i in 100001 .. 200001
  4  loop
  5  insert into my_test values ( i, i );
  6  end loop;
  7  commit;
  8* end;
SQL&gt; /

PL/SQL procedure successfully completed.

Elapsed: 00:00:22.19
SQL&gt;

Elapsed: 00:00:22.19
SQL&gt; select count(*) from my_test ;

  COUNT(*)
----------
    200001

Elapsed: 00:00:00.01
SQL&gt; select count(*) from my_test_replica ;

  COUNT(*)
----------
    200001

Elapsed: 00:00:00.01
</code></pre>
<p>Take in consideration the degradation in performance of the second insert loop, due to the presence of the materialized view. There are different alternatives for refresh, try to look which one better fits your scenario.</p>
<p><a href="https://docs.oracle.com/database/121/DWHSG/refresh.htm#DWHSG-GUID-51191C38-D52F-4A4D-B6FF-E631965AD69A" rel="nofollow noreferrer">https://docs.oracle.com/database/121/DWHSG/refresh.htm#DWHSG-GUID-51191C38-D52F-4A4D-B6FF-E631965AD69A</a></p>

### Answer ID: 62992711
<p>To me, that sounds like a <strong>materialized view</strong> which refreshes on commit. For huge amount of data, that also <em>will</em> take some time.</p>

