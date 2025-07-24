# Hibernate Security Apprehension: Hibernate vs. Stored Procedures
[Link to question](https://stackoverflow.com/questions/1401058/hibernate-security-apprehension-hibernate-vs-stored-procedures)
**Creation Date:** 1252518336
**Score:** 1
**Tags:** security, nhibernate, hibernate, stored-procedures
## Question Body
<p>At the company that I work with, we often have to integrate with client’s infrastructure.
Recently, after hearing that we use Hibernate, one client manifested following concern: Since user under which Hibernate connects to database has a direct access to tables and Hibernate generates SQL dynamically, then such user can do pretty mach anything in the database. </p>

<p>Had the user only permission to execute stored procedures, then SPs can limit the data but more importantly type of queries he can issue to database: basically no dynamic and injected SQL. So, if there is a stored procedure that eliminates a row, malicious person who got hold of user credentials will be able to eliminate single row in one go, but will not be able to issue the DELETE *.  I know Hibernate can also map views, but again this limits the data and not the operations user can perform. Hibernate can also execute SPs, but that in a great extent beats the purpose of using Hibernate and would imply a complete rewrite of application.</p>

<p>While I don’t see this as a major concern, since application servers also provide security, I had a problem of convincing the client. What’s your take on this? Is Hibernate really less secure than application using stored procedures? What are additional security measures that can be put in place when working with Hibernate?</p>

## Answers
### Answer ID: 1401113
<p>Hibernate <em>can</em> be less secure than using stored procedures, since in theory, DBAs can limit user access to only calling stored procedures, rather than direct access to the underlying data structures.</p>

<p>In practice and in my experience, it's extremely rare for this style of security to be implemented in a meaningful way. If a stored procedure is written for each CRUD operation, and a user is granted access to  all of the stored procedures, there is no real difference between that and just granting rights to the underlying structures themselves.</p>

<p>If the company is audited for SOX or security compliance, they might get dinged for not using stored procedures.</p>

<p>It is possible to use Hibernate over stored procedures, but <a href="http://www.coderanch.com/t/216142/Object-Relational-Mapping/java/Executing-stored-procedures-hibernate" rel="nofollow noreferrer">it seems like a pain in the ass</a>.</p>

### Answer ID: 1401096
<p>Hibernate of course is just a ORM layer over sql.  </p>

<p>Add the show_sql=true property on, show them what sql is being generated, and they'll see exactly what it does (parametrized queries as was mentioned). </p>

### Answer ID: 1401093
<ol>
<li>NHibernate can map to sprocs instead of tables</li>
<li>You can map read operations onto tables / views and insert / update / delete operations onto sprocs if you like</li>
<li>NHibernate does generates parameterised SQL, i.e. there is no chance of SQL injection</li>
<li>User permissions can always be restricted to certain operations on certain tables, if you decide to map onto tables and / or views</li>
<li>Most projects using sprocs start off by generating CRUD procedures for every table and assigning execute permissions on them all - this is not really much more secure than allowing table access</li>
</ol>

### Answer ID: 1401089
<p>If I am not mistaken NHibernate use parametrized sql queries.  This will stop injection. </p>

### Answer ID: 1401079
<p>I would assume Hibernate uses paramaterized queries. That should alleviate much of the concern for SQL Injection. You can also prevent the user account from being able to do everything in the database. It doesn't need to be the SA account after all.</p>

