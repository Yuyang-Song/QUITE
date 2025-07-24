# Oracle SQL Query rewriting
[Link to question](https://stackoverflow.com/questions/31855125/oracle-sql-query-rewriting)
**Creation Date:** 1438862169
**Score:** 1
**Tags:** sql, oracle-database
## Question Body
<p>I have an Oracle database server running on a machine. Clients performs operations through a frontend application build from a different company, which generates corresponding SQL queries for these operations.</p>

<p>The frontend application generates SQL queries that we cannot modify. What I would like to know if there is any way to rewrite the SQL query upon its arrival. More specifically, we would like to be able to change tablespace names, default attribute values and most importantly compression parameters. For example, change this query:</p>

<pre><code>CREATE TABLE EXAMPLE_TABLE (
    ID INTEGER NOT NULL,  
    AMOUNT FLOAT(126) DEFAULT 0.0, 
    TAG VARCHAR2(50) DEFAULT ' '
)
TABLESPACE EXAMPLE_TABLESPACE NOCOMPRESS
</code></pre>

<p>to:</p>

<pre><code>CREATE TABLE EXAMPLE_TABLE (
    ID INTEGER NOT NULL,  
    AMOUNT FLOAT(126) DEFAULT 2.0, 
    TAG VARCHAR2(50) DEFAULT ' '
)
TABLESPACE EXAMPLE_TABLESPACE_TWO COMPRESS FOR OLTP
</code></pre>

<p>Note that the rewrites are not limited to create table statements, but can be applied to any SQL queries.</p>

<p>Any ideas about how to do this?</p>

## Answers
### Answer ID: 31857427
<p>If I didn't understand correctly, you want to do two things. </p>

<ol>
<li>Change tablespace for this table </li>
<li>Change metadata from this table</li>
</ol>

<p>You can do both easily.</p>

<ol>
<li><p><code>alter table [table_name] move [new_tablespace];  -- it must exists</code>
( check tablespace quota in this tb for this user )</p></li>
<li><p><code>alter table [table_anem] MODIFY(AMOUNT  DEFAULT 0.2);</code></p></li>
</ol>

### Answer ID: 31857288
<p>You might enjoy this Oracle Database 12c feature, the SQL Translation Framework. Designed for taking T-SQL to SQL when migrating applications from Sybase or SQL Server to Oracle, it can also be used to help with hard-coded vendor SQL you need to optimize/fix.</p>

<p><a href="https://docs.oracle.com/database/121/DRDAA/sql_transl_arch.htm" rel="nofollow">Oracle Docs</a></p>

<p><a href="http://kerryosborne.oracle-guy.com/2013/07/sql-translation-framework/" rel="nofollow">Blog Example</a></p>

### Answer ID: 31857173
<p>There is no way to modify a query upon its arrival. I think it would be a better idea to create tablespaces and everything else, according to your standards and requirements, before running the application.</p>

