# Avoid SQL injection while inserting a mix of hard-coded and variable values?
[Link to question](https://stackoverflow.com/questions/45858430/avoid-sql-injection-while-inserting-a-mix-of-hard-coded-and-variable-values)
**Creation Date:** 1503568296
**Score:** 3
**Tags:** sql, postgresql, pg-promise
## Question Body
<p>I'm writing database queries with <a href="https://github.com/vitaly-t/pg-promise" rel="nofollow noreferrer">pg-promise</a>. My tables look like this:</p>

<pre><code>                                    Table "public.setting"
│ user_id          │ integer           │ not null                
│ visualisation_id │ integer           │ not null  
│ name             │ character varying │ not null                                  

                                    Table "public.visualisation"
│ visualisation_id │ integer           │ not null                
│ template_id      │ integer           │ not null  
</code></pre>

<p>I want to insert some values into <code>setting</code> - three are hard-coded, and one I need to look up from <code>visualisation</code>. </p>

<p>The following statement does what I need, but must be vulnerable to SQL injection:</p>

<pre><code>var q = "INSERT INTO setting (user_id, visualisation_id, template_id) (" +
        "SELECT $1, $2, template_id, $3 FROM visualisation WHERE id = $2)";
conn.query(q, [2, 54, 'foo']).then(data =&gt; {
    console.log(data); 
});
</code></pre>

<p>I'm aware I should be using <a href="https://github.com/vitaly-t/pg-promise#sql-names" rel="nofollow noreferrer">SQL names</a>, but if I try using them as follows I get <code>TypeError: Invalid sql name: 2</code>:</p>

<pre><code>var q = "INSERT INTO setting (user_id, visualisation_id, template_id) (" +
        "SELECT $1~, $2~, template_id, $3~ FROM visualisation WHERE id = $2)";
</code></pre>

<p>which I guess is not surprising since it's putting the <code>2</code> in double quotes, so SQL thinks it's a column name.</p>

<p>If I try rewriting the query to use <code>VALUES</code> I also get a syntax error:</p>

<pre><code>var q = "INSERT INTO setting (user_id, visualisation_id, template_id) VALUES (" +
        "$1, $2, SELECT template_id FROM visualisation WHERE id = $2, $3)";
</code></pre>

<p>What's the best way to insert a mix of hard-coded and variable values, while avoiding SQL injection risks?</p>

## Answers
### Answer ID: 45861537
<p>Your query is fine. I think you know value placeholders ($X parameter) and SQL Names too, but you are a bit confused.</p>

<p>In your query you only assign values to placeholders. The database driver will handle them for you, providing proper escaping and variable substitution.</p>

<p>The <a href="https://www.postgresql.org/docs/9.6/static/sql-prepare.html" rel="nofollow noreferrer">documentation</a> says:</p>

<blockquote>
  <p>When a parameter's data type is not specified or is declared as
  unknown, the type is inferred from the context in which the parameter
  is used (if possible).</p>
</blockquote>

<p>I can't find a source that states what is the default type, but I think the INSERT statement provides enough context to identify the real types.</p>

<p>On the other hand you have to use <a href="https://github.com/vitaly-t/pg-promise#sql-names" rel="nofollow noreferrer">SQL Names</a> when you build your query dinamically. For example you have variable column or table names. They must be inserted through <code>$1~</code> or <code>$1:name</code> style parameters keeping you safe from injection attacks.</p>

