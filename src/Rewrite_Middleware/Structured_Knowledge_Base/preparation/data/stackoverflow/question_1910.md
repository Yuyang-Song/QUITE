# How to format url for database query
[Link to question](https://stackoverflow.com/questions/11903803/how-to-format-url-for-database-query)
**Creation Date:** 1344609025
**Score:** 0
**Tags:** php, mysql, .htaccess, url, url-rewriting
## Question Body
<p>I'm new here I and need your help. 
I started playing with .htaccess and php and I came across a problem.
When doing url rewriting, I pass into the url a string which is the title of an article extracted from the database. The problem is that the string(title) has a lot of characters who in the url are misspelled. EG: localhost/news/php%5%is%out 
Here % are the blank spaces. I tried to format every title with preg_replace and I replaced every space with '-' but there are a lot of characters and I wanted to know if there is any way of doing this without preg_replace so any string can be good for a query.
In news.php I get the string from the url and I use it for the query in the database from which I extract the body of the entire article. </p>

<pre><code>RewriteRule ^news/([a-zA-Z0-9._]+)/?$ /news.php?news_title=$1
</code></pre>

<p>This is my .htaccess file so in the news.php i get the 'news_title' variable through $_GET and then query the database to find the articol with this title.
So my question is, am I doing this all wrong? Is there any other way of doing this? I started working with htaccess only 2 days ago and I want to make my urls more friendly.
I hope my question is clear.
Thank everyone who helps me.</p>

<p>Just for an example, this is what I use to transform the normal tile in a string that won't be change with symbols(;amp, %, ?, etc) in the url</p>

<pre><code>function generateUrl($url) {

    $v1 = preg_replace("/[\s\:\;\,\_\'\`\"\?\!\%\(\)\+\=\#\@\[\]\{\}\/]/", "-", $url );
    $v2= preg_replace('/[-]{2,}/', '-', $v1);
    $v3 = preg_replace('/^[-]/', '', $v2);
    $final = preg_replace('/[-]$/', '', $v3);

    return $final;
}
</code></pre>

## Answers
### Answer ID: 11904123
<p>I think the answer for your problem is here <a href="https://stackoverflow.com/questions/2103797/url-friendly-username-in-php">URL Friendly Username in PHP?</a>. When you add article to the table, use this function (Slug) to convert article title and store converted title in column "slug". When user enters the address (.....)/article.php?name=some-title, use $slug = $_GET['title'] and find article by a slug. Before you save article you should check whether the article with this slug exists. If exists add to slug some number and then save to db. You can't allow to exists two record with the same slug in the table.</p>

