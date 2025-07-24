# ASP.NET MVC authentication using custom database instead of ASPNETDB?
[Link to question](https://stackoverflow.com/questions/2054973/asp-net-mvc-authentication-using-custom-database-instead-of-aspnetdb)
**Creation Date:** 1263365968
**Score:** 28
**Tags:** c#, asp.net, sql-server, asp.net-mvc, authentication
## Question Body
<p>I already have a <code>User</code> table in my primary application database with an email address (which will act as the user name) and a password. I would like to authenticate using my database instead of the default authentication database (ASPNETDB).</p>

<p><strong>Questions:</strong></p>

<ol>
<li><p>Is this a bad idea? Is it a huge can of worms to use my own DB for authentication?</p></li>
<li><p>How much work am I adding by doing this? I already have code for hashing the password and a query that will check if the email and password match the DB. So, I wouldn't be starting from scratch.</p></li>
<li><p>What would I need to do to use my database instead of ASPNETDB? I'm hoping this can be described in a few simple steps, but if not, could you point me to good source?</p></li>
</ol>

<p><strong>Update</strong></p>

<p><strong>I'm still looking for a little more detail here on my third question.</strong> Do I need to write my own <code>MembershipProvider</code>? What changes do I need to make to my web.config file? Will the <code>[Authorize]</code> attribute still work if I write my own solution? Can I use the automatically-generated AccountController with some minor modifications or do I basically need to rewrite the account controller from scratch?</p>

## Answers
### Answer ID: 48602804
<p><strong>Hi ,
Just follow these simple steps :</strong></p>

<p><strong>First</strong>, you can delete the .mdf file in App_Data folder. Since we don’t need any of these tables.<strong>Then</strong>, we need to update the default connection string in the web.config to point to our database.</p>

<pre><code>&lt;connectionStrings&gt;
    &lt;add name=”DefaultConnection” connectionString=”Data Source=SERVER\INSTANCENAME;Initial Catalog=DBNAME;Integrated Security=True” providerName=”System.Data.SqlClient” /&gt;
  &lt;/connectionStrings&gt;
</code></pre>

<p><strong>Third</strong>, Open Nuget Package Manager and write the following commands:</p>

<pre><code>Enable-Migrations
Add-Migration Init
Update-Database
</code></pre>

<p>Check out your database, all ASP.NET membership tables with Prefix Asp have been create and then you can test it out by running your application and execute membership actions such as Signing up or Signing in to your application.</p>

<p>Created tables after running above commands:</p>

<ul>
<li>AspNetRoles</li>
<li>AspNetUserClaims</li>
<li>AspNetUserLogins</li>
<li>AspNetUserRoles</li>
<li>AspNetUsers</li>
<li>__MigrationHistory</li>
</ul>

<p>Source : <a href="https://blogs.msmvps.com/marafa/2014/06/13/how-to-create-asp-net-mvc-authentication-tables-in-an-existing-database/" rel="nofollow noreferrer">https://blogs.msmvps.com/marafa/2014/06/13/how-to-create-asp-net-mvc-authentication-tables-in-an-existing-database/</a></p>

### Answer ID: 2059689
<p>It's quite simple, you need to derrive MembershipProvider and implement the ValidateUser method. Take a look at this <a href="http://www.hurryupandwait.io/blog/implementing-custom-membership-provider-and-role-provider-for-authenticating-asp-net-mvc-applications" rel="nofollow noreferrer">post</a>. I'm using custom membership provider with Postgres and MVC just fine.</p>

### Answer ID: 2059821
<p>I'll answer your updated questions:</p>

<blockquote>
  <p>Do I need to write my own MembershipProvider?</p>
</blockquote>

<p>If you (a) want to continue using Forms Authentication, and (b) have an authorization table structure that doesn't follow the same conventions as the ASPNETDB, then yes.  If you don't need FormsAuth (see below), then you can do away with the <code>MembershipProvider</code> entirely, but I wouldn't recommend it. Or, if you're using the exact same security tables as ASPNETDB but just want to point it to a different database, you can continue using the default provider and simply change its configuration.</p>

<blockquote>
  <p>What changes do I need to make to my web.config file?</p>
</blockquote>

<p>If you are using your own custom <code>MembershipProvider</code>, then you need to register it in the <code>&lt;providers&gt;</code> section of the <code>&lt;membership&gt;</code> element and change the <code>defaultProvider</code> property.  If you are using the standard <code>AspNetSqlProvider</code> then you probably just need to change the connection string.</p>

<blockquote>
  <p>Will the [Authorize] attribute still work if I write my own solution?</p>
</blockquote>

<p>Yes, if you stick to Forms Authentication (either use the <code>AspNetSqlProvider</code> or write and register your own membership provider).  No, if you abandon Forms Authentication (again, not recommended).</p>

<blockquote>
  <p>Can I use the automatically-generated AccountController with some minor modifications or do I basically need to rewrite the account controller from scratch?</p>
</blockquote>

<p>You should rewrite the <code>AccountController</code> anyway - don't leave demo code in a production app.  But if you must - yes, the <code>AccountController</code> will work under the same conditions as above.</p>

### Answer ID: 2056003
<p>just building the same, so answer to 1 must be NO :)
I'm using the standard  asp.net forms authentication, where i use the FormsAuthentication.RedirectFromLoginPage(username, createCookieBool) method to log a user in.
I gave a user a unique guid (you can use any other user id) and i'm storing it in the UserName parameter along with the username (to display on the masterpage: Html.Encode(Page.User.Identity.Name.Split("|".ToCharArray())[1]))</p>

<p>In each controller/method in which i must know which user is logged on (via User.Identity.Name, split the string and get the userguid).
Also i decorate those routines with the  [Authorize] attribute.</p>

### Answer ID: 2055176
<p>We're doing exactly this in one of our applications, and find it quite simple.  We have an authentication service (called from the controller) that handles the mechanics of hashing the entered password to see if it is a match, then simply returns a bool for a method we call "IsValidLogon".</p>

<p>In our case, the purpose was to keep the management of what should be a pretty trivial task as lightweight as possible.</p>

<p>We bascially ignored ASPNETDB entirely.  If we get a valid response from our user/password check, we simply call the standard FormsAuthentication.RedirectFromLoginPage(username, createCookieBool);</p>

<p>Hope that helps.</p>

### Answer ID: 2055005
<ol>
<li><p>No.  And I would suspect most people do not trust that cruddy mechanism</p></li>
<li><p>Not much at all, especially since you have the table already.</p></li>
<li><p>Take a look at this for example: <a href="http://forums.asp.net/t/1250726.aspx" rel="nofollow noreferrer">http://forums.asp.net/t/1250726.aspx</a></p></li>
</ol>

