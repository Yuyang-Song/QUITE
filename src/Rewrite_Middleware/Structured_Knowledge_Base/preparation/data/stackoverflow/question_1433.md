# WebDAVModule: Cannot query authoring rules
[Link to question](https://stackoverflow.com/questions/76376732/webdavmodule-cannot-query-authoring-rules)
**Creation Date:** 1685561511
**Score:** 0
**Tags:** webdav, iis-10, windows-server-2022
## Question Body
<p>I am upgrading an IIS application server from Windows 2012 to Windows 2022. Naturally, IIS is being upgraded from v8.5 to v10 during the course of the OS upgrade.</p>
<p>The application hosted on this server is a file upload gateway. It accepts files via https:// using either POST or PUT. For the latter, we use WebDAV to process the PUT. (Our application, engineered as an HttpModule performs some &quot;extension processing&quot;, we rewrite the name of the file placed onto our server and we log certain data to our application database. I mention this just for the sake of completeness. These features are working well when files are POSTed to the application server.)</p>
<p>In order to pre-test this migration, I set up a clone of our production server into a separate VNet so it won't conflict with the original production server. The original production server is in a domain, but user accounts for all file uploads are local accounts and the domain is not integral to the server's function. Therefore, I've exited the test server - in its separate VNet - from a domain which is simply inaccessible to it and I'd joined it to a workgroup - WORKGROUP.</p>
<p>I have two test cases set up in Postman, to test both POST and PUT. I've tested both of these against my production server. In each case the file is created on the server. Each Postman test case is valid! Now I change the host name to my test server. Oddly enough, the POST succeeds but the PUT fails. I turned on Failed request tracing and here is what I find:</p>
<p><strong>Cannot query authoring rules</strong></p>
<pre><code>&lt;Event xmlns=&quot;http://schemas.microsoft.com/win/2004/08/events/event&quot;&gt;
 &lt;System&gt;
  &lt;Provider Name=&quot;WWW Server&quot; Guid=&quot;{3A2A4E84-4C21-4981-AE10-3FDA0D9B0F83}&quot;/&gt;
  &lt;EventID&gt;0&lt;/EventID&gt;
  &lt;Version&gt;1&lt;/Version&gt;
  &lt;Level&gt;3&lt;/Level&gt;
  &lt;Opcode&gt;5&lt;/Opcode&gt;
  &lt;Keywords&gt;0x200&lt;/Keywords&gt;
  &lt;TimeCreated SystemTime=&quot;2023-05-31T18:31:35.121Z&quot;/&gt;
  &lt;Correlation ActivityID=&quot;{40000004-0006-FD00-B63F-84710C7967BB}&quot;/&gt;
  &lt;Execution ProcessID=&quot;7412&quot; ThreadID=&quot;5536&quot;/&gt;
  &lt;Computer&gt;R8EUSXREX&lt;/Computer&gt;
 &lt;/System&gt;
 &lt;EventData&gt;
  &lt;Data Name=&quot;ContextId&quot;&gt;{40000004-0006-FD00-B63F-84710C7967BB}&lt;/Data&gt;
  &lt;Data Name=&quot;ModuleName&quot;&gt;WebDAVModule&lt;/Data&gt;
  &lt;Data Name=&quot;Data1&quot;&gt;Cannot query authoring rules&lt;/Data&gt;
  &lt;Data Name=&quot;Data2&quot;&gt;/_REXDTSTesting/ab6b04fd/MyFile[r8#e13c1f92ba614aee80f2b5694a6094ff].txt&lt;/Data&gt;
  &lt;Data Name=&quot;ErrorCode&quot;&gt;2147943732&lt;/Data&gt;
 &lt;/EventData&gt;
 &lt;RenderingInfo Culture=&quot;en-US&quot;&gt;
  &lt;Opcode&gt;MODULE_WARNING&lt;/Opcode&gt;
  &lt;Keywords&gt;
   &lt;Keyword&gt;Module&lt;/Keyword&gt;
  &lt;/Keywords&gt;
  &lt;freb:Description Data=&quot;ErrorCode&quot;&gt;No mapping between account names and security IDs was done.
 (0x80070534)&lt;/freb:Description&gt;
 &lt;/RenderingInfo&gt;
 &lt;ExtendedTracingInfo xmlns=&quot;http://schemas.microsoft.com/win/2004/08/events/trace&quot;&gt;
  &lt;EventGuid&gt;{D79A948E-95F1-417B-A731-B7A79DEC7AE5}&lt;/EventGuid&gt;
 &lt;/ExtendedTracingInfo&gt;
&lt;/Event&gt;
</code></pre>
<p>Several things to keep in mind.</p>
<p>This happens AFTER Basic authentication has succeeded. The credentials are valid. Here is the abstract from the trace (the abstract below precedes the one presented above in the actual trace output) to prove it:</p>
<pre><code>&lt;Event xmlns=&quot;http://schemas.microsoft.com/win/2004/08/events/event&quot;&gt;
 &lt;System&gt;
  &lt;Provider Name=&quot;WWW Server&quot; Guid=&quot;{3A2A4E84-4C21-4981-AE10-3FDA0D9B0F83}&quot;/&gt;
  &lt;EventID&gt;0&lt;/EventID&gt;
  &lt;Version&gt;1&lt;/Version&gt;
  &lt;Level&gt;4&lt;/Level&gt;
  &lt;Opcode&gt;11&lt;/Opcode&gt;
  &lt;Keywords&gt;0x2&lt;/Keywords&gt;
  &lt;TimeCreated SystemTime=&quot;2023-05-31T18:41:42.723Z&quot;/&gt;
  &lt;Correlation ActivityID=&quot;{40000002-0000-FC00-B63F-84710C7967BB}&quot;/&gt;
  &lt;Execution ProcessID=&quot;7412&quot; ThreadID=&quot;5836&quot;/&gt;
  &lt;Computer&gt;R8EUSXREX&lt;/Computer&gt;
 &lt;/System&gt;
 &lt;EventData&gt;
  &lt;Data Name=&quot;ContextId&quot;&gt;{40000002-0000-FC00-B63F-84710C7967BB}&lt;/Data&gt;
  &lt;Data Name=&quot;AuthType&quot;&gt;4&lt;/Data&gt;
  &lt;Data Name=&quot;NTLMUsed&quot;&gt;false&lt;/Data&gt;
  &lt;Data Name=&quot;RemoteUserName&quot;&gt;_REXDTSTesting&lt;/Data&gt;
  &lt;Data Name=&quot;AuthUserName&quot;&gt;_REXDTSTesting&lt;/Data&gt;
  &lt;Data Name=&quot;TokenImpersonationLevel&quot;&gt;2&lt;/Data&gt;
 &lt;/EventData&gt;
 &lt;RenderingInfo Culture=&quot;en-US&quot;&gt;
  &lt;Opcode&gt;AUTH_SUCCEEDED&lt;/Opcode&gt;
  &lt;Keywords&gt;
   &lt;Keyword&gt;Authentication&lt;/Keyword&gt;
  &lt;/Keywords&gt;
  &lt;freb:Description Data=&quot;AuthType&quot;&gt;NT&lt;/freb:Description&gt;
  &lt;freb:Description Data=&quot;TokenImpersonationLevel&quot;&gt;ImpersonationImpersonate&lt;/freb:Description&gt;
 &lt;/RenderingInfo&gt;
 &lt;ExtendedTracingInfo xmlns=&quot;http://schemas.microsoft.com/win/2004/08/events/trace&quot;&gt;
  &lt;EventGuid&gt;{C33BBE8F-985B-4080-81E6-005F1A06B9E2}&lt;/EventGuid&gt;
 &lt;/ExtendedTracingInfo&gt;
&lt;/Event&gt;
</code></pre>
<p>So authentication to the server has succeeded. The WebDAV authoring rule does exist. In fact, I deleted it an recreated it to rule out any confusion which might have been caused by the transition from Domain to Workgroup. (These are local accounts, and I can't envision any direct correlation but no harm to drop and recreate the rule, just to rule that out.)</p>
<p><a href="https://i.sstatic.net/GSc7I.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/GSc7I.png" alt="enter image description here" /></a></p>
<p>The web application runs under the identity of <strong>LocalSystem</strong>.</p>
<p>In a nutshell, the final question this all leads up to is, why can't WebDAVModule query the authoring rules?</p>
<p>Thanks for your assistance!</p>

## Answers
### Answer ID: 76376902
<p>The problem was due to those smudged out users, the first line of authoring rules in the screenshot below. Those user accounts are domain accounts. But I had pulled this server out of the domain so WebDAV's attempt to resolve those users failed. This aborted WebDAV's attempt to process any more authoring rules. (One could argue that WebDAV should be more fault-tolerant in this regard since the deletion of a single account for a terminated user - for example - can bring down all of your authoring rules. But, it is what it is.)</p>
<p>So to make this relevant for the broader context; if you are seeing this WebDAV error - Cannot query authoring rules - check to ensure that the accounts identified in your authoring rules are all valid!</p>
<p><a href="https://i.sstatic.net/JHPTn.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/JHPTn.png" alt="enter image description here" /></a></p>
<p>As soon as I removed those offending user accounts, my PUTs started succeeding!</p>
<p><a href="https://i.sstatic.net/HAxZT.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/HAxZT.png" alt="enter image description here" /></a></p>

