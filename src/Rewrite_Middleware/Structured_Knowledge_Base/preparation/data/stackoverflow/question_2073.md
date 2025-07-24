# Search through multiple tables
[Link to question](https://stackoverflow.com/questions/18019433/search-through-multiple-tables)
**Creation Date:** 1375453689
**Score:** 0
**Tags:** php, mysql, search
## Question Body
<p>I had a working search function for my news website, but I have been rewriting my code and restructuring my database in order to add more functions. Before, all the info I wanted searched through could be found in one table. Now there is a table for the basic data of a news article, and a second which contains the text (could be multiple rows per article). The first search function was easy:</p>

<pre><code>SELECT * 
FROM pages 
WHERE page_status != '99' 
AND (page_title LIKE '%".mysql_real_escape_string($words)."%' OR page_text LIKE '%".mysql_real_escape_string($words)."%') 
ORDER BY page_onlinedate DESC
</code></pre>

<p>Now I need to query multiple tables, as 'pages.page_text' does not exist anymore. It moved to a second table named 'page_content.content_text', and is linked to 'pages.page_id' with 'page_content.content_page_id'.</p>

<p>I can't find out how to get the results displayed without having duplicates (querying every table once, and as it is possible to have multiple rows in page_content, it could display the same article for example four times if the searched word can be found once in the title and in every text row). I guess it has to be done with table joins, but joins get my really confused.</p>

<p>Once more, my database layout to be clear:</p>

<pre><code>PAGES
page_id
page_title
page_onlinedate
...

PAGE_CONTENT
content_id
content_text
content_page_id 
</code></pre>

<p>Thank you for your help.</p>

## Answers
### Answer ID: 18019587
<p>Please try this:</p>

<pre><code>select p.*, pc.* 
from pages p join page_content pc on p.page_id = pc.content_page_id 
where p.page_status != '99' 
  and (p.page_title like '%" . mysql_real_escape_string($words) . "%' or pc.content_text like '%" . mysql_real_escape_string($words) . "%') 
group by p.page_id 
order by p.page_onlinedate desc;
</code></pre>

### Answer ID: 18019574
<p>Try this:</p>

<pre><code>SELECT * 
FROM   pages 
WHERE  page_status != '99' 
       AND ( page_title LIKE '%".mysql_real_escape_string($words)."%' 
              OR page_id IN (SELECT content_page_id 
                             FROM   page_content 
                             WHERE 
                 page_text LIKE '%".mysql_real_escape_string($words)."%' 
                            ) ) 
ORDER  BY page_onlinedate DESC 
</code></pre>

