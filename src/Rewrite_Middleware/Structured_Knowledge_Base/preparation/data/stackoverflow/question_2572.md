# Use session variable or copy PHP code from second page to third page of a website
[Link to question](https://stackoverflow.com/questions/41009983/use-session-variable-or-copy-php-code-from-second-page-to-third-page-of-a-websit)
**Creation Date:** 1481088181
**Score:** 1
**Tags:** php, html, sql-server, session, session-variables
## Question Body
<p>I have three pages in the website. The first is login page,second is profile page and third is main page.</p>

<p><div class="snippet" data-lang="js" data-hide="false" data-console="true" data-babel="false">
<div class="snippet-code">
<pre class="snippet-code-html lang-html prettyprint-override"><code>&lt;?php
session_start();
$servername="blah blah blah";
$connectioninfo=array('Database'=&gt;'mbr');
$conn=sqlsrv_connect($servername,$connectioninfo);
if($conn)
{
echo 'connection established';
}
else
{
echo 'connection failure';
die(print_r(sqlsrv_errors(),TRUE));
}

$q1="SELECT * FROM EmployeeTable WHERE EmployeeID = '" . $_SESSION['id'] . "' ";
$stmt=sqlsrv_query($conn,$q1);
if($stmt==false)
{
echo 'error to retrieve info !! &lt;br/&gt;';
die(print_r(sqlsrv_errors(),TRUE));
}
$row=sqlsrv_fetch_array($stmt);
echo $row['EmployeeName'];

$q2="SELECT * FROM pointsBadgeTable WHERE EmployeeID = '" . $_SESSION['id'] . "' ";
$stmt1=sqlsrv_query($conn,$q2);
if($stmt1==false)
{
echo 'error to retrieve info !! &lt;br/&gt;';
die(print_r(sqlsrv_errors(),TRUE));
}
$pbrow=sqlsrv_fetch_array($stmt1);
?&gt;</code></pre>
</div>
</div>
</p>

<p>The above is the php used in the second page of the website. Here I am using two queries $q1 and $q2 to retrieve information from two different tables (EmployeeTable and pointsBadgeTable) after connection to the database "mbr" here.</p>

<p>I then echo the desired Info in my html after retrieving info from the tables.</p>

<p>For instance,</p>

<p><div class="snippet" data-lang="js" data-hide="false" data-console="true" data-babel="false">
<div class="snippet-code">
<pre class="snippet-code-html lang-html prettyprint-override"><code>&lt;?php echo "". $row['goldTotal'] .""?&gt;&gt;</code></pre>
</div>
</div>
</p>

<p>Here 'goldtotal' is a column in the pointsBadgeTable in the above php. Also please note that I am using  " . $_SESSION['id'] ."  here to show info only about the person who logs in the first page of the website.</p>

<p>The issue here is that I want to echo the same value in the third page as in second page. Will I have to write the same php code in third page as I wrote in second page or I need to store it in some session variable. How to use a session variable here?</p>

<p>Also, is it correct to rewrite the same code in third page also as in second page and use the same queries $q1 and $q2? I will copy and paste the same PHP to the third page also.</p>

## Answers
### Answer ID: 41010134
<p>You Can include the second page in third page , you will get the value .
Example : file3.php</p>

<pre><code>**&lt;?php 
include 'file2.php';
?&gt;**
</code></pre>

