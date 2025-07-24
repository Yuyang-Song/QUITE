# Best &quot;pattern&quot; for Data Access Layer to Business Object
[Link to question](https://stackoverflow.com/questions/644941/best-pattern-for-data-access-layer-to-business-object)
**Creation Date:** 1236985902
**Score:** 16
**Tags:** c#, asp.net, design-patterns, data-access-layer
## Question Body
<p>I'm trying to figure out the cleanest way to do this.</p>

<p>Currently I have a customer object:</p>

<pre><code>public class Customer
{
    public int Id {get;set;}
    public string name {get;set;}
    public List&lt;Email&gt; emailCollection {get;set}
    public Customer(int id)
    {
        this.emailCollection = getEmails(id);
    }
}
</code></pre>

<p>Then my Email object is also pretty basic.</p>

<pre><code>public class Email
{
    private int index;
    public string emailAddress{get;set;}
    public int emailType{get;set;}
    public Email(...){...}
    public static List&lt;Email&gt; getEmails(int id)
    {
        return DataAccessLayer.getCustomerEmailsByID(id);
    }
}
</code></pre>

<p>The DataAccessLayer currently connects to the data base, and uses a SqlDataReader to iterate over the result set and creates new Email objects and adds them to a List which it returns when done.</p>

<p>So where and how can I improve upon this?</p>

<p>Should I have my DataAccessLayer instead return a DataTable and leave it up to the Email object to parse and return a List back to the Customer?</p>

<p>I guess "Factory" is probably the wrong word, but should I have another type of EmailFactory which takes a DataTable from the DataAccessLayer and returns a List to the Email object?  I guess that kind of sounds redundant...</p>

<p>Is this even proper practice to have my Email.getEmails(id) as a static method?</p>

<p>I might just be throwing myself off by trying to find and apply the best "pattern" to what would normally be a simple task.</p>

<p>Thanks.</p>

<hr>

<p>Follow up</p>

<p>I created a working example where my Domain/Business object extracts a customer record by id from an existing database.  The xml mapping files in nhibernate are really neat.  After I followed a tutorial to setup the sessions and repository factories, pulling database records was pretty straight forward.</p>

<p>However, I've noticed a huge performance hit.</p>

<p>My original method consisted of a Stored Procedure on the DB, which was called by a DAL object, which parsed the result set into my domain/business object.</p>

<p>I clocked my original method at taking 30ms to grab a single customer record.  I then clocked the nhibernate method at taking 3000ms to grab the same record.</p>

<p>Am I missing something?  Or is there just a lot of overhead using this nhibernate route?</p>

<p>Otherwise I like the cleanliness of the code:</p>

<pre><code>protected void Page_Load(object sender, EventArgs e)
{
    ICustomerRepository repository = new CustomerRepository();
    Customer customer = repository.GetById(id);
}

public class CustomerRepository : ICustomerRepository
        {
            public Customer GetById(string Id)
            {
                using (ISession session = NHibernateHelper.OpenSession())
                {
                    Customer customer = session
                                        .CreateCriteria(typeof(Customer))
                                        .Add(Restrictions.Eq("ID", Id))
                                        .UniqueResult&lt;Customer&gt;();
                    return customer;
                }
            }
        }
</code></pre>

<p>The <a href="http://web.archive.org/web/20090805054123/http://blogs.hibernatingrhinos.com/nhibernate/archive/2008/04/01/your-first-nhibernate-based-application.aspx" rel="nofollow noreferrer">example I followed</a> had me create a helper class to help manage the Session, maybe that's why i'm getting this overhead?  </p>

<pre><code>public class NHibernateHelper
    {
        private static ISessionFactory _sessionFactory;
        private static ISessionFactory SessionFactory
        {
            get
            {
                if (_sessionFactory == null)
                {
                    Configuration cfg = new Configuration();
                    cfg.Configure();
                    cfg.AddAssembly(typeof(Customer).Assembly);
                    _sessionFactory = cfg.BuildSessionFactory();
                }
                return _sessionFactory;
            }

        }

        public static ISession OpenSession()
        {
            return SessionFactory.OpenSession();
        }
    }
</code></pre>

<p>With the application i'm working on, speed is of the essence.  And ultimately a lot of data will pass between the web-app and the database.  If it takes an agent 1/3 of a second to pull up a customer record as opposed to 3 seconds, that would be a huge hit.  But if i'm doing something weird and this is a one time initial setup cost, then it might be worth it if the performance was just as good as executing stored procedures on the DB.</p>

<p>Still open to suggestions!</p>

<hr>

<p>Updated.</p>

<p>I'm scrapping my ORM/NHibernate route.  I found the performance is just too slow to justify using it.  Basic customer queries just take too long for our environment.  3 seconds compared to sub-second responses is too much.</p>

<p>If we wanted slow queries, we'd just keep our current implementation.  The idea to rewrite it was to drastically increase times.</p>

<p>However, after having played with NHibernate this past week, it is a great tool!  It just doesn't quite fit my needs for this project.</p>

## Answers
### Answer ID: 644994
<p>This may be too radical for you and doesn't really solve the question, but how about completely scrapping your data layer and opting for an ORM? You will save a lot of code redundancy that spending a week or so on a DAL will bring.</p>

<p>That aside, the pattern you're using resembles a repository pattern, sort of. I'd say your options are </p>

<ul>
<li>A service object in your Email class - say EmailService - instantiated in the constructor or a property. Accessed via an instance such as email.Service.GetById(id) </li>
<li>A static method on Email, like Email.GetById(id) which is a similar approach</li>
<li>A completely separate static class that is basically a façade class, EmailManager for example, with static  methods like EmailManager.GetById(int) </li>
<li>The ActiveRecord pattern where you are dealing with an instance, like 
email.Save() and email.GetById()</li>
</ul>

### Answer ID: 644998
<p>Most likely your application has its domain logic setup in <a href="http://martinfowler.com/eaaCatalog/transactionScript.html" rel="nofollow noreferrer">transaction scripts</a>. For .NET implementations that use transaction script Martin Fowler recommends the usage of the <a href="http://martinfowler.com/eaaCatalog/tableDataGateway.html" rel="nofollow noreferrer">table data gateway</a> pattern. .NET provides good support for this pattern because the table data gateway pattern is great with <a href="http://martinfowler.com/eaaCatalog/recordSet.html" rel="nofollow noreferrer">record set</a>, which Microsoft implements with its DataSet-type classes.</p>

<p>Various tools within the Visual Studio environment should increase your productivity. The fact that DataSets can easily be databound to various controls (like the DataGridView) makes it a good choice for data-driven applications.</p>

<p>If your business logic is more complex than a few validations a <a href="http://martinfowler.com/eaaCatalog/domainModel.html" rel="nofollow noreferrer">domain model</a> becomes a good option. Do note that a domain model comes with a whole different set of data access requirements!</p>

### Answer ID: 644986
<p>I've implemented a DAL layer by basically doing what NHibernate does but manually.  What NHibernate does is create a Proxy class that inherits from your Domain object (which should have all its fields marked as virtual).  All data access code goes into property overrides, its pretty elegant actually.</p>

<p>I simplified this somewhat by having my Repositories fill out the simple properties themselves and only using a proxy for Lazy loading.  What I ended up is a set of classes like this:</p>

<pre><code>public class Product {
  public int Id {get; set;}
  public int CustomerId { get; set;}
  public virtual Customer Customer { get; set;}
}
public class ProductLazyLoadProxy {
  ICustomerRepository _customerRepository;
  public ProductLazyLoadProxy(ICustomerRepository customerRepository) {
    _customerRepository = customerRepository;
  }
  public override Customer {
    get {
      if(base.Customer == null)
        Customer = _customerRepository.Get(CustomerId);
      return base.Customer
    }
    set { base.Customer = value; }
  }
}
public class ProductRepository : IProductRepository {
  public Product Get(int id) {
    var dr = GetDataReaderForId(id);
    return new ProductLazyLoadProxy() {
      Id = Convert.ToInt(dr["id"]),
      CustomerId = Convert.ToInt(dr["customer_id"]),
    }
  }
}
</code></pre>

<p>But after writing about 20 of these I just gave up and learned NHibernate, with Linq2NHibernate for querying and FluentNHibernate for configuration nowadays the roadblocks are lower than ever.</p>

### Answer ID: 644952
<p>If the configuration you've got works now, why mess with it?  It doesn't sound like you're identifying any particular needs or issues with the code as it is.</p>

<p>I'm sure a bunch of OO types could huddle around and suggest various refactorings here so that the correct responsibilities and roles are being respected, and somebody might even try to shoehorn in a design pattern or two.  But the code you have now is simple and sounds like it doesn't have any issues - i'd say leave it.</p>

