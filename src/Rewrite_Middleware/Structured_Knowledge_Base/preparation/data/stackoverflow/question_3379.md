# Is this a risk of SQL injection or a security risk in general?
[Link to question](https://stackoverflow.com/questions/77836532/is-this-a-risk-of-sql-injection-or-a-security-risk-in-general)
**Creation Date:** 1705544346
**Score:** 0
**Tags:** c#, sql, security, sql-injection, dapper
## Question Body
<p>I am using Dapper to write SQL queries and have written a generic repository. Seeing as parameterized table names are not supported, I am trying to figure out the best / safest way to dynamically change my table names depending on the implementation of the generic repository.</p>
<p>Originally I thought that I would just pass the table name as a string in the repositories constructor, but that seemed like I was delegating the responsibility of not passing a malicious string to the child class so I opted instead to get the table name directly from a custom attribute.</p>
<pre><code>public class TableAttribute : Attribute
{
    public string Name { get; private set; }

    public TableAttribute(string name)
    {
        Name = name;
    }

}
</code></pre>
<p>Then, on my database models, I would set them as follows:</p>
<pre><code>[Table(&quot;StudyType&quot;)]
public class StudyTypeModel
{

    public int Id { get; set; }
    public string TypeName { get; set; }

}
</code></pre>
<p>Then in my generical repository, I would directly access these attributes:</p>
<pre><code>public abstract class GeneralRepository&lt;T&gt; : IGeneralRepository&lt;T&gt;
{
    private readonly IConfiguration _config;
    
    private string _tableName = typeof(T).GetCustomAttribute&lt;TableAttribute&gt;()?.Name ?? throw new Exception(&quot;No Table Attribute found.&quot;);
    public GeneralRepository(IConfiguration config)
    {
        _config = config;
    }

    public async virtual Task&lt;ICollection&lt;T&gt;&gt; GetAllAsync()
    {
        try
        {
            using IDbConnection connection = new SqlConnection(_config.GetConnectionString(&quot;Default&quot;));
    
            var parameters = new { TableName = _tableName };
    
            var query = $&quot;&quot;&quot;
                SELECT *
                FROM {_tableName}
                &quot;&quot;&quot;;
    
            var result = (await connection.QueryAsync&lt;T&gt;(query, parameters)).ToList();
    
            return result;
        }
        catch (Exception ex)
        {
            throw;
        }
    }

    ... more generic methods
</code></pre>
<p>I know that you generally want to use parameterized queries, but unfortunately I don't believe this is possible in this scenario. I want to avoid rewriting basic CRUD methods for every table, but I definitely do not want that to come at the expense of application security. Is this a security risk / bad practice?</p>
<p>Thanks.</p>

