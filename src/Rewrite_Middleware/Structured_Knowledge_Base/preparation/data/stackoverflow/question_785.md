# Authorize user based on API-key supplied in request header in ASP.NET Core
[Link to question](https://stackoverflow.com/questions/42069867/authorize-user-based-on-api-key-supplied-in-request-header-in-asp-net-core)
**Creation Date:** 1486390426
**Score:** 11
**Tags:** asp.net-core, authorization, asp.net-authorization, asp.net-core-identity
## Question Body
<p>I'm trying to rewrite some authorization I currently have for ASP.NET 4.6 in ASP.NET Core.</p>

<p>I understand that Authorization has changed a bit, and I find it difficult to implement my very simple auth strategy in ASP.NET Core. </p>

<p><strong>My requirements:</strong></p>

<p>Every request to the server should include a header called "key". Based on the value of that key, I will be able to query the database and check whether that key represents a regular user or an admin user. If the request does not contain a valid key, the request is not authorized.</p>

<p>How would I implement this in ASP.NET Core? Every example I find seems totally overkill for my needs. </p>

<p>In ASP.NET 4.6 I used my own custom AuthorizeAttributes to use on my controllers, e.g.</p>

<pre><code>[User]
public IHttpActionResult DoSomethingOnlyUsersCanDo() {}
</code></pre>

<p>and</p>

<pre><code>[Admin]
public IHttpActionResult DoSomethingOnlyAdminsCanDo() {}
</code></pre>

<p>Can I do the same in ASP.NET Core?</p>

## Answers
### Answer ID: 42071958
<p>In ASP.NET Core, it is recommended that you <em>do not inherit from AuthorizeAttribute</em>. Instead, you can make custom authorization policies: <a href="https://learn.microsoft.com/en-us/aspnet/core/security/authorization/claims" rel="noreferrer">https://learn.microsoft.com/en-us/aspnet/core/security/authorization/claims</a>.</p>

<p>You will need to have an authentication handler that creates a ClaimsIdentity for the user based on the header. Then you can make policies that assert the existence of certain claims on the user.</p>

<p>You can find an implementation of Basic authentication here: <a href="https://github.com/blowdart/idunno.Authentication" rel="noreferrer">https://github.com/blowdart/idunno.Authentication</a>.
Note Barry's comment there of course:</p>

<blockquote>
  <p>It is meant as a demonstration of how to write authentication middleware and not as something you would seriously consider using.</p>
</blockquote>

<p>Its core is in <a href="https://github.com/blowdart/idunno.Authentication/blob/master/src/idunno.Authentication/BasicAuthenticationHandler.cs" rel="noreferrer">BasicAuthenticationHandler</a>, which inherits from <code>AuthenticationHandler&lt;BasicAuthenticationOptions&gt;</code>.</p>

<p>The principal in this implementation is created in the developer-made event callback, in the sample it is <a href="https://github.com/blowdart/idunno.Authentication/blob/master/src/idunno.Authentication.Demo/Startup.cs#L32" rel="noreferrer">here</a>:</p>

<pre><code>if (context.Username == context.Password)
{
    var claims = new[]
    {
        new Claim(ClaimTypes.NameIdentifier, context.Username, ClaimValueTypes.String, context.Options.ClaimsIssuer),
        new Claim(ClaimTypes.Name, context.Username, ClaimValueTypes.String, context.Options.ClaimsIssuer)
    };

    context.Principal = new ClaimsPrincipal(new ClaimsIdentity(claims, context.Scheme.Name));
    context.Success();
}
</code></pre>

<p>The authentication ticket is then created in the handler after calling this callback based on the principal:</p>

<pre><code>var ticket = new AuthenticationTicket(validateCredentialsContext.Principal, Scheme.Name);
return AuthenticateResult.Success(ticket);
</code></pre>

<p>I also made an article on implementing custom authentication schemes: <a href="https://joonasw.net/view/creating-auth-scheme-in-aspnet-core-2" rel="noreferrer">Creating an authentication scheme in ASP.NET Core 2.0</a>.</p>

