# Decorating specific command handlers with unit of work
[Link to question](https://stackoverflow.com/questions/18803979/decorating-specific-command-handlers-with-unit-of-work)
**Creation Date:** 1379176759
**Score:** 1
**Tags:** c#, dependency-injection, cqrs, simple-injector
## Question Body
<p>I am trying to rewrite my app from a service pattern to a command and query pattern (before I move to CQRS). Currently I'm stuck on <a href="https://cuttingedge.it/blogs/steven/pivot/entry.php?id=93" rel="nofollow">this blog</a>.</p>

<p>It shows where he moved unit of work commit from the base command into a <code>PostCommitCommandHandlerDecorator</code>, then use Simple Injector to bind them up. The writer also stated that not all commands will require the use of unit of work, which is true in my case because not every command talks to a database but some send emails, etc.</p>

<p>How do I architect my commands and bindings in such a way that only those commands that are required to be wrapped in a unit of work commit will be bound as such by the IoC container?</p>

## Answers
### Answer ID: 18804399
<blockquote>
  <p>How do I architect my commands and bindings in such a way that only those commands that are required to be wrapped in a unit of work commit will be bound as such by the IoC container?</p>
</blockquote>

<p>First of all, does that really matter that not all handlers use the unit of work? Is it a problem when a unit of work is created, while it isn’t used? Because when there are no performance problems, there’s no need to make your code more complicated.</p>

<p>But let’s assume that it does matter. In that case, the trick is to query the container whether the unit of work is injected somewhere. You can make use of <code>Lazy&lt;T&gt;</code> to get this working. Take a look at the following registration:</p>

<pre><code>Func&lt;IUnitOfWork&gt; uowFactory = 
    () =&gt; new MyUnitOfWork(connectionString);

// Register the factory as Lazy&lt;IUnitOfWork&gt;
container.Register&lt;Lazy&lt;IUnitOfWork&gt;&gt;(
    () =&gt; new Lazy&lt;IUnitOfWork&gt;(uowFactory), 
    Lifestyle.Scoped);

// Create a registration that redirects to Lazy&lt;IUnitOfWork&gt;
container.Register&lt;IUnitOfWork&gt;(
    () =&gt; container.GetInstance&lt;Lazy&lt;IUnitOfWork&gt;&gt;().Value, 
    Lifestyle.Scoped);
</code></pre>

<p><em>For the rest of the article I assume you're building a web application, but the idea will be the same.</em></p>

<p>With this registration, when the container resolves an object graph with a component that depends on <code>IUnitOfWork</code>, under the covers it will resolve the <code>Lazy&lt;IUnitOfWork&gt;</code> and get its value. We cache the <code>Lazy&lt;IUnitOfWork&gt;</code> per request, so this allows us to have another component that depends on <code>Lazy&lt;IUnitOfWork&gt;</code> and check its <code>IsValueCreated</code> property to see if the <code>IUnitOfWork</code> was injected anywhere.</p>

<p>Now your decorator could look like this:</p>

<pre><code>public class TransactionCommandHandlerDecorator&lt;TCommand&gt;
    : ICommandHandler&lt;TCommand&gt;
{
    private readonly ICommandHandler&lt;TCommand&gt; decorated;
    private readonly Lazy&lt;IUnitOfWork&gt; lazyUnitOfWork;

    public TransactionCommandHandlerDecorator(
        ICommandHandler&lt;TCommand&gt; decorated,
        Lazy&lt;IUnitOfWork&gt; lazyUnitOfWork)
    {
        this.decorated = decorated;
        this.lazyUnitOfWork = lazyUnitOfWork;
    }

    public void Handle(TCommand command)
    {
        this.decorated.Handle(command);

        if (this.lazyUnitOfWork.IsValueCreated)
        {
            this.lazyUnitOfWork.Value.SubmitChanges();
        }
    }
}
</code></pre>

<p>Note however that you still don’t know whether the unit of work is actually used or not, but I think it’s safe to assume that the unit of work will be used when it gets injected. You don’t want to inject an unused dependency.</p>

<p>If that doesn’t cut it, and you want to check whether it is created, you will have to inject a proxy unit of work that allows you to check this. For instance:</p>

<pre><code>public class DelayedUnitOfWorkProxy : IUnitOfWork
{
    private Lazy&lt;IUnitOfWork&gt; uow;

    public DelayedUnitOfWorkProxy(Lazy&lt;IUnitOfWork&gt; uow)
    {
        this.uow = uow;
    }

    void IUnitOfwork.SubmitChanges()
    {
        this.uow.Value.SubmitChanges();
    }

    // TODO: Implement All other IUnitOfWork methods
}
</code></pre>

<p>Your configuration will now look like this:</p>

<pre><code>Func&lt;IUnitOfWork&gt; uowFactory = 
    () =&gt; new MyUnitOfWork(connectionString);

// Register the factory as Lazy&lt;IUnitOfWork&gt;
container.Register&lt;Lazy&lt;IUnitOfWork&gt;&gt;(
    () =&gt; new Lazy&lt;IUnitOfWork&gt;(uowFactory), 
    Lifestyle.Scoped);

// Register the proxy that delays the creation of the UoW
container.Register&lt;IUnitOfWork, DelayedUnitOfWorkProxy&gt;(
    Lifestyle.Scoped);
</code></pre>

<p>When a command or any other  dependency needs an <code>IUnitOfWork</code>, they will get the <code>DelayedUnitOfWorkProxy</code>, and it is injected with a <code>Lazy&lt;IUnitOfWork&gt;</code>. So after the object graph is created, the unit of work itself will not be created yet. Only when one of the <code>DelayedUnitOfWorkProxy</code> method is called, such instance is created. The decorator will stay the same.</p>

<p>But even this might not be good enough. It is possible that your MVC controller (assuming you are building an ASP.NET MVC application) depends on a query that uses the unit of work, but the command handler does not. In that case you probably still wouldn't want to commit the unit of work, because the command handler (or one of its dependencies) still doesn't use the unit of work.</p>

<p>In that case what you’re actually trying to do is to isolate the execution of command handlers in their own scope. As if they are running in a different App Domain. You want them to be independent of the web request in which they execute.</p>

<p>In that case you need an hybrid lifestyle. With Simple Injector you can leave all your code and configuration in tact, but switch to an hybrid lifestyle like this:</p>

<pre><code>container.Options.DefaultScopedLifestyle = Lifestyle.CreateHybrid(
    () =&gt; container.GetCurrentLifetimeScope() != null,
    new LifetimeScopeLifestyle(),
    new WebRequestLifestyle());

Func&lt;IUnitOfWork&gt; uowFactory = 
    () =&gt; new MyUnitOfWork(connectionString);

// Register the factory as Lazy&lt;IUnitOfWork&gt;
container.Register&lt;Lazy&lt;IUnitOfWork&gt;&gt;(
    () =&gt; new Lazy&lt;IUnitOfWork&gt;(uowFactory), 
    Lifestyle.Scoped);

// Register a proxy that depends on Lazy&lt;IUnitOfWork&gt;    
container.Register&lt;IUnitOfWork, DelayedUnitOfWorkProxy&gt;(
    Lifestyle.Scoped);
</code></pre>

<p>An hybrid lifestyle is a composite of two (or more) lifestyles and it contains a predicate delegate that the container will call to check which lifestyle should be applied.</p>

<p>With just this configuration nothing will happen, because the <code>LifetimeScopeLifestyle</code> requires you to explicitly start and stop a new scope. Without a scope the <code>container.GetCurrentLifetimeScope()</code> method will always return null, which means that the hybrid lifestyle will always pick the WebRequestLifestyle.</p>

<p>What you need is to start a new lifetime scope just before you resolve a new command handler. As always, this can be done by defining a decorator:</p>

<pre><code>private sealed class LifetimeScopeCommandHandlerDecorator&lt;T&gt;
    : ICommandHandler&lt;T&gt;
{
    private readonly Container container;
    private readonly Func&lt;ICommandHandler&lt;T&gt;&gt; decorateeFactory;

    public LifetimeScopeCommandHandlerDecorator(Container container,
        Func&lt;ICommandHandler&lt;T&gt;&gt; decorateeFactory)
    {
        this.decorateeFactory = decorateeFactory;
        this.container = container;
    }

    public void Handle(T command)
    {
        using (this.container.BeginLifetimeScope())
        {
            var decoratee = this.decorateeFactory.Invoke();
            decoratee.Handle(command);
        }
    }
}
</code></pre>

<p>You should register this decorator as last decorator (outer most decorator). Instead of depending on an <code>ICommandHandler&lt;T&gt;</code> this decorator depends on an <code>Func&lt;ICommandHandler&lt;T&gt;&gt;</code>. This makes sure that the decorated command handler will only get resolved when the <code>Func&lt;T&gt;</code> delegate is invoked. This postpones the creation and and allows the creation of a lifetime scope first.</p>

<p>Since this decorator depends on two singletons (both the container and the <code>Func&lt;T&gt;</code> are singletons), the decorator itself can also be registered as singleton. This is what your configuration might look like:</p>

<pre><code>// Batch register all command handlers
container.Register(
    typeof(ICommandHandler&lt;&gt;), 
    typeof(ICommandHandler&lt;&gt;).Assembly);

// Register one or more decorators
container.RegisterDecorator(
    typeof(ICommandHandler&lt;&gt;), 
    typeof(TransactionCommandHandlerDecorator&lt;&gt;));

// The the lifetime scope decorator last (as singleton).
container.RegisterDecorator(
    typeof(ICommandHandler&lt;&gt;), 
    typeof(LifetimeScopeCommandHandlerDecorator&lt;&gt;),
    Lifestyle.Singleton);
</code></pre>

<p>This will effectively isolate the unit of work used by commands from any unit of work that is created outside the context of a command handler within the rest of the request.</p>

### Answer ID: 18825833
<p>There is a simple way to achieve what you are asking. There are overloaded versions of the <a href="http://simpleinjector.cuttingedge.it/ReferenceLibrary/html/Overload_SimpleInjector_Extensions_DecoratorExtensions_RegisterDecorator.htm" rel="nofollow"><code>RegisterDecorator</code></a> extension method that accept a <code>Predicate</code> which, in combination with a <a href="http://en.wikipedia.org/wiki/Marker_Interface_pattern" rel="nofollow">marker interface</a>, can be used to selectively apply a decorator.</p>

<p>Here's an example in code:</p>

<pre><code>public interface ICommandHandler&lt;T&gt; where T : class { }
public interface IDontUseUnitOfWork { }

public class MyCommand { }

public class MyCommandHandler : 
    ICommandHandler&lt;MyCommand&gt;, IDontUseUnitOfWork { }

public sealed class UnitOfWorkCommandDecorator&lt;T&gt; :
    ICommandHandler&lt;T&gt; where T : class
{
    public UnitOfWorkCommandDecorator(ICommandHandler&lt;T&gt; decorated) { }
}
</code></pre>

<p>And the registration to apply the <code>UnitOfWorkCommandDecorator</code> to command handlers <strong>except</strong> those that are tagged with the <code>IDontUseUnitOfWork</code> interface:</p>

<pre><code>container.RegisterDecorator(
    typeof(ICommandHandler&lt;&gt;), 
    typeof(UnitOfWorkCommandDecorator&lt;&gt;),
    x =&gt; !typeof(IDontUseUnitOfWork).IsAssignableFrom(x.ImplementationType));
</code></pre>

<p>This predicate feature is very useful and well worth getting to grips with.</p>

