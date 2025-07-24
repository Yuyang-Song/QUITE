# Joomla DB query not executing properly
[Link to question](https://stackoverflow.com/questions/17118790/joomla-db-query-not-executing-properly)
**Creation Date:** 1371253314
**Score:** 0
**Tags:** php, mysql, joomla
## Question Body
<p>I'm creating several custom components and when I delete an entry in one component, it will have to delete the entry with the same key in all the other components.</p>

<p>I thought I was smart and did the following so I don't have to rewrite the code for every single table. This used to work but now it stopped working and I can't figure out why. The main item gets deleted but all the other corresponding items stay put. I checked the database and all the values match up. Is there perhaps a way to check the full query joomla is executing? A print_r of <code>$query</code> gives me nothing readable.</p>

<pre><code>public function deleteRecords($order_ids, $tables) {
    foreach ($tables as $table) {
        foreach ($order_ids as $id) {
            $db = JFactory::getDbo();
            $query = $db-&gt;getQuery(true);
            $query-&gt;delete($db-&gt;quoteName('#__' . $table));
            $query-&gt;where('order_id=' . $id-&gt;order_id);
            $db-&gt;setQuery($query);
            try {
                $result = $db-&gt;query();
            } catch (Exception $e) {

            }
        }
    }
</code></pre>

<p>Where <code>$order_ids</code> and <code>$tables</code> look like this:</p>

<pre><code>Array
(
    [0] =&gt; modeling
    [1] =&gt; exo_product
    [2] =&gt; shoe_production
    [3] =&gt; order_status
    [4] =&gt; hikashop_order
)
Array
(
    [0] =&gt; stdClass Object
        (
            [order_id] =&gt; 50
        )
)
</code></pre>

<p>I probably made some stupid mistake somewhere but I've been on it for 3 hours now and I can't get it to work :(</p>

## Answers
### Answer ID: 17121817
<p>I figured it out.</p>

<p>I was first deleting the main entry and THEN all the other ones. I swapped the order around and now it seems to work. I have no clue why. Perhaps the deleting function was being skipped after the main entry had been cleared or something.</p>

