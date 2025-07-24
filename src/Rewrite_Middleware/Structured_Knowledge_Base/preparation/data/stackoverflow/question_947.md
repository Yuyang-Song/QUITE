# Truncate Magento 1.9 Core URL Rewrites
[Link to question](https://stackoverflow.com/questions/51625151/truncate-magento-1-9-core-url-rewrites)
**Creation Date:** 1533096008
**Score:** 1
**Tags:** sql, database, magento, url-rewriting, magento-1.9
## Question Body
<p>I need to delete/truncate the Magento 1.9 core URL rewrites which are <strong>older than 3 months of core_url_rewrite table</strong> in database.</p>

<p>What's the exact SQL query to achieve this?</p>

## Answers
### Answer ID: 51658737
<p>You can't. There is no information about the date in the <code>core_url_rewrite</code> table. You should also watch out for custom redirects, that won't be recreated automatically. The SQL request to clear out the table, without deleting custom redirects is : </p>

<pre><code>DELETE FROM core_url_rewrite WHERE is_system = 1;
</code></pre>

<p>Once you run a reindex, all the categories and products URLs will be generated again.</p>

### Answer ID: 51635305
<p>You can truncate whole table, Magento will automatically create required ones, just do a reindexing of catalog url rewrites.</p>

