# Kestrel Server Login Redirection Goes to HTTP Instead of HTTPS
[Link to question](https://stackoverflow.com/questions/45108478/kestrel-server-login-redirection-goes-to-http-instead-of-https)
**Creation Date:** 1500052520
**Score:** 1
**Tags:** c#, asp.net-core, asp.net-core-mvc, kestrel-http-server
## Question Body
<p>I'm having trouble with my MVC site. We use Shibboleth and Kerberos to handle automatic logins based on the user's network ID. We configure Shibboleth so that it protects the entire website, minus a couple of Anonymous-allowed pages to display errors or access denied messages.</p>

<p>The system works great if you try to navigate to the root of the site. It forwards to Shibboleth to authenticate, then it forwards back to my site with Headers including the User ID, which we then authorize against a database list of users and permissions.</p>

<p>The problem comes if the first navigation is to any page other than /Home. The redirection steps are as follows. Note that this is an internal site, and I changed the domain, so don't try any of the actual links below. They won't work.</p>

<p><strong>Update</strong>: The Kestrel web server is the one passing us on to HTTP, while the Apache load balancer in front swoops in and says "http isn't allowed, go to https".</p>

<p>1) A user navigates to <a href="https://ets.com/ets/Employees" rel="nofollow noreferrer">https://ets.com/ets/Employees</a>, and receives a 302 due to Shibboleth's site-wide protection. This points to our IDP server's SSOService.php?SAMLResponse=giantquerystringhere to perform automatic login based on the user ID logged into the computer.</p>

<p>2) Shibboleth authenticates and then forwards to a POST event at <a href="https://ets.com/Shibboleth.sso/SAML2/POST" rel="nofollow noreferrer">https://ets.com/Shibboleth.sso/SAML2/POST</a> which fills the header with their ID.</p>

<p>3) The POST event finishes and forwards the user to <a href="https://ets.com/ets/Employees" rel="nofollow noreferrer">https://ets.com/ets/Employees</a> as intended.</p>

<p>4) BUT we need to process the login in the app itself, so the Kestrel server calls 302 and forwards the user to <a href="http://ets.com/ets/Home/Index?ReturnUrl=%2Fets%2FEmployees" rel="nofollow noreferrer">http://ets.com/ets/Home/Index?ReturnUrl=%2Fets%2FEmployees</a> INSTEAD of https</p>

<p>5) The Apache LB picks up on this, and since HTTP is not permitted, it calls 301 (Moved Permanently) and forwards to <a href="https://ets.com/ets/Home/Index?ReturnUrl=%252Fets%252FEmployees" rel="nofollow noreferrer">https://ets.com/ets/Home/Index?ReturnUrl=%252Fets%252FEmployees</a> (note the double-encoded query string)</p>

<p>6) That URL responds 302, processes the Return URL, and forwards the user to the bad URL of <a href="https://ets.com/ets/Home/%2Fets%2FEmployees" rel="nofollow noreferrer">https://ets.com/ets/Home/%2Fets%2FEmployees</a> instead of <a href="https://ets.com/ets/Employees" rel="nofollow noreferrer">https://ets.com/ets/Employees</a></p>

<p>Is there a way to prevent it from forwarding to http in the first place? I've tried some of the "forced HTTPS" methods I've seen in my searching, but most of these required changes that would break the Shibboleth integration, or just didn't work. (Forced reliance on ASP Identity, URL rewriting, etc.)</p>

<p>My question is, why is Kestrel/MVC forwarding to HTTP anyway? Is something configured wrong? Is there an option to enable to prevent this? I cannot change my login mechanism, but I could change how we process the Shibboleth response and process the login on the application side.</p>

<p>I'll try to include the relevant code. Let me know if there's any other info that can help.</p>

<p>Startup.cs</p>

<pre><code>public class Startup
{
    public static IConfigurationRoot Configuration { get; private set; }

    public Startup(IHostingEnvironment env) {
        var builder = new ConfigurationBuilder()
            .SetBasePath(env.ContentRootPath)
            .AddJsonFile("appsettings.json", optional: true, reloadOnChange: true)
            .AddJsonFile($"appsettings.{env.EnvironmentName}.json", optional: true);

        builder.AddEnvironmentVariables();
        Configuration = builder.Build();
    }

   public void ConfigureServices(IServiceCollection services) {
        services.AddMvc(options =&gt; {
            // Only allow authenticated users.
            var defaultPolicy = new AuthorizationPolicyBuilder()
                .RequireAuthenticatedUser()
                .Build();

            options.Filters.Add(new AuthorizeFilter(defaultPolicy));
        });

        // Authorization policies.
        services.AddAuthorization(options =&gt; {
            options.AddPolicy("EditPolicy", policy =&gt; {
                policy.RequireClaim("readwrite", "true");
            });

            options.AddPolicy("AdminPolicy", policy =&gt; {
                policy.RequireClaim("admin", "true");
            });

            options.AddPolicy("SuperAdminPolicy", policy =&gt; {
                policy.RequireClaim("superadmin", "true");
            });
        });

        services.AddDbContext&lt;LoanDbContext&gt;(options =&gt;
            options.UseSqlServer(Configuration.GetConnectionString("ETS_Web")));
    }

    // This method gets called by the runtime. Use this method to configure the HTTP request pipeline.
    public void Configure(IApplicationBuilder app, IHostingEnvironment env, ILoggerFactory loggerFactory, LoanDbContext context) {
        loggerFactory.AddConsole(Configuration.GetSection("Logging"));
        loggerFactory.AddDebug();

        app.UseStatusCodePagesWithReExecute("/Home/Error/{0}");
        if (env.IsDevelopment()) {
            app.UseDeveloperExceptionPage();
            app.UseBrowserLink();
        } else {
            app.UseExceptionHandler("/Home/Error");
        }
        app.UseExceptionLogger(loggerFactory);      // Custom middleware to log exceptions. Rethrows the exception for Exception Handler/Page

        // Forces the website to use en-US locale, no matter what the browser settings are.
        // This is done to enforce date format of mm/dd/yyyy (Canada uses dd/mm/yyyy)
        var supportedCultures = new[] {
            new CultureInfo("en-US")
        };

        app.UseRequestLocalization(new RequestLocalizationOptions {
            DefaultRequestCulture = new RequestCulture("en-US"),
            SupportedCultures = supportedCultures,      // Formatting numbers, dates, etc.
            SupportedUICultures = supportedCultures     // UI strings that may be localized.
        });

        app.UseStaticFiles();   // Allows serving pages that don't belong to a controller.

        app.UseCookieAuthentication(new CookieAuthenticationOptions() {
            CookieName = $"ETS.Web.{env.EnvironmentName.ToLower()}",
            AuthenticationScheme = "ETSCookieAuth",
            LoginPath = new PathString("/Home/Index"),
            AccessDeniedPath = new PathString("/Home/AccessDenied"),
            AutomaticAuthenticate = true,
            AutomaticChallenge = true,
            ExpireTimeSpan = TimeSpan.FromHours(2),
            SlidingExpiration = true
        });

        app.UseMvc(routes =&gt; {
            routes.MapRoute(name: "default", template: "{controller=Home}/{action=Index}/{id?}");
            routes.MapRoute(name: "loan", template: "{controller=LoanRequests}/{action=Index}/{id?}");
            routes.MapRoute(name: "budget", template: "{controller=Budgets}/{action=Index}/{id?}");
            routes.MapRoute(name: "company", template: "{controller=Companies}/{action=Index}/{id?}");
            routes.MapRoute(name: "employee", template: "{controller=Employees}/{action=Index}/{id?}");
            routes.MapRoute(name: "product", template: "{controller=Products}/{action=Index}/{productID?}");
            routes.MapRoute(name: "inventory", template: "{controller=Inventory}/{action=Index}/{productID?}");
            routes.MapRoute(name: "salesarea", template: "{controller=SalesAreas}/{action=Index}/{id?}");
            routes.MapRoute(name: "reports", template: "{controller=Reports}/{action=Index}/{id?}");
        });
    }
</code></pre>

<p>HomeController.cs</p>

<pre><code>public class HomeController : Controller
{
    private const string SHIB_HEAD_IDP = "IDP_uid";
    private readonly LoanDbContext _context;

    public HomeController(LoanDbContext context) {
        _context = context;
    }

    [AllowAnonymous]
    public async Task&lt;IActionResult&gt; Index(string returnUrl = null) {
        string ldapID = "";

        if (HttpContext.Request.Headers.ContainsKey(SHIB_HEAD_IDP)) {  // In a hosted environment, the Shibboleth IDP will automatically log the user in.
            ldapID = HttpContext.Request.Headers[SHIB_HEAD_IDP].ToString();
        } else if (HttpContext.Request.Host.ToString().Contains("localhost")) {  // For a Development machine, there is no Shibboleth to read Headers from.
            ldapID = "FallbackIdNumber";
        }

        if (!string.IsNullOrWhiteSpace(ldapID)) {
            Employee loginUser = await _context.Employees.SingleOrDefaultAsync(m =&gt; m.LdapID == ldapID);
            if (loginUser?.AccessLevel == AccessType.Disabled)
                return RedirectToAction("AccessDenied");   // If the user isn't in the DB, or is Disabled, they are not authorized to access ETS.

            List&lt;Claim&gt; claims = new List&lt;Claim&gt;
            {
                new Claim("id", loginUser.LdapID),
                new Claim("name", loginUser.FullName),
                new Claim("email", loginUser.Email),
                new Claim("role", loginUser.AccessLevel.ToString()),
                new Claim("department", loginUser.Department),
                new Claim("readonly", (loginUser.AccessLevel &gt;= AccessType.ReadOnly).ToString()),
                new Claim("readwrite", (loginUser.AccessLevel &gt;= AccessType.ReadWrite).ToString()),
                new Claim("admin", (loginUser.AccessLevel &gt;= AccessType.Admin).ToString()),
                new Claim("superadmin", (loginUser.AccessLevel &gt;= AccessType.SuperAdmin).ToString())
            };

            // Update the Employee's Last Login time
            loginUser.LastLogin = DateTime.UtcNow;
            await _context.SaveChangesAsync();

            // Create a cookie to hold the user's login details
            var id = new ClaimsIdentity(claims, "local", "name", "role");
            await HttpContext.Authentication.SignInAsync("ETSCookieAuth", new ClaimsPrincipal(id));
            if (string.IsNullOrWhiteSpace(returnUrl))
                return RedirectToAction("Login");
            else {
                // May require multiple Decodes to change characters like "%252F" to "%2F" to "/" This code seems not to help.
                if (returnUrl.Contains("%")) {
                    returnUrl = System.Net.WebUtility.UrlDecode(returnUrl);
                    if (returnUrl.Contains("%"))
                        returnUrl = System.Net.WebUtility.UrlDecode(returnUrl);
                }
                return Redirect(returnUrl);
            }
        }

        return RedirectToAction("AccessDenied");
    }

    [HttpGet]
    public IActionResult Login(string returnUrl = null) {
        ViewData["ReturnUrl"] = System.Net.WebUtility.UrlDecode(returnUrl);
        return View();
    }

    [AllowAnonymous]
    public async Task&lt;IActionResult&gt; Logout() {
        await HttpContext.Authentication.SignOutAsync("ETSCookieAuth");
        return View();
    }

    [AllowAnonymous]
    public IActionResult Error(int id = 0) {
        string pageTitle = "An Unhandled Exception Occurred";
        string userMessage = "";
        string returnUrl = "/Home";
        string routeWhereExceptionOccurred;

        try {
            if (id &gt; 0) {
                userMessage = GetErrorTextFromCode(id);
                pageTitle = $"An HTTP Error {id} has occurred; {userMessage}";
            }

            // Get the details of the exception that occurred
            var exceptionFeature = HttpContext.Features.Get&lt;IExceptionHandlerPathFeature&gt;();

            if (exceptionFeature != null) {
                routeWhereExceptionOccurred = exceptionFeature.Path;
                Exception ex = exceptionFeature.Error;

                if (ex is ArgumentException argEx) {
                    userMessage = argEx.Message;
                } else if (ex is InvalidOperationException ioEx) {
                    userMessage = "An error occurred while trying to fetch a single item from the database. Either none, or more than one were found. "
                        + "This may require manual database changes to fix.";
                } else if (ex is System.Data.SqlClient.SqlException sqlEx) {
                    userMessage = $"A SQL database error occurred. Error Number {sqlEx.Number}";
                } else if (ex is NullReferenceException nullEx) {
                    userMessage = $"A Null Reference error occurred. Source: {nullEx.Source}.";
                } else if (ex is DbUpdateConcurrencyException dbEx) {
                    userMessage = "An error occurred while trying to update your item in the database. This is usually due to someone else modifying the item since you loaded it. Please try again.";
                } else {
                    userMessage = "An unhandled exception has occurred.";
                }
            }
        } catch (Exception) {
            pageTitle = "Your Error Cannot Be Displayed";
            userMessage = "An unknown error occurred while trying to process your error. The original error has been logged, but please report this one as it has not been logged.";
            // TODO: Log the exception
        } finally {
            // Set up the Error page by passing data into the ViewBag/ViewData
            ViewBag.Title = pageTitle;
            ViewBag.UserMessage = userMessage;
            ViewBag.ReturnURL = returnUrl;
        }
        return View();
    }

    [AllowAnonymous]
    public IActionResult AccessDenied() {
        return View();
    }
</code></pre>

## Answers
### Answer ID: 66443540
<p>in aspnet core i managed to solve this by below code.</p>
<pre><code>app.Use(async (ctx, next) =&gt;
        {
            ctx.Request.Scheme = &quot;https&quot;;
            await next();
        });

        ForwardedHeadersOptions forwardOptions = new 
  ForwardedHeadersOptions
        {
            ForwardedHeaders = ForwardedHeaders.XForwardedFor | 
   ForwardedHeaders.XForwardedProto,
            RequireHeaderSymmetry = false
        };

        forwardOptions.KnownNetworks.Clear();
        forwardOptions.KnownProxies.Clear();

        app.UseForwardedHeaders(forwardOptions);
</code></pre>
<p>Setup:
My web app was sitting behind traefik reverse proxy which handled https requests with letsencrypt certs. The calls coming to my web app hosted in kestrel were https.</p>
<p>When user tries to call Action decorated with Authorize attribute, kestrel used to redirect to identity server for login with http scheme and this caused problems as google/facebook did not support http in production no longer.</p>
<p>I changed the scheme for incoming request to https which should be safe as already traefik has handled the public request coming from internet and now the kestrel which only knows http is forced to https scheme from code above. And again my identity server also sits behind a traefik reverse proxy which handles the auth requests.</p>
<p>note: my app had no http only end points.</p>

