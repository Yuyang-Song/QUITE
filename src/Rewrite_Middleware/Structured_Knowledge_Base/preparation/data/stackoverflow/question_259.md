# How Do I Compare 2 Records In The Same Table with Wildcard?
[Link to question](https://stackoverflow.com/questions/18281958/how-do-i-compare-2-records-in-the-same-table-with-wildcard)
**Creation Date:** 1376686369
**Score:** 1
**Tags:** mysql, magento, compare, records
## Question Body
<p>I need to compare records in the same mysql magento table. Is there a way to compare 2 records in the same table, by comparing the url_key to the url? I posted the information below that coresponds to what I'm looking for.</p>

<p>I'm hoping this will help out others who work on Magento's Database as well, as I have posted my 2 previous queries as to how I compared 2 mysql tables to make sure the records were created for categories in magento. I have found that Magento will fail to run flat file reindexing if url-keys and urls do not match. I have ran a few checks to make sure that my url's are correct in both my catalog_category_entity_varchar table as well as my core_url_rewrite table. I intially ran:</p>

<p>SELECT * 
FROM <code>catalog_category_entity_varchar</code> c2t
WHERE NOT EXISTS (
    SELECT * 
    FROM <code>core_url_rewrite</code> c 
    WHERE c.category_id = c2t.entity_id
)</p>

<p>to make sure all of our categories are also entered into core_url rewrite. Then I ran another query to make sure that all of the urls in both tables matched with:</p>

<p>SELECT * 
FROM <code>core_url_rewrite</code> c
WHERE NOT EXISTS (
    SELECT * 
    FROM <code>catalog_category_entity_varchar</code> c2t 
    WHERE c2t.<code>entity_id</code> = c.<code>category_id</code>
    AND c2t.<code>value</code> = c.<code>request_path</code><br>
)</p>

<p>Now I would like to run one more query to ensure that the url's on catalog_category_entity_varchar are also correct to it's corresponding url key, but I'm completely stuck on it and have no idea how to write the statement.</p>

<p>Basically the catalog_category_entity_varchar table looks like this:</p>

<p>catalog_category_entity_varchar:<p></p>

<p>Record 1:<br>
value_id:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;68<br>
entity_type_id:&#160;&#160;&#160;&#160;&#160;&#160;3<br>
attribute_id:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;43<br>
store_id:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;0<br>
entity_id:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;10<br>
value:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;shop-by<p></p>

<p>Record 2:<br>
value_id:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;73<br>
entity_type_id:&#160;&#160;&#160;&#160;&#160;&#160;3<br>
attribute_id:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;57<br>
store_id:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;0<br>
entity_id:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;10<br>
value:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;shop-by.html<p></p>

<p>The entity_id is 10 for both records. The attribute ID for url_key is 43 and for the url ID is 57. I imagine that these are what I'll need to use for to identify what I'm comparing.</p>

<p>So basically I'll need to run a query that will matches the entity id's to each other and then compare's the url-key to the url itslef to make sure that it contains the url key. It will have to strip the .html as well as any other part of the url code since records deeper than first level will look something like catalog/shirts/shop-by.html.</p>

<p>Record 3:<br>
value_id:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;637<br>
entity_type_id:&#160;&#160;&#160;&#160;&#160;&#160;3<br>
attribute_id:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;57<br>
store_id:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;0<br>
entity_id:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;88<br>
value:&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;&#160;catalog/shirts/shop-by.html<p></p>

<p>Also, there will be records that also contain this URL-Key, but I'm assuming that since the query will be based on it's primary key (entity_id), we won't have to worry about that.</p>

<p>I apologize if I haven't written this in the correct format, as I'm still new to this forum. I appreciate in advance for the help. If there's anything unclear or more information is needed, please let me know. </p>

## Answers
### Answer ID: 18283756
<p>Check this query, it's a little ugly but it worked as far as I could tell.</p>

<pre><code>SELECT `t1`.*, `t2`.`value` AS `url_path`
FROM `catalog_category_entity_varchar` AS `t1`
LEFT JOIN (
    SELECT `catalog_category_entity_varchar`.`value`,
        `catalog_category_entity_varchar`.`entity_id`,
        `catalog_category_entity_varchar`.`attribute_id`
    FROM `catalog_category_entity_varchar`
) AS `t2`
ON `t1`.`entity_id`=`t2`.`entity_id`
WHERE `t1`.`attribute_id` = 43
AND `t2`.`attribute_id` = 57
AND `t1`.`value` != `t2`.`value`
</code></pre>

