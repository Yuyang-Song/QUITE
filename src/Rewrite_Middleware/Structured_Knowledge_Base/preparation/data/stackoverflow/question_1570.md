# url rewriting by .htaccess files in php
[Link to question](https://stackoverflow.com/questions/9989081/url-rewriting-by-htaccess-files-in-php)
**Creation Date:** 1333438875
**Score:** 0
**Tags:** php, .htaccess
## Question Body
<p>I am rewriting my problem .
Below I am giving all the details of what i am trying to do, and what is the result I am getting. I hope to be very clear this time. I have a samples page here www.broadcast2world.com/samples.php. 
All the links and data which we see on the page is coming from a database. Now suppose we click on a link "More Info" for a particular video say social control. A specific href for that video is triggered as <code>&lt;a href="video.php?pid='.$id.'"&gt;</code> . It passes its id over url in the format <code>http://www.broadcast2world.com/video.php?pid=66.</code> </p>

<p>I catch that id into a variable using </p>

<pre><code>if(!isset($_GET['pid'])){
    $pageid='66';
}
else{
  $pageid=$_GET['pid'];  
} 
</code></pre>

<p>Using the $pageid variable, I run a query which ultimately prepare the page for that particular video.</p>

<p>What my SEO guy need is a url in the format www.broadcast2world.com/video/name-of-the-video.</p>

<p>Now the problem is that if I make a mod_rewrite amendments which is wonderfully explained by Ben below, I am not able to figure out, how to link that name-of-the-video to its id. I am sure there must be something I have to modify while creating specific url for videos as explained above. But I really don't know what? Thanks again for your wonderful support </p>

## Answers
### Answer ID: 9989111
<p>Instead of id, you have to search the database based on title then.</p>

<p>Here are what you are going to need.</p>

<p><strong>.htaccess</strong></p>

<pre><code>RewriteEngine on
RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^videos/(.*)$ video.php?title=$1
</code></pre>

<p><strong>Link generation</strong></p>

<pre><code>$title = "...";
$title = str_replace(" ", "-", $title); //add dashes on the link
echo "&lt;a href="videos/$title"&gt;Click Me&lt;/a&gt;";
</code></pre>

### Answer ID: 9989117
<p>You should add a column in your <code>videos</code> table in which you will store <code>name-of-the-video</code> that is suitable to be put in URL. You will need to <code>UPDATE</code> all your videos and set the <code>name-of-the-video</code> to a unique value for each video. From then on it will be simple to fetch a video by name instead of by id.</p>

