# LINQ to Entities query takes long to compile, SQL runs fast
[Link to question](https://stackoverflow.com/questions/10054856/linq-to-entities-query-takes-long-to-compile-sql-runs-fast)
**Creation Date:** 1333804880
**Score:** 6
**Tags:** c#, linq-to-entities, sql-server-2008-r2
## Question Body
<p>I'm working on a piece of code, written by a coworker, that interfaces with a CRM application our company uses. There are two LINQ to Entities queries in this piece of code that get executed many times in our application, and I've been asked to optimize them because one of them is really slow.</p>

<p>These are the queries:</p>

<p>First query, this one compiles pretty much instantly. It gets relation information from the CRM database, filtering by a list of relation IDs given by the application:</p>

<pre><code>from relation in context.ADRELATION
where ((relationIds.Contains(relation.FIDADRELATION)) &amp;&amp; (relation.FLDELETED != -1))
join addressTable in context.ADDRESS on relation.FIDADDRESS equals addressTable.FIDADDRESS
   into temporaryAddressTable
from address in temporaryAddressTable.DefaultIfEmpty()
join mailAddressTable in context.ADDRESS on relation.FIDMAILADDRESS equals
   mailAddressTable.FIDADDRESS into temporaryMailAddressTable
from mailAddress in temporaryMailAddressTable.DefaultIfEmpty()
select new { Relation = relation, Address = address, MailAddress = mailAddress };
</code></pre>

<p>The second query, which takes about 4-5 seconds to <strong>compile</strong>, and takes information about people from the database (again filtered by a list of IDs):</p>

<pre><code>from role in context.ROLE
join relationTable in context.ADRELATION on role.FIDADRELATION equals relationTable.FIDADRELATION into temporaryRelationTable
from relation in temporaryRelationTable.DefaultIfEmpty()
join personTable in context.PERSON on role.FIDPERS equals personTable.FIDPERS into temporaryPersonTable
from person in temporaryPersonTable.DefaultIfEmpty()
join nationalityTable in context.TBNATION on person.FIDTBNATION equals nationalityTable.FIDTBNATION into temporaryNationalities
from nationality in temporaryNationalities.DefaultIfEmpty()
join titelTable in context.TBTITLE on person.FIDTBTITLE equals titelTable.FIDTBTITLE into temporaryTitles
from title in temporaryTitles.DefaultIfEmpty()
join suffixTable in context.TBSUFFIX on person.FIDTBSUFFIX equals suffixTable.FIDTBSUFFIX into temporarySuffixes
from suffix in temporarySuffixes.DefaultIfEmpty()
where ((rolIds.Contains(role.FIDROLE)) &amp;&amp; (relation.FLDELETED != -1))
select new { Role = role, Person = person, relation = relation, Nationality = nationality, Title = title.FTXTBTITLE, Suffix = suffix.FTXTBSUFFIX };
</code></pre>

<p>I've set up the SQL Profiler and took the SQL from both queries, then ran it in SQL Server Management Studio. Both queries ran very fast, even with a large (~1000) number of IDs. So the problem seems to lie in the compilation of the LINQ query. </p>

<p>I have tried to use a compiled query, but since those can only contain primitive parameters, I had to strip out the part with the filter and apply that after the Invoke() call, so I'm not sure if that helps much. Also, since this code runs in a WCF service operation, I'm not sure if the compiled query will even still exist on subsequent calls.</p>

<p>Finally what I tried was to only select a single column in the second query. While this obviously won't give me the information I need, I figured it would be faster than the ~200 columns we're selecting now. No such case, it still took 4-5 seconds.</p>

<p>I'm not a LINQ guru at all, so I can barely follow this code (I have a feeling it's not written optimally, but can't put my finger on it). Could anyone give me a hint as to why this problem might be occurring?</p>

<p>The only solution I have left is to manually select all the information instead of joining all these tables. I'd then end up with about 5-6 queries. Not too bad I guess, but since I'm not dealing with horribly inefficient SQL here (or at least an acceptable level of inefficiency), I was hoping to prevent that.</p>

<p>Thanks in advance, hope I made things clear. If not, feel free to ask and I'll provide additional details.</p>

<hr>

<p><strong>Edit:</strong>
I ended up adding associations on my entity framework (the target database didn't have foreign keys specified) and rewriting the query thusly:</p>

<pre><code>context.ROLE.Where(role =&gt; rolIds.Contains(role.FIDROLE) &amp;&amp; role.Relation.FLDELETED != -1)
            .Select(role =&gt; new 
                            { 
                                ContactId = role.FIDROLE, 
                                Person = role.Person, 
                                Nationality = role.Person.Nationality.FTXTBNATION,
                                Title = role.Person.Title.FTXTBTITLE,
                                Suffix = role.Person.Suffix.FTXTBSUFFIX
                            });
</code></pre>

<p>Seems a lot more readable and it's faster too. </p>

<p>Thanks for the suggestions, I will definitely keep the one about making multiple compiled queries for different numbers of arguments in mind!</p>

## Answers
### Answer ID: 10057290
<p>Gabriels answer is correct: Use a compiled query.</p>

<p>It looks like you are compiling it again for every WCF request which of course defeats the purpose of one-time initialization. Instead, put the compiled query into a static field.</p>

<p>Edit:</p>

<p>Do this: Send maximum load to your service and pause the debugger 10 times. Look at the call stack. Did it stop more often in L2S code or in ADO.NET code? This will tell you if the problem is still with L2S or with SQL Server.</p>

<p>Next, let's fix the filter. We need to push it back into the compiled query. This is only possible by transforming this:</p>

<pre><code>rolIds.Contains(role.FIDROLE)
</code></pre>

<p>to this:</p>

<pre><code>role.FIDROLE == rolIds_0 || role.FIDROLE == rolIds_1 || ...
</code></pre>

<p>You need a new compiled query for every cardinality of rolIds. This is nasty, but it is necessary to get it to compile. In my project, I have automated this task but you can do a one-off solution here.</p>

<p>I guess most queries will have very few role-id's so you can materialize 10 compiled queries for cardinalities 1-10 and if the cardinality exceeds 10 you fall back to client-side filtering.</p>

### Answer ID: 10055725
<p>If you decide to keep the query inside the code, you could compile it. You still have to compile the query once when you run your app, but all subsequent call are gonna use that already compiled query. You can take a look at MSDN help here: <a href="http://msdn.microsoft.com/en-us/library/bb399335.aspx" rel="nofollow">http://msdn.microsoft.com/en-us/library/bb399335.aspx</a>.<br/>
<br/>
Another option would be to use a stored procedure and call the procedure from your code. Hence no compile time.</p>

