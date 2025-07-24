# OPTION(QUERYTRACEON 9481), Dynamic SQL &amp; DBCC TRACEON error
[Link to question](https://stackoverflow.com/questions/57418462/optionquerytraceon-9481-dynamic-sql-dbcc-traceon-error)
**Creation Date:** 1565287666
**Score:** 2
**Tags:** sql-server, sql-server-2017
## Question Body
<p>I'm in a bit of an odd-ball situation...  a) We are in the process of upgrading all SQL Server instances to 2017. b) More than a few of the impacted databases are using legacy Compatability Levels/Cardinality Estimator. c) We would like to have all databases on the current (2017) CL and using the most recent CE.</p>

<p>The plan is to use "OPTION(QUERYTRACEON 9481)" at the individual statement level to deal with queries that don't play nice with the new CE. Not as a permanent fix, but as a means to get over the hump (rewriting every impacted procedure is simply outside the scope of the current project).</p>

<p>Cutting to the chase... This appears to be working as expected EXCEPT when the stored procedure is using dynamic SQL and is being executed by a non-SA user. This does, of course, make sense. As long as the "OPTION(QUERYTRACEON 9481)" is executed in the scope of the procedure, ownership chaining provides the permissions necessary to execute the underlying DBCC TRACEON command. The use of dynamic SQL, however, essentially treats the code as AD-HOC SQL and is executed under the users own security context... Which is not a SA and therefore does not have rights to execute DBCC TRACEON;</p>

<p>Short or rewriting queries or giving application service accounts SA roles, does anyone have a usable solution?</p>

<p>Thank you in advance,</p>

<p>Jason</p>

## Answers
### Answer ID: 58433679
<p><strong>Problem:</strong></p>
<blockquote>
<p>...The use of dynamic SQL, however, essentially treats the code as AD-HOC SQL and is executed under the users own security context... Which is not a SA and therefore does not have rights to execute DBCC TRACEON;</p>
</blockquote>
<p><strong>Solution:</strong></p>
<p>Wonderfully explained by Kimberly Tripp in her post on sqlskills.com:<br />
<a href="https://www.sqlskills.com/blogs/kimberly/sp_settraceflag/" rel="nofollow noreferrer">&quot;Setting CE TraceFlags on a query-by-query (or session) basis&quot;</a></p>
<ol>
<li><p>Create a Stored Procedure on msdb database which allows setting of a desired Trace Flag without sysadmin permissions.<br />
(of course, sysadmin takes care of setting-up a list of allowed Trace Flag values).</p>
</li>
<li><p>Wrap any problematic statement (dynamic sql, ad-hoc query, or procedure call) with a call to this Stored Procedure and change the session trace flag for execution.<br />
This allows users with lower permissions to change the Cardinality Estimator for execution of the problematic statement.</p>
</li>
</ol>
<p><strong>Example usage:</strong></p>
<pre><code>EXEC msdb.dbo.msdbSetTraceFlag 9481, 1; 
GO  
   
Problematic STATEMENT or PROCEDURE   
 
EXEC msdb.dbo.msdbSetTraceFlag 9481, 0;  -- don't forget to turn it back off!    
GO
</code></pre>
<p><strong>Stored Procedure code:</strong></p>
<pre><code>USE msdb;
GO
 
CREATE PROCEDURE msdbSetTraceFlag
    (@TraceFlag int,
     @OnOff bit = 0)
WITH EXECUTE AS OWNER
AS
DECLARE @OnOffStr char(1) = @OnOff;
-- Sysadmins can add supported trace flags and then use this
-- from their applications
IF @TraceFlag NOT IN (
              9481 -- LegacyCE if database is compat mode 120 or higher
            , 2312 -- NewCE if database compat mode 110 or lower
                     )
     BEGIN
         RAISERROR('The Trace Flag supplied is not supported. Please contact your system administrator to determine inclusion of this trace flag: %i.', 16, 1, @TraceFlag);
         RETURN
     END
ELSE
     BEGIN
         DECLARE @ExecStr nvarchar(100);
         IF @OnOff = 1
             SELECT @ExecStr = N'DBCC TRACEON(' + CONVERT(nvarchar(4), @TraceFlag) + N')';
         ELSE
             SELECT @ExecStr = N'DBCC TRACEOFF(' + CONVERT(nvarchar(4), @TraceFlag) + N')';
         -- SELECT (@ExecStr)
         EXEC(@ExecStr)
         -- RAISERROR (N'TraceFlag: %i has been set to:%s (1 = ON, 0 = OFF).', 10, 1, @TraceFlag, @OnOffStr);
     END;
GO
 
GRANT EXECUTE ON msdbSetTraceFlag TO PUBLIC --or to a specific set of users;
GO
</code></pre>
<p><strong>Note:</strong> This Stored procedure is created in msdb, and not on master, because of &quot;trustworthy&quot; prerequisite, which is default for msdb.</p>

