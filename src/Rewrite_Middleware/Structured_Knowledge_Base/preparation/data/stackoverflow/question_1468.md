# Adding two values in a select statement where one of the values is coming from a function - codeigniter/php/mysql
[Link to question](https://stackoverflow.com/questions/7727939/adding-two-values-in-a-select-statement-where-one-of-the-values-is-coming-from-a)
**Creation Date:** 1318344467
**Score:** 1
**Tags:** php, mysql, codeigniter, stored-procedures
## Question Body
<p>I have a function that is returning one result "3" and i have another main function that is making a query to the database and within the select statement i need the value to be added to the select statement. </p>

<p>This query returns the one value from the first function:</p>

<pre><code>function insert() {
$siteid = 1;
$field = 3;
$time = "2011-10-11 15:04:56";
$this-&gt;db-&gt;select('Offset_value', 1)
     -&gt;from('offset')
     -&gt;where('siteid', $siteid)
     -&gt;where('Offset_field', $field)
     -&gt;where('time &lt;', $time);
$query = $this-&gt;db-&gt;get()-&gt;result_array();

foreach ($query as $row) {
    echo $row['Offset_value'];
    }
return $query;

}
</code></pre>

<p>Then i need that to calculate in this select statement:</p>

<pre><code>$this-&gt;db-&gt;select("kwh * $dr * $kwp + $this-&gt;insert() AS kwhdata")
         -&gt;from('expected_kwh')
         -&gt;where('direction', $direction)
         -&gt;where('tilt', $tilt)
         -&gt;where('month', $month);
    $query2 = $this-&gt;db-&gt;get()-&gt;result_array();

    return $query2;
</code></pre>

<p>I'm trying to rewrite a stored procedure that was created in mssql and this is how it works there so i'm trying to use the same approach here. </p>

<p>Thanks</p>

## Answers
### Answer ID: 7728005
<p>I think php just doesn't like the $obj->method syntax inside quotes. Try this for that select line:</p>

<pre><code>$this-&gt;db-&gt;select("kwh * $dr * $kwp + ".$this-&gt;insert()." AS kwhdata")
</code></pre>

