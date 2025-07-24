# Using IIS URL Rewrite in conjunction with SQL server to verify security on static content
[Link to question](https://stackoverflow.com/questions/23925101/using-iis-url-rewrite-in-conjunction-with-sql-server-to-verify-security-on-stati)
**Creation Date:** 1401332971
**Score:** 1
**Tags:** sql-server, security, iis, coldfusion, url-rewrite-module
## Question Body
<p>I am working on a project where I need to prevent access to static content on a windows server running IIS 7.5 and ColdFusion. </p>

<p>I already have an authentication system build with ColdFusion to handle logging in a user. The  difficulty is ColdFusion is unable to provide any processing on files that are not handled by the ColdFusion server.</p>

<p>My thought was to utilize IIS URL Rewrite and my ColdFusion system to do the following:</p>

<ul>
<li>User logs in with their Username and Password</li>
<li>Upon successful log in, a database record is created with a unique random key and date identifying a valid session</li>
<li>The last part of the log in process is to write a cookie with the random key created in the previous step</li>
</ul>

<p>With the cookie and authenticated session now established my thoughts on how IIS URL Rewrite would prevent access to static content:</p>

<ul>
<li>Request is sent for a protected file</li>
<li>IIS URL Rewrite will take the passed cookie value and send a request to the database table </li>
<li>If the database reports that the unique key from the cookie is a valid session the request is allowed to continue. If the cookie value returns from the database is invalid, the file is redirected the a 403 response.</li>
</ul>

<p>I have read some documentation (<a href="http://www.iis.net/learn/extensions/url-rewrite-module/using-custom-rewrite-providers-with-url-rewrite-module" rel="nofollow">http://www.iis.net/learn/extensions/url-rewrite-module/using-custom-rewrite-providers-with-url-rewrite-module</a>) that shows you can do database queries with the IIS URL Rewrite module.</p>

<p>My main question is if this is a viable solution to protect content from being hosted when a user has not been authenticated as a user? If so, I have been hard pressed to find any examples of this online.</p>

<p>I appreciate any insight in the validity or stupidity of this potential solution.</p>

<p>Cheers!</p>

