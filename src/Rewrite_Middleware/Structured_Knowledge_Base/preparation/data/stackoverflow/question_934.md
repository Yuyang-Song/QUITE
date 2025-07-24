# Join tables from multiple databases
[Link to question](https://stackoverflow.com/questions/50732839/join-tables-from-multiple-databases)
**Creation Date:** 1528344685
**Score:** 1
**Tags:** java, oracle-database, jdbc, jdbctemplate
## Question Body
<p>I have a legacy web application, WAR packaging.</p>

<p>It is written with hardcoded sql strings in DAO files. It connects to multiple schemas of an oracle db.</p>

<pre><code>select ... from schema1.one_table join schema2.other_table on...
</code></pre>

<p>What I have to achieve is to make this work with schemas in separate databases.</p>

<p>I was advised to autowire two jdbcTemplates and query the data from them, then do the joining-filtering logic in java.</p>

<p>I smell this is a bad solution, for several reasons. I don't want to implement joining-filtering in java, I am sure the oracle engine does it hundred times more efficiently.</p>

<p>How can I rewrite queries to specify not only the schema but the db instance also? Is this possible?</p>

## Answers
### Answer ID: 50732912
<p>I think this cannot be done directly with JDBC. you can follow below steps as I did in one of my projects:</p>

<ul>
<li>Create a dblink between databases with the help of DBA.</li>
<li>Create synonym of remote database tables in your primary database.</li>
</ul>

<p>This way you can access remote tables directly from one database and you can then use any of plain JDBC/JDBCTemplate/Hibernate etc to run your business.</p>

