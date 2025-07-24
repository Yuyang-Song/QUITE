# PHP script for SQL querying
[Link to question](https://stackoverflow.com/questions/22697114/php-script-for-sql-querying)
**Creation Date:** 1395947777
**Score:** 0
**Tags:** php, mysql, sql
## Question Body
<p>I'm still learning php so please take it easy on me. This might sound a silly question for you guys.</p>

<p>Right so. I have categories lets say Blogs, eCommerce, Portfolios etc. Files according too. Blog.php etc.</p>

<p>I also have functions.php where all my functions are. </p>

<p>MYSQL database is where I store information from them files. Website information, descriptions etc. </p>

<p>I want to have 1 function that queries data from a website just about 1 category so then  I can display it in Blogs.php, eCommerce.php etc. 
My function to query data from mysql looks like this. </p>

<p>This is an example:</p>

<pre><code>function querying_category($category){
    $db = DB::getInstance();
    $all = $db-&gt;query('SELECT * FROM website WHERE category = {$category} ORDER BY id DESC');

    if($all-&gt;count()){
       foreach($all-&gt;results() as $website){
              $web_data[] = $website;
       }
    }
    return $web_data;
}
</code></pre>

<p>and then let's say in my blog.php would go like:</p>

<pre><code>$category = 'blog';
$website = querying_category($category);
</code></pre>

<p>Could you please tell me what am I doing wrong? I want to declare a variable in my blog.php or ecommerce.php etc without rewriting the following query:</p>

<pre><code>'SELECT * FROM website WHERE category = {$category} ORDER BY id DESC
</code></pre>

<p>Can I achieve it with passing in <code>$category</code> as an argument in <code>querying_category()</code> but declaring <code>$category</code> in my blog.php or ecommerce.php?</p>

## Answers
### Answer ID: 22713898
<p>It seems as if the editing I made to the question fixed the OP's problem.</p>

<p>There were a few lines of code that were not properly indented along with a few spelling mistakes.</p>

<p>As per the OP's request, this answer has been given in order to close the question.</p>

<p><em>However</em>, this line <code>return $web_data;</code> should have been <code>return $website;</code></p>

