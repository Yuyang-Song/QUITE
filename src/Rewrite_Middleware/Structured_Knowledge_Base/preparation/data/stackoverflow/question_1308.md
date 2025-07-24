# EFcore Joining InMemory Table for duplication of entry
[Link to question](https://stackoverflow.com/questions/69725018/efcore-joining-inmemory-table-for-duplication-of-entry)
**Creation Date:** 1635258610
**Score:** 0
**Tags:** c#, linq, entity-framework-core
## Question Body
<p>Contrary to most questions about joining to an inmemory table in efcore, my objective is not to reduce the amount of records returned, but to actually increase it.</p>
<p>I have an object that has an <code>ins</code> and an <code>outs</code> property.</p>
<p>because of the project it is on, theses need to be in the same object. but in my case, I need to consider both of these properties as seperate entities. (kindof how you would use them in a pivot table in excel)</p>
<p>my immediate objective is to transform the <code>{ins:x, outs:y}</code> into two lines : <code>{type:'ins', value:x}</code> and <code>{type:'outs', value:y}</code></p>
<p>The reason I need them seperate is because I'm later joining on other table differently depending on the type.</p>
<p>in SQL, this is how I would do things :</p>
<pre><code>SELECT CASE WHEN t.type = 'ins' THEN d.ins ELSE d.outs END, t.type
FROM Data d
JOIN (VALUES ('ins'), ('outs')) as t (type) on 1=1;
</code></pre>
<p><code>(VALUES (1,0), (3,5)) as d (ins, outs)</code> instead of <code>Data d</code> can be used as an exemple.</p>
<p>I need to do that with linq in order to &quot;duplicate&quot; all lines (with specific data attached).</p>
<p>These lines are then used later to make other joins.</p>
<p>What I would have liked is something like that :</p>
<pre><code>var q = from d in data
        from type in new string[] {&quot;ins&quot;,&quot;outs&quot;}
        select new {type, value = (type == &quot;ins&quot; ? d.ins : d.outs)}
</code></pre>
<p>but it isn't valid.</p>
<p>the error I get with that is :</p>
<blockquote>
<p>The LINQ expression 'd =&gt; string[] { &quot;ins&quot;, &quot;outs&quot;, }' could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>creating the array outside doesn't change anything, the error stays the same (well, the expression in the error changes, but not the main message itself)</p>
<p>is there a way to do that ? or do I have no other choice than creating a dummy table in the database containing my <code>ins</code> and <code>outs</code> to have the join be possible directly (if that is the only choice, what would be the best way to add that ?)</p>

## Answers
### Answer ID: 69726438
<p>I would propose extension <a href="https://github.com/linq2db/linq2db.EntityFrameworkCore" rel="nofollow noreferrer">linq2db.EntityFrameworkCore</a> (disclaimer: I'm one of the creators).</p>
<p>Nothing in query should be changed, just add call <code>ToLinqToDB()</code>:</p>
<pre class="lang-cs prettyprint-override"><code>var q = from d in data
        from type in new string[] {&quot;ins&quot;,&quot;outs&quot;}
        select new {type, value = (type == &quot;ins&quot; ? d.ins : d.outs)};

q = q.ToLinqToDB();
</code></pre>
<p>It should create desired SQL.</p>

### Answer ID: 69725301
<p>Hi and welcome to StackOverflow community!</p>
<p>You are on the right way and you only need to correct a thing in your code:</p>
<p>The problem is that you haven't named the variable containing data in the anonymous type:</p>
<pre class="lang-cs prettyprint-override"><code>var q = from d in data
        from type in new string[] {&quot;ins&quot;,&quot;outs&quot;}
        select new {
           type, 
           datas = type == &quot;ins&quot; ? d.ins : d.outs 
        };
</code></pre>
<p>EDIT:</p>
<p>The error is saying that the creation of the string array cannot be translated into SQL language...</p>
<p>I thought that also 'Data' table was in-memory, but I think that you cannot join 'concrete' (db) tables with in-memory ones, so I suggest to force linq to load the data before joining calling ToList() to the db table (as the error suggests):</p>
<pre class="lang-cs prettyprint-override"><code>var q = from d in Data.Tolist()
        from type in new string[] {&quot;ins&quot;,&quot;outs&quot;}
        select new {
           type, 
           value = type == &quot;ins&quot; ? d.ins : d.outs 
        };
</code></pre>
<p>If loading the enitire table into memory is a problem you can create the &quot;ins/outs&quot; table inside the DB and join with it...</p>

