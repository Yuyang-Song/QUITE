# Link tables issue for Compiled Access (mde) file
[Link to question](https://stackoverflow.com/questions/794330/link-tables-issue-for-compiled-access-mde-file)
**Creation Date:** 1240850572
**Score:** 0
**Tags:** sql-server, vba, ms-access
## Question Body
<p>I have an old compiled Access Application <code>mde</code> file. This application has linked tables to network shared folder. I tried to upgrade main database using upsizing wizard on main database and everything went well. Then when the application starts it gives error message that</p>

<blockquote>
  <p>Microsoft jet database engine cannot find the input table or query table</p>
</blockquote>

<p>I have checked the shared mdb file it has exact table names and everything.
Then I called the guy who developed this application. He said I have to rewrite the application to not use Jet engine...</p>

<p>What does Jet Engine has to do with linking tables? Do I really have to rewrite the whole application to use ADO?</p>

## Answers
### Answer ID: 795092
<p>You did change Access database version?
It is possible that your mdb was linked with old version of Jet drivers and these drivers cannot connect to newer mdb version.</p>

### Answer ID: 795029
<p>Many questions:</p>

<ol>
<li><p>do you have the source MDB file? I can't recall if creating an MDE fails if the linked tables are not correctly connected. In any event, should you end up needing to alter the app, you're going to need the source MDB file.</p></li>
<li><p>the error message you report should give the name of the missing table.</p></li>
<li><p>do you know when the error is being reported? There could be any number of places where simply replacing tables linked to a Jet MDB back end with ODBC links to a server will not fix things. For instance, should there be any saved queries or SQL in code that bypasses linked tables and uses a direct connection string, that could produce an error like you see.</p></li>
<li><p>in regard to the developer's response that "I have to rewrite the application to not use Jet engine..." either you misunderstood what he said, or your developer is completely incompetent. Or both, I guess. Jet works very well with ODBC linked tables and if you're using an MDB front end, it is impossible to completely eliminate Jet, as the MDB is a Jet data file. The desire to eliminate Jet mostly comes from people who can't be bothered to learn how to use it properly.</p></li>
</ol>

<p>It sounds to me as though you're getting an unhandled errror but insufficient information on what's producing it. You need the actual MDB to troubleshoot it, as the code isn't there to display in the MDE so there's no way to figure out what the actual source of the problem is. If your developer won't give you the MDB, then you need to check the contract under which the app was developed -- if you agreed to letting him control the source code, you're basically at his mercy and should fire whoever signed off on that. For what it's worth, when I deliver an MDE to a client, they also get the full MDB. They generally don't do anything with it, but should I no longer be available to do further development work, they've got the source code that they can give to whomever they want.</p>

<p>Last of all, I think it's very unlikely that even if you get your app working, a mere upsizing is going to offer much in terms of performance or stability. It is true that very often, 90% or more of an upsized app will work without alteration, but the other 10% can be very problematic. Often you need to move certain operations server-side to get the efficiency a server back end offers. This means your front end app needs to be re-architected to work better with your upsized back end. The degree to which this is true will differ from app to app, but it's very seldom that absolutely everything works without revision.</p>

