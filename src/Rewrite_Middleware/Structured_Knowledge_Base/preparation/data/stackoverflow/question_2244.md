# Zend\Db: Select from subquery
[Link to question](https://stackoverflow.com/questions/25606544/zend-db-select-from-subquery)
**Creation Date:** 1409576711
**Score:** 0
**Tags:** mysql, sqlite, zend-framework2, zend-db
## Question Body
<p>I'm porting an application from ZF1 to ZF2 and as part of that I have to rewrite our database mappers.</p>

<p>I'm struggling with this SQL statement:</p>

<pre><code>SELECT full_name, GROUP_CONCAT(value)
FROM (
   SELECT full_name, value
   FROM my_table
   ORDER BY id DESC
   ) as subtable
GROUP BY full_name
ORDER BY full_name DESC;
</code></pre>

<p>The underlying problem I'm trying to solve is that I need to order the results of the sub query before running <code>GROUP_CONCAT</code> and I need it to work for both MySQL and Sqlite. In MySQL I could simply specify the order within the <code>GROUP_CONCAT</code> function, but this is not possible with Sqlite so I need the sub query for it to be compatible with both MySQL and Sqlite.</p>

<p>In ZF1 I could do:</p>

<pre><code>$fromSql = $db-&gt;select()
              -&gt;from('my_table', array('full_name', 'value'))
              -&gt;order('id DESC');

$sql = $db-&gt;select()
          -&gt;from(array(
                'subtable' =&gt; new Zend_Db_Expr('(' . $fromSql . ')')
            ), array(
                'full_name' =&gt; 'full_name',
                'value' =&gt; new Zend_Db_Expr('GROUP_CONCAT(subtable.value)'),
            )
          )
          -&gt;group('full_name')
          -&gt;order('full_name DESC');
</code></pre>

<p>However, using a sub query in the from clause doesn't seem possible with ZF2. Is there some work around for this?</p>

## Answers
### Answer ID: 25623610
<p><strong>EDIT</strong>: Actually, I now see that my query was flawed. It won't work as expected with MySQL, which means I still have to write specialized queries. See <a href="https://stackoverflow.com/questions/5432547/group-concat-change-group-by-order">GROUP_CONCAT change GROUP BY order</a></p>

<hr>

<p>After going through the code of <code>Zend\Db\Sql\Select</code> I found these lines:</p>

<pre><code>if ($table instanceof Select) {
    $table = '(' . $this-&gt;processSubselect($table, $platform, $driver, $parameterContainer) . ')';
} else {
    $table = $platform-&gt;quoteIdentifier($table);
}
</code></pre>

<p>So the answer is actually quite simple, all I had to do was to provide a <code>Zend\Db\Sql\Select</code> object to <code>from()</code>, without wrapping it in a <code>Zend\Db\Sql\Expression</code> like I used to with ZF1.</p>

<p>Code example:</p>

<pre><code>$adapter = $this-&gt;getAdapter(); // Returns Zend\Db\Adapter\Adapter
$sql = new Zend\Db\Sql\Sql($adapter);

$from = $sql-&gt;select()
    -&gt;from(static::$table)
    -&gt;columns(array(
        'full_name',
        'value',
    ))
    -&gt;order('id DESC');

$select = $sql-&gt;select()
    -&gt;from(array(
        'subtable' =&gt; $from,
    ))
    -&gt;columns(array(
        'full_name' =&gt; 'full_name',
        'value' =&gt; new Expression('GROUP_CONCAT(value)'),
    ))
    -&gt;group('full_name')
    -&gt;order('full_name DESC');

$selectString = $sql-&gt;getSqlStringForSqlObject($select);

$resultSet = $adapter-&gt;query($selectString, $adapter::QUERY_MODE_EXECUTE);

return $resultSet-&gt;toArray();
</code></pre>

