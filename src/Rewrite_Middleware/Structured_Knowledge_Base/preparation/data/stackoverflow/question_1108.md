# Unable to seed data in ASP.NET Core in a static method due to exception &#39;A second operation started on this context before a previous&#39;
[Link to question](https://stackoverflow.com/questions/59539480/unable-to-seed-data-in-asp-net-core-in-a-static-method-due-to-exception-a-secon)
**Creation Date:** 1577765532
**Score:** 3
**Tags:** asp.net-core, entity-framework-core
## Question Body
<p>I am attempting to seed my database with the following code:</p>

<p><code>Startup.Configure</code>: </p>

<pre><code>app.UseCors("AllowAll")
   .UseMiddleware&lt;JwtBearerMiddleware&gt;()
   .UseAuthentication()
   .SeedDatabase() &lt;= here
   .UseHttpsRedirection()
   .UseDefaultFiles()
   .UseMvc()
   .UseSpa(SpaApplicationBuilderExtensions =&gt; { });
</code></pre>

<p><code>SeedDatabase</code> method:</p>

<pre><code>public static IApplicationBuilder SeedDatabase(this IApplicationBuilder app)
{
            IServiceProvider serviceProvider = app.ApplicationServices.CreateScope().ServiceProvider;
            try
            {
                UserManager&lt;ApplicationUser&gt; userManager = serviceProvider.GetService&lt;UserManager&lt;ApplicationUser&gt;&gt;();
                RoleManager&lt;IdentityRole&gt; roleManager = serviceProvider.GetService&lt;RoleManager&lt;IdentityRole&gt;&gt;();
                IConfiguration configuration = serviceProvider.GetService&lt;IConfiguration&gt;();
                ThePLeagueContext dbContext = serviceProvider.GetService&lt;ThePLeagueContext&gt;();
                DataBaseInitializer.SeedUsers(userManager, roleManager, configuration, dbContext);
                DataBaseInitializer.SeedTeams(dbContext);

            }
            catch (Exception ex)
            {
                ILogger&lt;Program&gt; logger = serviceProvider.GetRequiredService&lt;ILogger&lt;Program&gt;&gt;();
                logger.LogError(ex, "An error occurred while seeding the database.");
            }

            return app;
  }
</code></pre>

<p>Everything worked fine until I added <code>ThePLeagueContext dbContext = serviceProvider.GetService&lt;ThePLeagueContext&gt;();</code> and then the <code>DataBaseInitializer.SeedTeams(dbContext)</code></p>

<p><code>DataBaseInitializer.SeedTeams(dbContext)</code>:</p>

<pre><code>public static async void SeedTeams(ThePLeagueContext dbContext)
{
        List&lt;Team&gt; teams = new List&lt;Team&gt;();

        // 7 because we have 7 leagues
        for (int i = 0; i &lt; 7; i++)...

        if (dbContext.Teams.Count() &lt; teams.Count)
        {
            foreach (Team newTeam in teams)
            {                    
                await dbContext.Teams.AddAsync(newTeam);
                await dbContext.SaveChangesAsync();
            }
        }
}
</code></pre>

<p>When I attempt to seed the database with the above code I get the following exception:</p>

<blockquote>
  <p>System.InvalidOperationException: 'A second operation started on this context before a previous operation completed. This is usually caused by different threads using the same instance of DbContext, however instance members are not guaranteed to be thread safe. This could also be caused by a nested query being evaluated on the client, if this is the case rewrite the query avoiding nested invocations.'</p>
</blockquote>

<p>My database context is registered with the LifeTime of <code>Scoped</code>. </p>

<p>Two workarounds I found:</p>

<ol>
<li>When I change my database context to <code>Transient</code> the seeding issue goes away. This however causes other issues in the application so I cannot use <code>Transient</code></li>
<li>When I call <code>DatabaseInitializer.SeedTeams(dbContext)</code> from inside the <code>DatabaseInitializer.SeedUsers(...)</code> method, this also works, I have no clue why.</li>
</ol>

<p><code>DatabaseInitializer.SeedUsers(...)</code> method:</p>

<pre><code>public async static void SeedUsers(UserManager&lt;ApplicationUser&gt; userManager, RoleManager&lt;IdentityRole&gt; roleManager, IConfiguration configuration, ThePLeagueContext dbContext)
{
            string[] roles = new string[] { AdminRole, SuperUserRole, UserRole };

            foreach (string role in roles)
            {
                if (!roleManager.Roles.Any(r =&gt; r.Name == role))
                {
                    IdentityRole newRole = new IdentityRole
                    {
                        Name = role,
                        NormalizedName = role.ToUpper()
                    };
                    await roleManager.CreateAsync(newRole);

                    if (role == AdminRole)
                    {
                        await roleManager.AddClaimAsync(newRole, new Claim(Permission, ModifyPermission));
                    }
                    else if (role == SuperUserRole)
                    {
                        await roleManager.AddClaimAsync(newRole, new Claim(Permission, RetrievePermission));
                    }
                    else
                    {
                        await roleManager.AddClaimAsync(newRole, new Claim(Permission, ViewPermission));
                    }
                }
            }

            ApplicationUser admin = new ApplicationUser()...

            ApplicationUser sysAdmin = new ApplicationUser()...;

            PasswordHasher&lt;ApplicationUser&gt; password = new PasswordHasher&lt;ApplicationUser&gt;();

            if (!userManager.Users.Any(u =&gt; u.UserName == admin.UserName))
            {
                string hashed = password.HashPassword(admin, configuration["ThePLeagueAdminInitPassword"]);
                admin.PasswordHash = hashed;

                await userManager.CreateAsync(admin);
                await userManager.AddToRoleAsync(admin, AdminRole);
            }

            if (!userManager.Users.Any(u =&gt; u.UserName == sysAdmin.UserName))
            {
                string hashed = password.HashPassword(sysAdmin, configuration["ThePLeagueAdminInitPassword"]);
                sysAdmin.PasswordHash = hashed;

                await userManager.CreateAsync(sysAdmin);
                await userManager.AddToRoleAsync(sysAdmin, AdminRole);
            }

            SeedTeams(dbContext);

 }
</code></pre>

<p>Is there any way I can use two separate static async methods to seed the database and keep my context as scoped?</p>

## Answers
### Answer ID: 59539837
<p>So I like to keep things ordered and seperated. Therefore I'd do something like:</p>

<pre class="lang-cs prettyprint-override"><code>public static class SeedData 
{
    public static void Populate(IServiceProvider services) 
    {
        ApplicationDbContext context = services.GetRequiredService&lt;ApplicationDbContext&gt;();
        if (!context.SomeDbSet.Any()) 
        {
            // ...code omitted for brevity...
        );
        context.SaveChanges();
    }
}
</code></pre>

<pre class="lang-cs prettyprint-override"><code>public static class IdentitySeedData 
{
    public static async Task Populate(IServiceProvider services) 
    {
        UserManager&lt;ApplicationUser&gt; userManager = services.GetService&lt;UserManager&lt;ApplicationUser&gt;&gt;();
        RoleManager&lt;IdentityRole&gt; roleManager = services.GetService&lt;RoleManager&lt;IdentityRole&gt;&gt;();
        IConfiguration configuration = services.GetService&lt;IConfiguration&gt;();
        ApplicationDbContext context = services.GetRequiredService&lt;ApplicationDbContext&gt;();

        if (!context.Users.Any()) 
        {
            // ...code omitted for brevity...
            await userManager.CreateAsync(sysAdmin);
            await userManager.AddToRoleAsync(sysAdmin, AdminRole);
        );
        context.SaveChanges();
    }
}
</code></pre>

<p>And then the one to top it off:</p>

<pre class="lang-cs prettyprint-override"><code>public static class DatabaseInitializer 
{
    public static void Initialize(IServiceProvider services) 
    {
         IdentitySeedData.Populate(services).Wait();
         SeedData.Populate(services);
    }
}
</code></pre>

<p>Disclaimer: I haven't run the code. So if it requires some tweaking let me know. I'll make the adjustments. It's a bit time-consuming to test this out.</p>

