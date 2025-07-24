# Rewriting LINQ to SQL
[Link to question](https://stackoverflow.com/questions/53861125/rewriting-linq-to-sql)
**Creation Date:** 1545267240
**Score:** 1
**Tags:** c#, entity-framework, linq, t-sql
## Question Body
<p>I have a LINQ query that I need to rewrite in TSQL to understand why it's pulling duplicate data. However, I'm not able to actually run the code so I have to do it by just looking at the LINQ.</p>

<p>Since you can use JOIN in LINQ, I'm not sure what's going on with these 2 FROMs.</p>

<p>When I try to write a query to pull this data, I am not getting any duplicates -- yet when the code runs, it is failing on a SingleOrDefault call for duplicate data.</p>

<pre><code>var myQ = from T in context.TableModels
          .Where(T =&gt; T.ID == 'ID')
        from C in context.ChairModels
         .Where(C =&gt; C.TableID == T.ID &amp;&amp; C.TableKey == T.TableKey)
       .DefaultIfEmpty()
    select new
     {
       ...
      };
</code></pre>

<p>SingleOrDefault is called elsewhere and uses a key to select the 1 record. The database only has this key 1 time, yet SingleOrDEfault is failing for there being more than 1 item returned.</p>

## Answers
### Answer ID: 53861181
<p><code>SingleOrDefault()</code> has nothing to do with duplicate data. It's purpose is to get the <em>only</em> result of a query, and it throws an exception of it gets more than one row (duplicate or not).</p>

<p>Remember that when you do a join, if there are two matching records in the joined table, you will get multiple rows back with the data from the primary table duplicated. So in this case, there could be more than one row in the ChairModels table where <code>C.TableID == T.ID &amp;&amp; C.TableKey == T.TableKey</code>.</p>

<p>If you want to see the resulting SQL, see <a href="https://stackoverflow.com/a/20751723/1202807">here</a> for a way to output the SQL to the debug window in Visual Studio. </p>

