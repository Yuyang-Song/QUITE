# Failing to register scoped or transient service for PostgreSQL DbContext with EF 6
[Link to question](https://stackoverflow.com/questions/68896332/failing-to-register-scoped-or-transient-service-for-postgresql-dbcontext-with-ef)
**Creation Date:** 1629737564
**Score:** 0
**Tags:** c#, dependency-injection, entity-framework-core, npgsql, transient
## Question Body
<p>We try to use PostgreSQL (through Npgsql) on a ASP .Net Core project with EF Core. With Dependence Injection we can add the DbContext as a singleton but trying to use it as a transient or scoped service triggers a 500.30 error at application start.</p>
<p>The problem is that as a singleton the DbContext fails when used simultaneously by concurrent queries on the server, generating 500 errors then when executing controllers and services. And as it is said below in comments this is a major bug, a no go.</p>
<p>So we are trying to add it as a transient but we fail to insert it correctly in service collection. Here is our Startup configuration code without the singleton (miserable) approach:</p>
<pre><code>public void ConfigureServices(IServiceCollection services)
{
  try
  {
    services.AddHttpContextAccessor();
    services.AddSingleton&lt;IActionContextAccessor, ActionContextAccessor&gt;();

    // initiating database service for DI
    DbContextOptions&lt;EFCoreContext&gt; optionsBuilder = new DbContextOptions&lt;EFCoreContext&gt;();
    OurDbContext context = new OurDbContext (optionsBuilder);
                
    services.AddDbContext&lt;OurDbContext &gt;(
      options =&gt; options.UseNpgsql(
        Configuration[&quot;ConnectionStrings:ConnectionString&quot;]
      )
    );

    // initiating session service with in memory store
    Services.AddDistributedMemoryCache();

    services.AddSession(options =&gt;
    {
      options.IdleTimeout = TimeSpan.FromMinutes(
        Double.Parse(
          Configuration[&quot;Session:DurationInMinutes&quot;]
        )
      );
      options.Cookie.HttpOnly = true;
      options.Cookie.IsEssential = true;
      options.Cookie.Name = &quot;.api.myAccess-TDF&quot;;
    });

    services.AddControllers();

    // adding localization, with customized PO file finder
    services.AddMvc().
      AddViewLocalization(
        LanguageViewLocationExpanderFormat.Suffix
     );

    services.AddPortableObjectLocalization(
      options =&gt; options.ResourcesPath = &quot;Localization&quot;
    );

    // adding application services
    services.AddSingleton&lt;ILocalizationFileLocationProvider, TranslatorFileLocationProvider&gt;();
    services.AddSingleton&lt;ISiteService, SiteService&gt;();
    services.AddSingleton&lt;IQueryService, QueryService&gt;();
    services.AddSingleton&lt;IQueryStatusService, QueryStatusService&gt;();
    services.AddSingleton&lt;IAccountService, AccountService&gt;();
    services.AddSingleton&lt;ISnowService, SnowService&gt;();

    // adding HttpContextAccessor dependency injection
    services.AddSingleton&lt;IHttpContextAccessor, HttpContextAccessor&gt;();

    // configurating application cultures
    services.Configure&lt;RequestLocalizationOptions&gt;(options =&gt; {
      var supportedCultures = new List&lt;CultureInfo&gt;
      {
        new CultureInfo(&quot;fr-FR&quot;),
        new CultureInfo(&quot;fr&quot;)
      };

      options.DefaultRequestCulture = new RequestCulture(&quot;fr-FR&quot;);
      options.SupportedCultures = supportedCultures;
      options.SupportedUICultures = supportedCultures;
    });

    // adding translation service (which use Localizer by D.I.)
    services.AddSingleton&lt;ITranslator, Translator&gt;();

    // adding swagger interface
    services.AddSwaggerGen(c =&gt;
    {
      c.SwaggerDoc(
        &quot;v1&quot;, new OpenApiInfo {Title = &quot;WebApi&quot;, Version = &quot;v1&quot;}
      );
    });

    // adding super permissive CORS, 
    // since this is an open API server, anybody can access it
    services.AddCors(options =&gt; {
      options.AddDefaultPolicy(builder =&gt; {
        builder.AllowAnyOrigin()
          .AllowAnyMethod()
          .AllowAnyHeader();
      });
    });

    // Create a MapperConfiguration instance with profiles 
    // and add the mapper as a service for Dependency Injection
    var mappingConfig = new MapperConfiguration(mc =&gt; {
      mc.AddProfile(new MappingProfile());
    });
    IMapper mapper = mappingConfig.CreateMapper();
    services.AddSingleton(mapper);

  } catch (Exception e) {
    Console.WriteLine(e)
  }
}
</code></pre>
<p>OurDbContext is a class that derives from EFCoreContext and that let us configure our connection string from appsettings.json file even when we execute Scaffold-DbContext manually (we use database first, so when we execute scaffolding it rewrites the EFCoreContext and we can't put our configuration reference in this class). Here is the code of that class :</p>
<pre><code>namespace App_DAL
{
  public partial class OurDbContext : EFCoreContext
  {
    private readonly DbContextOptionsBuilder OptionBuilder;

    public OurDbContext(DbContextOptions&lt;EFCoreContext&gt; options)
    : base(options)
    {
      OptionBuilder = new DbContextOptionsBuilder();
    }

    public OurDbContext(
      DbContextOptions&lt;EFCoreContext&gt; options, 
      DbContextOptionsBuilder optionBuilder
    ) : base(options)
    {
      OptionBuilder = optionBuilder;
    }

    /// &lt;summary&gt;
    /// Executes the database connection string definition when the context is configured
    /// The connection string is read from the main application appsettings.json file
    /// This file is defined in the starting project of the solution
    /// &lt;/summary&gt;
    /// &lt;param name=&quot;optionsBuilder&quot;&gt;Optional context builder options&lt;/param&gt;
    protected override void OnConfiguring(
      DbContextOptionsBuilder optionsBuilder
    ){
      if (!optionsBuilder.IsConfigured) {

        // getting the connection string from configuration files
        // two configuration files can be used : 
        // appsettings.json and appsettings.Development.json, 
        // both placed in the main project root directory

        string testingProjectDir = Directory.GetCurrentDirectory();
        string configPath = Path.Combine(
          testingProjectDir, &quot;appsettings.json&quot;
        );
        string configPathDev = Path.Combine(
          testingProjectDir, &quot;appsettings.Development.json&quot;
        );

        IConfigurationBuilder builder = new ConfigurationBuilder()
          .AddJsonFile(
            configPath, optional: false, 
            reloadOnChange: true
          );

        // if we have a development configuration file 
        // in the project then we add it to the main one, 
        // so it can redefine properties linked to the 
        // development platform

        if (File.Exists(configPathDev))
        {
          builder.AddJsonFile(
            configPathDev, optional: false, 
            reloadOnChange: true
          );
        }

        // now we read the connection string inside the configuration

        IConfigurationRoot configuration = builder.Build();

        string connectionString = configuration.GetSection(
          &quot;ConnectionStrings:ConnectionString&quot;
        ).Value;

        // unable to get the connection string :/
        // trigering an exception

        if (string.IsNullOrEmpty(connectionString))
        {
          string msg = &quot;&lt;ERROR&gt; DemandesAccesContext.OnConfiguring - Unable to read connection string in application settings. Please check settings file content&quot;;
          Console.WriteLine(msg);
          throw new System.Exception(msg);
        }
        else
        {
          // the connection string is defined to access the database

          optionsBuilder.UseNpgsql(
            connectionString, 
            options =&gt; options.EnableRetryOnFailure()
          );
        }
      }
    }
  }
}
</code></pre>
<p>So, from there, starting the API application will trigger a 500.30 error displayed on the Swagger page that is opened by default. When trying to access the API we get the same error :</p>
<p>No exception is traced in IIS Express log but the application logs (Serilog) in database contains an exception that points to this :</p>
<pre><code>Error while validating the service descriptor 'ServiceType: App_DAL.OurDbContext Lifetime: Scoped ImplementationType: App_DAL.OurDbContext': 
No constructor for type 'App_DAL.OurDbContext' can be instantiated using services from the service container and default values. 
</code></pre>
<p>The complete exception stack contains 5 inner exceptions but they all get to this: OurDbContext can't be validated because of something missing between its constructors and the way we add it in the service collection. But frankly I don't understand how to correct this. Sorry for my lack of understanding here. Does anybody know how to make this thing work ?</p>
<p>Thanks, François</p>

