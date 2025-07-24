# Codeigniter database errors
[Link to question](https://stackoverflow.com/questions/21555370/codeigniter-database-errors)
**Creation Date:** 1391524691
**Score:** 0
**Tags:** php, mysql, codeigniter
## Question Body
<p>So I'm rewriting our internal intranet to use the CodeIgniter framework.
Up until now, I've been using <code>$this-&gt;db-&gt;affected_rows()</code> to determine whether rows were inserted, updated or deleted. </p>

<p>If this method returns <code>TRUE</code>, then I assume the SQL has succeeded. Unfortunately, this fails when no records were updated.</p>

<p>For example, I want to update all records in the database, if there aren't any records which match the where clause, even though the SQL has actually worked, <code>affected_rows()</code> will return FALSE because nothing was updated.</p>

<p>I've looked on Stackoverflow, and people are suggesting to use <code>$this-&gt;db-&gt;_error_message()</code> and the <code>_error_code()</code> equivalent. From what <strong>I've read, to use these functions, I need to turn off DB_DEBUG, which I don't want to do</strong>, because I'm still rewriting the intranet on a private server, and want to easily view the error message without trawling through log files.</p>

<p>Is there any way to keep <code>db_debug</code> set to <code>true</code>, and call a method which returns TRUE or FALSE based on whether the query was successful or not?</p>

## Answers
### Answer ID: 21555776
<p>You can turn off <code>DB_DEBUG</code> and still view the error messages (if any). </p>

<pre><code>$config['db_debug'] = FALSE;
</code></pre>

<p>...</p>

<pre><code>$this-&gt;db-&gt;query('UPDATE all.tables SET x=1 WHERE y=2');//update all tables; y is never 2

$ar = $this-&gt;db-&gt;affected_rows();

if($ar === 0){
    if($this-&gt;db-&gt;_error_message()){
        //there was a db error; print it
        echo $this-&gt;db-&gt;_error_message();//and error_code if you want
    }else{
        echo "No records affected, also no db error &lt;br&gt;";
        echo $this-&gt;db-&gt;last_query();//see last query if you want
    }
}else{
    echo "$ar rows affected";
}
</code></pre>

