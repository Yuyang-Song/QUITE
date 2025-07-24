# Does WCF suppress first-chance exceptions?
[Link to question](https://stackoverflow.com/questions/261539/does-wcf-suppress-first-chance-exceptions)
**Creation Date:** 1225796907
**Score:** 2
**Tags:** c#, linq, wcf, exception
## Question Body
<p>I've got a WCF service that uses a LinqToSql DataContext to fetch some information out of a database. The return type of the operation is IEnumerable<code>&lt;DomainObject</code>>, and I have a helper method that converts from the Table-derived LINQ object to a WCF data contract like so:</p>

<pre><code>[OperationContract]
public IEnumerable&lt;DomainObjectDTO&gt; RetrieveDomainObjects()
{
    var context = CreateDataContext();
    return from domainObject in context.DomainObjects
           select ConvertDomainObject(domainObject);
}

private DomainObjectDTO ConvertDomainObject(DomainObject obj)
{
    // etc...
}
</code></pre>

<p>This code exhibits a strange behaviour if I pass an invalid connection string to the DataContext. Being unable to find the correct database, presumably the above code throws a SqlException when enumerating the IEnumerable<code>&lt;DomainObjectDTO</code>> when serialization is happening. However, when I run this code in my debugger, I see no first-chance exception on the server side at all! I told the debugger in the Exceptions tab to break on all thrown CLR exceptions, and it simply doesn't. I also don't see the characteristic "First chance exception" message in the Output window.</p>

<p>On the client side, I get a CommunicationException with an error message along the lines of "The socket connection terminated unexpectedly". None of the inner exceptions provides any hint as to the underlying cause of the problem.</p>

<p>The only way I could figure this out was to rewrite the LINQ code in such a way that the query expression is evaluated inside of the OperationContract method. Incidentally, I get the same result if there is a permissions problem, or if I wrap the DataContext in a using statement, so this is not just isolated to SqlExceptions.</p>

<p>Disregarding the inadvisability of making the return type an IEnumerable<code>&lt;T</code>> and only enumerating the query somewhere in the depths of the serializer, is WCF suppressing or somehow preventing exceptions from being thrown in this case? And if so, why?</p>

## Answers
### Answer ID: 4799428
<blockquote>
  <p>is WCF suppressing or somehow preventing exceptions from being thrown in this case? And if so, why?</p>
</blockquote>

<p>I don't know much about WCF but it doesn't sound very likely to me.</p>

<p>The special thing about first-chance exception is that it goes directly to the debugger and the debugger gets the chance to see it <em>before</em> the exception is actually raised - hence the words 'first chance' - the debugger has the 'first chance' to handle the exception. How could anything bypass it? It would have to be some way of stopping the exception being raised completely. (Is there security or reliability features in CLR that can do this?).</p>

<p>The best alternative explanation I can propose is that something goes wrong in advance of the point where you expect the SqlException to be thrown. I would try also looking at unmanaged exceptions, not just managed exceptions, in case it is a case of e.g. something goes wrong in unmanaged serialization code trying to use the managed IEnumerable, or some CLR bug...</p>

### Answer ID: 262335
<p>Try putting the following in the App.config for your client and service:</p>

<pre><code>&lt;system.diagnostics&gt;
&lt;sources&gt;
    &lt;source name="System.ServiceModel" switchValue="Verbose,ActivityTracing"
        propagateActivity="true"&gt;
        &lt;listeners&gt;
            &lt;add type="System.Diagnostics.DefaultTraceListener" name="Default"&gt;
                &lt;filter type="" /&gt;
            &lt;/add&gt;
            &lt;add name="NewListener"&gt;
                &lt;filter type="" /&gt;
            &lt;/add&gt;
        &lt;/listeners&gt;
    &lt;/source&gt;
&lt;/sources&gt;
&lt;sharedListeners&gt;
    &lt;add initializeData="C:\App_tracelog.svclog"
        type="System.Diagnostics.XmlWriterTraceListener, System, Version=2.0.0.0, Culture=neutral, PublicKeyToken=b77a5c561934e089"
        name="NewListener" traceOutputOptions="LogicalOperationStack, DateTime, Timestamp, ProcessId, ThreadId, Callstack"&gt;
        &lt;filter type="" /&gt;
    &lt;/add&gt;
&lt;/sharedListeners&gt;
</code></pre>

<p>
Then load both the resulting log files in the Service Trace Viewer that comes with the Windows SDK.  You will be able to see the actual exception thrown that way.</p>

<p>Links: <a href="http://msdn.microsoft.com/en-us/library/aa751795.aspx" rel="nofollow noreferrer">http://msdn.microsoft.com/en-us/library/aa751795.aspx</a> </p>

### Answer ID: 261587
<p>WCF does seem, at least in my experience, to do some magic with exceptions. I'm really not sure what it does with exceptions but I've found that if the FaultContract attribute is used to specify exceptions that the contract could throw, it'll at least give a bit more information to the client about the why the error occurred.</p>

<p>We would also catch any exceptions and re throw them as FaultExceptions, something like:</p>

<pre><code>try
{
    DoSomething();
}
catch ( Exception ex )
{ 
   throw new FaultException&lt;CustomException&gt;( new CustomException( ex ), ex.Message );
}
</code></pre>

<p>Where custom exception is specified in the fault contract. This seems to give a bit more information to the client about the exception. So I suspect if you add SQLException as part of the FaultContract then it'll get sent to the client.</p>

### Answer ID: 261556
<p>WCF is a curious beast that lives slightly outside of regular IIS; it may be that the standard debugging gets glitchy. However, you could try <a href="http://msdn.microsoft.com/en-us/library/system.servicemodel.description.servicedebugbehavior.includeexceptiondetailinfaults.aspx" rel="nofollow noreferrer">enabling debug exceptions</a>, and/or implementing (and configuring) your own <a href="http://msdn.microsoft.com/en-us/library/system.servicemodel.dispatcher.ierrorhandler.aspx" rel="nofollow noreferrer"><code>IErrorHandler</code></a> to log the issues.</p>

<p>Another option: is there perhaps an iterator block (<code>yield return</code>) somewhere in the mix here? <em>Nothing</em> in an iterator block is evaluated until the enumerator is iterated, which can lead to some odd looking issues with data that should have been validated earlier. In the case above, this isn't an issue (no <code>yield return</code>), but it is one to watch.</p>

<p>For example, the following is <em>very</em> different:</p>

<pre><code>var context = CreateDataContext();
var query = from domainObject in context.DomainObjects
       select ConvertDomainObject(domainObject);
foreach(var item in query) { yield return item; }
</code></pre>

### Answer ID: 261555
<p>Did you configure your "<a href="http://msdn.microsoft.com/en-us/library/system.servicemodel.description.servicedebugbehavior.includeexceptiondetailinfaults.aspx" rel="nofollow noreferrer">IncludeExceptionDetailInFaults</a>" settings? (it defaults to 'false' for security purposes).</p>

