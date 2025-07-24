# PHP Form Posts to MySQL Database Successfully, But Adds Blank Rows
[Link to question](https://stackoverflow.com/questions/20668467/php-form-posts-to-mysql-database-successfully-but-adds-blank-rows)
**Creation Date:** 1387401034
**Score:** 1
**Tags:** php, mysql, forms
## Question Body
<p>I have searched, incessantly, for a fix to the problem of a PHP form causing blank rows in a MySQL database (of which my search query was, "form submitting blank rows to mysql database" here on SO). I find that I'm having the problem REGARDLESS of the fact that I constructed a suitable "post/redirect/get" pattern;</p>

<pre><code>PHP Form Page (input.php) ---&gt; 
PHP Form Processing Page (backend.php) ---&gt; 
Database Entry Results Display page (thanks.php - return link to index.php set also)
</code></pre>

<p>The problem of the blank row submission escapes me as I've attempted to add validation to the form so that there are no empty submissions, whether the page was reloaded (via back button or otherwise) and do the standard <code>isset()</code> checks. </p>

<p><strong>PHP Form</strong> (input.php)</p>

<pre><code>    &lt;form name="input" action="backend.php" method="post"&gt;
    &lt;font color="#0000CC" face="arial black"&gt;Article/News Title:&lt;/font&gt;&lt;br&gt;
    &lt;input type="text" name="Title" size="35" /&gt;
    &lt;br&gt;&lt;br&gt;
    &lt;font color="#0000CC" face="arial black"&gt;Article/News URL:&lt;/font&gt;&lt;br&gt;
    &lt;input type="text" name="Link" value="http://" size="40" /&gt;
    &lt;br&gt;&lt;br&gt;
    &lt;font color="#0000CC" face="arial black"&gt;Article/News description&lt;/font&gt; &lt;font size="4" color="#0000CC"&gt;(300 Characters Max)&lt;/font&gt;&lt;br&gt;
    &lt;TABLE style="BORDER-RIGHT: #000000 1px ; BORDER-TOP: #000000 1px ; BORDER-LEFT: #000000 1px ; WIDTH: 100px; BORDER-BOTTOM: #000000 1px ; BORDER-COLLAPSE: separate; BACKGROUND-COLOR: #ffffff" cellSpacing=0 cellPadding=0 border=0 alignment=""&gt;
   &lt;TBODY&gt;
   &lt;TR&gt;
   &lt;TD style="BORDER-RIGHT: #000000 1px solid; PADDING-RIGHT: 3px; BORDER-TOP: #000000 1px solid; PADDING-LEFT: 3px; PADDING-BOTTOM: 3px; BORDER-LEFT: #000000 1px solid; PADDING-TOP: 3px; BORDER-BOTTOM: #000000 1px solid"&gt;
    &lt;textarea id="bob" rows="8" name="Body" cols="60"&gt;&lt;/textarea&gt;
    &lt;script language="JavaScript"&gt;
    generate_wysiwyg("bob");
    &lt;/script&gt;
    &lt;/TD&gt;&lt;/TR&gt;&lt;/TBODY&gt;&lt;/TABLE&gt;
    &lt;br&gt;
    &lt;font color="#0000CC" face="arial black"&gt;Article/News Category?&lt;/font&gt;&lt;br&gt;
    &lt;SELECT name="category"&gt;
    &lt;OPTION&gt;games
    &lt;OPTION&gt;hardware
    &lt;OPTION&gt;humor
    &lt;OPTION&gt;movies
    &lt;OPTION&gt;music
    &lt;OPTION&gt;online
    &lt;OPTION&gt;politics
    &lt;OPTION&gt;programming
    &lt;OPTION&gt;radio
    &lt;OPTION&gt;science
    &lt;OPTION&gt;social
    &lt;OPTION&gt;software
    &lt;OPTION&gt;sports
    &lt;OPTION&gt;technology
    &lt;OPTION&gt;television
    &lt;/SELECT&gt;
    &lt;br&gt;&lt;br&gt;
    &lt;input type="submit" name="submit" value="Input"&gt;&lt;/form&gt;
</code></pre>

<p><strong>PHP Form Processing</strong> (backend.php)</p>

<pre><code>    // Connect to database
   $con=mysql_connect("localhost","db_user","pwd") or die(mysql_error("Cannot Connect To Database"));
   mysql_select_db('db_name', $con) or die(mysql_error("Cannot Select Database"));
   if (isset($_POST['submit'])) {

   // Define query variables
   $ArticleTitle = mysql_real_escape_string(strip_tags($_POST['Title']));
   $ArticleBody = mysql_real_escape_string(stripslashes($_POST['Body']));
   $ArticleLink = mysql_real_escape_string(strip_tags($_POST['Link'],'&lt;a&gt;'));
   $ArticleCategory = mysql_real_escape_string($_POST['category']);

   // Sets the timestamp format
   $Datum = date('D - M. j - g:ia');
   }

    //CHECK FOR EMPTY FIELDS 
    if (empty($_POST["Title"]) or empty($_POST["Body"]) or empty($_POST["Links"]) or empty($_POST["category"])) {

    $error =''; 
    if (trim($_POST['Title'])==''){ 
     $error .= "&lt;li&gt;Please enter a title&lt;/li&gt;"; 

    } elseif (trim($_POST['Body'])==''){ 
      $error .= "&lt;li&gt;Please enter some content&lt;/li&gt;"; 

    } elseif (trim($_POST['Link'])==''){ 
      $error .= "&lt;li&gt;Please enter a URL&lt;/li&gt;"; 

    } elseif (trim($_POST['category'])==''){ 
      $error .= "&lt;li&gt;Please enter a category&lt;/li&gt;"; 

    } else {

    //IF NO ERRORS DO SQL QUERY
    $query1=sprintf("INSERT INTO articles (title, link, body, date, category) VALUES ('%s', '%s', '%s', '%s', '%s')", $ArticleTitle, $ArticleLink, $ArticleBody, $Datum, $ArticleCategory);

    // Execute the query or die and echo an error message
    mysql_query($query1) or die("Unable to execute query:" . mysql_error());

    if ($query1) {
    include("thanks.php");
    }
    else {
    header('Location: input.php');
        }
      }
    }
    mysql_close($con);
</code></pre>

<p><strong>Entry Result Display Page</strong> (thanks.php)</p>

<pre><code>    echo "Your Article/News URL Has Been Posted - Thank You!";
    echo "&lt;br /&gt;&lt;br /&gt;&lt;b&gt;";
    echo $_POST['Title'];
    echo "&lt;/b&gt;&lt;br /&gt;&lt;br /&gt;&lt;b&gt;";
    echo $_POST['Body'];
    echo "&lt;/b&gt;&lt;br /&gt;&lt;br /&gt;&lt;b&gt;";
    echo $_POST['Link'];
    echo "&lt;/b&gt;&lt;br /&gt;&lt;br /&gt;&lt;/b&gt;";
    echo $_POST['Date'];
    echo "&lt;/b&gt;&lt;br /&gt;&lt;br /&gt;&lt;b&gt;";
    echo $_POST['category'];
    echo "&lt;/b&gt;&lt;br /&gt;&lt;br /&gt;";
    echo "&lt;a href='index.php'&gt;&lt;font face='arial black' size='2' color='#0000CD'&gt;&lt;u&gt;Return To Articles&lt;/u&gt;&lt;/font&gt;&lt;/a&gt;";
</code></pre>

<p>I have no problem with the end display, and this PRG pattern works insanely well except for the blank row additions which manifest several minutes to hours later. When debugging, I would let 24 hrs go by sometimes, and all was good. But the blank row would multiply (all with stated <code>NULL</code> values when I accessed PHPMyAdmin). I'm convinced that the logic in <strong>backend.php</strong> is skewed in some weird fashion. I have rewritten that page at least twenty times (four different versions of the page gave me my desired db output). There has got to be something that I'm missing, but after nearly thirty days of straight "search-and-code", I haven't been able to suss it out. </p>

<p>Yes, I know I'm working with deprecation, but I can't begin a complete PDO rewrite on my app until I can get this last issue sorted, and (believe me), it's BEGGING for it (lol!). I think it's relevant to mention also that <strong>input.php</strong> is protected by a PDO login script preventing random site visitors from posting willy-nilly. The only two problems that I can think that I'm having is that;</p>

<p>1) The visitation of <strong>input.php</strong> while in a non-logged state is tripping the form submission process (or some searchbot traffic, for that matter), </p>

<p>or   </p>

<p>2) Correct coding/wrong placement</p>

<p>All I need is a pointer to how I could solve this. I appreciate any and every reply. Thanks.</p>

<p><strong>EDIT</strong></p>

<p>OK, you know what, I've noticed that the other ancillary pages carrying information to the categories and their sub-headings (i.e - category:Programming / Sub-Headings: new/old/most/least - the php pages under the particular category topic - each one having its' own folder to keep those four pages grouped together), NEVER EVER have displayed the problem that the <strong>index.php</strong> has just errored out on so I may just have to change how the data comes out of the database by trashing the idea of trying to display the code on the front page. That would actually give me lattitude to do something uber-cool and include in some insanely small app that I've battle-tested and KNOW that works in the trenches, since, even as propellor-headed and code-tweakled I am, I'm still trying to upgrade my ability to make myself a living and actually continue to eat off this enterprise we call "Web Development" (lol!)</p>

## Answers
### Answer ID: 20944751
<p>Two things helped me in the process of finding my answer;</p>

<p>A) The conversion of my PHP processing page to PDO;</p>

<pre><code>    &lt;?php
    if (isset($_POST['submit'])) {
    $ArticleTitle = $ArticleLink = $ArticleBody = $ArticleCategory = $Datum = '';

    // Define a boolean and set to true before validating
    $formValid = true;

    // Data pulled from input form
    $ArticleTitle = $_POST['title'];
    $ArticleLink = $_POST['link'];
    $ArticleBody = $_POST['body'];
    $ArticleCategory = $_POST['category'];

    //Set date parameters
    $Datum = date('D - M. j - g:ia');

    if ($_SERVER['REQUEST_METHOD'] == "POST") {
    if ($_POST['title'] == null OR trim($_POST['title']) ==''|| $_POST['link'] == null OR trim($_POST['link']) =='' || $_POST['body'] == null OR trim($_POST['body']) =='' || $_POST['category'] == null OR trim($_POST['category']) =='') {
        echo '&lt;br&gt;&lt;br&gt;&lt;div align="center"&gt;&lt;a href="input.php"&gt;&lt;font color="#0000CC" face="arial black"&gt;Please return to form and supply required data!&lt;/font&gt;&lt;/a&gt;&lt;br&gt;&lt;img src="http://www.promodrone.com/images/myimage.gif"&gt;&lt;/div&gt;';
        $formValid = false; // Invalid input - set the flag to false
        exit;
        } else {

        if ($formValid){

        //PDO connection string details
        try {
        $dsn = 'mysql:host=localhost;dbname=dbname';
        $username ='user_name';
        $password ='pwd';
        $options = array(PDO::MYSQL_ATTR_INIT_COMMAND =&gt; 'SET NAMES utf8', PDO::ATTR_ERRMODE =&gt;PDO::ERRMODE_EXCEPTION, PDO::ATTR_EMULATE_PREPARES, false); 
        $dbh = new PDO($dsn, $username, $password, $options);
        } catch (Exception $e) {
        echo "WTF?!" . $e-&gt;getMessage('Cannot connect: ' . mysql_error());
        }
         //Insert data into db
            try {
            $sth = $dbh-&gt;prepare('INSERT INTO articles(title, link, body, category, date) VALUES (?, ?, ?, ?, ?)');
            $sth-&gt;execute(array($ArticleTitle, $ArticleLink, $ArticleBody, $ArticleCategory, $Datum));

            //If successful redirect to display database insertion details
            if($sth){
            exit(include('thanks.php'));
            }                 
            else{
            echo '&lt;a href="input.php"&gt;&lt;font color="#0000CC" face="arial black"&gt;No record added. Return to form, please!&lt;/font&gt;&lt;/a&gt;';
            }
            } catch (Exception $e) {
            echo "Glugh?!" . $e-&gt;getMessage('Cannot continue:  &lt;a href="input.php"&gt;&lt;font color="#0000CC" face="arial black" size="3"&gt;Return to form, please!&lt;/font&gt;&lt;/a&gt;' . mysql_error());
            }
            }
            }
            }
            } 
            $dbh = NULL;
            ?&gt;
</code></pre>

<p>and, B) that you have to check SUPER-THOROUGHLY so you don't commit errors caused by overlooking. </p>

<p>On my index.php page, I didn't close a table correctly and, somehow, that kept helping to insert an extra (empty) row in the database. I was only led there this afternoon, after I took a spin at another coding website I have an account with. For some reason, I was compelled to look at the HTML table structure. My forehead is STILL sore from the nuclear facepalm after my realization;</p>

<pre><code>             echo "&lt;p style='font-size:95%'&gt;&lt;b&gt;Category -&lt;/b&gt;&lt;b&gt;";
             echo "&lt;/b&gt;&lt;/p&gt;&lt;/table&gt;&lt;/center&gt;&lt;br&gt;";
</code></pre>

<p><strong>NOT</strong></p>

<pre><code>             echo "&lt;p style='font-size:95%'&gt;&lt;b&gt;Category -&lt;/b&gt;&lt;b&gt;";
             echo "&lt;/p&gt;&lt;/b&gt;&lt;/font&gt;&lt;/table&gt;&lt;/center&gt;&lt;br&gt;";
</code></pre>

<p>The only thing that I'm <strong>NOT</strong> happy about is I had to destroy my nice little "P/R/G" pattern, since I couldn't (no matter what I tried), get the vars from the processing page (backend.php) to be echoed from the thanks.php page. The reason for this is that when a user finishes entering the details of their article/news URL, the thanks php is supposed to present them with their input;</p>

<pre><code>             $ArticleTitle    (Article/News title)
             $ArticleLink     (Article/News link)
             $ArticleBody     (Article/News content/image body)
             $ArticleCategory (Article/News category)
</code></pre>

<p>stacked exactly in the above fashion. Since earlier this afternoon, I've played the complete paranoiac (lol), because I jumped the gun and celebrated too early the night before. My solution has held for me since this afternoon, and the same error described above in the HTML table had been replicated to all the other category index pages. After changing them all in one fell swoop via my IDE, I tested rigorously by adding ten more entries back to back (about three hours ago), and I haven't even seen the problem pop-up again. :deep sigh: (lol!). Hope this helps someone. I don't know if this is even SLIGHTLY off-topic (and I'm sure that someone will let me know), but the time of MySQL is FINISHED. I understand why many people aren't gung-ho on PHP Data Objects, but after a period of seven days straight on it, it began to "talk" to me. I'M - NEVER - GOING - BACK.....now, to rewrite the rest of the application (lol!).</p>

### Answer ID: 20673573
<p>Well, there is advice on your overall database structure, but your data filtering sanitizing—and overall chain of logic connected to the data being inserted—could be improved to truly have content if there only if there is content. So I would change this:</p>

<pre><code>   $ArticleTitle = mysql_real_escape_string(strip_tags($_POST['Title']));
   $ArticleBody = mysql_real_escape_string(stripslashes($_POST['Body']));
   $ArticleLink = mysql_real_escape_string(strip_tags($_POST['Link'],'&lt;a&gt;'));
   $ArticleCategory = mysql_real_escape_string($_POST['category']);
</code></pre>

<p>To this:</p>

<pre><code>   // Let’s set all the variables to null to begin with.
   $ArticleTitle = $ArticleBody = $ArticleLink = $ArticleCategory = null;

   // Here is an array of variables from '$_POST' as the key with final variables as a value.
   $post_variables = array('Title' =&gt; 'ArticleTitle', 'Body' =&gt; 'ArticleBody', 'Link' =&gt; 'ArticleLink', 'category' =&gt; 'ArticleCategory');

   // Here is an array of items that are links, so they should be parsed differently.
   $link_variables = array('Link');

   // Roll through the '$post_variables'.
   foreach ($post_variables as $post_key =&gt; $post_variable) {

     // Check if the keys exist in $_POST.
     if (array_key_exists($post_key, $_POST) &amp;&amp; !empty(trim($_POST))) {

       // Check if the key needs special handling in $link_variables.
       if (in_array($post_key, $link_variables)) {
         $$post_variable = mysql_real_escape_string(strip_tags($_POST[$post_variable]),'&lt;a&gt;');
       }
       // If it doesn't need special handling, set it as normal.
       else {
         $$post_variable = mysql_real_escape_string(strip_tags($_POST[$post_variable]));
       }

     }

   }
</code></pre>

<p>This new method does a few things. First, it restructures your variable sanitizing logic to be in arrays to avoid repeated code. But more importantly, it makes sure your values are set only if the content is truly there and not a stray empty space submitted in a form. If that happens, the variable comes out as simply <code>null</code> and at that point it can be inserted into your MySQL table as such.</p>

<p>Also the logic for <code>CHECK FOR EMPTY FIELDS</code> should be changed to factor in the sanitizing like so. I mean, we have already checked the <code>$_POST</code> so why do it again? Work with the data that is now known to be clean &amp; valid. Also, I find it best for the <code>if</code> to be a positive outcome and the <code>else</code> to be the fallback. I mean, the goal is not to have errors, the <code>if</code> is basically confirming the positive condition of a data validation chain, right?</p>

<pre><code>// If the fields are not empty, insert it.
if (!empty($ArticleTitle) || !empty($ArticleBody) || !empty($ArticleLink) || !empty($ArticleCategory)) {

  $query1 = sprintf("INSERT INTO articles (title, link, body, date, category) VALUES ('%s', '%s', '%s', '%s', '%s')", $ArticleTitle, $ArticleLink, $ArticleBody, $Datum, $ArticleCategory);

  // Execute the query or die and echo an error message
  mysql_query($query1) or die("Unable to execute query:" . mysql_error());

  if ($query1) {
    include("thanks.php");
  }
  else {
    header('Location: input.php');
  }
  mysql_close($con);
}
else {
  $error = ''; 
  if (empty($ArticleTitle)) { 
   $error .= "&lt;li&gt;Please enter a title&lt;/li&gt;"; 
  }
  elseif (empty($ArticleBody)) { 
    $error .= "&lt;li&gt;Please enter some content&lt;/li&gt;"; 
  }
  elseif (empty($ArticleLink)) { 
    $error .= "&lt;li&gt;Please enter a URL&lt;/li&gt;"; 
  }
  elseif (empty($ArticleCategory)){ 
    $error .= "&lt;li&gt;Please enter a category&lt;/li&gt;"; 
  }
}
</code></pre>

<p><strong>EDIT</strong> Also, adding some overall advice on PHP form processing you have in <code>backend.php</code>. In general, it seems muddled. I mean, all of it works, but it is also causing you problems, right?  Okay, so this is the basic flow of what it should be:</p>

<ol>
<li>Sanitize the data.</li>
<li>If after sanitizing the data is valid by your criteria, do the MySQL work.</li>
<li>If after sanitizing, the data is invalid, generate error messages. 3.</li>
</ol>

<p>I know this sounds obvious, but when I see your code is making a MySQL connection prior to validating, the only question that comes to mind is: Why? Why open a connection when you have no idea the data is valid? Only set a MySQL connection when you know you need it.</p>

