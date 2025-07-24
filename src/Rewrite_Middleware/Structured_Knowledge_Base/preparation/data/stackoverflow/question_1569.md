# Query takes extremely long in client app but is fast in SQL Server Management Studio
[Link to question](https://stackoverflow.com/questions/9943644/query-takes-extremely-long-in-client-app-but-is-fast-in-sql-server-management-st)
**Creation Date:** 1333112982
**Score:** 8
**Tags:** sql, sql-server-2008, database-performance
## Question Body
<p>I'm developing an application that stores images and related metadata. I'm running into issues when performing a certain query using NHibernate. The query is taking prohibitively long (on my machine something like 31 seconds), although the same query takes only a fraction of a second when executed in SQL Server Management Studio.</p>

<p>I've reduced and extraced the problem to a small test application:</p>

<p>Entities:</p>

<p><em>Tag</em>, consisting of Id (string, the tag value itself)</p>

<pre><code>public class Tag
{
    public virtual string Id { get; set; }
}
</code></pre>

<p><em>Image</em>, consisting of Id (int), Name (string) and Tags (many-to-many, set of <em>Tag</em> instances)</p>

<pre><code>public class Image
{
    private Iesi.Collections.Generic.ISet&lt;Tag&gt; tags = new HashedSet&lt;Tag&gt;();

    public virtual int Id { get; set; }

    public virtual string Name { get; set; }

    public virtual IEnumerable&lt;Tag&gt; Tags
    {
        get { return tags; }
    }

    public virtual void AddTag(Tag tag)
    {
        tags.Add(tag);
    }
}
</code></pre>

<p>I'm using "mapping by code" with the following mappings:</p>

<pre><code>public class TagMapping : ClassMapping&lt;Tag&gt;
{
    public TagMapping()
    {
        Id(x =&gt; x.Id, map =&gt; map.Generator(Generators.Assigned));
    }
}

public class ImageMapping : ClassMapping&lt;Image&gt;
{
    public ImageMapping()
    {
        Id(x =&gt; x.Id, map =&gt; map.Generator(Generators.Native));
        Property(x =&gt; x.Name);
        Set(x =&gt; x.Tags, 
            map =&gt; map.Access(Accessor.Field),
            map =&gt; map.ManyToMany(m2m =&gt; { }));
    }
}
</code></pre>

<p>The NHibernate/database configuration looks like this:</p>

<pre><code>  &lt;hibernate-configuration xmlns="urn:nhibernate-configuration-2.2"&gt;
    &lt;session-factory&gt;
      &lt;property name="dialect"&gt;NHibernate.Dialect.MsSql2008Dialect&lt;/property&gt;
      &lt;property name="connection.connection_string_name"&gt;PrimaryDatabase&lt;/property&gt;
        &lt;property name="format_sql"&gt;true&lt;/property&gt;
    &lt;/session-factory&gt;
  &lt;/hibernate-configuration&gt;
  &lt;connectionStrings&gt;
    &lt;add name="PrimaryDatabase" providerName="System.Data.SqlClient" connectionString="Data Source=.\SQLEXPRESS;Initial Catalog=PerfTest;Integrated Security=True" /&gt;
  &lt;/connectionStrings&gt;
</code></pre>

<p>I want to achieve the following query: give me all images where the name contains a specific string or where any tag contains a specific string. To find the latter I use a subquery that gives me the Ids of all images with matching tags. So in the end the search criteria are: the image has a name containing a specific string or its ID is one of those returned by the subquery.</p>

<p>Here's the code that executes the query:</p>

<pre><code>var term = "abc";
var mode = MatchMode.Anywhere;

var imagesWithMatchingTag = QueryOver.Of&lt;Image&gt;()
    .JoinQueryOver&lt;Tag&gt;(x =&gt; x.Tags)
    .WhereRestrictionOn(x =&gt; x.Id).IsLike(term, mode)
    .Select(x =&gt; x.Id);

var qry = session.QueryOver&lt;Image&gt;()
    .Where( Restrictions.On&lt;Image&gt;(x =&gt; x.Name).IsLike(term, mode) ||
            Subqueries.WhereProperty&lt;Image&gt;(x =&gt; x.Id).In(imagesWithMatchingTag))
    .List();
</code></pre>

<p>The test database (DBMS: SQL Server 2008 Express R2) I run this query against was created specifically for this test and does not contain anything else. I have filled it with random data: 10.000 images (table <em>Image</em>), 4.000 tags (table <em>Tag</em>) and roughly 200.000 associations between images and tags (table <em>Tags</em>), ie. each image has about 20 associated tags. The database </p>

<p>The SQL NHibernate claims to use is:</p>

<pre><code>SELECT
    this_.Id as Id1_0_,
    this_.Name as Name1_0_
FROM
    Image this_
WHERE
    (
        this_.Name like @p0
        or this_.Id in (
            SELECT
                this_0_.Id as y0_
            FROM
                Image this_0_
            inner join
                Tags tags3_
                    on this_0_.Id=tags3_.image_key
            inner join
                Tag tag1_
                    on tags3_.elt=tag1_.Id
            WHERE
                tag1_.Id like @p1
        )
    );
@p0 = '%abc%' [Type: String (4000)], @p1 = '%abc%' [Type: String (4000)]
</code></pre>

<p>This looks reasonable given the query I'm creating.</p>

<p>If I run this query using NHibernate the query takes about 30+ seconds (<code>NHibernate.AdoNet.AbstractBatcher - ExecuteReader took 32964 ms</code>) and returns 98 entities. </p>

<p>However, if I execute an equivalent query directly inside Sql Server Management studio:</p>

<pre><code>DECLARE @p0 nvarchar(4000)
DECLARE @p1 nvarchar(4000)

SET @p0 = '%abc%'
SET @p1 = '%abc%'    

SELECT
    this_.Id as Id1_0_,
    this_.Name as Name1_0_
FROM
    Image this_
WHERE
    (
        this_.Name like @p0
        or this_.Id in (
            SELECT
                this_0_.Id as y0_
            FROM
                Image this_0_
            inner join
                Tags tags3_
                    on this_0_.Id=tags3_.image_key
            inner join
                Tag tag1_
                    on tags3_.elt=tag1_.Id
            WHERE
                tag1_.Id like @p1
        )
    );
</code></pre>

<p>The query takes much less than one second (and returns 98 results as well).</p>

<p>Further experiments:</p>

<p>If I only search by name or only by tags, ie.:</p>

<pre><code>var qry = session.QueryOver&lt;Image&gt;()
    .Where( Subqueries.WhereProperty&lt;Image&gt;(x =&gt; x.Id).In(imagesWithMatchingTag))
    .List();
</code></pre>

<p>or</p>

<pre><code>var qry = session.QueryOver&lt;Image&gt;()
    .Where(Restrictions.On&lt;Image&gt;(x =&gt; x.Name).IsLike(term, mode))
    .List();
</code></pre>

<p>the queries are fast.</p>

<p>If I don't use like but an exact match in my subquery:</p>

<pre><code>var imagesWithMatchingTag = QueryOver.Of&lt;Image&gt;()
    .JoinQueryOver&lt;Tag&gt;(x =&gt; x.Tags)
    .Where(x =&gt; x.Id == term)
    .Select(x =&gt; x.Id);
</code></pre>

<p>the query is fast, too.</p>

<p>Changing the match mode for the name to Exact doesn't change anything.</p>

<p>When I debug the program and pause while the query is executing the top of the managed call stack looks like:</p>

<pre><code>[Managed to Native Transition]   
System.Data.dll!SNINativeMethodWrapper.SNIReadSync(System.Runtime.InteropServices.SafeHandle pConn, ref System.IntPtr packet, int timeout) + 0x53 bytes  
System.Data.dll!System.Data.SqlClient.TdsParserStateObject.ReadSni(System.Data.Common.DbAsyncResult asyncResult, System.Data.SqlClient.TdsParserStateObject stateObj) + 0xa3 bytes   
System.Data.dll!System.Data.SqlClient.TdsParserStateObject.ReadNetworkPacket() + 0x24 bytes  
System.Data.dll!System.Data.SqlClient.TdsParserStateObject.ReadBuffer() + 0x1f bytes     
System.Data.dll!System.Data.SqlClient.TdsParserStateObject.ReadByte() + 0x46 bytes   
System.Data.dll!System.Data.SqlClient.TdsParser.Run(System.Data.SqlClient.RunBehavior runBehavior, System.Data.SqlClient.SqlCommand cmdHandler, System.Data.SqlClient.SqlDataReader dataStream, System.Data.SqlClient.BulkCopySimpleResultSet bulkCopyHandler, System.Data.SqlClient.TdsParserStateObject stateObj) + 0x67 bytes     
System.Data.dll!System.Data.SqlClient.SqlDataReader.ConsumeMetaData() + 0x22 bytes   
System.Data.dll!System.Data.SqlClient.SqlDataReader.MetaData.get() + 0x57 bytes  
System.Data.dll!System.Data.SqlClient.SqlCommand.FinishExecuteReader(System.Data.SqlClient.SqlDataReader ds, System.Data.SqlClient.RunBehavior runBehavior, string resetOptionsString) + 0xe1 bytes  
...
</code></pre>

<p>So, my questions are:</p>

<ul>
<li>Why does the query so much longer when performed by NHibernate even though the SQL used is the same?</li>
<li>How can I get rid of the difference? Is there a setting that can cause this behavior?</li>
</ul>

<p>I know the query in general isn't the most efficient thing in the world, but what's striking me here is the difference between using NHibernate and manualy querying. There is definitively something strange going on here.</p>

<p>Sorry for the long post, but I wanted to include as much as possible about the issue. Thanks a lot in advance for your help!</p>

<p><strong>Update 1:</strong>
I've tested the application with NHProf without much added value: NHProf shows that the executed SQL is</p>

<pre><code>SELECT this_.Id   as Id1_0_,
       this_.Name as Name1_0_
FROM   Image this_
WHERE  (this_.Name like '%abc%' /* @p0 */
         or this_.Id in (SELECT this_0_.Id as y0_
                         FROM   Image this_0_
                                inner join Tags tags3_
                                  on this_0_.Id = tags3_.image_key
                                inner join Tag tag1_
                                  on tags3_.elt = tag1_.Id
                         WHERE  tag1_.Id like '%abc%' /* @p1 */))
</code></pre>

<p>Which is exactly what I posted before (because that's what NHibernate wrote to its log in the first place).</p>

<p>Here's a screenshot of NHProf
<img src="https://i.sstatic.net/01Tmg.jpg" alt="Screenshot of NHProf"></p>

<p>The warnings are understandable but don't explain the behavior.</p>

<p><strong>Update 2</strong>
@surfen sugested to pull the results of the sub query out of the DB first and stick them back into the main query:</p>

<pre><code>var imagesWithMatchingTag = QueryOver.Of&lt;Image&gt;()
    .JoinQueryOver&lt;Tag&gt;(x =&gt; x.Tags)
    .WhereRestrictionOn(x =&gt; x.Id).IsLike(term, mode)
    .Select(x =&gt; x.Id);

var ids = imagesWithMatchingTag.GetExecutableQueryOver(session).List&lt;int&gt;().ToArray();

var qry = session.QueryOver&lt;Image&gt;()
    .Where(
            Restrictions.On&lt;Image&gt;(x =&gt; x.Name).IsLike(term, mode) ||
            Restrictions.On&lt;Image&gt;(x =&gt; x.Id).IsIn(ids))
    .List();
</code></pre>

<p>While this does indeed make the main query fast again, I'd rather not take this approach as it does not fit well with the intended usage in the real world application. It is interesting that this is so much faster, though. I'd expect the subquery approach to be equally fast given that it is not dependent on the outer query.</p>

<p><strong>Update 3</strong>
This doesn't seem to be related to NHibernate. If I run the query using normal ADO.NET objects I get the same behavior:</p>

<pre><code>var cmdText = @"SELECT this_.Id   as Id1_0_,
                        this_.Name as Name1_0_
                FROM   Image this_
                WHERE  (this_.Name like  @p0 
                            or this_.Id in 
                        (SELECT this_0_.Id as y0_
                        FROM   Image this_0_
                            inner join Tags tags3_
                                on this_0_.Id = tags3_.image_key
                            inner join Tag tag1_
                                on tags3_.elt = tag1_.Id
                        WHERE  tag1_.Id like  @p1 ));";

using (var con = new SqlConnection(ConfigurationManager.ConnectionStrings["PrimaryDatabase"].ConnectionString))
{
    con.Open();
    using (var txn = con.BeginTransaction())
    {
        using (var cmd = new SqlCommand(cmdText, con, txn))
        {
            cmd.CommandTimeout = 120;
            cmd.Parameters.AddWithValue("p0", "%abc%");
            cmd.Parameters.AddWithValue("p1", "%abc%");

            using (var reader = cmd.ExecuteReader())
            {
                while (reader.Read())
                {
                    Console.WriteLine("Match");
                }
            }

        }
        txn.Commit();
    }
}
</code></pre>

<p><strong>Update 4</strong></p>

<p>Query-plans (click to zoom):</p>

<p>Slow query 
<img src="https://i.sstatic.net/zcLIY.png" alt="Slow plan"></p>

<p>Fast query
<img src="https://i.sstatic.net/PXQ1B.png" alt="Fast plan"></p>

<p>There definitively is a difference in the plan.</p>

<p><strong>Update 5</strong></p>

<p>As it indeed seems that Sql Server treats the subquery as being correlated I tried something different: I moved the criterion related to the name to a subquery by itself:</p>

<pre><code>var term = "abc";
var mode = MatchMode.Anywhere;

var imagesWithMatchingTag = QueryOver.Of&lt;Image&gt;()
    .JoinQueryOver&lt;Tag&gt;(x =&gt; x.Tags)
    .WhereRestrictionOn(x =&gt; x.Id).IsLike(term, mode)
    .Select(x =&gt; x.Id);

var imagesWithMatchingName = QueryOver.Of&lt;Image&gt;()
    .WhereRestrictionOn(x =&gt; x.Name).IsLike(term, mode)
    .Select(x =&gt; x.Id);

var qry = session.QueryOver&lt;Image&gt;()
    .Where(
      Subqueries.WhereProperty&lt;Image&gt;(x =&gt; x.Id).In(imagesWithMatchingName) ||        
      Subqueries.WhereProperty&lt;Image&gt;(x =&gt; x.Id).In(imagesWithMatchingTag) 
    ).List();
</code></pre>

<p>Generated SQL:</p>

<pre><code>SELECT
    this_.Id as Id1_0_,
    this_.Name as Name1_0_
FROM
    Image this_
WHERE
    (
        this_.Id in (
            SELECT
                this_0_.Id as y0_
            FROM
                Image this_0_
            inner join
                Tags tags3_
                    on this_0_.Id=tags3_.image_key
            inner join
                Tag tag1_
                    on tags3_.elt=tag1_.Id
            WHERE
                tag1_.Id like @p0
        )
        or this_.Id in (
            SELECT
                this_0_.Id as y0_
            FROM
                Image this_0_
            WHERE
                this_0_.Name like @p1
        )
    );
@p0 = '%abc%' [Type: String (4000)], @p1 = '%abc%' [Type: String (4000)]
</code></pre>

<p>This seems to break the correlation and as a result the query becomes "fast" again ("fast" as in "acceptable for the moment"). The query time went down from 30+ seconds to ~170ms. Still not a lightweight query, but at least will allow me to continue from here. I know that a <code>"like '%foo%'"</code> will never be super fast. If it comes to the worst I can still move to a specialized search server (Lucene, solr) or real full text searching.</p>

<p><strong>Update 6</strong>
I was able to rewrite the query to NOT use subqueries at all:</p>

<pre><code>var qry = session.QueryOver(() =&gt; img)
    .Left.JoinQueryOver(x =&gt; x.Tags, () =&gt; tag)
    .Where(
        Restrictions.Like(Projections.Property(() =&gt; img.Name), term, mode) ||
        Restrictions.Like(Projections.Property(() =&gt; tag.Id), term, mode))
    .TransformUsing(Transformers.DistinctRootEntity)
    .List();
</code></pre>

<p>SQL:</p>

<pre><code>SELECT
    this_.Id as Id1_1_,
    this_.Name as Name1_1_,
    tags3_.image_key as image1_3_,
    tag1_.Id as elt3_,
    tag1_.Id as Id0_0_
FROM
    Image this_
left outer join
    Tags tags3_
        on this_.Id=tags3_.image_key
left outer join
    Tag tag1_
        on tags3_.elt=tag1_.Id
WHERE
    (
        this_.Name like @p0
        or tag1_.Id like @p1
    );
@p0 = '%abc%' [Type: String (4000)], @p1 = '%abc%' [Type: String (4000)]
</code></pre>

<p>However, the query performs now slightly worse than the version with subqueries. I'll investigate this further.</p>

## Answers
### Answer ID: 75418308
<p>Have you check for Parameter Sniffing Issue? I saw you did not mention data type when adding parameter to a Sql Command. Please See <a href="https://stackoverflow.com/questions/20699393/sql-server-parameter-sniffing">SQL Server - parameter sniffing</a></p>

### Answer ID: 9943961
<p>My bet is that it's the second query that is slow:</p>

<pre><code>var qry = session.QueryOver&lt;Image&gt;()
.Where( Restrictions.On&lt;Image&gt;(x =&gt; x.Name).IsLike(term, mode) ||
        Subqueries.WhereProperty&lt;Image&gt;(x =&gt; x.Id).In(imagesWithMatchingTag))
.List();
</code></pre>

<p>You provided SQL for only the first query. What about the second? Did you test it under SQL Management Studio? Use SQL Server Profiler as @JoachimIsaksson suggests to find out what queries exacly NHibernate executes server-side.</p>

<p>This looks like you're loading 97 <code>image</code> objects into memory. How large is each of them?</p>

<p><strong>EDIT</strong></p>

<p>Another bet is that your first query executes ad inner query for the second query. Try doing .List() on the first query to load the tags into memory.</p>

<p><strong>EDIT 2</strong></p>

<p>From the query plans it really looks like your query is being called as a <a href="http://en.wikipedia.org/wiki/Correlated_subquery" rel="nofollow">Correlated subquery</a>. 
You mentioned that these queries are fast:</p>

<pre><code>var qry = session.QueryOver&lt;Image&gt;()
.Where( Subqueries.WhereProperty&lt;Image&gt;(x =&gt; x.Id).In(imagesWithMatchingTag))
.List();
</code></pre>

<p>or</p>

<pre><code>var qry = session.QueryOver&lt;Image&gt;()
.Where(Restrictions.On&lt;Image&gt;(x =&gt; x.Name).IsLike(term, mode))
.List();
</code></pre>

<p>Just UNION them and you should get the same result as running both of them separately.
Also make sure that all the join columns have indexes.</p>

<p>That's the catch with IS IN (query) - you can't be sure how the database executes it (unless you somehow force it to use a certain plan). Maybe you could change .In() it into JoinQueryOver() somehow?</p>

