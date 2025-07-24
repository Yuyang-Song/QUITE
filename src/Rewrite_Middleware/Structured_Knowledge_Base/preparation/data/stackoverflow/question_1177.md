# .Net Core 3.1 Linq to Entities - How to concat strings in where clause
[Link to question](https://stackoverflow.com/questions/62207385/net-core-3-1-linq-to-entities-how-to-concat-strings-in-where-clause)
**Creation Date:** 1591325838
**Score:** 2
**Tags:** mysql, entity-framework, .net-core, linq-to-entities
## Question Body
<p>I have a user table with [FirstName] and [LastName] columns.
I'm trying to build a search function that returns users that meet one of the criteria below:</p>

<ul>
<li>FirstName == myPattern, or</li>
<li>LastName == myPattern, or</li>
<li>FirstName LastName == myPattern</li>
</ul>

<p>For example, if I have the following users in my database:</p>

<ul>
<li>Jack One</li>
<li>Jack Two</li>
<li>Jack Three</li>
</ul>

<p>I'd like the function to return all of them when the input is <strong>Jack</strong>, but only return Jack One when the input is <strong>Jack One</strong></p>

<p>I currently have the following code:</p>

<pre><code>var users = context.User.Where(x =&gt; x.FirstName == pattern 
            || x.LastName == pattern
            || x.FirstName + " " + x.LastName == pattern)

</code></pre>

<p>But this does not work as the it gets translated to the following query in MySQL</p>

<pre><code>...WHERE (`p`.`firstName` = 'Jack One') OR (`p`.`lastName` = 'Jack One')) OR (((`p`.`firstName` + ' ') + `p`.`lastName`) = 'Jack One')
</code></pre>

<p>It does not work because I believe we need to use CONCAT(firstName, ' ', lastName) if I want to concat multiple strings in MySQL.</p>

<p>I tried using the following .NET functions but they cannot be translated to sql (The LINQ expression ... could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to either AsEnumerable(), AsAsyncEnumerable(), ToList(), or ToListAsync())</p>

<ul>
<li>string.Join(' ', firstName, lastName)</li>
<li>string.Concat(firstName, " ", lastName)</li>
</ul>

<p>How can I achieve this in .NET CORE 3.1 <strong>without</strong> pulling all data into memory and evaluating it in client?</p>

<p>Thanks</p>

## Answers
### Answer ID: 63276630
<p>It seems a bug of MySql.Data.EntityFrameworkCore.</p>
<p>I use <a href="https://github.com/PomeloFoundation/Pomelo.EntityFrameworkCore.MySql" rel="nofollow noreferrer">Pomelo.EntityFrameworkCore.MySql</a> instead to solve the problem.</p>

### Answer ID: 62207954
<p>This looks like an case of Linq translating the query in a manner you aren't predicting. </p>

<p>Going from memory and no IDE on hand to check it, but give this a shot. If you split the full name on the space first, you can use the values in your query. </p>

<pre class="lang-cs prettyprint-override"><code>// returns an array based on the patter, if it can be split
var names = pattern.Split(" ");

// then use the array elements in the query
var users = context.User.Where(x =&gt; x.FirstName == pattern 
    || x.LastName == pattern
    || (x.FirstName == names[0] &amp;&amp; x.LastName == names[1]));
</code></pre>

<p>The last OR condition of the query should then evaulate the 2 new elements in the names array, that was created off the pattern </p>

