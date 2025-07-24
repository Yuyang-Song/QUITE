# How do I convert SQL results into a list of objects in C#?
[Link to question](https://stackoverflow.com/questions/3552523/how-do-i-convert-sql-results-into-a-list-of-objects-in-c)
**Creation Date:** 1282607045
**Score:** 1
**Tags:** c#, sql
## Question Body
<p>I am working on converting a web application over to a WPF desktop application. I want to use the existing data access layer so I don't have to rewrite all the SQL queries.</p>

<p>But, as it stands, everything is populated almost purely from DataTables returned from SQL queries. To make things a bit easier to manage, in some instances, it would really be nice to convert these things into objects.</p>

<p>For example, I have a query that pulls out report information. I may get 500 results with columns like ReportID, ReportTitle, ReportDate.</p>

<p>I would like to make a report class that has these public attributes and somehow convert the SQL query results into a collection of these report objects.</p>

<p>What is the best way to go about doing this?</p>

<p>Super bonus points if there is an easy way of going backwards (updating the database if the objects are changed).</p>

## Answers
### Answer ID: 3553136
<p>Check out this method. First you can create a class that inherits DataContext. And then you can use methods of DataContext like to ExecuteQuery&lt;> to convert your results in to objects. With this method you can directly use your queries you wrote earlier. Also, I feel that this way is a lot better than maintaining a .dbml file, because of the issues associated to synchronization with the actual database schema.</p>

<p>Consider the following example. First you need to define a class for interacting with your database</p>

<pre><code>public class DBManagerDataContext : DataContext
{
    private static string connectionString = ""; // Your connection string

    public static DBManagerDataContext CreateInstance()
    {
        return new DBManagerDataContext(connectionString);
    }

    protected DBManagerDataContext(string connectionString)
        : base(connectionString, new AttributeMappingSource())
    {

    }
}
</code></pre>

<p>Then you can use this context to execute queries and convert them in to objects as shown below:</p>

<pre><code>public class Report
{
    public int ReportID;
    public string ReportTitle;
    public DateTime ReportDate;

    private static string query = "select ReportID, ReportTitle, ReportDate from dbo.Reports"; // Your query

    public static List&lt;Report&gt; GetReportList()
    {
        DBManagerDataContext context = DBManagerDataContext.CreateInstance();
        return context.ExecuteQuery&lt;Report&gt;(query).ToList();
    }
}
</code></pre>

<p>You can use the method "GetReportList()" given above like this for example:</p>

<pre><code>List&lt;Report&gt; reports = Report.GetReportList();
</code></pre>

<p>In the case of updates, the method suggested by "jdandison" is a nice option, apart from using the data context as above. In the case of updates it would be "ExecuteCommand" though. Please explore the DataContext class for more information.</p>

<p>Edit: Please note that the query column names should match the definition in the object</p>

### Answer ID: 3552627
<p>While I would also like to suggest ORM (NHibernate is the way to go:)) a possible solution is:</p>

<pre><code>public IEnumerable&lt;Report&gt; ToReportList(DataTable dt)
{
  return dt.AsEnumerable().Select(dr =&gt; new Report
                                        {
                                            member1 = dr["column1"].ToString(),
                                            ...
                                        });
}
</code></pre>

<p>Report is your class here by the way.Such as,</p>

<pre><code>internal class Report
{
  public string member1{ get; set;}
  ...
}
</code></pre>

<p>You may also want to check this,</p>

<ul>
<li><a href="http://msdn.microsoft.com/en-us/library/Bb399375(v=VS.100).aspx" rel="nofollow noreferrer">http://msdn.microsoft.com/en-us/library/Bb399375(v=VS.100).aspx</a></li>
</ul>

<p>I think if you search stackoverflow, you will find nicer examples as I remember learning this from here.</p>

<p>By the way, if you use NHibernate, you won't have to rewrite your queries at all. All you have to do is map your tables to a class and booya you are good to go. It will handle all your DML stuff (well mostly) and you can easily tell the ORM to do LazyLoad, Batch processing etc which is pretty cool.</p>

<blockquote>
  <p>Super bonus points if there is an easy
  way of going backwards (updating the
  database if the objects are changed).</p>
</blockquote>

<p>For that , go for ORM i.e. NHibernate (I know I am biased :)). For LINQ to SQL examples check the 2 links below:</p>

<ul>
<li><a href="http://msdn.microsoft.com/en-us/library/bb386931.aspx" rel="nofollow noreferrer">http://msdn.microsoft.com/en-us/library/bb386931.aspx</a></li>
<li><a href="http://csainty.blogspot.com/2008/01/linq-to-sql-insertupdatedelete.html" rel="nofollow noreferrer">http://csainty.blogspot.com/2008/01/linq-to-sql-insertupdatedelete.html</a></li>
</ul>

### Answer ID: 3552771
<p>+1 ORM. Entity Framework is good, LINQ to SQL is good too, but you'd need a good database design and is better for pretty basic SQL CRUD actions. For custom entities from multiple datasources, I'd go EF.</p>

<p>As far as backwards updating - LINQ to SQL has an easy-peasy implementation, sorta like this - say you've got a db called MyDatabase with Dog entities in it:</p>

<pre><code>using(MyDatabaseDataContext db = new MyDatabaseDataContext())
{
    //LINQ will automatically pluralize your items (entity named Dog becomes Dogs)
    Dog d = db.Dogs.Where(x=&gt;x.DogName.Equals(dogName));
    d.Owner = "Steve";
    db.SubmitChanges();
    //adding new items is easy too
    Dog newdog = new Dog();
    newDog.DogName = "Scruff";
    newDog.Owner = "Jim";
    db.Dogs.Add(newDog);
    db.SubmitChanges();
}
</code></pre>

### Answer ID: 3552542
<p>You should learn about <a href="http://en.wikipedia.org/wiki/Object-relational_mapping" rel="nofollow noreferrer">Object-Relational Mapping</a> <strong>(ORM)</strong>. A good ORM can save you tonnes of work in the future, and gets those nasty queries out of your code.</p>

<p>I'd recommend <a href="http://nhforge.org/" rel="nofollow noreferrer">NHibernate</a> or <a href="http://msdn.microsoft.com/en-us/data/aa937723.aspx" rel="nofollow noreferrer">Entity Framework 4.0</a></p>

