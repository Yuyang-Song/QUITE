# Authorization and Authentication with Clean Architecture using Asp.Net Core Identity
[Link to question](https://stackoverflow.com/questions/71784435/authorization-and-authentication-with-clean-architecture-using-asp-net-core-iden)
**Creation Date:** 1649343352
**Score:** 6
**Tags:** asp.net-mvc, asp.net-core, asp.net-identity, clean-architecture
## Question Body
<p>I'm learning about Clean and Vertical Slice Architecture for the first time and I'm having trouble understanding where Authorization and Authentication would fit in if we are using ASP.NET Core Identity. Also it feels as though, in some scenarios, separating the Identity User (with username, password, email etc), from any user related domain entity would be tricky.</p>
<p>For example, if we had a solution which used ASP.NET Core MVC, ASP.NET Core Identity, then an example project structure could be as follows:</p>
<p><strong>Presentation/WebUI Project:</strong></p>
<ul>
<li>cshtml views / Razor pages would live here, along with controllers (if not using Razor pages).</li>
<li>The program/startup.cs for this project is where the extension methods from other layers could be called:</li>
</ul>
<pre><code>app.services.InjectInfrastructure(); // same for application
</code></pre>
<p><strong>Infrastructure Project:</strong></p>
<ul>
<li>Implementations of application layer contracts.</li>
<li>Database contexts.</li>
<li>Perhaps implementations of repositories if you are using them.</li>
</ul>
<p><strong>Application Project:</strong></p>
<ul>
<li>Commands / queries (assuming using something like MassTransit.Mediator or MediatR).</li>
<li>Validators (for example with fluent validation).</li>
</ul>
<p><strong>Domain Project:</strong></p>
<ul>
<li>Domain entities (anaemic or with methods if following DDD).</li>
<li>Any aggregates, value objects etc (if using).</li>
</ul>
<p>We could therefore have a scenario that has the following flow:</p>
<ol>
<li>Controller action invoked to get some data (representing the application layer query), which returns rendered html (cshtml view).</li>
<li>Data is populated on this html page and a POST request (representing the application layer Command) is sent to a controller action.</li>
<li>The command or query is sent using MediatR.</li>
<li>Command handler runs (with data access such as dbcontext or repository), which validates, makes the appropriate changes to the data and returns a response.</li>
<li>Response returned to the controller, which can then determine if the command/query has been successful</li>
<li>Controller redirects to another action or populates ModelState errors.</li>
</ol>
<p>Where I struggle to separate auth concerns is in a scenario where a user in the system has different roles and permissions depending on chocies they make on sign in.</p>
<p>For example, a education application where a teacher can select the school they are currently representing. In one school, they may have a certain role (for example head teacher) and in another they may have a role with lesser privellage.</p>
<p>In a scenario such as this, it seems like the Roles, Application Users (both identity concerns) are tightly coupled with the domain (which would house the different schools and roles that each school has).</p>
<p><strong>My overarching question being, how would we implement this sort of Authentication/Authorization scenario using ASP.NET identity in a clean architecture fashion?</strong></p>
<p>At the moment this scenario poses multiple problems:</p>
<ol>
<li>If we are to decouple Authentication / Authorization from the presentation layer, we cannot rely on the [Authorize(Role = &quot;X&quot;)] [Authorize(Policy = &quot;Y&quot;)] decorators on our controllers, as this logic should be delegated to infrastructure
(to ensure if we wanted to swap presentation layer at any point, we do not need to rewrite authentication / authorization)</li>
<li>The user in this scenario is tightly coupled to the domain logic, so I can only see it working if identity related entities and domain entities are squashed together in a single
dbContext</li>
</ol>
<p>Has anyone ever come across / implemented a system like this using clean architecture? Any insight anyone has on this would be great!</p>

## Answers
### Answer ID: 78783265
<p>So you have authorization policies defined in domain layer?</p>
<p>You just need to wire up your &quot;clean&quot; authorization logic (policies) defined in domain to ASP.NET Core Authorization policies and continue using <code>[Authorization]</code> attribute.</p>
<pre><code>authorizationOptions.AddPolicy(YourCleanPolicy.Name, policy =&gt;
{
   policy.AddRequirements(new DomainPolicyRequirement(YourCleanPolicy.Name))
   //or alternatively
   policy.RequireAssertion(ctx =&gt; ...)
});
</code></pre>
<p>The RequirementHandler might go to the database and fetch additional user details if needed, but ideally you <code>IPrincipal</code> should contain all the claims needed. You can achieve this via <code>IClaimsTransformation</code></p>

