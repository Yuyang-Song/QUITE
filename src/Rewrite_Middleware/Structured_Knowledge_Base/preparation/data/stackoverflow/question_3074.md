# CPU Spikes / Wait time for ASP.NET Core application
[Link to question](https://stackoverflow.com/questions/65291272/cpu-spikes-wait-time-for-asp-net-core-application)
**Creation Date:** 1607958098
**Score:** 8
**Tags:** c#, .net, azure, asp.net-core, azure-web-app-service
## Question Body
<p>The issue is that CPU is regularly spiking from ~10% up to more than 70%:</p>
<p><a href="https://i.sstatic.net/PyUaT.png" rel="noreferrer"><img src="https://i.sstatic.net/PyUaT.png" alt="Application CPU percentage" /></a></p>
<p>Unfortunately, this seems to have an impact to the average response time, causing some spikes there as well.</p>
<p><a href="https://i.sstatic.net/3q71A.png" rel="noreferrer"><img src="https://i.sstatic.net/3q71A.png" alt="Average response time" /></a></p>
<p>This is a happy scenario, where the average stays under 1s, but sometimes it can perform quite badly.</p>
<p>I have tried to investigate this issue from the Azure Portal and I have noticed that some requests stay in this block, leaving me to think it was a query issue (it is not exactly a stack trace here from what I can see, there can be more than one query happening inside <code>GetValidFunction()</code> via another service which is not displayed here).</p>
<p><a href="https://i.sstatic.net/9xvS0.png" rel="noreferrer"><img src="https://i.sstatic.net/9xvS0.png" alt="waiting block 1" /></a></p>
<p>If this is the case, I have no problem rewriting the queries inside, since they are done via LINQ with EF, but then I noticed something strange. Notice that in this request the waiting is being done for <code>Framework/Library CEEJitInfo::allocMem</code></p>
<p><a href="https://i.sstatic.net/ScA90.png" rel="noreferrer"><img src="https://i.sstatic.net/ScA90.png" alt="waiting block 2" /></a></p>
<p>For another request, the Waiting block was happening for a <code>REDIS</code> query. But most of the time, it seems that the call is blocked inside the <code>GetResults()</code> like in the third picture. Could all these waiting times be related only to database queries? (DTU there is also spiking but this is another issue I have to fix - probably due to the poor design, lot of tables with GUID as PK / FK - index rebuilds maybe? but this is to be addressed another time)</p>
<p>To give some context to this application:</p>
<ul>
<li>Web API running on .NET 5</li>
<li>Allows users to create their own razor templates</li>
<li>Templates are stored in a SQL Server database</li>
<li>Templates are queried and then compiled and rendered at runtime</li>
</ul>
<p>Another possible cause I have in mind is the large number of compiled razor templates. There can be hundreds of these views or even more than a thousand. I am thinking something about view cache invalidation which the framework is doing internally, forcing the view to be recompiled?</p>
<p>This may be a little bit off topic from the initial question, but does someone know how razor runtime compilation works exactly in ASP.NET Core?</p>
<p>Specifically:</p>
<ul>
<li>How long are these views held in cache?</li>
<li>Is it creating a DLL for each view like it did in .NET Framework or are they held only in memory?</li>
</ul>
<p>I tried looking for answers to these two questions but could not found any.</p>
<p>All in all, I would appreciate enormously if you have some recommendations to the CPU spikes / Waiting time issue. Do you know any possible reason that could cause the waiting time beside the query itself? Can it be related to the view recompilation / Garbage collector ?</p>
<p>Thank you for your time.</p>
<hr />
<p>Later edit:
The code executed looks similar to this</p>
<p><code>Controller-&gt; GET ExecuteFunction(functionCode) -&gt; ValidateFunction(functionCode) -&gt; GetValidFunction(functionCode)</code></p>
<p><code>ValidateFunction</code> is also performing other queries, but after <code>GetValidFunction</code>.</p>
<pre><code>private (string, Functions) GetValidFunction(Guid functionCode)
{
    var cacheKey = CacheKeys.FunctionError(functionCode);
    var cacheTimeSpan = new TimeSpan(0, cacheValidationMinutes, 0);
    var validationErrorMessage = cacheProvider.GetWithSlidingExpiration&lt;string&gt;(cacheKey, cacheTimeSpan);
    var function = functionLogic.GetValidFunctionByCode(functionCode);
    if (function == null)
    {
        cacheProvider.AddToCacheInvariantCase(cacheKey, invalidErrorCode, cacheTimeSpan);
        return (invalidErrorCode, null);
    }
    if (string.isNullOrEmpty(validationErrorMessage)) return (validationErrorMessage, function);
    var functionCodeData = functionCodeLogic.GetFunctionCode(functionCode);
    if (functionCodeData == null)
    {
        cacheProvider.AddToCacheInvariantCase(cacheKey, invalidErrorCode, cacheTimeSpan);
        return (invalidErrorCode, null);
    }
    if (function.StatusId == (int)FunctionStatusName.Active || function.StatusId == (int)FunctionStatusName.Draft)
    {
        cacheProvider.AddToCacheInvariantCase(cacheKey, NoErrorFunction, cacheTimeSpan);
    }

    return (null, function);
}
</code></pre>
<p>The queries inside <code>GetValidFunction</code> will execute this logic</p>
<pre><code>   public T Get(Expression&lt;Func&lt;T, bool&gt;&gt; where)
    {
        return dbset.Where(where).FirstOrDefault();
    }
</code></pre>

## Answers
### Answer ID: 65335660
<p><del>Though you have not shared relevant piece of code, but from the description and symptoms,</del> it seems to be result of synchronous (blocking) I/O done somewhere in your code causing thread contention.</p>
<p>UPDATE:
In your shared code, I see sync I/O call for example in <code>GetValidFunction</code> and <code>Get</code> method. Should be like below and caller should await. <strong>Remember, <a href="https://learn.microsoft.com/en-us/archive/msdn-magazine/2013/march/async-await-best-practices-in-asynchronous-programming" rel="noreferrer"><code>async</code> all the way</a></strong>.</p>
<pre class="lang-cs prettyprint-override"><code>public Task&lt;T&gt; GetAsync(Expression&lt;Func&lt;T, bool&gt;&gt; where)
    {
        return dbset.Where(where).FirstOrDefaultAsync();
    }
</code></pre>
<hr />
<p>Below would be very generic answer to this problem mostly sourced from <a href="https://learn.microsoft.com/azure/architecture/antipatterns/synchronous-io/" rel="noreferrer">Synchronous I/O antipattern</a>. <strong>Some of the reference of old asp.net app and old cloud service below might be outdated today, but the concept is still relevant</strong>.</p>
<h1>Synchronous I/O antipattern</h1>
<p>Blocking the calling thread while I/O completes can reduce performance and affect vertical scalability.</p>
<h2>Problem description</h2>
<p>A synchronous I/O operation blocks the calling thread while the I/O completes. The calling thread enters a wait state and is unable to perform useful work during this interval, wasting processing resources.</p>
<p>Common examples of I/O include:</p>
<ul>
<li>Retrieving or persisting data to a database or any type of persistent storage.</li>
<li>Sending a request to a web service.</li>
<li>Posting a message or retrieving a message from a queue.</li>
<li>Writing to or reading from a local file.</li>
</ul>
<p>This antipattern typically occurs because:</p>
<ul>
<li>It appears to be the most intuitive way to perform an operation.</li>
<li>The application requires a response from a request.</li>
<li>The application uses a library that only provides synchronous methods for I/O.</li>
<li>An external library performs synchronous I/O operations internally. A single synchronous I/O call can block an entire call chain.</li>
</ul>
<p>The following code uploads a file to Azure blob storage. There are two places where the code blocks waiting for synchronous I/O, the <code>CreateIfNotExists</code> method and the <code>UploadFromStream</code> method.</p>
<pre class="lang-cs prettyprint-override"><code>var blobClient = storageAccount.CreateCloudBlobClient();
var container = blobClient.GetContainerReference(&quot;uploadedfiles&quot;);

container.CreateIfNotExists();
var blockBlob = container.GetBlockBlobReference(&quot;myblob&quot;);

// Create or overwrite the &quot;myblob&quot; blob with contents from a local file.
using (var fileStream = File.OpenRead(HostingEnvironment.MapPath(&quot;~/FileToUpload.txt&quot;)))
{
    blockBlob.UploadFromStream(fileStream);
}
</code></pre>
<p>Here's an example of waiting for a response from an external service. The <code>GetUserProfile</code> method calls a remote service that returns a <code>UserProfile</code>.</p>
<pre class="lang-cs prettyprint-override"><code>public interface IUserProfileService
{
    UserProfile GetUserProfile();
}

public class SyncController : ApiController
{
    private readonly IUserProfileService _userProfileService;

    public SyncController()
    {
        _userProfileService = new FakeUserProfileService();
    }

    // This is a synchronous method that calls the synchronous GetUserProfile method.
    public UserProfile GetUserProfile()
    {
        return _userProfileService.GetUserProfile();
    }
}
</code></pre>
<p>You can find the complete code for both of these examples <a href="https://github.com/mspnp/performance-optimization/tree/master/SynchronousIO" rel="noreferrer">here</a>.</p>
<h2>How to fix the problem</h2>
<p>Replace synchronous I/O operations with asynchronous operations. This frees the current thread to continue performing meaningful work rather than blocking, and helps improve the utilization of compute resources. Performing I/O asynchronously is particularly efficient for handling an unexpected surge in requests from client applications.</p>
<p>Many libraries provide both synchronous and asynchronous versions of methods. Whenever possible, use the asynchronous versions. Here is the asynchronous version of the previous example that uploads a file to Azure blob storage.</p>
<pre class="lang-cs prettyprint-override"><code>var blobClient = storageAccount.CreateCloudBlobClient();
var container = blobClient.GetContainerReference(&quot;uploadedfiles&quot;);

await container.CreateIfNotExistsAsync();

var blockBlob = container.GetBlockBlobReference(&quot;myblob&quot;);

// Create or overwrite the &quot;myblob&quot; blob with contents from a local file.
using (var fileStream = File.OpenRead(HostingEnvironment.MapPath(&quot;~/FileToUpload.txt&quot;)))
{
    await blockBlob.UploadFromStreamAsync(fileStream);
}
</code></pre>
<p>The <code>await</code> operator returns control to the calling environment while the asynchronous operation is performed. The code after this statement acts as a continuation that runs when the asynchronous operation has completed.</p>
<p>A well designed service should also provide asynchronous operations. Here is an asynchronous version of the web service that returns user profiles. The <code>GetUserProfileAsync</code> method depends on having an asynchronous version of the User Profile service.</p>
<pre class="lang-cs prettyprint-override"><code>public interface IUserProfileService
{
    Task&lt;UserProfile&gt; GetUserProfileAsync();
}

public class AsyncController : ApiController
{
    private readonly IUserProfileService _userProfileService;

    public AsyncController()
    {
        _userProfileService = new FakeUserProfileService();
    }

    // This is an synchronous method that calls the Task based GetUserProfileAsync method.
    public Task&lt;UserProfile&gt; GetUserProfileAsync()
    {
        return _userProfileService.GetUserProfileAsync();
    }
}
</code></pre>
<p>For libraries that don't provide asynchronous versions of operations, it may be possible to create asynchronous wrappers around selected synchronous methods. Follow this approach with caution. While it may improve responsiveness on the thread that invokes the asynchronous wrapper, it actually consumes more resources. An extra thread may be created, and there is overhead associated with synchronizing the work done by this thread. Some tradeoffs are discussed in this blog post: <a href="https://blogs.msdn.microsoft.com/pfxteam/2012/03/24/should-i-expose-asynchronous-wrappers-for-synchronous-methods" rel="noreferrer">Should I expose asynchronous wrappers for synchronous methods?</a></p>
<p>Here is an example of an asynchronous wrapper around a synchronous method.</p>
<pre class="lang-cs prettyprint-override"><code>// Asynchronous wrapper around synchronous library method
private async Task&lt;int&gt; LibraryIOOperationAsync()
{
    return await Task.Run(() =&gt; LibraryIOOperation());
}
</code></pre>
<p>Now the calling code can await on the wrapper:</p>
<pre class="lang-cs prettyprint-override"><code>// Invoke the asynchronous wrapper using a task
await LibraryIOOperationAsync();
</code></pre>
<h2>Considerations</h2>
<ul>
<li><p>I/O operations that are expected to be very short lived and are unlikely to cause contention might be more performant as synchronous operations. An example might be reading small files on an SSD drive. The overhead of dispatching a task to another thread, and synchronizing with that thread when the task completes, might outweigh the benefits of asynchronous I/O. However, these cases are relatively rare, and most I/O operations should be done asynchronously.</p>
</li>
<li><p>Improving I/O performance may cause other parts of the system to become bottlenecks. For example, unblocking threads might result in a higher volume of concurrent requests to shared resources, leading in turn to resource starvation or throttling. If that becomes a problem, you might need to scale out the number of web servers or partition data stores to reduce contention.</p>
</li>
</ul>
<h2>How to detect the problem</h2>
<p>For users, the application may seem unresponsive periodically. The application might fail with timeout exceptions. These failures could also return HTTP 500 (Internal Server) errors. On the server, incoming client requests might be blocked until a thread becomes available, resulting in excessive request queue lengths, manifested as HTTP 503 (Service Unavailable) errors.</p>
<p>You can perform the following steps to help identify the problem:</p>
<ol>
<li><p>Monitor the production system and determine whether blocked worker threads are constraining throughput.</p>
</li>
<li><p>If requests are being blocked due to lack of threads, review the application to determine which operations may be performing I/O synchronously.</p>
</li>
<li><p>Perform controlled load testing of each operation that is performing synchronous I/O, to find out whether those operations are affecting system performance.</p>
</li>
</ol>
<h2>Example diagnosis</h2>
<p>The following sections apply these steps to the sample application described earlier.</p>
<h3>Monitor web server performance</h3>
<p>For Azure web applications and web roles, it's worth monitoring the performance of the IIS web server. In particular, pay attention to the request queue length to establish whether requests are being blocked waiting for available threads during periods of high activity. You can gather this information by enabling Azure diagnostics. For more information, see:</p>
<ul>
<li><a href="https://learn.microsoft.com/azure/app-service/web-sites-monitor" rel="noreferrer">Monitor Apps in Azure App Service</a></li>
<li><a href="https://learn.microsoft.com/azure/cloud-services/diagnostics-performance-counters" rel="noreferrer">Create and use performance counters in an Azure application</a></li>
</ul>
<p>Instrument the application to see how requests are handled once they have been accepted. Tracing the flow of a request can help to identify whether it is performing slow-running calls and blocking the current thread. Thread profiling can also highlight requests that are being blocked.</p>
<h3>Load test the application</h3>
<p>The following graph shows the performance of the synchronous <code>GetUserProfile</code> method shown earlier, under varying loads of up to 4000 concurrent users. The application is an ASP.NET application running in an Azure Cloud Service web role.</p>
<p><img src="https://learn.microsoft.com/azure/architecture/antipatterns/synchronous-io/_images/syncperformance.jpg" alt="Performance chart for the sample application performing synchronous I/O operations" /></p>
<p>The synchronous operation is hard-coded to sleep for 2 seconds, to simulate synchronous I/O, so the minimum response time is slightly over 2 seconds. When the load reaches approximately 2500 concurrent users, the average response time reaches a plateau, although the volume of requests per second continues to increase. Note that the scale for these two measures is logarithmic. The number of requests per second doubles between this point and the end of the test.</p>
<p>In isolation, it's not necessarily clear from this test whether the synchronous I/O is a problem. Under heavier load, the application may reach a tipping point where the web server can no longer process requests in a timely manner, causing client applications to receive time-out exceptions.</p>
<p>Incoming requests are queued by the IIS web server and handed to a thread running in the ASP.NET thread pool. Because each operation performs I/O synchronously, the thread is blocked until the operation completes. As the workload increases, eventually all of the ASP.NET threads in the thread pool are allocated and blocked. At that point, any further incoming requests must wait in the queue for an available thread. As the queue length grows, requests start to time out.</p>
<h3>Implement the solution and verify the result</h3>
<p>The next graph shows the results from load testing the asynchronous version of the code.</p>
<p><img src="https://learn.microsoft.com/azure/architecture/antipatterns/synchronous-io/_images/asyncperformance.jpg" alt="Performance chart for the sample application performing asynchronous I/O operations" /></p>
<p>Throughput is far higher. Over the same duration as the previous test, the system successfully handles a nearly tenfold increase in throughput, as measured in requests per second. Moreover, the average response time is relatively constant and remains approximately 25 times smaller than the previous test.</p>

