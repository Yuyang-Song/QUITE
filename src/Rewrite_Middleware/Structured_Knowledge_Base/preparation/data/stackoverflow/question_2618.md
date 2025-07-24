# mysqli_fetch_array() expects parameter 1 to be mysqli_result, boolean given in C:\xampp\htdocs\wst\admin1.php on line 297
[Link to question](https://stackoverflow.com/questions/43026888/mysqli-fetch-array-expects-parameter-1-to-be-mysqli-result-boolean-given-in-c)
**Creation Date:** 1490518759
**Score:** -3
**Tags:** php, mysql, mysqli
## Question Body
<p>I want to add 2 rows of a table having numbers in that and I want that sum of 2 rows in a new row of the table </p>

<p>I wrote my code using sql query..</p>

<pre><code>&lt;?php
    $con =  mysqli_connect("localhost", "root", "", "project");
    if(!$con) {
      die('not connected');
    }
    $con =  mysqli_query($con, "SELECT addplace, stayamount, foodamount, airlinesamount, noofdays, totalamount AS sum(stayamount + foodamount + airlinesamount) choose FROM adddetails");

?&gt;
&lt;div class="container"&gt;
  &lt;center&gt;&lt;h2&gt;view packages&lt;/h2&gt;&lt;/center&gt;  
  &lt;table class="table table-bordered"&gt;
    &lt;th&gt;place&lt;/th&gt;
    &lt;th&gt;stay cost&lt;/th&gt;
    &lt;th&gt;food cost&lt;/th&gt;
    &lt;th&gt;flight cost&lt;/th&gt;
    &lt;th&gt;no of days&lt;/th&gt;
    &lt;th&gt;total amount&lt;/th&gt;
    &lt;th&gt;image&lt;/th&gt;

    &lt;?php while($row = mysqli_fetch_array($con, MYSQLI_ASSOC)) { ?&gt;
    &lt;tr&gt;
      &lt;td&gt;&lt;?php echo $row['addplace']; ?&gt;&lt;/td&gt;
      &lt;td&gt;&lt;?php echo $row['stayamount']; ?&gt;&lt;/td&gt;
      &lt;td&gt;&lt;?php echo $row['foodamount'] ;?&gt;&lt;/td&gt;
      &lt;td&gt;&lt;?php echo $row['airlinesamount'] ;?&gt;&lt;/td&gt;
      &lt;td&gt;&lt;?php echo $row['noofdays'] ;?&gt;&lt;/td&gt;
      &lt;td&gt;&lt;?php echo $row['totalamount'] ;?&gt;&lt;/td&gt;
      &lt;td&gt;&lt;?php echo $row['choose'] ;?&gt;&lt;/td&gt;
    &lt;/tr&gt;
    &lt;?php } ?&gt;
  &lt;/table&gt;
&lt;/div&gt;
</code></pre>

<p>and I am getting an error.</p>

<p>Can any one rewrite my <code>sql</code> query or <code>php</code> to add 2 rows containing numbers and I want the sum of that rows in a new row</p>

<p>[database image in phpmyadmin ][1]</p>

<p>[my table in my web page (image)][2]</p>

<p>Thanking You</p>

<p>code for image </p>

<pre><code>&lt;input  name="choose"  class="form-control" type="file" &gt;
</code></pre>

<p>i want the selected image to be displyed in my website as full image,nt the name of the image
what should i do..</p>

<p>[in chose row the image is stored][3]</p>

## Answers
### Answer ID: 43027464
<p>Change your <code>mysql</code> query as below and try. I am considering <code>packageid</code> is <code>primary</code> key</p>

<pre><code>SELECT addplace, stayamount, foodamount, airlinesamount, noofdays, 
    SUM(stayamount + foodamount + airlinesamount) AS totalamount, choose
FROM adddetails GROUP BY packageid
</code></pre>

### Answer ID: 43026975
<p>While it is not source of the problem, it's not good that you are overriding your $con variable with results. Instead use <code>$result</code> to store result of <code>mysqli_query()</code></p>

<pre><code>&lt;?php
    $con = mysqli_connect("localhost", "root", "", "project");
    if(!$con) {
      die('not connected');
    }

    $result = mysqli_query($con, "SELECT addplace, stayamount, foodamount, airlinesamount, noofdays, totalamount AS sum(stayamount + foodamount + airlinesamount) choose FROM adddetails");
    print_r($result); # make sure u have expected output here, if it works delete this line

?&gt;
&lt;div class="container"&gt;
  &lt;center&gt;&lt;h2&gt;view packages&lt;/h2&gt;&lt;/center&gt;  
  &lt;table class="table table-bordered"&gt;
    &lt;th&gt;place&lt;/th&gt;
    &lt;th&gt;stay cost&lt;/th&gt;
    &lt;th&gt;food cost&lt;/th&gt;
    &lt;th&gt;flight cost&lt;/th&gt;
    &lt;th&gt;no of days&lt;/th&gt;
    &lt;th&gt;total amount&lt;/th&gt;
    &lt;th&gt;image&lt;/th&gt;

    &lt;?php while($row = mysqli_fetch_assoc($result)) { ?&gt;
    &lt;tr&gt;
      &lt;td&gt;&lt;?php echo $row['addplace']; ?&gt;&lt;/td&gt;
      &lt;td&gt;&lt;?php echo $row['stayamount']; ?&gt;&lt;/td&gt;
      &lt;td&gt;&lt;?php echo $row['foodamount'] ;?&gt;&lt;/td&gt;
      &lt;td&gt;&lt;?php echo $row['airlinesamount'] ;?&gt;&lt;/td&gt;
      &lt;td&gt;&lt;?php echo $row['noofdays'] ;?&gt;&lt;/td&gt;
      &lt;td&gt;&lt;?php echo $row['totalamount'] ;?&gt;&lt;/td&gt;
      &lt;td&gt;&lt;?php echo $row['choose'] ;?&gt;&lt;/td&gt;
    &lt;/tr&gt;
    &lt;?php } ?&gt;
  &lt;/table&gt;
&lt;/div&gt;
</code></pre>

