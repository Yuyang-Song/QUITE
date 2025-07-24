# SQL Server datetime2 in OPENQUERY
[Link to question](https://stackoverflow.com/questions/32911493/sql-server-datetime2-in-openquery)
**Creation Date:** 1443802552
**Score:** 2
**Tags:** sql, sql-server, datetime, sql-server-2014, openquery
## Question Body
<p>We're migrating form SQL Server 2005 to 2014 for a pretty large environment. And we've noticed that OPENQUERY behaves differently when interacting with MySQL database when it comes to datetime. Previously, it would translate just fine to DATETIME column. With 2014 (I assume started in 2008 or so), it now converts to DATETIME2 (with maximum precision). This causes problems when comparing to or inserting into DATETIME columns.</p>

<p>Is there a way to specify on a server-level (or specify default) for which type those will translate to? Rewriting all of the queries will be quite an undertaking, and I'd like to avoid this now, if possible (rather rewrite as we edit or introduce new things).</p>

## Answers
### Answer ID: 37051006
<p>Try to Use VARCHAR datatype while migration of date fields, and it is always easy to Convert/Cast in various types as per need. </p>

