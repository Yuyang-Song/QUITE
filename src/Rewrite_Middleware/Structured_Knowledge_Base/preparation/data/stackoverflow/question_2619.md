# azure http error 404 keeps logging and wordpress database error
[Link to question](https://stackoverflow.com/questions/43037518/azure-http-error-404-keeps-logging-and-wordpress-database-error)
**Creation Date:** 1490585477
**Score:** 0
**Tags:** php, wordpress, azure
## Question Body
<p>Good day!We newly migrated our Wordpress site to Azure, it was successful but when I turned On Detailed Errors &amp; php error log in portal,I found lots of error logs stating http 404.
After reading many forums and applied their solutions still the errors aren't solved, Also contacted Azure supports, while we are waiting for actions from their end, I am seeking other opinions for help cause our site is experiencing some downtime and thinking if these errors were related.</p>

<p>php_error.log says:</p>

<pre><code>WordPress database error Lock wait timeout exceeded; try restarting transaction for query UPDATE
PHP Fatal error:  Cannot use object of type stdClass as array in D:\home\site\wwwroot\wp-content\plugins\floating-social-bar\class-floating-social-bar.php on line 687
</code></pre>

<p>One of the errors in Detailed Errors folder: </p>

<pre><code>HTTP Error 404.0 - Not Found
    The resource you are looking for has been removed, had its name changed, or is temporarily unavailable.
    Detailed Error Information:
    Module     FastCgiModule
    Notification     ExecuteRequestHandler
    Handler    PHP56_via_FastCGI
    Error Code     0x00000000
    Requested URL    https://ourdomain:80/index.php?url=apple-touch-icon.png
    Physical Path    D:\home\site\wwwroot\index.php
    Logon Method     Anonymous
    Logon User     Anonymous
</code></pre>

<p>I have tried this in web.config, although some of the errors are not displaying anymore but I think it crawls to other files and keeps throwing http errors.</p>

<pre><code>&lt;rule name="WordPress: https://ourdomain.com" stopProcessing="true"&gt;
  &lt;match url="^(.*)$" ignoreCase="false" /&gt;
  &lt;conditions logicalGrouping="MatchAll"&gt;
    &lt;add input="{REQUEST_FILENAME}" matchType="IsFile" ignoreCase="false" negate="true"/&gt;
    &lt;add input="{REQUEST_FILENAME}" matchType="IsDirectory" ignoreCase="false" negate="true"/&gt;
  &lt;/conditions&gt;
  &lt;action type="Rewrite" url="index.php?url={R:1}" appendQueryString="true"/&gt;
&lt;/rule&gt;
</code></pre>

<p>Do you have any idea how to resolved this?What should I do?</p>

<p>Appreciate your great help for this.</p>

<p>Thank you very much,</p>

<p>Bong</p>

## Answers
### Answer ID: 43060060
<p>Seems you are using Azure App Service <strong>MySQL in-app</strong>, and as you mentioned, "<em>our site is experiencing some downtime</em>".
I suppose that you have not turned on <code>Always on</code> for your app service.</p>

<blockquote>
  <p><strong>Always On</strong>. By default, web apps are unloaded if they are idle for some period of time. This lets the system conserve resources. In Basic or Standard mode, you can enable Always On to keep the app loaded all the time. If your app runs continuous web jobs, you should enable Always On, or the web jobs may not run reliably.</p>
</blockquote>

<p>Form <a href="https://learn.microsoft.com/en-us/azure/app-service-web/web-sites-configure" rel="nofollow noreferrer">https://learn.microsoft.com/en-us/azure/app-service-web/web-sites-configure</a></p>

<p>You can enable it via <a href="http://portal.azure.com" rel="nofollow noreferrer">Azure portal</a> if you are running in Basic or Standard mode.</p>

