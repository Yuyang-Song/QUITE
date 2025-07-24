# Textarea line break no working properly
[Link to question](https://stackoverflow.com/questions/30562025/textarea-line-break-no-working-properly)
**Creation Date:** 1433102041
**Score:** 3
**Tags:** php, sql, .htaccess, str-replace, fwrite
## Question Body
<p>I have a best problem in my experience, I want to write .htaccess file by fwrite(), when it debug its show ok in side the textarea but when I going to submit that then it show \n\r\n\r.... I was try str_replace() and its work but that does not break line. This is my all codes, please help me.</p>

<blockquote>
  <p>submit.php</p>
</blockquote>

<pre><code>&lt;?php

//.htaccess file write and rewrite query

$file = ".htaccess";

$submit7 = $_POST['submit7'];

$edit = mysql_real_escape_string(str_replace( array("\r\n", "\n"), " ", $_POST['edit']));




function wee() {

    echo "&lt;IfModule mod_rewrite.c&gt; \n
\n RewriteEngine on \n";

    require('config2.php'); $getquery=mysql_query("SELECT * FROM menu ORDER BY menu_id DESC"); while($rows=mysql_fetch_assoc($getquery)){$menu_id=$rows['menu_id']; $linkname=$rows['linkname'];

echo "\n RewriteRule ^".$linkname."/{0,1}$  pagee.php?menu_id=".$menu_id. "[QSA,L] \n"; }

    echo "\n &lt;/IfModule&gt;";



} 




    if ($submit7) {
    if ( is_writable( $file ) ) {
        // is_writable() not always reliable, check return value. see comments @ http://uk.php.net/is_writable
        $f = fopen( $file, 'w+');
        if ( $f !== false ) {
            fwrite( $f, $edit );
            fclose( $f );

        }
    }
}



?&gt;





&lt;form id="form7" name="form7" method="post" action="&lt;?php echo $_SERVER['PHP_SELF']; ?&gt;"&gt;
      &lt;label&gt;
        &lt;input type="submit" name="submit7" value="Write" /&gt;
      &lt;/label&gt;

&lt;textarea name="edit"&gt;&lt;?php echo wee(); ?&gt;&lt;/textarea&gt;



    &lt;/form&gt;
</code></pre>

<blockquote>
  <p>config2.php</p>
</blockquote>

<pre><code>&lt;?php

mysql_connect("localhost","root","");
mysql_select_db("myweb");


?&gt;


&lt;?php
$con = mysql_connect('localhost','root','')
or die(mysql_error());
mysql_select_db ("myweb");
?&gt;
</code></pre>

<blockquote>
  <p>sql.sql</p>
</blockquote>

<pre><code>--
-- Database: `myweb`
--

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE IF NOT EXISTS `menu` (
  `menu_id` int(11) NOT NULL,
  `mname` text NOT NULL,
  `level` text NOT NULL,
  `linkname` text NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`menu_id`, `mname`, `level`, `linkname`) VALUES
(1, 'Home', 'home', 'aaaa'),
(2, 'Music', 'Music', 'Music'),
(3, 'Movie', 'Movie', 'Movie'),
(4, 'Song', 'Song', 'Song');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`menu_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `menu_id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
</code></pre>

<blockquote>
  <p>.htaccess --- output result now showing</p>
</blockquote>

<pre><code>&lt;IfModule mod_rewrite.c&gt;  RewriteEngine on  RewriteRule ^Song/{0,1}$  pagee.php?menu_id=4[QSA,L]  RewriteRule ^Movie/{0,1}$  pagee.php?menu_id=3[QSA,L]  RewriteRule ^Music/{0,1}$  pagee.php?menu_id=2[QSA,L]  RewriteRule ^aaaa/{0,1}$  pagee.php?menu_id=1[QSA,L]  &lt;/IfModule&gt;
</code></pre>

<blockquote>
  <p>But I want that like this:</p>
</blockquote>

<pre><code>&lt;IfModule mod_rewrite.c&gt;  

RewriteEngine on  

RewriteRule ^Song/{0,1}$  pagee.php?menu_id=4[QSA,L]
RewriteRule ^Movie/{0,1}$  pagee.php?menu_id=3[QSA,L]  
RewriteRule ^Music/{0,1}$  pagee.php?menu_id=2[QSA,L]  
RewriteRule ^aaaa/{0,1}$  pagee.php?menu_id=1[QSA,L]  

&lt;/IfModule&gt;
</code></pre>

<p>Please Please Please HELP ME......</p>

## Answers
### Answer ID: 30562649
<p>OK Dear I think I find you result just do that replacement ok,</p>

<blockquote>
  <p>submit.php</p>
</blockquote>

<pre><code>&lt;?php
//.htaccess file write and rewrite query

$file = ".htaccess";
$submit7 = $_POST['submit7'];

if ($submit7) 
{
   $htfe = file_put_contents('.htaccess', $_POST['edit']);
}

function wee() 
{
    echo "&lt;IfModule mod_rewrite.c&gt; \n
    \n RewriteEngine on \n";
    require('config2.php'); $getquery=mysql_query("SELECT * FROM menu ORDER BY menu_id DESC"); while($rows=mysql_fetch_assoc($getquery)){$menu_id=$rows['menu_id']; $linkname=$rows['linkname'];
    echo "\n RewriteRule ^".$linkname."/{0,1}$  pagee.php?menu_id=".$menu_id. "[QSA,L] \n"; }
    echo "\n &lt;/IfModule&gt;";
}
?&gt;

&lt;form id="form7" name="form7" method="post" action="&lt;?php echo $_SERVER['PHP_SELF']; ?&gt;"&gt;
      &lt;label&gt;
        &lt;input type="submit" name="submit7" value="Write" /&gt;
      &lt;/label&gt;
      &lt;textarea name="edit"&gt;&lt;?php echo wee(); ?&gt;&lt;/textarea&gt;
&lt;/form&gt;
</code></pre>

<p>I thing you should get you solution, ok
Just change this file <code>submit.php</code> ok</p>

### Answer ID: 30562253
<p><strong>Four solutions:</strong></p>

<p><strong>1)</strong> Use PHP function <a href="http://php.net/manual/en/function.nl2br.php" rel="nofollow">nl2br()</a></p>

<p><strong>e.g.</strong></p>

<pre><code>echo nl2br("This\r\nis\n\ra\nstring\r");

// will output
This&lt;br /&gt;
is&lt;br /&gt;
a&lt;br /&gt;
string&lt;br /&gt;
</code></pre>

<hr>

<p><strong>2)</strong> Wrap the input in <code>&lt;pre&gt;&lt;/pre&gt;</code> tag.</p>

<p><strong>See:</strong> <a href="http://www.w3.org/wiki/HTML/Elements/pre" rel="nofollow">http://www.w3.org/wiki/HTML/Elements/pre</a></p>

<p><hr><strong>3)</strong> Use,</p>

<pre><code>$textToStore = nl2br(htmlentities($inputText, ENT_QUOTES, 'UTF-8'));
</code></pre>

<p><hr><strong>4)</strong> Use,</p>

<pre><code>file_put_contents('.htaccess', $_POST['textarea_value']);
</code></pre>

<p><code>file_put_contents()</code> combines the functions of <code>fopen</code>, <code>fwrite</code>, <code>fclose</code></p>

