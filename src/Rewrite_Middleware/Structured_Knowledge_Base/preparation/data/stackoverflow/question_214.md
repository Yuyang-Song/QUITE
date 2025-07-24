# Differ Domain Model From Database Schema in Entity Framework 4.0
[Link to question](https://stackoverflow.com/questions/1689537/differ-domain-model-from-database-schema-in-entity-framework-4-0)
**Creation Date:** 1257533395
**Score:** 1
**Tags:** c#, entity-framework, repository-pattern
## Question Body
<p>I'm very new to the Entity Framework and trying to understand how to best architect my data layer in way that makes the most sense from the prospective of a developer. I'm working on a proof of concept using the <a href="http://www.codeplex.com/Wikipage?ProjectName=SqlServerSamples" rel="nofollow noreferrer">AventureWorks</a> database. I built a generic repository that I use to query any table in the database. Following is a short, but compilable (I hope), snippet (the actual code has methods to update, delete, etc.):</p>

<pre><code>    /// &lt;summary&gt;
    /// A generic repository for working with data in the database
    /// &lt;/summary&gt;
    /// &lt;typeparam name="T"&gt;A POCO that represents an Entity Framework entity&lt;/typeparam&gt;
    public class DataRepository&lt;T&gt; : IDisposable, IRepository&lt;T&gt; where T : class
    {
        /// &lt;summary&gt;
        /// The context object for the database
        /// &lt;/summary&gt;
        private ObjectContext _context;

        /// &lt;summary&gt;
        /// The IObjectSet that represents the current entity. Used to query, add, modify and delete objects of the specified entity.
        /// &lt;/summary&gt;
        private IObjectSet&lt;T&gt; _objectSet;

        /// &lt;summary&gt;
        /// Initializes a new instance of the DataRepository class
        /// &lt;/summary&gt;
        public DataRepository()
            : this(new AdventureWorksEntities())
        {
        }

        /// &lt;summary&gt;
        /// Initializes a new instance of the DataRepository class
        /// &lt;/summary&gt;
        /// &lt;param name="context"&gt;The Entity Framework ObjectContext&lt;/param&gt;
        public DataRepository(ObjectContext context)
        {
            _context = context;
            _objectSet = _context.CreateObjectSet&lt;T&gt;();
        }

        /// &lt;summary&gt;
        /// Gets all records as an IQueryable
        /// &lt;/summary&gt;
        /// &lt;returns&gt;An IQueryable object, containing the results of the query&lt;/returns&gt;
        public IQueryable&lt;T&gt; GetQuery()
        {
            return from x in _objectSet select x;
        }

        /// &lt;summary&gt;
        /// Releases all resources used by the WarrantManagement.DataExtract.Dal.ReportDataBase
        /// &lt;/summary&gt;
        public void Dispose()
        {
            Dispose(true);
            GC.SuppressFinalize(this);
        }

        /// &lt;summary&gt;
        /// Releases all resources used by the WarrantManagement.DataExtract.Dal.ReportDataBase
        /// &lt;/summary&gt;
        /// &lt;param name="disposing"&gt;A boolean value indicating whether or not to dispose managed resources&lt;/param&gt;
        protected virtual void Dispose(bool disposing)
        {
            if (disposing)
            {
                if (_context != null)
                {
                    _context.Dispose();
                    _context = null;
                }
            }
        }
    }
</code></pre>

<p>In my ASP.NET demo app, I can use the repository, as follows, to get an Employee record (notice the reference to Contact):</p>

<pre><code>        using (DataRepository repository = new DataRepository())
        {
            this.GridView1.DataSource = from x in repository.GetQuery()
                                        select new
                                        {
                                            x.MaritalStatus,
                                            x.Contact.FirstName,
                                            x.Contact.LastName,
                                            x.BirthDate
                                        };
            this.GridView1.DataBind();
        }
</code></pre>

<p>This could work out well, but my concern is that the View now has knowledge of the database schema, which I don't like. For example, if I were to decide to move the FirstName and LastName columns into the Employee table, I would have to rewrite all lines of code where I referenced the columns as I did in the snippet above. My preference is to change the conceptual model by creating properties off of the Employee class and have Entity Framework automatically perform the JOIN, as necessary.</p>

<p>Firstly, are there any "lessons learned" from anybody that has designed a model like I have proposed? Anything negative that I should look out for? Secondly, are there any alternatives that I should be aware of?</p>

## Answers
### Answer ID: 1690305
<p>Part of what you're running up against is ASP.NET. Having the view aware of the repository at all is suspicious. In MVC, for example, binding repository public types to a view model would be done in the controller, and the view would only know about the view model.</p>

<p>But even in straight ASP.NET I'd suggest creating dedicated view/presentation models and projecting onto them using an L2E query, similar to what you're doing now with the anonymous type. Using a presentation model instead of an anonymous type will allow you to move the query out of the Page and remove knowledge of the Entity type from the page.</p>

