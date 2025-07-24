# Find the first free id
[Link to question](https://stackoverflow.com/questions/54842771/find-the-first-free-id)
**Creation Date:** 1550933145
**Score:** 1
**Tags:** c#, sql, linq
## Question Body
<p>One of my small database management projects (written in delphi) used sql queries to find the first free id of mysql table.</p>

<p>Example: I have to find the first free id (hole) in a table like this:</p>

<pre class="lang-none prettyprint-override"><code>| id   | Col1 |
|------|------|
| 5101 | ABC  |
| 5102 | BCD  |
| 5103 | CDE  |
| 5105 | EFG  | 🡔 first missing id
| 5106 | GHI  |
| 5108 | ILM  |
</code></pre>

<p>The code should find the first free id <code>5104</code> </p>

<p>Here's how I'd do it in SQL (in old project): </p>

<pre class="lang-sql prettyprint-override"><code>SELECT
  MIN((doc.id + 1)) AS nextID
FROM (doc
  LEFT JOIN doc doc1
    ON (((doc.id + 1) = doc1.id)))
WHERE (ISNULL(doc1.id) AND (doc.id &gt; 5000))
</code></pre>

<p>Now, which I am rewriting in c # language, I need to convert sql statements into a LINQ query (which uses Devart dotConnect for mysql Entity Framework).
Starting from here:</p>

<pre><code>DC db = new DC();
var nums = db.Documentos.OrderBy(x =&gt; x.Id);
</code></pre>

## Answers
### Answer ID: 54844018
<p>Another method (similar to what you're using now).<br>
Assume you have an array of integers (or another type of collection) like this:  </p>

<pre><code>var myIDs = new int[] { 5101, 5113, 5102, 5103, 5110, 5104, 5105, 5116, 5106, 5107, 5108, 5112, 5114, 5115 };
</code></pre>

<p>If it's not already ordered, the <code>OrderBy()</code> it:</p>

<pre><code>myIDs = myIDs.OrderBy(n =&gt; n).ToArray();
</code></pre>

<p>Extract the first number that is less than <code>(next number) + 1</code>:  </p>

<pre><code>int result = myIDs.Where((n, i) =&gt; (i &lt; myIDs.Length - 1) &amp;&amp; (n + 1 &lt; myIDs[i + 1])).FirstOrDefault();
</code></pre>

<p>If none of the members of this collection satisfy the condition, take the last one and add <code>1</code>:  </p>

<pre><code>result = result == default ? myIDs.Last() + 1 : result;
</code></pre>

### Answer ID: 54843282
<p>This can give you all gaps within your table</p>

<pre><code>var nums= (new List&lt;int&gt; (){1,2,3,25,4,5,6,7,8, 12, 15,21,22,23}).AsQueryable();

nums
  .OrderBy(x =&gt; x)
  .GroupJoin(nums, n=&gt; n + 1, ni =&gt; ni, (o,i)=&gt; new {o, i})
  .Where(t=&gt; !(t.i is IGrouping&lt;int, int&gt;))
  .Dump();
</code></pre>

<p><a href="https://dotnetfiddle.net/rJphil" rel="nofollow noreferrer">.Net Fiddle</a></p>

### Answer ID: 54843187
<p>From <a href="https://stackoverflow.com/q/4270321/1366033">Can LINQ be used to find gaps in a sorted list?</a>: </p>

<pre><code>var strings = new string[] { "7", "13", "8", "12", "10", "11", "14" };
var list = strings.OrderBy(s =&gt; int.Parse(s));
var result = Enumerable.Range(list.Min(), list.Count).Except(list).First(); // 9
</code></pre>

<p>Basically, order the list.  Then create an array of sequential numbers (<code>1,2,3...</code>) from the minimum all the way to the max.  Check for missing values in the list, and grab the first one.  That's the first missing number.</p>

