# DB Structure : Multiple tables with common ID
[Link to question](https://stackoverflow.com/questions/21207780/db-structure-multiple-tables-with-common-id)
**Creation Date:** 1390068032
**Score:** 0
**Tags:** php, mysql, database-design, laravel, laravel-4
## Question Body
<p>I'm building an app that need to manage various objects (3 at the moment, but that might increase in time). All these objects have a unique ID using the same format, but no other attribute in common.</p>

<p>So I created a table for every object, but I'm wondering how to do an optimized search by ID.I  want to build a good process form the start, because the total number of rows could become very high, and I don't want to have to rewrite code in a couple of months because it would have become too slow. </p>

<p>I thought of NoSQL databases, but I am required to use MySQL. The PHP code uses Laravel 4 with the Eloquent ORM.</p>

<p>Let's say I want the item with ID <code>abcd-123456</code>, I have no idea which table to query, so I thought of this :</p>

<ol>
<li>When inserting an object, store the ID along with the table name in another table (<code>CommonIndex</code>)</li>
<li>When querying by ID, lookup the table name in the <code>CommonIndex</code> table, store in the <code>$tableName</code> variable</li>
<li>Retrieve the final data by using <code>$tableName::find('abcd-123456')</code> in Eloquent (using models nammed exactly like my tables)</li>
</ol>

<p>But I'm worried this process will become sluggish when I have to search my ID in 300k+ rows</p>

<p>Any thoughts about how to improve this process, or building a new one ?</p>

<p>Thanks !</p>

<p>EDIT : More informations: </p>

<ul>
<li>My tables are not linked to each other, each one represent a type of object</li>
<li>Each table has an ID field</li>
<li>Each object has a unique ID, but on the same format (ex : Table 1 contains objects <code>ab-1 de-3 hi-5</code> Table 2 <code>cd-2 gh-4 jk-6</code> etc...)</li>
<li>Two objects from different types cannot have the same ID</li>
<li>I do not assign the ID, each object already has one</li>
<li>Most of the searches will be done by ID, because it's easier for the users</li>
<li>In specific conditions, users may search a product on a different field than the ID, but I don't have the same worries about performance, because it will be very rare</li>
<li>To allow for searches on others fields, these specific fields will be indexed (1 or 2 per table)</li>
<li>The search will be one by one</li>
<li>If I add a batch search along the way, I will process it one by one</li>
</ul>

## Answers
### Answer ID: 21208082
<p><strong>Questions :</strong></p>

<p>Sorry, I can't add comments because I don't have 50 rep yet, but I have some questions :</p>

<p>Where are the ids coming from? Is it from an external system? Or are you giving them the ids?</p>

<p>Why do you need to search by id? For internal purpose or users will use those ids?</p>

<p>Are the ids really alphabetical? Numbers would be more efficient.</p>

<p>Will you search by multiple ids at the same time or just one by one?</p>

<hr>

<p><strong>One possible solution :</strong></p>

<p>One simple thing you could do (depending on your needs), is to use just one table with 2 columns :</p>

<ul>
<li>Your ID</li>
<li>The PHP object stored as a string (aka serialized)</li>
</ul>

<p>There's downsides though. Check out this URL for pros and cons :
<a href="http://www.mysqlperformanceblog.com/2010/01/21/when-should-you-store-serialized-objects-in-the-database/" rel="nofollow">http://www.mysqlperformanceblog.com/2010/01/21/when-should-you-store-serialized-objects-in-the-database/</a></p>

<p>(for example, if you need to search on other property than your id, it won't work. If you need to update the DB often, it's not what's more efficient either)</p>

<p>It's really easy to serialize and unserialize object in PHP :</p>

<pre><code>$a = your_object;
$s = serialize($a);
// save data into database. $s is now your object, but in a string format.

// retreive the value from your database ($s)
$s = get_from_database($id);
$a = unserialize($s);
// do whatever you want now with your object
</code></pre>

<hr>

<p>Another solution is the one you mentioned but I wouldn't store the table name. A number is more efficient.</p>

<hr>

<p>Update :</p>

<p>Since you can't really store the serialized object, I think what you suggested is the best way.
300k for MySQL is manageable, just ensure that you have an index on your id column.</p>

<p>Also, if there are often searches for a particular group of columns (for example the users often search by id, first name and last name), you'll want to use a composite index on both columns (it takes more disk space tough).</p>

<p>If you want to be certain that the queries (1 to get the table and the 2nd to get the data) will be efficient, you can easily enter 300K entries with a small php script (a loop with inserts) or with data generators (I found this one : <a href="http://www.generatedata.com/" rel="nofollow">http://www.generatedata.com/</a>).</p>

<p>I would enter 300k in 2 tables (in your "index" table and one of the object table) and test the time it takes to make 2 queries, one on the "index" table and the other one on the object table.</p>

<hr>

<p>Another thing you could try is using a stored procedure (you could do the choice of the table based on the type of the object in the stored procedure).</p>

### Answer ID: 21209152
<p>You have a fundamental problem with a one-query solution:  you don't know what columns are being returned for each object, because the columns depend on the type.</p>

<p>Your approach with the <code>CommonIndex</code> table sounds like a reasonable approach.  Just be sure that the <code>id</code> column is indexed on each of the object tables.</p>

<p>I do find it surprising that objects that share a common format for an <code>id</code> do not have <em>any</em> fields in common.  If there are common fields, then these would go in <code>CommonIndex</code>.</p>

