# PDO - bulk UPDATE statement with question mark parameters, hint?
[Link to question](https://stackoverflow.com/questions/19891238/pdo-bulk-update-statement-with-question-mark-parameters-hint)
**Creation Date:** 1384095757
**Score:** 1
**Tags:** php, parameters, pdo, updates, bulk
## Question Body
<p>I would like to update a MySQL table containing up-to-date currency symbol &amp; value pairs from a given exchange rates service once every 24 hours.</p>

<p>Right now, I do something like this:</p>

<pre><code>foreach ($currencies-&gt;rates as $currency =&gt; $rate) {
    $connection-&gt;addQuery("update/{$currency}", "UPDATE `i18n/currencies` SET `rate` = ? WHERE `code` = ?;", $rate, $currency);
}

$connection-&gt;output();
</code></pre>

<p>I get the <code>$currencies</code> object out from a JSON-encoded response, <code>$connection</code> is a reference to my database connection class.</p>

<p>If I want to create a SQL query group (a class I created to perform bulk commands), the syntax would be like this:</p>

<pre><code>if (!empty($this-&gt;attributes["queries"])) {
    $queries = implode(" ", array_map(function ($input) { return (mb_strpos($input-&gt;attributes["query"], ";") !== false ? $input-&gt;attributes["query"] : "{$input-&gt;attributes["query"]};"); }, $this-&gt;attributes["queries"]));
    $parameters = [];

    foreach ($this-&gt;attributes["queries"] as $query) {
        if (!empty($query-&gt;attributes["parameters"])) {
            $parameters = array_merge($parameters, $query-&gt;attributes["parameters"]);
        }
    }
}
</code></pre>

<p>This way, if I have the following set of queries (with their final values after the query):</p>

<pre><code>UPDATE `i18n/currencies` SET `rate` = ? WHERE `code` = ?; [1.7, AED]
UPDATE `i18n/currencies` SET `rate` = ? WHERE `code` = ?; [2.1, BYR]
UPDATE `i18n/currencies` SET `rate` = ? WHERE `code` = ?; [0.7, EUR]
UPDATE `i18n/currencies` SET `rate` = ? WHERE `code` = ?; [1.1, GBP]
</code></pre>

<p>The final string would be like this:</p>

<pre><code>UPDATE `i18n/currencies` SET `rate` = ? WHERE `code` = ?; UPDATE `i18n/currencies` SET `rate` = ? WHERE `code` = ?; UPDATE `i18n/currencies` SET `rate` = ? WHERE `code` = ?; UPDATE `i18n/currencies` SET `rate` = ? WHERE `code` = ?; [1.7, AED, 2.1, BYR, 0.7, EUR, 1.1, GBP]
</code></pre>

<p>The query is prepared and executed like this:</p>

<pre><code>if ($output = $this-&gt;attributes["references"]["parent"]-&gt;attributes["link"]-&gt;prepare($queries, [\PDO::ATTR_CURSOR =&gt; \PDO::CURSOR_FWDONLY])) {
    $result = ($output-&gt;execute((!empty($parameters) ? $parameters : null)) ? true : false);
}
</code></pre>

<p>But it's not working. I've tried different modifications to my code, but none of them seems to provide me with the solution I'm looking for.</p>

<p>Is it really possible to do BULK updates with PDO passing the parameters like this? Or is it another way I haven't discovered yet? Maybe it's not doable at all and I'm just being stubborn. I could rewrite this update script with single SQL queries, as my connection class will fire them up, from the first to the last one.</p>

<p>Can you give me a hint?</p>

