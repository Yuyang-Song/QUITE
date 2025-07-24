# Cannot execute() a query after bindValue() is done in a loop, but executes when bindValue is run standalone for each column name in the table
[Link to question](https://stackoverflow.com/questions/61554698/cannot-execute-a-query-after-bindvalue-is-done-in-a-loop-but-executes-when)
**Creation Date:** 1588395655
**Score:** 1
**Tags:** php, pdo
## Question Body
<p>I have following two blocks of code, serving the same purpose(according to me), but the latter doesn't work as intended.
Following code executes as it was designed to do. All the changes are reflected in the database as anticipated.</p>

<pre><code>$sql = 'INSERT INTO lesson_plan (class_date, v_id_lp) VALUES(:class_date, :v_id_lp)';
$this-&gt;query_new($sql);
$class_date_string = 'class_date';
$id_string = 'v_id_lp';
$class_date = '05-May-2020';
$id = '6';
$this-&gt;stmt-&gt;bindValue(':' . $class_date_string, $class_date);
$this-&gt;stmt-&gt;bindValue(':' . $id_string, $id);
$this-&gt;stmt-&gt;execute();
</code></pre>

<p>But the above mentioned column names after <code>table_name</code> are merely a drop of water in a mighty ocean as compared to other queries in my app and I don't want to to rewrite all the <code>bindValue()</code> repeatedly as above. So, I divised (or tried to) loop, upon which I have been trying to work since yesterday afternoon, with no success. The following code returns the error <code>Warning:  PDOStatement::execute(): SQLSTATE[HY093]: Invalid parameter number: parameter was not defined in 'File path' on 'line number'.</code> </p>

<pre><code>$sql = 'INSERT INTO lesson_plan (class_date, v_id_lp) VALUES(:class_date, :v_id_lp)';
$this-&gt;query_new($sql);
$some_array = ['class_date' =&gt; '06-May-2020','id' =&gt; '6'];
foreach(array_keys($some_array) as $string){
            $this-&gt;stmt-&gt;bindValue(':' . $string, array_values($some_array));
        }
$this-&gt;stmt-&gt;execute();
</code></pre>

<p>I read multiple similar question on stack overflow (some information to those who wish to close my question), but being a beginner I didn't understand any of those answers. Now in case someone please wants to help please do, in case someone does still wish to close the question, feel free to do (as you always do), but know that not all medical students code during lockdown especially when they have no knowledge of coding, at least comment the error in my code before closing my question, it would be a great help.</p>

## Answers
### Answer ID: 61555018
<p>When you bind each item, you are then binding <code>array_values()</code>. Change the loop to...</p>

<pre><code>foreach($some_array as $name =&gt; $value){
    $this-&gt;stmt-&gt;bindValue(':' . $name, $value);
}
</code></pre>

