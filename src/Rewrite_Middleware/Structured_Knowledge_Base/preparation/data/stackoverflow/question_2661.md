# C++ use Stored Procedure to return results
[Link to question](https://stackoverflow.com/questions/45285480/c-use-stored-procedure-to-return-results)
**Creation Date:** 1500913086
**Score:** 0
**Tags:** c++, stored-procedures
## Question Body
<p>For the past couple years, I've been maintaining a large C++ application (v100) that utilizes some form of non-ADO database connections, but it works great.</p>

<p>During this time, getting a resultset from the database is quite simple.  I instantiate the return class, with the database object, then Open a query.  </p>

<pre><code>CUpdates cUpdates(GetDatabase());
CString strQuery = "SELECT * FROM Updates";
cUpdates.Open(-1, strQuery);
</code></pre>

<p>Just that simple, cUpdates is filled with records.</p>

<p>NOW however, we want to execute a stored procedure, and return the results from it.  But no matter what I try, even changing 'EXEC' to 'CALL', the call fails.  Is there a similar simple method for executing a stored procedure, and returning the results, without having to totally rewrite how the application handles the database connection and returning of data?</p>

<pre><code>        strQuery.Format("EXEC dbo.[GetUpdates_ComputerName] '%s', %d, %d", GetWorkstationName(), m_bRetainUpdates, m_bScheduleUpdate);
        cUpdates.Open(-1, strQuery);  //FAILS ON EXEC
</code></pre>

<p>(I have tested the EXEC statement in SSMS, and it works fine)</p>

<p>We do also use another sql command, for strictly executing statements, but I see no way of returning data with it. Maybe there is a similar command I don't know of?</p>

<pre><code>GetDatabase()-&gt;ExecuteSQL(strQuery);
</code></pre>

<p>note:  for the record, I am C# developer (since 1.0 beta).  My only experience in c++ has been learning on the fly over the past 2 years, occasionally maintaining a few of our massive systems.</p>

## Answers
### Answer ID: 45287978
<p>It would seem that CRecordset cannot handle an EXEC statement inside of it. So we converted the new stored procedure to a Tabular Function, so I can use a SELECT instead... which works properly. (though I'd rather use the stored procedure) </p>

