# hot chocolate and automapper could not be translated when model contains collection
[Link to question](https://stackoverflow.com/questions/79102802/hot-chocolate-and-automapper-could-not-be-translated-when-model-contains-collect)
**Creation Date:** 1729267036
**Score:** 0
**Tags:** entity-framework-core, automapper, hotchocolate
## Question Body
<p>I have a resolver that returns an IQueryable from Entity Framework Core. When I return the EF Core entity directly, everything works fine. However, when I attempt to map the EF Core entity to my GraphQL model, the query fails to translate properly, specifically when the model contains a collection</p>
<p>When I make this request with the ProjectTo&lt;Graphql.Models.Patient&gt; it fails and I get the response:</p>
<pre class="lang-json prettyprint-override"><code>{
  &quot;errors&quot;: [
    {
      &quot;message&quot;: &quot;Unexpected Execution Error&quot;,
      &quot;locations&quot;: [
        {
          &quot;line&quot;: 2,
          &quot;column&quot;: 3
        }
      ],
      &quot;path&quot;: [
        &quot;patients&quot;
      ],
      &quot;extensions&quot;: {
        &quot;message&quot;: &quot;The LINQ expression 'p2 =&gt; new Session{ Token = p2.Token }\r\n' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.&quot;,
        &quot;stackTrace&quot;: &quot;   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.VisitLambda[T](Expression`1 lambdaExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.TranslateInternal(Expression expression, Boolean applyDefaultTypeMapping)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalSqlTranslatingExpressionVisitor.TranslateProjection(Expression expression, Boolean applyDefaultTypeMapping)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberAssignment(MemberAssignment memberAssignment)\r\n   at System.Linq.Expressions.ExpressionVisitor.VisitMemberBinding(MemberBinding node)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberInit(MemberInitExpression memberInitExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitConditional(ConditionalExpression conditionalExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberAssignment(MemberAssignment memberAssignment)\r\n   at System.Linq.Expressions.ExpressionVisitor.VisitMemberBinding(MemberBinding node)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.VisitMemberInit(MemberInitExpression memberInitExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Visit(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.RelationalProjectionBindingExpressionVisitor.Translate(SelectExpression selectExpression, Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.TranslateSelect(ShapedQueryExpression source, LambdaExpression selector)\r\n   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)\r\n   at Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.Translate(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.Translate(Expression expression)\r\n   at Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)\r\n   at Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass12_0`1.&lt;ExecuteAsync&gt;b__0()\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.ExecuteAsync[TResult](Expression query, CancellationToken cancellationToken)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.ExecuteAsync[TResult](Expression expression, CancellationToken cancellationToken)\r\n   at Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryable`1.GetAsyncEnumerator(CancellationToken cancellationToken)\r\n   at System.Runtime.CompilerServices.ConfiguredCancelableAsyncEnumerable`1.GetAsyncEnumerator()\r\n   at HotChocolate.DefaultAsyncEnumerableExecutable`1.ToListAsync(CancellationToken cancellationToken)\r\n   at HotChocolate.Execution.ListPostProcessor`1.ToCompletionResultAsync(Object result, CancellationToken cancellationToken)\r\n   at HotChocolate.Execution.Processing.Tasks.ResolverTask.ExecuteResolverPipelineAsync(CancellationToken cancellationToken)\r\n   at HotChocolate.Execution.Processing.Tasks.ResolverTask.TryExecuteAsync(CancellationToken cancellationToken)&quot;
      }
    }
  ],
  &quot;data&quot;: null
}
</code></pre>
<p>when i run it using the IQueryable directly i do get the excpected result:</p>
<pre class="lang-json prettyprint-override"><code>{
  &quot;data&quot;: {
    &quot;patients&quot;: [
      {
        &quot;user&quot;: {
          &quot;address&quot;: {
            &quot;street&quot;: &quot;Elm St&quot;
          },
          &quot;sessions&quot;: [
            {
              &quot;token&quot;: &quot;token6&quot;
            }
          ]
        }
      },
      {
        &quot;user&quot;: {
          &quot;address&quot;: {
            &quot;street&quot;: &quot;Pine Rd&quot;
          },
          &quot;sessions&quot;: [
            {
              &quot;token&quot;: &quot;token9&quot;
            }
          ]
        }
      }
    ]
  }
}
</code></pre>
<p>and if i remove the List from my Graphql models (and also don't request it) it also works as expected</p>
<p>request query:</p>
<pre class="lang-json prettyprint-override"><code>query {
  patients {
    user {
      address {
        street
      }
      sessions{
        token
      }
    }
  }
}
</code></pre>
<p>PatientRepository method</p>
<pre class="lang-cs prettyprint-override"><code>public IQueryable&lt;Data.Table.Patient&gt; GetPatientsQueryable()
{
    return Context.Patients.AsNoTracking().AsQueryable();
}
</code></pre>
<p>resolvers examples</p>
<pre class="lang-cs prettyprint-override"><code>[UseProjection]        
public async Task&lt;IQueryable&lt;Patient&gt;&gt; GetPatients([Service] IPatientRepository repository, [Service] IMapper Mapper)
{
    //DOES NOT WORK
    var dataModelQueryable = repository.GetPatientsQueryable();
    var graphqlModelQueryable = Mapper.ProjectTo&lt;Patient&gt;(dataModelQueryable);

    return graphqlModelQueryable;
}

[UseProjection]
public async Task&lt;IQueryable&lt;Data.Tables.Patient&gt;&gt; GetPatients([Service] IPatientRepository repository, [Service] IMapper Mapper)
{
    //WORKS
    var dataModelQueryable = repository.GetPatientsQueryable();
    return dataModelQueryable;
}
</code></pre>
<p>graphql models</p>
<pre class="lang-cs prettyprint-override"><code>namespace Api.GraphQL.Models
{
    public class Patient
    {
        public User User { get; set; }

        public BloodType BloodType { get; set; }

        public int Height { get; set; }

        public decimal Weight { get; set; }
    }
}

namespace Api.GraphQL.Models
{
    public class User
    {
        public int Bsn { get; set; }

        public string FirstName { get; set; }
        public string MiddleName { get; set; } = string.Empty;
        public string LastName { get; set; }

        public DateOnly DateOfBirth { get; set; }

        //WHEN REMOVING THIS LIST BOTH METHODS WORK 
        public List&lt;Session&gt; Sessions { get; set; }
        public Address Address { get; set; }
    }
}

namespace Api.GraphQL.Models
{
    public class Session
    {
        public string Token { get; set; }
        public DateTime ExpirationDate { get; set; }
    }
}

</code></pre>
<p>EF Core tables</p>
<pre class="lang-cs prettyprint-override"><code>namespace Data.Tables
{
    public class Patient
    {
        [Key, ForeignKey(nameof(User)), DatabaseGenerated(DatabaseGeneratedOption.None)]
        public int UserBsn { get; set; }
        public virtual User User { get; set; }

        public BloodType BloodType { get; set; }

        public required int Height { get; set; }

        [Column(TypeName = &quot;decimal(5,2)&quot;)]
        public required decimal Weight { get; set; }
    }
}

namespace Data.Tables
{
    public class User
    {
        [Key, DatabaseGenerated(DatabaseGeneratedOption.None)]
        public int Bsn { get; set; }

        [MaxLength(255)]
        public required string? FirstName { get; set; }
        
        [MaxLength(255)]
        public string MiddleName { get; set; } = string.Empty;
        
        [MaxLength(255)]
        public required string LastName { get; set; }

        public DateOnly DateOfBirth { get; set; }

        public ICollection&lt;Session&gt; Sessions { get; set; } 
    }
}

namespace Data.Tables
{
    public class Session
    {
        [Key]
        public int Id { get; set; }

        [ForeignKey(nameof(User))]
        public int UserBsn { get; set; }
        public virtual User User { get; set; }

        [MaxLength(128)]
        public required string Token { get; set; }

        public required DateTime ExpirationDate { get; set; }
    }
}
</code></pre>
<pre class="lang-cs prettyprint-override"><code>using AutoMapper;

namespace Api
{
    public class MappingProfile : Profile
    {
        /// &lt;summary&gt;
        /// Mapping profile for AutoMapper (data tables to graphql models)
        /// &lt;/summary&gt;
        public MappingProfile()
        {
            CreateMap&lt;Data.Tables.Patient, GraphQL.Models.Patient&gt;();
            CreateMap&lt;GraphQL.Models.Patient, Data.Tables.Patient&gt;();

            CreateMap&lt;Data.Tables.User, GraphQL.Models.User&gt;();
            CreateMap&lt;GraphQL.Models.User, Data.Tables.User&gt;();

            CreateMap&lt;Data.Tables.Session, GraphQL.Models.Session&gt;();
            CreateMap&lt;GraphQL.Models.Session, Data.Tables.Session&gt;();

            CreateMap&lt;Data.Tables.Address, GraphQL.Models.Address&gt;();
            CreateMap&lt;GraphQL.Models.Address, Data.Tables.Address&gt;();
        }
    }
}

</code></pre>
<p>EXTRA:</p>
<p>when logging the compilation with EntityFramework it looks the same for how the session is mapped</p>
<p>but automapper gives the error and my own .Select doesn't</p>
<p>Own Select:</p>
<pre class="lang-cs prettyprint-override"><code>public async Task&lt;IQueryable&lt;Patient&gt;&gt; GetPatients2([Service] IPatientRepository repository, [Service] IMapper Mapper)
{

    var dataModelQueryable = repository.GetPatientsQueryable();
    var graphqlModelQueryable = dataModelQueryable.Select(dtoPatient =&gt; new GraphQL.Models.Patient()
    {
        BloodType = dtoPatient.BloodType,
        Height = dtoPatient.Height,
        User = new GraphQL.Models.User()
        {
            Bsn = dtoPatient.User.Bsn,
            Address = new GraphQL.Models.Address()
            {
                City = dtoPatient.User.Address.City,
                CountryOfResidence = dtoPatient.User.Address.CountryOfResidence,
                HouseNumber = dtoPatient.User.Address.HouseNumber,
                Id = dtoPatient.User.Address.Id,
                PostalCode = dtoPatient.User.Address.PostalCode,
                Province = dtoPatient.User.Address.PostalCode,
                Street = dtoPatient.User.Address.Street,
            },
            DateOfBirth = dtoPatient.User.DateOfBirth,
            FirstName = dtoPatient.User.FirstName,
            MiddleName = dtoPatient.User.MiddleName,
            LastName = dtoPatient.User.LastName,
            Sessions = dtoPatient.User.Sessions.Select(dtoSession =&gt; new GraphQL.Models.Session()
            {
                ExpirationDate = dtoSession.ExpirationDate,
                Token = dtoSession.Token,
            }).ToList()
        },
        Weight = dtoPatient.Weight
    });

    return graphqlModelQueryable;
}
</code></pre>
<pre><code>dbug: 18/10/2024 20:20:43.318 CoreEventId.QueryCompilationStarting[10111] (Microsoft.EntityFrameworkCore.Query)
      Compiling query expression:
      'DbSet&lt;Patient&gt;()
          .AsNoTracking()
          .Select(dtoPatient =&gt; new Patient{
              BloodType = dtoPatient.BloodType,
              Height = dtoPatient.Height,
              User = new User{
                  Bsn = dtoPatient.User.Bsn,
                  Address = new Address{
                      City = dtoPatient.User.Address.City,
                      CountryOfResidence = dtoPatient.User.Address.CountryOfResidence,
                      HouseNumber = dtoPatient.User.Address.HouseNumber,
                      Id = dtoPatient.User.Address.Id,
                      PostalCode = dtoPatient.User.Address.PostalCode,
                      Province = dtoPatient.User.Address.PostalCode,
                      Street = dtoPatient.User.Address.Street
                  }
                  ,
                  DateOfBirth = dtoPatient.User.DateOfBirth,
                  FirstName = dtoPatient.User.FirstName,
                  MiddleName = dtoPatient.User.MiddleName,
                  LastName = dtoPatient.User.LastName,
                  Sessions = dtoPatient.User.Sessions
                      .Select(dtoSession =&gt; new Session{
                          ExpirationDate = dtoSession.ExpirationDate,
                          Token = dtoSession.Token
                      }
                      )
                      .ToList()
              }
              ,
              Weight = dtoPatient.Weight
          }
          )
          .Select(_s1 =&gt; new Patient{ User = _s1.User != null ? new User{
                  Address = _s1.User.Address != null ? new Address{ Street = _s1.User.Address.Street }
                   : null,
                  Sessions = _s1.User.Sessions
                      .Select(p2 =&gt; new Session{ Token = p2.Token }
                      )
                      .ToList()
              }
               : null }
          )'
</code></pre>
<p>Automapper:</p>
<pre><code>      'DbSet&lt;Patient&gt;()
          .AsNoTracking()
          .Select(dtoPatient =&gt; new Patient{
              User = dtoPatient.User == null ? null : new User{
                  Bsn = dtoPatient.User.Bsn,
                  FirstName = dtoPatient.User.FirstName,
                  MiddleName = dtoPatient.User.MiddleName,
                  LastName = dtoPatient.User.LastName,
                  DateOfBirth = dtoPatient.User.DateOfBirth,
                  Sessions = dtoPatient.User.Sessions
                      .Select(dtoSession =&gt; new Session{
                          Token = dtoSession.Token,
                          ExpirationDate = dtoSession.ExpirationDate
                      }
                      )
                      .ToList(),
                  Address = dtoPatient.User.Address == null ? null : new Address{
                      Id = dtoPatient.User.Address.Id,
                      Street = dtoPatient.User.Address.Street,
                      HouseNumber = dtoPatient.User.Address.HouseNumber,
                      PostalCode = dtoPatient.User.Address.PostalCode,
                      City = dtoPatient.User.Address.City,
                      Province = dtoPatient.User.Address.Province,
                      CountryOfResidence = dtoPatient.User.Address.CountryOfResidence
                  }

              }
              ,
              BloodType = dtoPatient.BloodType,
              Height = dtoPatient.Height,
              Weight = dtoPatient.Weight
          }
          )
          .Select(_s1 =&gt; new Patient{ User = _s1.User != null ? new User{
                  Address = _s1.User.Address != null ? new Address{ Street = _s1.User.Address.Street }
                   : null,
                  Sessions = _s1.User.Sessions
                      .Select(p2 =&gt; new Session{ Token = p2.Token }
                      )
                      .ToList()
              }
               : null }
          )'
</code></pre>
<p>Pinpointed the problem to the null check <code>dtoPatient.User == null ? null :  new GraphQL.Models.User()</code></p>
<p>when adding this to my own select it also gives the issue but I don't see what the collection has to do with this as it only fails when also requesting a field from the sessions collection</p>

## Answers
### Answer ID: 79105362
<p>If you're sure you don't need the null checks, use <code>DoNotAllowNull</code>.
That tells AM to skip null checking.</p>

