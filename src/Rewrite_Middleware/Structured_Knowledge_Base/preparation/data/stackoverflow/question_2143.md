# How to rewrite HTML in to PHP echoes?
[Link to question](https://stackoverflow.com/questions/20523788/how-to-rewrite-html-in-to-php-echoes)
**Creation Date:** 1386777276
**Score:** 1
**Tags:** javascript, php, jquery, html, ajax
## Question Body
<p>I am trying to split my last post into more sections. </p>

<p>I am working with AJAX &amp; Database. The goal is to a have a clickable division (button) in a view. When this div is clicked the AJAX query is called and retrieves 5 movies from my DB and displays them in the view. What I am struggling the most with, is how to style the newly retrieved array, that I am displaying with jquery in the original division. </p>

<p>I am trying to follow <a href="http://www.w3schools.com/php/php_ajax_database.asp" rel="nofollow">this</a> <em>w3schools</em> tutorial. I am trying to rework my original styling according to how it is done in the tutorial. But <strong>I do not know how to write all the opening tags with their attributes into the echoes</strong>. </p>

<p>So if anyone here would be so kind and could show me how to rewrite at least few of them I would really appreciate it. All the lines starting with the comment <code>&lt;!--fix--&gt;</code> are those I need to rewrite.</p>

<p><strong>EDIT ----------------------------------------------------</strong></p>

<p>The problem is that I have a CI view page. On that page is a division with content. I am trying to replace this content with new content retrieved using the xmlhttp request. The request calls a file that establishes connection with my DB, runs the query, stores the result in an array and then echoes back the result already split and styled using the while loop. Below is the content of the file called by the jquery request.</p>

<pre><code>&lt;?php
$con = mysqli_connect('localhost','root','root','obs2');
if (!$con)
  {
  die('Could not connect: ' . mysqli_error($con));
  }

mysqli_select_db($con,"obs2");
$sql="SELECT * FROM user WHERE id &gt; 5";

$result = mysqli_query($con,$sql);

echo "&lt;table&gt;";
  while($row = mysqli_fetch_array($result))
  {
        &lt;a style="display:block" href="&lt;?php echo base_url('core/detail/'.$row-&gt;id) ?&gt;"&gt;
            &lt;div id="suggested" onmouseover="" style="cursor: pointer;"&gt;
                &lt;div id="info"&gt;
                    &lt;div id="info_center"&gt;
                        &lt;p&gt;&lt;b&gt;&lt;?php echo $row-&gt;name ?&gt;&lt;/b&gt;&lt;/p&gt;
                    &lt;/div&gt;
                &lt;/div&gt;

                &lt;div class="mosaic-block fade"&gt;
                    &lt;a href="&lt;?php echo base_url('core/detail/'.$row-&gt;id) ?&gt;" class="mosaic-overlay"&gt;

                    &lt;div class="details"&gt;
                        &lt;p&gt;&lt;?php echo $row-&gt;summary ?&gt;&lt;/p&gt;
                    &lt;/div&gt;
                    &lt;/a&gt;

                    &lt;div class="mosaic-backdrop"&gt;&lt;img src="http://puu.sh/5DSWj.jpg"&gt;&lt;/div&gt;
                &lt;/div&gt;

                &lt;div id="info"&gt;
                    &lt;div id="info_center"&gt;
                        &lt;p&gt;Rating: 7.7&lt;/p&gt;
                    &lt;/div&gt;
                &lt;/div&gt;
            &lt;/div&gt;
        &lt;/a&gt;    

  }
echo "&lt;/table&gt;";

?&gt;
</code></pre>

<p>So from what I understand from the tutorial is that I need to be echoing each of the lines in inside the while loop. And what I do not know is how to rewrite all the tags and the php echoes that are already in there. I hope this makes it more clear.</p>

<p><strong>----------------------------------------------------</strong></p>

<p><strong>original code</strong></p>

<pre><code>&lt;table&gt;
  &lt;?php foreach ($pages-&gt;result() as $row): ?&gt;
    &lt;a style="display:block" href="&lt;?php echo base_url('core/detail/'.$row-&gt;id) ?&gt;"&gt;
      &lt;div id="suggested" onmouseover="" style="cursor: pointer;"&gt;
        &lt;div id="info"&gt;
          &lt;div id="info_center"&gt;
            &lt;p&gt;&lt;b&gt;&lt;?php echo $row-&gt;name ?&gt;&lt;/b&gt;&lt;/p&gt;
          &lt;/div&gt;
        &lt;/div&gt;

        &lt;div class="mosaic-block fade"&gt;
          &lt;a href="&lt;?php echo base_url('core/detail/'.$row-&gt;id) ?&gt;" class="mosaic-overlay"&gt;

            &lt;div class="details"&gt;
              &lt;p&gt;&lt;?php echo $row-&gt;summary ?&gt;&lt;/p&gt;
            &lt;/div&gt;
          &lt;/a&gt;

          &lt;div class="mosaic-backdrop"&gt;&lt;img src="http://puu.sh/5DSWj.jpg"&gt;&lt;/div&gt;
        &lt;/div&gt;

        &lt;div id="info"&gt;
          &lt;div id="info_center"&gt;
            &lt;p&gt;Rating: 7.7&lt;/p&gt;
          &lt;/div&gt;
        &lt;/div&gt;
      &lt;/div&gt;
    &lt;/a&gt;    
  &lt;?php endforeach; ?&gt;
&lt;/table&gt;
</code></pre>

<p><strong>according to this</strong></p>

<pre><code>echo "&lt;table&gt;";
while($row = mysqli_fetch_array($result))
  {
  echo "&lt;tr&gt;";
  echo "&lt;td&gt;" . $row['FirstName'] . "&lt;/td&gt;";
  echo "&lt;td&gt;" . $row['LastName'] . "&lt;/td&gt;";
  echo "&lt;td&gt;" . $row['Age'] . "&lt;/td&gt;";
  echo "&lt;td&gt;" . $row['Hometown'] . "&lt;/td&gt;";
  echo "&lt;td&gt;" . $row['Job'] . "&lt;/td&gt;";
  echo "&lt;/tr&gt;";
  }
echo "&lt;/table&gt;";
</code></pre>

<p><strong>progress</strong></p>

<pre><code>echo "&lt;table&gt;";
while($row = mysqli_fetch_array($result))
{
&lt;!--fix--&gt;&lt;a style="display:block" href="&lt;?php echo base_url('core/detail/'.$row-&gt;id) ?&gt;"&gt;
&lt;!--fix--&gt;&lt;div id="suggested" onmouseover="" style="cursor: pointer;"&gt;
&lt;!--fix--&gt;  &lt;div id="info"&gt;
&lt;!--fix--&gt;    &lt;div id="info_center"&gt;
                echo "&lt;p&gt;" . $row['name'] . "&lt;/p&gt;";
              echo "&lt;/div&gt;";
            echo "&lt;/div&gt;";

&lt;!--fix--&gt;  &lt;div class="mosaic-block fade"&gt;
&lt;!--fix--&gt;    &lt;a href="&lt;?php echo base_url('core/detail/'.$row-&gt;id) ?&gt;" class="mosaic-overlay"&gt;

&lt;!--fix--&gt;      &lt;div class="details"&gt;
                  echo "&lt;p&gt;" . $row['summary'] . "&lt;/p&gt;";
                echo "&lt;/div&gt;";
              echo "&lt;/a&gt;";

&lt;!--fix--&gt;    &lt;div class="mosaic-backdrop"&gt;&lt;img src="http://puu.sh/5DSWj.jpg"&gt;&lt;/div&gt;
            echo "&lt;/div&gt;";

&lt;!--fix--&gt;  &lt;div id="info"&gt;
&lt;!--fix--&gt;    &lt;div id="info_center"&gt;
&lt;!--fix--&gt;      &lt;p&gt;Rating: 7.7&lt;/p&gt;
              echo "&lt;/div&gt;";
            echo "&lt;/div&gt;";
          echo "&lt;/div&gt;";
        echo "&lt;/a&gt;";
}
echo "&lt;/table&gt;";
</code></pre>

## Answers
### Answer ID: 20523991
<p>Don't follow the convention used in that tutorial. Not only can't you trust everything W3schools says (they even say that in their disclaimer), but it's just less readable. Especially when you have a propert editor, you can benefit from code highlighting in your HTML. That will be gone if you echo all your html. Apart from that you just clutter your code, and you have to escape every quote. Long story short: don't do that. :)</p>

<p>Regarding the echos of the values inside the html, you can shorten this:</p>

<pre><code>&lt;?php echo base_url('core/detail/'.$row-&gt;id) ?&gt;
</code></pre>

<p>to this:</p>

<pre><code>&lt;?=base_url('core/detail/'.$row-&gt;id) ?&gt;
</code></pre>

<p><code>&lt;?=</code> is just a shorthand. I think it even works when the short opening tag (<code>&lt;?</code>) is disabled, but if you want your code to be independent of that setting you should verify that.</p>

<p>Also, though I prefer the <code>{ .. }</code> style of blocks, I think using <code>: ... endforeach</code> is much clearer when combined with HTML. So I wouldn't change that either. </p>

<p>If you do want to change it anyway, you will still need the PHP closing tag, which you have forgotten now. So:</p>

<pre><code>while($row = mysqli_fetch_array($result)): ?&gt;
</code></pre>

<p>becomes:</p>

<pre><code>while($row = mysqli_fetch_array($result)) 
{ ?&gt;
</code></pre>

<p>Of course you can put <code>{ ?&gt;</code> or only the <code>{</code> on the same line as the <code>while</code> statement, if you like.</p>

<p>[edit]
Regarding your comment: Everything outside PHP tags gets outputted as-is. So the code:</p>

<pre><code>Hello &lt;?php echo 'lovely'; ?&gt; world &lt;?php /* More code without output*/ ?&gt;
</code></pre>

<p>results in the phrase: </p>

<pre><code>Hello lovely world
</code></pre>

<p>So as you can see, it is often much easier to put large chunks of plain text/html outside of PHP tags, and only briefly open and close PHP tags to echo some variable content.</p>

### Answer ID: 20524356
<p>Your original code is the CORRECT way to do it. The w3schools version is completely wrong and you should avoid that.</p>

<p>Everyone would be better able to assist you if you try to describe what is NOT working with your original code.</p>

