# PHP - Sort and order an array of objects by category name
[Link to question](https://stackoverflow.com/questions/55941993/php-sort-and-order-an-array-of-objects-by-category-name)
**Creation Date:** 1556740764
**Score:** -3
**Tags:** php, mysql
## Question Body
<p>I am learning PHP and have decided to code my own OOP MVC framework. Now, I have realized several times already that it might not be the smartest move but I mean to see this out to the end. And then onwards...</p>

<p>My issue is creating a listing sidebar based on categories and a second based on year-month-postname.
I am officially stuck on the first one, let alone the second damn option. I have included some code and description of what I have tried. The lack of OOP info on the net is daunting or maybe it is because I am searching for the wrong thing, I dont know. But the tutorials have not given me any insight as to how to actually do this in a way where my database is in a model file and my class logic is in the class file.</p>

<p>Sorting logic should be like this Array-Object-Propertyname-Value.
The value, as I hope is easy to understand in my example below, is the category name eg Javascript, PHP, HTML. By that category i wish to sort my blog posts. But not in the way that requires me to manually input the category names to the code. I want to allow users to enter categories if they so choose.
I also wish to display the blog posts inside said category, lets say 5 most recent. But that should not be too hard with a</p>

<pre><code>for($i=0,$i&lt;5,i++)
</code></pre>

<p>nested inside whatever solution in the end will work for the category sort.</p>

<p>I have tried MySQLI procedural solutions ranging from multiple google searches and tutorials. Can do it, but dont want to do it procedurally. Tried foreach loop and nesting multiple foreach loops - simply cannot get either the problem of having duplicates based on the shared category name or if trying to group in the SQL query, it simply groups results with same category and then displays only the first one in the group. While loops with mysqli procedural work but with pdo in my case they produce infinite loops, no matter the condition I try to set.
So foreach is the way to go I believe. I have read up on loops and array sorting but I've yet to find a solution. I thought of sorting by key because that is what i need but to no applicable solutions.
It's easy to display the category names and dates and all that. But with category I always get duplicates.
Ive tried some logic where as to assign category names as variables but only to have them all be different variables, meaning still having duplicates or only rewriting the variable with each iteration.
Also, array sorts havent worked because I havent gotten any to work with sorting either on property or if converting Objects to a multidimensional array. Granted that may be because I am a beginner and not understood the syntax but I am not going to post them all here I think.
If you think an array sorting function will do the trick then perhaps give me an example and I will look into it with some new perspective hopefully.</p>

<p>PDO query : </p>

<pre><code>'SELECT * FROM postTable 
INNER JOIN userTable ON postTable.postUserId = userTable.id 
INNER JOIN postCategories ON postTable.postCategoryId = postCategories.categoryName 
ORDER BY postTable.postDate DESC'
</code></pre>

<p>Tried also to add</p>

<pre><code>GROUP BY categoryName
</code></pre>

<p>but that resulted in only one entry per category shown when using var_dump. Sidenote - same is when grouping by creation date. Is there another layer added to the array when using group in the SQL command and I missed that in the docs?</p>

<p>PDO returns to view file : </p>

<pre><code>$this-&gt;stmt-&gt;fetchAll(PDO::FETCH_OBJ);
</code></pre>

<p>this all gets passed into an array of </p>

<pre><code>$results
</code></pre>

<p>and then that is sent to the php on the view page where the resulting array has this structure with var_dump.</p>

<pre><code>array() {
  [0]=&gt;
  object(stdClass)# () {
   ["categoryName"]=&gt;
    string() "Help"
  }
  [1]=&gt;
  object(stdClass)# () {
   ["categoryName"]=&gt;
    string() "Me"
  }
</code></pre>

<p>and so on.</p>

<p>Note - also tried using -</p>

<pre><code>fetchAll(PDO::FETCH_ASSOC);
</code></pre>

<p>But ive had similar failures with attempting any sorting or limiting to just one category name displayed but all entries under said category being displayed correctly and not just one per category.</p>

<p>I will be checking back when i finish work tomorrow so in about 20-22 hours from the time of posting.
If you need any more info just let me know and I'll post it.</p>

## Answers
### Answer ID: 55942697
<p>You can order by multiple columns. Use:</p>

<pre><code>ORDER BY categoryName, postDate DESC
</code></pre>

<p>This will keep all the posts in the same category together, and in decreasing date order within each category.</p>

<p>See <a href="https://stackoverflow.com/questions/27575562/how-can-i-list-has-same-id-data-with-while-loop-in-php/27575685#27575685">How can i list has same id data with while loop in PHP?</a> for how you can output the results, showing a heading for each category.</p>

<p>If you just want to get the 5 latest posts in each category, see <a href="https://stackoverflow.com/questions/2129693/mysql-using-limit-within-group-by-to-get-n-results-per-group">Using LIMIT within GROUP BY to get N results per group?</a></p>

