# Unit testing a .NET Web API/SQL project with existing methods?
[Link to question](https://stackoverflow.com/questions/41406803/unit-testing-a-net-web-api-sql-project-with-existing-methods)
**Creation Date:** 1483173732
**Score:** 0
**Tags:** sql-server, unit-testing, asp.net-web-api
## Question Body
<p>I have inherited a Web API 2 project written in C#/.NET that uses ADO.NET to access an SQL Server database.</p>

<p>The data access layer of the project contains many methods which look similar to this:</p>

<pre><code>public class DataAccessLayer
{
    private SqlConnection _DBConn;
    public DataAccessLayer()
    {
        _DBConn = new SqlConnection(ConfigurationManager.ConnectionStrings["DefaultConnection"].ConnectionString);
    }

    public string getAllProductsAsJSON()
    {
        DataTable dt = new DataTable();
        using (SqlConnection con = _DBConn)
        {
            using (SqlCommand cmd = new SqlCommand("SELECT productId, productName FROM product ORDER BY addedOn DESC", con))
            {
                cmd.CommandType = CommandType.Text;
                // add parameters to the command here, if required.
                con.Open();
                SqlDataAdapter da = new SqlDataAdapter(cmd);
                da.Fill(dt);
                return JsonConvert.SerializeObject(dt);
            }
        }
    }

    // ... more methods here, but all basically following the above style of 
    //     opening a new connection each time a method is called.

}
</code></pre>

<p>Now, I want to write some unit tests for this project. I have studied the idea of using SQL transactions to allow for insertion of mock data into the database, testing against the mock data, and then rolling back the transaction in order to allow for testing against a "live" (development) database, so you can have access to the SQL Server functionality without mocking it out completely (e.g. you can make sure your views/functions are returning valid data AND that the API is properly processing the data all at once). Some of the methods in the data access layer add data to the database, so the idea is that I would want to start a transaction, call a set of DAL methods to insert mock data, call other methods to test the results with assertions, and then roll back the entire test so that no mock data gets committed.</p>

<p>The problem I am having is that, as you can see, this class has been designed to create a new database connection every single time that a query is made. If I try to think like the original developer probably thought, I could see how it could make at least some sense to do this, considering the fact that these classes are used by a web API, so a persistent database connection would be impractical especially if a web API call involves transactions, because you then do need a separate connection per request to maintain separation.</p>

<p>However, because this is happening I don't think I can use the transaction idea to write tests as I described, because uncommitted data would not be accessible across database connections. So if I wrote a test which calls DAL methods (and also business-logic layer methods which in turn call DAL methods), each method will open its own connection to the database, and thus I have no way to wrap all of the method calls in a transaction to begin with.</p>

<p>I could rewrite each method to accept an SQLConnection as one of its parameters, but if I do this, I not only have to refactor over 60 methods, but I also have to rework every single place that such methods are called in the Web API controllers. I then have to move the burden of creating and managing DB connections to the Web API (and away from the DAL, which is where it philosophically should be).</p>

<p>Short of literally rewriting/refactoring 60+ methods and the entire Web API, is there a different approach I can take to writing unit tests for this project?</p>

<hr>

<p>EDIT: My new idea is to simply remove all calls to <code>con.Open()</code>. Then, in the constructor, not just create the connection but also open it. Finally, I'll add beginTransaction, commitTransaction and rollbackTransaction methods that operate directly upon the connection object. The core API never needs to call these functions, but the unit tests can call them. This means the unit test code can simply create an instance, which will create a connection which persists across the entire lifetime of the class. Then it can use beginTransaction, then do whatever tests it wants, and finally rollbackTransaction. Having a commitTransaction is good for completeness and also exposing this functionality to the business-logic layer has potential use.</p>

## Answers
### Answer ID: 41418602
<p>There are multiple possible answers to this question, depending on what exactly you are trying to accomplish:</p>

<ol>
<li>Are you primarily interested in unit testing your application logic (e.g., controller methods), rather than the data access layer itself?</li>
<li>Are you looking to unit test the logic inside your data access layer?</li>
<li>Or are you trying to test everything together (i.e., integration or end-to-end testing)?</li>
</ol>

<p>I am assuming you are interested in the first scenario, testing your application logic. In that case, I would advise against connecting to the database at all (even a development database) in your unit tests. Generally, unit tests should not be interacting with any outside system (e.g., database, filesystem, or network).</p>

<p>I know you mentioned you were interested in testing multiple parts of the functionality all at once:</p>

<blockquote>
  <p>I have studied the idea of using SQL transactions [...] so you can have access to the SQL Server functionality without mocking it out completely (e.g. you can make sure your views/functions are returning valid data AND that the API is properly processing the data all at once).</p>
</blockquote>

<p>However, that rather goes against the philosophy of unit testing. The whole point of a unit test is to test a single <strong>unit</strong> in isolation. Typically, this unit ("System Under Test", or <a href="https://stackoverflow.com/questions/7321407/what-is-sut-and-where-did-it-come-from">SUT</a>, in more technical terms) is a single method inside some class (for instance, an action method in one of your controllers). Anything other than the SUT should be stubbed or mocked out.</p>

<p>To accomplish this, broadly speaking, you will need to refactor your code to use dependency injection, and also use a mocking framework in your tests:</p>

<ul>
<li><strong>Dependency Injection:</strong> If you are not using a dependency injection framework already, chances are your controller classes are instantiating your <code>DataAccessLayer</code> class directly. This approach will not work for unit tests - instead, you will want to refactor the controller class to accept its dependencies via the constructor, and then use a dependency injection framework to inject the real <code>DataAccessLayer</code> in your application code, and inject a mock/stub implementation in your tests. Some popular dependency injection frameworks include <a href="https://autofac.org/" rel="nofollow noreferrer">Autofac</a>, <a href="http://www.ninject.org/" rel="nofollow noreferrer">Ninject</a>, and <a href="https://msdn.microsoft.com/en-us/library/dn223671(v=pandp.30).aspx" rel="nofollow noreferrer">Microsoft Unity</a>. Depending on which framework you choose, this may also require that you refactor <code>DataAccessLayer</code> a bit so it implements an interface (e.g., <code>IDataAccessLayer</code>).</li>
<li><strong>Mocking Framework:</strong> In your tests, rather than using the real <code>DataAccessLayer</code> class directly, you will instead create a mock, and set up expectations on that mock. Some popular mocking frameworks for .NET include <a href="https://github.com/moq/moq4" rel="nofollow noreferrer">Moq</a>, <a href="https://hibernatingrhinos.com/oss/rhino-mocks" rel="nofollow noreferrer">RhinoMocks</a>, and <a href="http://nsubstitute.github.io/" rel="nofollow noreferrer">NSubstitute</a>).</li>
</ul>

<p>Granted, if the code was not initially written with unit testing in mind (i.e., no dependency injection), this may involve a fair amount of refactoring. This is where alltej's suggestion comes in with creating a wrapper for interacting with the legacy (i.e., untested) code.</p>

<p>I strongly recommend you read the book <strong>The Art of Unit Testing: With Examples in C#</strong> (by Roy Osherove). That will help you understand the ideology behind unit testing a bit better.</p>

<p>If you are actually interested in testing multiple parts of your functionality at once, then what you are describing (as others have pointed out) is integration, or end-to-end testing. The setup for this would be entirely different (and often more challenging), but even then, the recommended approach would be to connect to a separate database (specifically for integration testing, separate even from your development database), rather than rolling back transactions.</p>

### Answer ID: 41409540
<p>Actually, from what I see in the code, the DAL creates only one connection in the constructor and then it keeps using it to fire commands, one command per method in the DAL. It will only create new connections if you create another instance of the DAL class.</p>

<p>Now, what you are describing is multiple test into, integration, end to end and I am not convinced that the transaction idea, while original, is actually doable.</p>

<p>When writing integration tests, I prefer to actually create all the data required by the test and then simply remove it at the end, that way nothing is left behind and you know for sure if your system works or not.</p>

<p>So imagine you're testing retrieving account data for a user, I would create a user, activate them, attach an account and then test against that real data.</p>

<p>The UI does not need to go all the way through, unless you really want to do end to end tests. If you don't, then you can just mock the data for each scenario you want to test and see how the UI behaves under each scenario.</p>

<p>What I would suggest is that you test your api separately, test each endpoint and make sure it works as expected with integration tests covering all scenarios needed.</p>

<p>If you have time, then write some end to end tests, possibly using a tool like Selenium or whatever else you fancy.</p>

<p>I would also extract an interface from that DAL in preparation of mocking the entire layer when needed. That should give you a good start in what you want to do.</p>

### Answer ID: 41409466
<p>When working with legacy system, what I would do is create a wrapper for this DLLs/projects to isolate communication with legacy and to protect integrity of your new subsystem/domain or bounded context. This isolation layer is known as anticorruption layer in DDD terminology. This layer contains interfaces written in terms of your new bounded context. The interface adapts and interacts with your API layer or to other services in the domain. You can then write unit/mock tests with this interfaces. You can also create an integration tests from your anticorruption layer which will eventually call the database via the legacy dlls.</p>

