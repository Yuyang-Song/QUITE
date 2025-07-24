# Encapsulate different data sources in an application
[Link to question](https://stackoverflow.com/questions/33565654/encapsulate-different-data-sources-in-an-application)
**Creation Date:** 1446808810
**Score:** 1
**Tags:** oop, encapsulation, software-design, business-logic
## Question Body
<p>I have the e-commerce website. It is based on Kohana <strong>php</strong>. My business faces new challenges and I'm trying to break my monolithic architecture into small parts.</p>

<p>Right now I have mysql database as the only data-source and access it in my application via ORM or DB queries:</p>

<pre><code>$product = ORM::factory('Product', $id_product);
$products = ORM::factory('Product')-&gt;where()-&gt;find_all()
$products = DB::query(Database::SELECT, "{my complex query}"-&gt;as_object('Product')-&gt;execute();
</code></pre>

<p>Problem arises when I decide to move to <strong>other</strong> data source: API, Mongodb, etc. I'm forced to rewrite many lines of my code.</p>

<p>I have gaps in my knowledge of software development and I need some hints, best practises how to encapsulate different data sources in an application.</p>

## Answers
### Answer ID: 33570076
<p>Encapsulate your data source interactions using the <a href="https://en.wikipedia.org/wiki/Adapter_pattern" rel="nofollow">adapter</a> and <a href="https://en.wikipedia.org/wiki/Factory_method_pattern" rel="nofollow">factory method</a> patterns. Make sure you have mock implementations of the adapters so that you can test interactions in the absence of an actual database. </p>

