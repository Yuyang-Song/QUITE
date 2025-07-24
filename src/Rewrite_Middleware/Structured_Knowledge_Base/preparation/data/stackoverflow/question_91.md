# Codeigniter 2 active record — How do I create temporary table to apply second sort order?
[Link to question](https://stackoverflow.com/questions/12518069/codeigniter-2-active-record-how-do-i-create-temporary-table-to-apply-second-so)
**Creation Date:** 1348163449
**Score:** 0
**Tags:** php, sql, database, codeigniter, activerecord
## Question Body
<p>I am in the middle of updating an old site. One of the things I am doing is rewriting the database queries because I have changed the structure of the database to make it more flexible and configurable from the admin.</p>

<p>I previously used the following query (and many others like it), which rely on a temporary table:</p>

<pre><code>$query = $this-&gt;db-&gt;query("SELECT * FROM (SELECT * FROM Links WHERE Cat LIKE ('$c') AND Type LIKE ('%$x%') LIMIT $s, $l) AS T ORDER BY $sort $o");
</code></pre>

<p>Because the queries have got more complicated and now involve a lot of joins I have decided to use active record syntax to make them easier to read. The problem is I cannot find any info on how to make a temporary table to apply a second sort to the data using active record; surely this is possible?</p>

<p>Here is my new query:</p>

<pre><code>    $this-&gt;db
        -&gt;select('*')
        -&gt;from('item_categories')
        -&gt;where('item_categories.cat_id', $c)
        -&gt;or_where('item_categories.parent_id', $c)
        -&gt;or_where('item_categories.gparent_id', $c)
        -&gt;join('item_categories_rel', 'item_categories_rel.cat_id = item_categories.cat_id', 'right')
        -&gt;join('item_entries', 'item_entries.item_id = item_categories_rel.item_id','right')
        -&gt;join('ratings_total', 'ratings_total.item_id = item_entries.item_id')
        -&gt;order_by("item_name", "asc")
        -&gt;limit($l, $s);
        // up to here I want to store as a temporary table then apply next order
        //-&gt;order_by($sort, $o); - ideally I want to apply a second order like this
    $result = $this-&gt;db-&gt;get();
</code></pre>

<p>I would like to apply 'order by' twice but this doesn't work — active record is not that cleaver (or more likeley would be ambiguous), how can I can I do this this within active record? </p>

<p>Any help is much appreciated. Failing the active record approach can anyone suggest how I might apply a sort to the result object?</p>

## Answers
### Answer ID: 12527348
<p>Try check the generated SQL: <code>print $this-&gt;db-&gt;_compile_select()</code>. And a plus information: CI doesn't support subqueries.</p>

