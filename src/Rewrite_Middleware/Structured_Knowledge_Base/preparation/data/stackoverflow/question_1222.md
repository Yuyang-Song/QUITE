# Linq expression could not be translated Error Entity Framework Core 3
[Link to question](https://stackoverflow.com/questions/64418519/linq-expression-could-not-be-translated-error-entity-framework-core-3)
**Creation Date:** 1603056484
**Score:** 2
**Tags:** c#, linq, entity-framework-core
## Question Body
<p>I am on a project and got some problem with data accessing. I use EF core and I have these stack trace.</p>
<h2>First code executed</h2>
<pre><code>public static void Main(){
 EntityServiceBase&lt;Product&gt; manager = new EntityServiceBase(new EFProductDal());//efproductdal for to access database
 Product result = manager.GetByPrimaryKey(5);
}
</code></pre>
<h2>Second file code executed</h2>
<p><strong>At the code IEntity is an empty interface to determine database objects</strong><br>
<strong>IEntityRepostiory has EF codes to access database which is shown in third code part at the belong</strong><br>
<strong>PrimaryKeyComparable has compare func to check if primary key of an object is equal to given key</strong></p>
<pre><code>using System;
using System.Collections.Generic;
using ECommercial.Core.DataAccess;
using ECommercial.Core.Entities;

namespace ECommercial.Core.Business
{
    public abstract class EntityServiceBase&lt;TEntity&gt; : IService&lt;TEntity&gt; 
        where TEntity :class,IEntity, new() // IENTITY IS AN EMPTY INTERFACE TO JUST DETERMINE DATABASE ENTITIES
    {
        private IEntityRepository&lt;TEntity&gt; _entityRepository;

        public EntityServiceBase(IEntityRepository&lt;TEntity&gt; entityRepository)
        {
            _entityRepository = entityRepository;
        }

        public TEntity GetByPrimaryKey(Object key)
        {
            PrimaryKeyComparable primaryKeyComparable = new PrimaryKeyComparable();
            return _entityRepository.Get(o=&gt;primaryKeyComparable.comparePrimaryKey&lt;TEntity&gt;(o,key));
        }
    }
}
</code></pre>
<h2>Third code part executed</h2>
<p><strong>At the code context is EF dbcontext</strong><br>
<strong>filter is given filter which is o=&gt;primaryKeyComparable.comparePrimaryKey(o,key) the second code file. The error occurs at .SingleOrDefault(filter) part. If I delete it function works well.</strong></p>
<pre><code>public TEntity Get(Expression&lt;Func&lt;TEntity, bool&gt;&gt; filter)
        {
            using (var context=new TContext()){
                TEntity result = context.Set&lt;TEntity&gt;().SingleOrDefault(filter);
                return result;
            }
        }
</code></pre>
<h2>ComparePrimaryKey function</h2>
<pre><code>public bool comparePrimaryKey&lt;TEntity&gt;(TEntity entity,Object value)
            where TEntity:class,IEntity,new()
        {
            Type entityType = typeof(TEntity);
            FieldInfo[] fields = entityType.GetFields();
            FieldInfo found =null;
            foreach(var field in fields){
                Attribute attribute=field.GetCustomAttribute(typeof(PrimaryKeyFieldAttribute));
                if(attribute!=null){
                    found=field;
                    break;
                }
            }
            if(found!=null){
                Type foundDeclaringType= found.DeclaringType;
                Type valueDeclaringType = value.GetType().DeclaringType;
                if((foundDeclaringType.IsSubclassOf(valueDeclaringType)) ||valueDeclaringType.IsSubclassOf(foundDeclaringType) || valueDeclaringType==foundDeclaringType)
                {
                    return entity.Equals(value);
                }
                throw new InvalidCastException(&quot;Given entity's primary key must have same or child-base related declaration type with key object compared&quot;);
            }
            throw new CustomAttributeFormatException(&quot;The Entity Has Any field has PrimaryKeyFieldAttribute attribute. Must be PrimaryKeyAttribute on primary key field.&quot;);
        }
</code></pre>
<h2>The Error Message (I think english parts is enough to understand)</h2>
<p><strong>ERROR OCCURS AT THE THIRD FILE AT .SingleOrDefault(filter) PART</strong></p>
<pre><code>Exception has occurred: CLR/System.InvalidOperationException
'System.InvalidOperationException' türünde özel durum Microsoft.EntityFrameworkCore.dll öğesinde oluştu, fakat kullanıcı kodunda işlenmedi: 'The LINQ expression 'DbSet&lt;Product&gt;
    .Where(p =&gt; new PrimaryKeyComparable().comparePrimaryKey&lt;Product&gt;(
        entity: p, 
        value: __key_0))' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync(). See https://go.microsoft.com/fwlink/?linkid=2101038 for more information.'
   konum Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.&lt;VisitMethodCall&gt;g__CheckTranslated|8_0(ShapedQueryExpression translated, &lt;&gt;c__DisplayClass8_0&amp; )
   konum Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   konum Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   konum System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   konum System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   konum Microsoft.EntityFrameworkCore.Query.QueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   konum Microsoft.EntityFrameworkCore.Query.RelationalQueryableMethodTranslatingExpressionVisitor.VisitMethodCall(MethodCallExpression methodCallExpression)
   konum System.Linq.Expressions.MethodCallExpression.Accept(ExpressionVisitor visitor)
   konum System.Linq.Expressions.ExpressionVisitor.Visit(Expression node)
   konum Microsoft.EntityFrameworkCore.Query.QueryCompilationContext.CreateQueryExecutor[TResult](Expression query)
   konum Microsoft.EntityFrameworkCore.Storage.Database.CompileQuery[TResult](Expression query, Boolean async)
   konum Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.CompileQueryCore[TResult](IDatabase database, Expression query, IModel model, Boolean async)
   konum Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.&lt;&gt;c__DisplayClass9_0`1.&lt;Execute&gt;b__0()
   konum Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQueryCore[TFunc](Object cacheKey, Func`1 compiler)
   konum Microsoft.EntityFrameworkCore.Query.Internal.CompiledQueryCache.GetOrAddQuery[TResult](Object cacheKey, Func`1 compiler)
   konum Microsoft.EntityFrameworkCore.Query.Internal.QueryCompiler.Execute[TResult](Expression query)
   konum Microsoft.EntityFrameworkCore.Query.Internal.EntityQueryProvider.Execute[TResult](Expression expression)
   konum System.Linq.Queryable.SingleOrDefault[TSource](IQueryable`1 source, Expression`1 predicate)
   konum ECommercial.Core.DataAccess.EntitiyFramework.EFIEntityRepositoryBase`2.Get(Expression`1 filter) C:\Users\nihaSWin\Desktop\ECommercial\ECommercial.Core\DataAccess\EntitiyFramework\EFIEntityRepositoryBase.cs içinde: 36. satır
   konum ECommercial.Core.Business.EntityServiceBase`1.GetByPrimaryKey(Object key) C:\Users\nihaSWin\Desktop\ECommercial\ECommercial.Core\Business\EntityServiceBase.cs içinde: 26. satır
   konum ECommercial.MVC.Startup..ctor(IConfiguration configuration) C:\Users\nihaSWin\Desktop\ECommercial\ECommercial.MVC\Startup.cs içinde: 19. satır
</code></pre>

## Answers
### Answer ID: 64419387
<p>So it looks like you're trying to use reflection to determine the primary key and query based on that. You can't use a method like that directly in an expression and expect EF to untangle what it does and turn it into sql.</p>
<p>However, you could use reflection to generate an expression and use that directly instead.</p>
<pre class="lang-cs prettyprint-override"><code>public Expression&lt;Func&lt;TEntity, bool&gt;&gt; comparePrimaryKey&lt;TEntity&gt;(object value)
{
    var parm = Expression.Parameter(typeof(TEntity), &quot;e&quot;);
    var objType = value.GetType();
    return Expression.Lambda&lt;Func&lt;TEntity, bool&gt;&gt;(
        typeof(TEntity)
            .GetFields()
            .Where(f =&gt; f.GetCustomAttribute(typeof(PrimaryKeyFieldAttribute)) != null)
            .Select(f =&gt; (Expression)Expression.Equal(
                Expression.MakeMemberAccess(parm, f),
                Expression.Constant(
                    (objType == f.FieldType)
                        ? value
                        : objType.GetField(f.Name).GetValue(value),
                    f.FieldType)
            ))
            .Aggregate((l, r) =&gt; Expression.AndAlso(l, r)),
        parm);
}

//...

return _entityRepository.Get(primaryKeyComparable.comparePrimaryKey&lt;TEntity&gt;(key));
</code></pre>
<p>Though I would recommend using dbContext.Model metadata to discover the primary key, instead of depending on reflection and attribute conventions.</p>

