# ExplicitExpansion() cause OData expand not work
[Link to question](https://stackoverflow.com/questions/63501923/explicitexpansion-cause-odata-expand-not-work)
**Creation Date:** 1597914823
**Score:** 1
**Tags:** asp.net-core, odata, automapper
## Question Body
<p>When using ExplicitExpansion() Odata expand does not work.
My DTo and EF Models can be found below link.
<a href="https://stackoverflow.com/questions/63450240/querying-dtos-based-on-ef-using-odata/63456016#63456016">Querying DTOs based on EF using Odata</a></p>
<p>My Automapper class:</p>
<pre><code>public class AutoMapperProfile : Profile
{
    public AutoMapperProfile()
    {
        CreateMap&lt;ClientRef, ClientContract&gt;().
        ForMember(dest =&gt; dest.ValidFrom,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.Clients.FirstOrDefault(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt; DateTime.Now).ValidFrom);
        }).
        ForMember(dest =&gt; dest.ValidTo,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.Clients.FirstOrDefault(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt; DateTime.Now).ValidTo);
        }).
       ForMember(dest =&gt; dest.FirstName,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.PhysicalPeople.FirstOrDefault(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt; DateTime.Now).FirstName);
        }).
        ForMember(dest =&gt; dest.LastName,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.PhysicalPeople.FirstOrDefault(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt; DateTime.Now).LastName);
        }).
        ForMember(dest =&gt; dest.BirthDate,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.PhysicalPeople.FirstOrDefault(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt; DateTime.Now).BirthDate);
        }).
        ForMember(dest =&gt; dest.FatherName,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.PhysicalPeople.FirstOrDefault(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt; DateTime.Now).FatherName);
        }).
        ForMember(dest =&gt; dest.CompanyName,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.Companies.FirstOrDefault(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt; DateTime.Now).CompanyName);

        })
        .
        ForMember(dest =&gt; dest.PinNumber,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.PhysicalPeople.FirstOrDefault(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt; DateTime.Now).Pin);

        }).
        ForMember(dest =&gt; dest.Position,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.PhysicalPeople.FirstOrDefault(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt; DateTime.Now).Position);

        }).
        ForMember(dest =&gt; dest.PositionCustom,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.PhysicalPeople.FirstOrDefault(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt; DateTime.Now).PositionCustom);

        }).
        ForMember(dest =&gt; dest.ClientType,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.Clients.FirstOrDefault(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt; DateTime.Now).ClientType);

        })
        .
        ForMember(dest =&gt; dest.Documents,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.Documents.Where(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt; DateTime.Now));
            //opt.ExplicitExpansion();
        })
        .ForMember(dest =&gt; dest.ContactsInfo,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.ClientContactInfoComps.Where(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt; DateTime.Now).Select(x =&gt; x.ContactInfo));
            //opt.ExplicitExpansion();
        }).
        ForMember(dest =&gt; dest.ClientComment,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.CommentComps.Where(x =&gt; x.Contact == null).Select(x =&gt; x.Comment));
            //opt.ExplicitExpansion();
        }).
        ForMember(dest =&gt; dest.Relations,
        opt =&gt;
        {
            opt.MapFrom(y =&gt; y.ClientRelationCompClient1Navigations);
            //opt.ExplicitExpansion();
        })
        ;


        CreateMap&lt;Document, DocumentContract&gt;();

        CreateMap&lt;ContactInfo, ContactInfoContract&gt;().
        ForMember(dest =&gt; dest.ContactComments,
        opt =&gt;
        {
        opt.MapFrom(y =&gt; y.CommentComps.Select(x =&gt; x.Comment));
        });

        CreateMap&lt;ClientRelationComp, RelationContract&gt;().
            ForMember(dest =&gt; dest.ClientINN,
            opt =&gt; {
                opt.MapFrom(x =&gt; x.Client2);
            }).
            ForMember(dest =&gt; dest.RelationType,
            opt =&gt; {
                opt.MapFrom(x =&gt; x.RelationId);
            });

        CreateMap&lt;ICollection&lt;Client&gt;, ClientContract&gt;();
        CreateMap&lt;ICollection&lt;PhysicalPerson&gt;, ClientContract&gt;();
        CreateMap&lt;ICollection&lt;Company&gt;, ClientContract&gt;();
        CreateMap&lt;Comment, CommentContract&gt;();
        CreateMap&lt;ICollection&lt;Comment&gt;, ICollection&lt;ContactInfoContract&gt;&gt;();
        CreateMap&lt;ICollection&lt;ClientRelationComp&gt;, ClientRef&gt;();
        
    }
}
</code></pre>
<p>My Controller:</p>
<pre><code>public class ClientContractController : ODataController
{
    CRMContext _context;
    IMapper _mapper;
    public ClientContractController(CRMContext ctx, IMapper mapper )
    {
        _context = ctx;
        _mapper = mapper;
    }

    [EnableQuery(MaxExpansionDepth = 10)]
    public IQueryable&lt;ClientContract&gt; Get()
    {
        return _mapper.ProjectTo&lt;ClientContract&gt;(_context.ClientRefs).Where(x =&gt; x.ValidFrom &lt;= DateTime.Now &amp;&amp; x.ValidTo &gt;= DateTime.Now);
    }
}
</code></pre>
<p>this gives the following exception
https://localhost:44371/odata/clientcontract?$expand=relations</p>
<p>System.InvalidOperationException: The LINQ expression '$it' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.
at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberAssignment(MemberAssignment memberAssignment)
at System.Linq.Expressions.ExpressionVisitor.VisitMemberBinding(MemberBinding node)
at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberInit(MemberInitExpression memberInitExpression)
at System.Linq.Expressions.MemberInitExpression.Accept(ExpressionVisitor visitor)
at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
at System.Linq.Expressions.ExpressionVisitor.VisitLambda[T](Expression<code>1 node) at System.Linq.Expressions.Expression</code>1.Accept(ExpressionVisitor visitor)
at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
at System.Dynamic.Utils.ExpressionVisitorUtils.VisitArguments(ExpressionVisitor visitor, IArgumentProvider nodes)
at System.Linq.Expressions.ExpressionVisitor.VisitMethodCall(MethodCallExpression node)
at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberAssignment(MemberAssignment memberAssignment)
at System.Linq.Expressions.ExpressionVisitor.VisitMemberBinding(MemberBinding node)
at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberInit(MemberInitExpression memberInitExpression)
at System.Linq.Expressions.MemberInitExpression.Accept(ExpressionVisitor visitor)
at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberAssignment(MemberAssignment memberAssignment)
at System.Linq.Expressions.ExpressionVisitor.VisitMemberBinding(MemberBinding node)
at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberInit(MemberInitExpression memberInitExpression)
at System.Linq.Expressions.MemberInitExpression.Accept(ExpressionVisitor visitor)
at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)
at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Translate(SelectExpression selectExpression, Expression expression)
at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.TranslateSelect(ShapedQueryExpression source, LambdaExpression selector)
at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
at System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
at System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass12_0<code>1.&lt;ExecuteAsync&gt;b__0() at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func</code>1 compiler)
at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression query, CancellationToken cancellationToken)
at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)
at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable<code>1.GetAsyncEnumerator(CancellationToken cancellationToken) at Microsoft.AspNetCore.Mvc.Infrastructure.AsyncEnumerableReader.ReadInternal[T](Object value) at Microsoft.AspNetCore.Mvc.Infrastructure.ObjectResultExecutor.ExecuteAsyncEnumerable(ActionContext context, ObjectResult result, Object asyncEnumerable, Func</code>2 reader)
at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.g__Logged|21_0(ResourceInvoker invoker, IActionResult result)
at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.g__Awaited|29_0[TFilter,TFilterAsync](ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.Rethrow(ResultExecutedContextSealed context)
at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.ResultNext[TFilter,TFilterAsync](State&amp; next, Scope&amp; scope, Object&amp; state, Boolean&amp; isCompleted)
at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.InvokeResultFilters()
--- End of stack trace from previous location where exception was thrown ---
at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.g__Awaited|19_0(ResourceInvoker invoker, Task lastTask, State next, Scope scope, Object state, Boolean isCompleted)
at Microsoft.AspNetCore.Mvc.Infrastructure.ResourceInvoker.g__Logged|17_1(ResourceInvoker invoker)
at Microsoft.AspNetCore.Routing.EndpointMiddleware.g__AwaitRequestTask|6_0(Endpoint endpoint, Task requestTask, ILogger logger)
at Microsoft.AspNetCore.Authorization.AuthorizationMiddleware.Invoke(HttpContext context)
at Microsoft.AspNetCore.Diagnostics.DeveloperExceptionPageMiddleware.Invoke(HttpContext context)</p>

## Answers
### Answer ID: 63508720
<p><strong>Update 21/08/20202</strong></p>
<p>Without <a href="https://docs.automapper.org/en/stable/Queryable-Extensions.html#explicit-expansion" rel="nofollow noreferrer">explicit instructions</a>, <code>AutoMapper</code> will expand all members in the result.</p>
<p>To control which members are expanded during projection, set <code>ExplicitExpansion</code> in the configuration and then pass in the members you want to explicitly expand:</p>
<pre><code>dbContext.Orders.ProjectTo&lt;OrderDto&gt;(configuration,
    dest =&gt; dest.Customer,
    dest =&gt; dest.LineItems);
// or string-based
dbContext.Orders.ProjectTo&lt;OrderDto&gt;(configuration,
    null,
    &quot;Customer&quot;,
    &quot;LineItems&quot;);
// for collections
dbContext.Orders.ProjectTo&lt;OrderDto&gt;(configuration,
    null,
    dest =&gt; dest.LineItems.Select(item =&gt; item.Product));
</code></pre>
<br>
<br><br>
<p><strong>Use the property name and not the attribute Name when use <code>OData</code>.</strong></p>
<p><code>OData</code> client library relies on it's own attribute <code>OriginalNameAttribute</code> to gain knowledge about class/member names as server emits them. The details you can see from <a href="https://github.com/OData/odata.net/issues/554" rel="nofollow noreferrer">here</a>.</p>

