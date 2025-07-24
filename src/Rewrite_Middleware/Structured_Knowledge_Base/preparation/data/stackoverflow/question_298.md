# What precautions can I take for using custom authentication on a Windows application?
[Link to question](https://stackoverflow.com/questions/19813160/what-precautions-can-i-take-for-using-custom-authentication-on-a-windows-applica)
**Creation Date:** 1383743889
**Score:** 1
**Tags:** c#, wpf, security, authentication, mvvm
## Question Body
<p>I am writing a new version of a Delphi app in WPF/MVVM. It is not a complete redesign from the ground up, but rather just replacing Delphi code with WPF code, with a few modernization changes. I currently only have access to the running Delphi app, not source, but will have that soon.</p>

<p>Currently authentication uses a database query for a user name and hashed - I suspect it's not quite one way, but must address that later than today - password. How do I store that a user is authenticated, to check for access to all application commands and data? A simple private boolean in the <code>User</code> view model, an instance which is contained in the top level, application, view model? Or maybe when I extend to authorization, simply the fact that the <code>User</code> view model has been allocated a null list of permissions? What is normally done here?</p>

<p>The application is an access control and time and attendance management app for a very large international corporation, so security levels need be fairly high. Using AD is not feasible at this point due to the equally massive user base and list of access rights, and the rewrite is on very high priority.</p>

## Answers
### Answer ID: 19813418
<p>Not a simple question, actually.</p>

<p>This doesn't fit as a comment, so I'm posting this as an answer:</p>

<ul>
<li>what is the architecture of your application? 2-tier? 3-tier?</li>
<li>are you using WCF for the communication?</li>
<li>who are the users of your application? Windows users?</li>
<li>from where is your application used? In a Windows domain? Over the Internet?</li>
</ul>

<p>Those questions might help you decide which way to go.</p>

<p>For example, if you're using 3-tier architecture, WCF for the communication, application used on a Windows domain, you might be interested in a non-custom authentication (you could use Windows authentication). See <a href="http://msdn.microsoft.com/en-us/library/ff647503.aspx" rel="nofollow">MSDN (Authentication, Authorization, and Identities in WCF)</a>.</p>

