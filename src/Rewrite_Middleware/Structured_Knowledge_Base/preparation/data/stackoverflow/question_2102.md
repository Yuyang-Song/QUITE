# Increment in UPDATE query not going over 4
[Link to question](https://stackoverflow.com/questions/18979511/increment-in-update-query-not-going-over-4)
**Creation Date:** 1380019660
**Score:** 0
**Tags:** php, mysql, sql, increment
## Question Body
<p>I have another problem which I have spent hours on understanding and rewriting. On the UPDATE query I included countr=countr+1. I successfully received the keyWords from the mobile application and was also able to store them in the database. The problem is, whenever the same keyWord is passed for the fifth time a new row is created. Instead of adding 1 to the countr of that keyWord. It's as if the countr is limited on holding number 4 only. </p>

<p>Is it because of a mistake I did with the UPDATE query or is it because of something else I missed?</p>

<p>Here is my code:</p>

<pre><code>$con= mysqli_connect("...","...","...") or die ('Error: ' . mysql_error()); 
mysqli_select_db($con,"...");
$sql= "SELECT keyWord FROM searchedWords";
$result= mysqli_query($con,$sql);
$row=mysqli_fetch_array($result, MYSQLI_ASSOC);

if($row['keyWord']==$_POST[keyWord])
{
  $upD="UPDATE searchedWords SET countr = countr + 1";
     while (!mysqli_query($con,$upD))
    {
     die('Error: ' . mysqli_error($con));
    }
}
else
{
   $insertIn="INSERT INTO `searchedWords`( `keyWord`, `countr`) values ('$_POST[keyWord]',1)";
 while (!mysqli_query($con,$insertIn))
    {
     die('Error: ' . mysqli_error($con));
    }
}
</code></pre>

<p>Here is the table where the keyWords and countr are stored:</p>

<p><img src="https://i.sstatic.net/La7SO.jpg" alt="the DB table"></p>

<p>It just wont go over 4. Android should have a countr of 9 and Java 5.
What do you think did I do wrong?</p>

## Answers
### Answer ID: 18979875
<p>You must specify which row to update in the update query otherwise it will update all the values...and another fault i can see but</p>

<p>I am not sure that<code>($row['keyWord']==$_POST[keyWord])</code> in this code <code>$_POST['keyword']</code> the keyword should be in quotes....Hope it will help</p>

### Answer ID: 18979853
<pre><code>$_POST[keyWord] 
</code></pre>

<p>should be </p>

<pre><code>$_POST['keyWord']
</code></pre>

