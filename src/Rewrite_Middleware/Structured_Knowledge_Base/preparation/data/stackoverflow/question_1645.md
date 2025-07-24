# data structure algorithms for database searching
[Link to question](https://stackoverflow.com/questions/2556567/data-structure-algorithms-for-database-searching)
**Creation Date:** 1270070534
**Score:** 0
**Tags:** algorithm, language-agnostic, search
## Question Body
<p>I was used to the traditional way of doing database searching with the following</p>

<ol>
<li>using wildcards for term searches</li>
<li>using where clause for specific data like addresses and names</li>
</ol>

<p>but at other times, I found these common methods to produce code that is so bloated, especially when it comes to complex searches. </p>

<p>Are there algorithms out there that you use for complex database searching? I tried to look for some but had a hard time doing so. I stumbled accross the binary search but I can't find a use for it :(</p>

<p><strong>EDIT</strong>: Here's a pseudocode of a search I was working on. It uses jquery range sliders for maximum and minimum searching</p>

<pre><code>query = 'select * from table'

if set minprice and not set maxprice
 if minprice = 'nomin'
  query += ' where price &lt; maxprice'
 else
  query += ' where price &lt; maxprice and price &lt; minprice'
if not set minprice and set maxprice
 if maxprice = 'nomax'
  query += ' where price &gt; minprice'
 else
  query += ' where price &gt; minprice and price &lt; maxprice'

if set maxprice and set minprice
 if maxprice = 'nomax'
  query += ' where price &gt; minprice'
 else
  query += ' where price &gt; minprice and price &lt; maxprice'
</code></pre>

<p>this may not be the codebase by which you base your answers. I'm looking for more elegant ways of doing database searching.</p>

<p><strong>EDIT</strong> by elegant I mean ways of rewriting the code to to achieve faster queries at less lines of code</p>

## Answers
### Answer ID: 2559514
<p>The major problem with your code is that it unnecessarily mulls over every possible combination of <code>set(minprice)</code> and <code>set(maxprice)</code>, while they can be treated independently:</p>

<pre><code>query = 'select * from table'
conditions = [] #array of strings representing conditions 
if set(minprice):
    conditions.append("price &lt; minprice")
if set(maxprice):
    conditions.append("price &gt; maxprice")
if len(conditions)&gt;0:
    query += ' WHERE ' + " and ".join(conditions)
</code></pre>

<p>In general it is beneficial to separate generation of conditions (the <code>if set(...)</code> lines above) from building the actual query. This way you don't need a separate <code>if</code> to generate (or skip) an <code>"AND"</code> or <code>"WHERE"</code> before each generated condition but instead you can just process it in one place (the last two lines above) adding the infixes as necessary.</p>

### Answer ID: 2556846
<p>try to focus on reorganizing your query building process.</p>

<p>query = select + ' where ' + filter1 + filter2</p>

<pre><code>select = 'select * from table'

filter1 = '';
if set minprice 
   if minprice = 'nomin'
      filter1 = price &gt; minprice'
   else
      filter1 = 'price &lt; minprice'
</code></pre>

<p>and so on ... 'til the building the full query :</p>

<pre><code>query = select;

if any filter on
   query += ' where '
   first = true

   if set filter 1
      if not first
         query += ' and '
      query += filter1
</code></pre>

<p>and so on... </p>

<p>you can put your filters in an array. it is more 'scalable' for your code.</p>

### Answer ID: 2556834
<p>When interfacing with a database, you're far better off with a complex and ugly query than with an 'elegant' query which has you duplicating database search functionality inside your application.  Each call to the database has a cost associated with it.  If you write code to search a database within your application, it's virtually guaranteed to be more expensive.</p>

<p>Unless you are actually writing a database (tall order), let the database do the searching.</p>

### Answer ID: 2556831
<p>Alright, I'm still not very clear on what you want, but I'll give it a shot...</p>

<p>If you're trying to speed up the query, you don't need to worry about "improved algorithms". Just make sure that any columns that you're searching on (<code>price</code> in your example) have an index on them, and the database will take care of searching efficiently. It's very good at it, I promise.</p>

<p>As for reducing the amount of code, again, I can't speak for every case, but your above pseudocode is bloated because you're handling the exact same case multiple times. My code for something like that would be more like this (pseudocode, no particular language):</p>

<pre><code>if (set(minprice) and minprice != 'nomin')
    conditions[] = 'price &gt; minprice'

if (set(maxprice) and maxprice != 'nomax')
    conditions[] = 'price &lt; maxprice'

query = 'select * from table'
if (notempty(conditions))
    query += ' where '+conditions.join(' and ')
</code></pre>

### Answer ID: 2556803
<p>Remeber speed of a query is not just the query itself.  Also, greatly depends on how the db is structured.  Is this a std relational layout, or a star, or?  Are your keys indexed, and do you have secondary indexes? Are you expecting to bring back a lot of data, or just a couple of rows?  Are you searching on columns where the db has to do a text search, or on numeric values.  And of course, on top of that, how is the db physically layed out?  index's and heavy hit tables on seperate drives?  and so forth.  Like the previous people mentioned, maybe a specific example would be more helpful in trying to solve</p>

