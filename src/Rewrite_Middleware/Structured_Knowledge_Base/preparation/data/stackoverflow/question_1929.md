# php sql multiple queries. Is it a big deal?
[Link to question](https://stackoverflow.com/questions/12534431/php-sql-multiple-queries-is-it-a-big-deal)
**Creation Date:** 1348244894
**Score:** 0
**Tags:** php, sql, cart
## Question Body
<p>I have a cart class, where I store the product ids. The user can open the cart through a button that opens the cart in a popup, so the cart content has to be loaded in every page.</p>

<p>I can store only the ids of the products because of the size limits, but I want to show the product names to the final user, so for each element I need to make a query and get the product data from the database.</p>

<p>Is there any major drawback by doing this? Or are there better solutions?</p>

<p>PS: I could get the id of all the products in the cart, and then do one single query that gets the data of any needed product. I’d rather avoid this since I would need to rewrite parts of the class, so is there any actual difference with the previous solution?</p>

<p>PPS: The total number of sql queries shouldn’t be too high in any case. Of course I wouldn’t mind, but I strongly doubt any user will purchase hundreds of different products at one time.</p>

## Answers
### Answer ID: 12537596
<p>I only like to highlight one sentence from your question:</p>

<blockquote>
  <p>so for each element I need to make a query and get the product data from the database.</p>
</blockquote>

<p>That is your problem. You do not need to do that. You can query your database with a single query and ask for all products that are in a list of IDs.</p>

<p>A helpful part of the SQL language is the <code>IN(....)</code> clause.</p>

<pre><code>$ids = [123, 884, 7848, 2882, 3232]; // let's say that is your input
$idList = implode(',', array_map('intval', $ids));
$sql = sprintf(
    "SELECT field1, field2, field3 FROM products WHERE products.ID IN(%s)",
    $idList
);
</code></pre>

<p>This is a single query for a list of product IDs. When you fetch the data from the data-base you create a in-memory-database on the fly (aka <em>Hashtable</em>) so that you can "fetch" data based on ID:</p>

<pre><code>foreach($ids as $id)
{
    $concreteProduct = $rows[$id];
    ...
}
</code></pre>

<p>You also know it as <code>array</code>, just keyed by the ID value returned from the database. As the ID is unique, this just works<sup>tm</sup>.</p>

<p>Hope this is helpful. Some might it call premature optimization, however, you should be aware of the concept, because this can be used in many cases.</p>

