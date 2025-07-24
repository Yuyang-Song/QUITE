# MultiDimensional Arrays
[Link to question](https://stackoverflow.com/questions/4074744/multidimensional-arrays)
**Creation Date:** 1288668695
**Score:** 2
**Tags:** php, mysql, codeigniter
## Question Body
<p>In Codeigniter, I have the following model</p>

<pre><code>function get_item_history($id)
{  
  //from metadata_history get item_id and corresponding metadata
  $this-&gt;db-&gt;from('metadata_history')-&gt;where(array('id'=&gt;$id, 'current_revision'=&gt; "TRUE"));
  $query = $this-&gt;db-&gt;get();
  $result = $query-&gt;result_array(); //store this in an array

  // loop through the array
  foreach( $result as $key =&gt; $row ) 
  {
   $array = array('item_id'=&gt;$row['item_id'], 'current_revision'=&gt; "TRUE");
   $this-&gt;db-&gt;from('history')-&gt;where($array);
   $query = $this-&gt;db-&gt;get();
   $row['items'] = $query-&gt;result_array(); //
   $result[$key] = $row; 
  }

  return $result;
}
</code></pre>

<p>The problem is that this results in multiple queries to the SQL table increasing the execution time significantly (pagination is not an option)</p>

<p>I want to be able to pass the first query results to the second query as an array, so that I would have only a single go at the database, then rebuild an array from the results.</p>

<p>How should I rewrite this code (the second part)? Will it be faster (I suppose so)?</p>

<p><strong>EDIT</strong></p>

<p>Rebuilding the array from the results is what is flummoxing me.</p>

<p><a href="http://www.phpbuilder.com/board/showthread.php?t=10373847" rel="nofollow">http://www.phpbuilder.com/board/showthread.php?t=10373847</a></p>

<p>this is what I probably want, but am failing the jump</p>

## Answers
### Answer ID: 4084268
<p>OK this took some work, and I also had to do some adjustments in my view</p>

<p>So the problem can be broken down into two main components</p>

<p>1) Pass the results of the first query as an array to the second one using <code>where_in</code></p>

<p>2) Reorder/regroup the results of the first array by  <code>item_id</code></p>

<p>My earlier code was doing the second component implicitly</p>

<p>So here is what I did (limits, offsets, ordering have been cut out to improve readablity)</p>

<pre><code>function get_item_history($id)
{  
 //from metadata_history get item_id and corresponding metadata
 $this-&gt;db-&gt;from('metadata_history')-&gt;where(array('id'=&gt;$id, 'current_revision'=&gt; "TRUE"));
 $query = $this-&gt;db-&gt;get();
 $result_query1 = $query-&gt;result_array(); //store this in an array




foreach ($result_query1 as $key-&gt; $row){
$result[$row['item_id']]['meta_info'] = $row; //the first query contains meta info, that must be passed to the view
$selected_id_array[] = $row['item_id'];  //Create a  array to pass on to the next query
$result[$row['item_id']]['items'] = array(); //declare an array which will hold the results of second query later
}


$this-&gt;db-&gt;select('h.*');
$this-&gt;db-&gt;from('history h');
$this-&gt;db-&gt;where_in('h.item_id', $selected_id_array);
$this-&gt;db-&gt;where(array('h.current_revision' =&gt; 'TRUE'));
$query = $this-&gt;db-&gt;get();

$row = $query-&gt;result_array();


        foreach ($row as $key =&gt; $datarow) {

        $result[$datarow['item_id']]['items'][] = $datarow; //populate the array we declared earlier with results from second query
}




return $result; // Now this variable holds an array which is indexed by item id and contains the results of second query 'grouped' by item_id
 }
</code></pre>

<p>So the number of queries have been cut from ~10 to 2.
On my local machine this saves ~50 msec/page, though I am not sure how this will do for larger databases.</p>

### Answer ID: 4080459
<p>You can use inner query here. It is ideal situation for that - </p>

<pre><code>function get_item_history($id)
{  

// Here the above requirement can be achieved in a single query.

$sql = "select * from history h 
where h.item_id IN (select item_id from metadata_history mh where mh.id = $id 
AND mh.current_revision = TRUE) AND h.current_revision = TRUE";

$result = $this-&gt;db-&gt;query($sql);

//Return whichever column of result you want to return or process result if you want.

$result;
}
</code></pre>

### Answer ID: 4074779
<p>Another option would be to do your wheres in the loop and move the query executation outside of the foreach:</p>

<pre><code>// loop through the array
foreach( $result as $key =&gt; $row )  
{
        $array = array('item_id'=&gt;$row['item_id'], 'current_revision'=&gt; "TRUE");
        $this-&gt;db-&gt;or_where($array);
}

$query = $this-&gt;db-&gt;get();
$row['items'] = $query-&gt;result_array(); //
$result[$key] = $row;
</code></pre>

### Answer ID: 4074753
<p>You should use JOINs to do this. It'll offload the execution of the query to the server. I can't give you too much more detail without knowing how your database is structured, but check out the docs on JOINs:</p>

<p><a href="http://dev.mysql.com/doc/refman/5.0/en/join.html" rel="nofollow">http://dev.mysql.com/doc/refman/5.0/en/join.html</a></p>

<p><a href="http://www.webdesign.org/web-programming/php/mysql-join-tutorial.14876.html" rel="nofollow">http://www.webdesign.org/web-programming/php/mysql-join-tutorial.14876.html</a></p>

<p><a href="http://www.keithjbrown.co.uk/vworks/mysql/mysql_p5.php" rel="nofollow">http://www.keithjbrown.co.uk/vworks/mysql/mysql_p5.php</a></p>

