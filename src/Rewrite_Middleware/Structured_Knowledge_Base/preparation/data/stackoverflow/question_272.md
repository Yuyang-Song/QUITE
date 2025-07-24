# ColdFusion 8 to ColdFusion 10 Migration: CFloginUser Not Working As Expected
[Link to question](https://stackoverflow.com/questions/18680629/coldfusion-8-to-coldfusion-10-migration-cfloginuser-not-working-as-expected)
**Creation Date:** 1378616896
**Score:** 2
**Tags:** iis, coldfusion, coldfusion-8, coldfusion-10, cflogin
## Question Body
<p>After upgrading from CF8 to CF10, moving all files and databases and jumping through all the configuration hoops, the new version of the site is up and running, but the authentication/login is not working.</p>

<p>Here are the environments:</p>

<p><strong>Old server:</strong> ColdFusion Enterprise 8,0,1,195765</p>

<blockquote>
  <p>Operating System: Windows Vista*</p>
  
  <p>OS Version: 6.0</p>
  
  <p>Update Level: .... hf801-00007.jar</p>
  
  <p>IIS Version: 7</p>
</blockquote>

<p>(*not sure where that "Vista" comes from? The System Information says "Windows Server 2008 Datacenter without Hyper-V")</p>

<p><strong>New server:</strong> ColdFusion Enterprise 10,0,11,285437</p>

<blockquote>
  <p>Tomcat Version: 7.0.23.0</p>
  
  <p>Operating System: Windows Server 2008 R2</p>
  
  <p>OS Version: 6.1</p>
  
  <p>Update Level: .... chf10000011.jar</p>
  
  <p>Adobe Driver Version: 4.1 (Build 0001)</p>
  
  <p>IIS Version: 7.5</p>
</blockquote>

<p>I have a pretty standard ColdFusion login system, using <a href="https://learn.adobe.com/wiki/display/coldfusionen/cfloginuser" rel="nofollow">cfloginuser</a> in Application.cfc. After I login on the old site, outputting <code>#GetAuthUser()#</code> prints my username to screen, and all my role-based rules work.</p>

<p>On the new server, outputting GetAuthUser() prints empty.</p>

<p>On the old site, <code>cfdump var="#SESSION#"</code> includes:</p>

<pre><code>cfauthorization_kllcms dXNlcm5hbWU6cGFzc3dvcmQ6YXBwX25hbWU= 
</code></pre>

<p>On the new site, <code>CFDUMP</code> of session does not show a <code>cfauthorization_kllcms</code> value at all. All other session values exist in both instances.</p>

<p>It is the exact same codebase, database structures, etc. Naturally, none of my role-based rules work, because they all depend on validation of getAuthUser() and IsUserInRole("x") conditionals.</p>

<p>I know the initial login process itself is working, because it is correctly setting session variables with user information, and they are available on subsequent requests. But none of the traditional cflogin data is available on subsequent calls.</p>

<p>Any ideas what might have changed?</p>

<p><strong>UPDATE:</strong> Per Adam's suggestion (below) I set up 2 test apps, one on the old server, one on the new. </p>

<p><strong>Old Server:</strong> <a href="http://cfloginold.cimhost.com/index.cfm" rel="nofollow">http://cfloginold.cimhost.com/index.cfm</a></p>

<p><strong>New Server:</strong> <a href="http://cflogin.cimhost.com/index.cfm" rel="nofollow">http://cflogin.cimhost.com/index.cfm</a> </p>

<p>Use "test" and "demo982013" as user and password.</p>

<p>Append <code>?logout=true</code> to the URL to logout and re-test. These two apps have exactly the same code, same database. I am dumping session and form values to screen, along with <code>GetAuthUser()</code> value. </p>

<p>The authentication method is pretty much exactly as outlined in <a href="http://help.adobe.com/en_US/ColdFusion/10.0/Developing/WSc3ff6d0ea77859461172e0811cbec22c24-7c30.html" rel="nofollow">Adobe's documentation</a>, and I can share all relevant code here if necessary. </p>

<p>Note that in the "new" server, the form loads each time you visit the page, whether you have logged in or not. This is exemplar of the fact that the <code>cflogin</code> session is not being retained or recognized, thus presenting the login form each visit (although not on initial form completion, which shows that cflogin is at least working on the initial login, I think).</p>

<p><strong>UPDATE 2:</strong>
I've been drilling deeper into this, and I am able to get cfloginuser to fire a couple of ways, just not as part of the standard <a href="http://help.adobe.com/en_US/ColdFusion/10.0/Developing/WSc3ff6d0ea77859461172e0811cbec22c24-7c30.html" rel="nofollow">Adobe documented application-based user security model</a>.</p>

<p><strong>Option 1:</strong> I created a standalone page, and placed the following code in it:</p>

<pre><code>&lt;cflogin&gt;&lt;cfloginuser name="directtest" Password = "2519D6025B5191F754D01BE163972628" roles="1"&gt;&lt;/cflogin&gt;
</code></pre>

<p>I then instructed Application.cfc to allow this past the <code>cflogin</code> gate. You can see the results by pointing your browser to: <a href="http://cflogin.cimhost.com/directlogin.cfm?bypass=true" rel="nofollow">http://cflogin.cimhost.com/directlogin.cfm?bypass=true</a></p>

<p>Voila. 'cfauthorization_cicmstest' value has been set, and user is logged in. Subsequent calls to <code>GetAuthUser()</code> are successful. So I know now that CF10 and the application do allow cfloginuser, and the user session can be created.</p>

<p><strong>Option 2:</strong> I then decided maybe it was something about my Application.cfc file, so I again bypassed the <code>cflogin</code> gate, and placed the hard-coded <code>cfloginuser</code> snippet directly in my Application.cfc <code>onRequestStart</code> function. Logged out and visited: <a href="http://cflogin.cimhost.com/index.cfm?bypass=true&amp;noquery=true" rel="nofollow">http://cflogin.cimhost.com/index.cfm?bypass=true&amp;noquery=true</a></p>

<p>Again, <code>cfauthorization_cicmstest</code> value was successfully set, and user is logged in.</p>

<p>However, logging in still fails if the <code>cfloginuser</code> directive is fired within the actual <code>cflogin</code> process in Application.cfc. Here is what that code looks like:</p>

<pre><code>        &lt;cfquery name="loginQuery" dataSource="mydatasource"&gt;
        SELECT id,username, userroles
        FROM myusertable
        WHERE
           username = '#cflogin.name#'
           AND userpass = '#HASH(cflogin.password)#'
        &lt;/cfquery&gt;
        &lt;cfif loginQuery.userroles NEQ ""&gt;
           &lt;cfloginuser name="#cflogin.name#" Password="#cflogin.password#" roles="#loginQuery.userroles#"&gt;
           &lt;cfset MyMessage = "#MyMessage#&lt;br /&gt;The Login Query fired and returned expected - loginQuery.userroles NEQ ''"&gt;

        &lt;cfelse&gt;
           &lt;CFSET MyMessage = "Your login information is not valid. &lt;a href='index.cfm?logout=1'&gt;If your session timed out, click here!&lt;/a&gt;"&gt;   
           &lt;cfinclude template="loginform.cfm"&gt;
           &lt;cfabort&gt;
        &lt;/cfif&gt;
</code></pre>

<p>I know that the query is successful, because I am setting an alert message that tells me the <code>loginquery.userroles</code> value was not empty, which is the condition for processing <code>cfloginuser</code>.</p>

<p>I know where the code is failing now, just not why. I've tried hard coding that <code>cfloginuser</code> value, and it still fails. I'm at a loss as to what to try next. The <code>cfloginuser</code> functionality works, just not in the one place (within the <code>loginQuery.userroles</code> conditional) that I need it to work.</p>

<p><strong>UPDATE 3:</strong></p>

<p>Just to prove to myself it wasn't my code, I created 2 more test sites, one on the old server, one on the new server:</p>

<p>New Server (CF10) = <a href="http://cf10loginadobe.cimhost.com/securitytest.cfm" rel="nofollow">http://cf10loginadobe.cimhost.com/securitytest.cfm</a></p>

<p>Old Server (CF8) = <a href="http://cf8loginadobe.cimhost.com/securitytest.cfm" rel="nofollow">http://cf8loginadobe.cimhost.com/securitytest.cfm</a></p>

<p>I copied exactly <a href="http://help.adobe.com/en_US/ColdFusion/10.0/Developing/WSc3ff6d0ea77859461172e0811cbec22c24-7c30.html" rel="nofollow">Adobe's 3 files from their Application-based security example.</a> I created a database table with their schema and values. I added my <code>cfdump</code> outputs to show the sessions being created.</p>

<p>Test with user of "Bob" and password of "secret". Even with Adobe's own code, the tests fail on CF10.</p>

<p>I'm not sure what to do next. Rewriting the application to not use <code>cfloginuser</code> is not an option, as we have more than a dozen applications we are migrating to CF10 that use this authentication model, across hundreds of templates.</p>

<p>It's possible it's something weird about how IIS7.5 is handling ColdFusion requests, but that seems unlikely given the ability to successfully instantiate <code>cfloginuser</code> outside of the query result conditional.</p>

## Answers
### Answer ID: 18705006
<p><strong>ColdFusion 10 Application Based User Security Is Broken</strong></p>
<p>I have deployed two test sites, using <a href="http://help.adobe.com/en_US/ColdFusion/10.0/Developing/WSc3ff6d0ea77859461172e0811cbec22c24-7c30.html" rel="nofollow noreferrer">Adobe's own example code for application based user security</a>, copied in its entirety from the Adobe website. One test site is in ColdFusion 8, one is ColdFusion 10. The code and databases are identical on both sites. I added <code>cfdump</code> output to monitor session variables and login status as they are set.</p>
<p><strong>Test Site ColdFusion 8:</strong>  <a href="http://cf8loginadobe.cimhost.com/securitytest.cfm" rel="nofollow noreferrer">http://cf8loginadobe.cimhost.com/securitytest.cfm</a></p>
<p><strong>Test Site ColdFusion 10:</strong> <a href="http://cf10loginadobe.cimhost.com/securitytest.cfm" rel="nofollow noreferrer">http://cf10loginadobe.cimhost.com/securitytest.cfm</a></p>
<p>Logging in using a user of &quot;Bob&quot; and password of &quot;secret&quot; demonstrates the failure in CF10. Initially it appears login was successful, but note that the <code>cfdump</code> of the session <em>does not show</em> a <code>cfauthorization_orders</code> value in CF10, where in CF8 the value is present.</p>
<p>In CF8 subsequent visits to the same URL after login correctly retain the logged in user status and do not present the login form. In CF10, no session was actually created for the user, and therefore subsequent visits to the same URL prompt for login again.</p>
<p>I have tested this thoroughly, including bypassing the <code>cflogin</code> logic and forcing <code>cfloginuser</code>, which successfully creates an authenticated user in CF10, demonstrating that <code>cfloginuser</code> is supported.</p>
<p>It appears to me there is something about CF10's handling of the <code>OnRequestStart</code> function in Application.cfc that creates and then immediately kills the user session.</p>
<p><strong>Workaround:</strong> The inelegant workaround I am using involves re-creating the <code>cfloginuser</code> session instantiation in a subsequent <code>OnRequest</code> function in Application.cfc. The code is as follows:</p>
<pre><code>&lt;cffunction name=&quot;onRequest&quot;&gt;
&lt;cfargument name = &quot;targetPage&quot; type=&quot;String&quot; required=true/&gt;
&lt;cfinclude template=#Arguments.targetPage#&gt;

&lt;cfif IsDefined(&quot;loginQuery&quot;)&gt;
  &lt;cfif loginQuery.userroles NEQ &quot;&quot;&gt;
    &lt;cflogin&gt;&lt;cfloginuser name=&quot;#loginQuery.username#&quot; Password = &quot;#loginQuery.userpass#&quot; roles=&quot;#loginQuery.userroles#&quot;&gt;&lt;/cflogin&gt;
  &lt;/cfif&gt;
&lt;/cfif&gt;

&lt;/cffunction&gt;
</code></pre>
<p>If there was an attempt to login in the <code>OnRequestStart</code>, I leverage the results of that request, check if it was valid (<code>loginQuery.userroles NEQ &quot;&quot;</code>), and then instantiate the authenticated session. There is a downside in that users have to click to a new page for logged in options to appear. The <code>GetAuthUser()</code> test is not met until another page load is requested.</p>
<p>Extensive testing of alternatives within Application.cfc did not reveal any alternative to this approach.</p>

