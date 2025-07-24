# Select one Table with different amount of Table Columns
[Link to question](https://stackoverflow.com/questions/19355768/select-one-table-with-different-amount-of-table-columns)
**Creation Date:** 1381737585
**Score:** 4
**Tags:** php, mysql
## Question Body
<p>I want to select a table from my SQL database.
This table can have many different columns, as I'm putting together a dynamic query.</p>

<p>How can I rewrite my <code>fetch_array</code> to a dynamic number of columns?
Here is my current code:</p>

<pre><code>$q = $db_object-&gt;query($query);
$returnstring = '';
while($r = $q-&gt;fetch_array()){
      $returnstring .= '&lt;tr&gt;';
      $returnstring .= '&lt;td&gt;'.$r.'&lt;/td&gt;'; //Here can appear many different columns.
      $returnstring .= '&lt;/tr&gt;'; 
}
</code></pre>

<p>In the query could e.g. two, three, four or more columns of the table show up.</p>

<p>Can I do a <code>foreach</code> or something like this?</p>

## Answers
### Answer ID: 19355826
<p>This will make as many <code>td</code>s as the number of columns in your row.</p>

<pre><code>$q = $db_object-&gt;query($query);
$returnstring = '';
while($r = $q-&gt;fetch_array()){
      $returnstring .= '&lt;tr&gt;';

      foreach($r as $key=&gt;$value)
      {
        $returnstring .= '&lt;td&gt;'.$key.' : value='.$value.'&lt;/td&gt;'; //Here can appear many different columns.
      }


      $returnstring .= '&lt;/tr&gt;'; 
}
</code></pre>

