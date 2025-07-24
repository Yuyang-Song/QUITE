# Mvc simple dependency injection from service layer to data layer (three layer application)
[Link to question](https://stackoverflow.com/questions/53517686/mvc-simple-dependency-injection-from-service-layer-to-data-layer-three-layer-ap)
**Creation Date:** 1543402130
**Score:** 0
**Tags:** asp.net-mvc, dependency-injection, service-layer, data-layers
## Question Body
<p>I have to rewrite an old asp classic web application.
I chose an architecture in three levels (tier/project = layer level)</p>

<ul>
<li>Web: views and controllers, thin as much as possible. References service layer project.</li>
<li>Service: business logic. References data layer project.</li>
<li>Data: ado net queries, database connection and transaction management. No reference to other projects</li>
</ul>

<p>In web layer I manage service layer injection with this class, simple DI</p>

<pre><code>[assembly: OwinStartupAttribute(typeof(MyApp.Startup))]
namespace MyApp
{
    public partial class Startup
    {
        public void Configuration(IAppBuilder app)
        {
            var services = new ServiceCollection();
            ConfigureServices(services);
            var resolver = new DefaultDependencyResolver(services.BuildServiceProvider());
            DependencyResolver.SetResolver(resolver);
        }

        public void ConfigureServices(IServiceCollection services)
        {
            services.AddControllersAsServices(typeof(Startup).Assembly.GetExportedTypes()
                .Where(t =&gt; !t.IsAbstract &amp;&amp; !t.IsGenericTypeDefinition)
                .Where(t =&gt; typeof(IController).IsAssignableFrom(t)
                   || t.Name.EndsWith("Controller", StringComparison.OrdinalIgnoreCase)));

            services.AddSingleton&lt;IAuthenticationService, AuthenticationService&gt;();
            services.AddSingleton&lt;IChannelService, ChannelService&gt;();
            //add more DI services here...
        }
    }
}
</code></pre>

<p>The web layer doesn't know anything of data layer so how do I inject data layer classes? I need at least to make available data layer in service layer but how do I make a class like the one above in service layer?</p>

<p>EDIT: possible solution from a comment now deleted.
Also i found a interesting article about this argument here </p>

<p><a href="https://asp.net-hacker.rocks/2017/03/06/using-dependency-injection-in-multiple-projects.html" rel="nofollow noreferrer">https://asp.net-hacker.rocks/2017/03/06/using-dependency-injection-in-multiple-projects.html</a></p>

<p>create a extension class in service layer that adds data layer dependencies to IServiceCollection instance</p>

<pre><code>namespace MyApp.Service
{
    public static class IServiceCollectionExtension
    {
        public static IServiceCollection AddDataQueries(this IServiceCollection services)
        {
            //services.AddTransient&lt;IQuery, Query&gt;();
            //...add here DI of other data services
            return services;
        }
    }
}
</code></pre>

<p>and in startup class</p>

<pre><code> services.AddSingleton&lt;IAuthenticationService, AuthenticationService&gt;();
 services.AddSingleton&lt;IChannelService, ChannelService&gt;();
 //add more DI services here...
 services.AddDataQueries();
 //add DI for other layers
</code></pre>

