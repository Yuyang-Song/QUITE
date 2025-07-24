# What is wrong with OrderBy Linq Extension in EF4?
[Link to question](https://stackoverflow.com/questions/4470295/what-is-wrong-with-orderby-linq-extension-in-ef4)
**Creation Date:** 1292587661
**Score:** 0
**Tags:** .net-4.0, entity-framework-4, linq-to-entities
## Question Body
<p>I have following two calls, both are same but results are different...</p>

<p>It is simple console application with connection to local database.</p>

<pre><code>DBContext db = new DBContext();
</code></pre>

<p>This one sorts as expected, </p>

<pre><code>var q = from x in db.Cities
        orderby x.CountryCode, x.City
        select x;

foreach(var x in q){
   Console.WriteLine("{0}:{1}",x.CountryCode, x.City);
}
</code></pre>

<p>But why this one does not sort by City, it only sorts by CountryCode</p>

<pre><code>foreach(var x in db.Cities.OrderBy(d=&gt;d.City).OrderBy(d=&gt;d.CountryCode)){
   Console.WriteLine("{0}:{1}",x.CountryCode, x.City);
}
</code></pre>

<p>If I change order of OrderBy statements, then only Last OrderBy seem to work correctly but intermediate OrderBy has no impact at all. Is this bug in EF or Linq extensions?</p>

<p>I have no problem in rewriting queries but I want to know what is wrong with OrderBy Linq Extension method?</p>

## Answers
### Answer ID: 4470335
<p>Change the second OrderBy to ThenBy.</p>

### Answer ID: 4470330
<p>I have a blog post about this: <a href="http://www.kristofclaes.be/blog/2010/07/06/order-on-multiple-fields-with-linq/" rel="nofollow">http://www.kristofclaes.be/blog/2010/07/06/order-on-multiple-fields-with-linq/</a></p>

<p>The problem is that the second <code>OrderBy()</code> overrules the first one. To fix this, you can replace the second <code>OrderBy()</code> with <code>ThenBy()</code> like this:</p>

<pre><code>db.Cities.OrderBy(d=&gt;d.City).ThenBy(d=&gt;d.CountryCode)
</code></pre>

