# Issue with SSIS package executing procedure that reads from a file share
[Link to question](https://stackoverflow.com/questions/40116938/issue-with-ssis-package-executing-procedure-that-reads-from-a-file-share)
**Creation Date:** 1476820445
**Score:** 1
**Tags:** sql, stored-procedures, ssis, sql-server-2012, bulkinsert
## Question Body
<p>I have an SSIS Package that runs via a SQL job on a SSIS server (Server A) that executes a stored procedure on the database server (server B). This stored procedure does a Bulk insert from a file share that is located on the SSIS Server (Server A). However, every time that the stored procedure runs it fails with the follow error:</p>

<p><em>Execute Membership Process:Error: Executing the query "exec storedprocname ?, ?" failed with the following error: "Cannot bulk load because the file "\ServerA\TestLoads\Membership\Processing\filename.csv" could not be opened. Operating system error code 5(Access is denied.).". Possible failure reasons: Problems with the query, "ResultSet" property not set correctly, parameters not set correctly, or connection not established correctly.</em></p>

<p>I am pretty positive that the issue is related to permissions. If I store the files on the database server (Server B) then it processes. Or if I run the proc manually, it will work. </p>

<p>When I execute the job on Server A it executes as the service account for that server. That account has full access to Server A and Server B (Admin in SQL and on the server). I believe what is happening is the credentials get passed the first time, but they are not continued once the stored proc runs. I ran wireshark on Server A (SSIS Server) so that I could see what was access the share and try to get some more information. What I found was that there was no account information being passed, it was just blank. </p>

<p>I went through a lot of steps just to try to see if could get that work such as granting everyone access to the share, enabling the guest account, allowing anonymous users, etc. Not stuff I would want to do, but trying to narrow down the issue. None of those worked. </p>

<p>I tried modify the stored proc to use WITH EXECUTE AS OWNER. Still did not work, but got a different error. Also tried a variety of other accounts to execute as and got the same error each time. </p>

<p><em>Execute Membership Process:Error: Executing the query "exec [storedprocname] ?, ?" failed with the following error: "Could not obtain information about Windows NT group/user '', error code 0x5.". Possible failure reasons: Problems with the query, "ResultSet" property not set correctly, parameters not set correctly, or connection not established correctly.</em></p>

<p>Tried a variety of solutions that I found online to get this to work and nothing so far has done it. </p>

<p>I understand that is not an ideal solution. I was under the impression that the developers where using SSIS to load the file initially and then using SQL for the rest of the process which would have worked. But because SQL has to touch the file system it keeps failing. And at this stage, there is not the option of rewriting this. Additionally, this process will work if we move the files to the database server (Server B), but that eliminates a large need for us in having the SSIS server in the first place which was to get files being processed off of the database server</p>

<p>Any ideas on if there is a way to get the current solution to work? Basically, what I think I am needing is to run the SSIS package and for a way to pass credentials via the stored proc to the file share during that process. </p>

<p>We are using Windows Server 2012 R2 on both servers and SQL Server 2012 sp3 Developer edition. </p>

<p>Thanks for the help!</p>

## Answers
### Answer ID: 40117291
<p>I've had this issue before, and I still don't fully understand <strong>Kerberos authentication</strong>, but that fixed it for me. It's something to do with "double-hop" of authentication i.e. creds going from SSIS, through SQL Server, to a network Server.</p>

<p>Try setting up <strong>Kerberos Authentication</strong> for SQL Server. There are detailed step-by-step instructions with screenshots here => <a href="http://www.sqlscientist.com/2014/01/setup-kerberos-authentication-for-sql.html" rel="nofollow">Setup Kerberos Authentication for SQL Server</a></p>

<p><a href="https://i.sstatic.net/R3LlQ.png" rel="nofollow"><img src="https://i.sstatic.net/R3LlQ.png" alt="enter image description here"></a></p>

<p>I understand this is like a "link-only" answer, but I don't want to copy-paste &amp; plagiarize the author's original works i.e. blog post, hence the link.</p>

