# Struts2 Authorization
[Link to question](https://stackoverflow.com/questions/12552383/struts2-authorization)
**Creation Date:** 1348403528
**Score:** 2
**Tags:** security, tomcat, struts2, spring-security, roles
## Question Body
<p>I am about to graduate from university with a web application that needs be implemented at school, everything is working perfect and this needs to be ready before november but I'm having a real trouble taking care of the security. The application must be able to have different users with one or more different roles, ( user1: roles: student; user 2: admin, user 3: professor, boss ).</p>

<p>When a user logs in it should be redirected to a different view depending on the roles it has and then if he tries to access to resources not allowed for his role, an error page should be shown.</p>

<p>This is what I've tried so far:</p>

<p><strong>Method 1:</strong> </p>

<p>Authentication Method: Specified in web.xml as</p>

<pre><code>&lt;login-config&gt;
   &lt;auth-method&gt;FORM&lt;/auth-method&gt;
   &lt;form-login-config&gt;
      &lt;form-login-page&gt;/login.jsp&lt;/form-login-page&gt;
   &lt;/form-login-config&gt;
&lt;/login-config&gt;
</code></pre>

<p>Then using the names j_username and j_password along with j_security_check on a custom jsp.</p>

<p>Authorization Method: Used Container Security (Tomcat) via <a href="http://tomcat.apache.org/tomcat-7.0-doc/realm-howto.html#DataSourceRealm" rel="nofollow">DataSourceRealm</a>, wich allow us to connect to a database and get the user and the roles associated with him from 2 Tables that need to be mapped in the server.xml:</p>

<pre><code>&lt;Resource auth="Container" driverClassName="com.microsoft.sqlserver.jdbc.SQLServerDriver" maxActive="100" maxIdle="30" maxWait="1000" name="jdbc/sstt" password="pass" type="javax.sql.DataSource" url="jdbc:sqlserver://localhost;databaseName=BDTT" username="sa"/&gt;
</code></pre>

<p>web.xml:</p>

<pre><code>&lt;security-constraint&gt;

    &lt;web-resource-collection&gt;
        &lt;web-resource-name&gt;Students Only&lt;/web-resource-name&gt;
        &lt;url-pattern&gt;/student/*&lt;/url-pattern&gt;
    &lt;/web-resource-collection&gt;

    &lt;auth-constraint&gt;
        &lt;role-name&gt;student&lt;/role-name&gt;
    &lt;/auth-constraint&gt;

&lt;/security-constraint&gt;

// Same mapping for professor, admin, and boss (/professor/* maps to professor role)
</code></pre>

<p><strong>Results:</strong> Whenever I tried to access a restricted area, for example, /members/ (configured in the web.xml inside a security constraint) it would work just perfect, so authorization goal was achieved.</p>

<p><strong>The problem:</strong> 
When I submit the login form it fires the j_security_check so I'm not able to fire a Struts2 Action that could help me to <strong>redirect depending on the user roles</strong> this is the main problem. Everything was perfect but I can't find a way to redirect after logging in with the Container security. </p>

<p><strong>Method 2:</strong> </p>

<p>Authentication Method: A LoginAction class that queries the database and checks if the password is correct. It also checks on the user roles and here we should be able to return a String like "admin", or "student" and redirect to the appropriate index.jsp resource, but that would work <strong>only if users were allowed to have only one role, but they can have many</strong>, so <strong>how should the view be constructed depending on the total user roles</strong>? What String would we return?</p>

<p>Authorization Method: I wrote a custom Interceptor wich retrieves the User object from the session (this User object should be in the session only if the user authenticated successfully) and then perform the authorization logic here. </p>

<p><strong>The problem:</strong> 
Unable to find a way to construct a view depending on several roles, and the problem about the Interceptor is that it only protects my actions, so the authorization goal was achieved but only on actions, that means I could write /students/ and the URL would change to /students/index.jsp without even trying to authorize.</p>

<p><strong>Other plans</strong></p>

<p>I was thinking that maybe I could use filters to achieve the authorization ( that way I could protect both the dynamic and static resources ) but I don't know if that would be a good practice since we have configured the Struts2 filter which maps to /*</p>

<p>I was also looking that I could use <strong>JAAS</strong> or <strong>Spring Security</strong> but I don't know if I could achieve this, <strong>authenticate, redirect based on roles and authorizate</strong>. I wouldn't want to spend more several hours to find out that I can't do what I need, and I have just a very short time to finish this.</p>

<p><strong>Other questions</strong></p>

<p>Is it really a good practice to put jsp under WEB-INF? if so I should rewrite all the access to my jsp's in the struts.xml to WEB-INF/jsp/students/index.jsp? ( for example ). Or should I stick to a security constraint defined in web.xml to avoid direct access to the /jsp/* url pattern?</p>

<p>Thank You very much in advance for all your time and help.</p>

## Answers
### Answer ID: 12642964
<p>For problem in method 1: You can write Struts2 interceptor to achieve what you want.</p>

<p>For Spring Security examples see my answer to this question <a href="https://stackoverflow.com/questions/12615354/how-to-implement-role-based-login/12629731#12629731">https://stackoverflow.com/questions/12615354/how-to-implement-role-based-login/12629731#12629731</a></p>

<p>And YES it is a good practice to put jsp under WEB-INF folder. See <a href="https://stackoverflow.com/questions/6825907/why-put-jsp-in-web-inf">Why put JSP in WEB-INF?</a></p>

