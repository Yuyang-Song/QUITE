# Oracle - selecting constant values as M x N table from dual
[Link to question](https://stackoverflow.com/questions/35016073/oracle-selecting-constant-values-as-m-x-n-table-from-dual)
**Creation Date:** 1453818191
**Score:** 3
**Tags:** sql, oracle-database, oracle11g
## Question Body
<p>Currently I'm using something similar to following statement for creating a temporary table like structure.</p>

<pre><code>WITH CONFIGURATION AS (
   SELECT 'some blah value' AS BLAH , 'some blee value' AS BLEE FROM DUAL
   UNION
   SELECT 'some other blah value' AS BLAH, 'some other blee value' AS BLEE FROM DUAL
)
SELECT 'BLAH BLAH' FROM CONFIGURATION C, SOME_OTHER_TABLE T WHERE C.BLAH=T.BLAH
</code></pre>

<p><strong>The problem that I'm facing here is that the query becomes considerably large and messy when I have to implement the same structure for a 10x7 table structure.</strong></p>

<p>Is there any easier way to achieve this using <code>DUAL</code> or any other system tables without having to use <code>UNION</code> and rewrite the <code>SELECT FROM DUAL</code> multiple times?</p>

<blockquote>
  <p><strong>NOTE:</strong> </p>
  
  <ul>
  <li><strong>I have no DDL permission on this database. Otherwise I would have created a table for achieving this already</strong>  </li>
  <li><strong>The database version is oracle 11g</strong></li>
  <li><strong>The data inside the M x N structure is to be will be irregular in nature</strong></li>
  </ul>
</blockquote>

## Answers
### Answer ID: 35021429
<p>Maybe something like this ?</p>

<pre><code>select * from (
  select trunc( (rownum - 1) / 3) as x, mod(rownum - 1, 3) as y, column_value
  from table( dbmsoutput_linesarray(
           'some blah value' , 'some blee value', 'some bluuu value',
           'some other blah value', 'some other blee value', 'some other bluuu value',
           'blah 5', 'blee 5', 'bluu 5',
           'blah 6', 'blee 6', 'bluu 6'
                ))
)
pivot (
  max( column_value )
  for y in ( 0 as blah, 1 as blee, 2 as bluuu )
)
</code></pre>

