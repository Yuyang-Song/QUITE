# Trying to write a mod rewrite to make my dynamic url user friendly but not working
[Link to question](https://stackoverflow.com/questions/44685202/trying-to-write-a-mod-rewrite-to-make-my-dynamic-url-user-friendly-but-not-worki)
**Creation Date:** 1498074956
**Score:** 0
**Tags:** php, apache, .htaccess, mod-rewrite, url-rewriting
## Question Body
<p>I have a news page that feeds a detail page with an id which in turn queries that database using id received to get results. I am trying to make the normal url e.g:</p>

<pre><code>xyz.com/news-detail.php?nrf=23
</code></pre>

<p>to something more friendly like:</p>

<pre><code>xyz.com/news/the-title-of-the-news/
</code></pre>

<p>On my news page, the link to the news article is like:</p>

<pre><code>&lt;a href="news-detail.php?nrf=&lt;?php echo $row_news['ntitle']; ?&gt;"&gt;&lt;?php echo $row_news['ntitle']; ?&gt;&lt;/a&gt;
</code></pre>

<p>and on the news-detail page, i have</p>

<pre><code> $newstitl = "";
    if (isset($_GET['nrf'])) {
      $newstitl = $_GET['nrf'];
    }

    $query_news = "SELECT newsID, ntitle, ndetail, nphoto, nauthor, ndate FROM news WHERE ntitle='$newstitl'";
    $result_news = mysqli_query($connJackie, $query_news);
    $row_news = mysqli_fetch_assoc($result_news);
    $totalRows_news = mysqli_num_rows($result_news);
</code></pre>

<p>which i believe is supposed to get the record from the database based on the title.
The problem is, its not working.The url shows like</p>

<pre><code>xyz.com/news-detail.php?nrf=the%20title%20of%20the%20news
</code></pre>

<p>I am quite new to mod-rewrite, but trying to improve my dynamic links to more friendly ones. I have read various articles on mod rewrite and that's how i tried to do this. 
My rewrite rule in the .htaccess file is:</p>

<pre><code>RewriteEngine On
RewriteRule ^news/([a-zA-Z0-9\\.\\_\\-]+)/?$ news-detail.php?nrf=$2 [NC,L]
</code></pre>

<p>I have also tried this but it also did not work</p>

<pre><code>RewriteEngine On
RewriteRule ^news/([\w-]+)/$    /news-detail.php?nrf=$1 [NC,L]
</code></pre>

<p>Any help in correcting and explaining would be greatly appreciated. </p>

