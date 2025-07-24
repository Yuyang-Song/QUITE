# magento url rewrite useless?
[Link to question](https://stackoverflow.com/questions/18231923/magento-url-rewrite-useless)
**Creation Date:** 1376483734
**Score:** 3
**Tags:** magento, url-rewriting, indexing
## Question Body
<p><strong>Two points I want to mention.</strong></p>

<p><strong>First Point.</strong>
I noticed a strange behavior, most probably a bug.
I configured a new clean instance of Magento (no other module, so from scratch) and an empty database.
 I created 3 categories below the root one.
And 3 products, one in each category.
Something like:</p>

<pre><code>Cat 1
+ Prod 1
Cat 2
+ Prod 2
Cat 3
+ Prod 3
</code></pre>

<p>If I change the order of the category so "Cat 3" is before "Cat 2" like this:</p>

<pre><code>Cat 1
+ Prod 1
Cat 3
+ Prod 3
Cat 2
+ Prod 2
</code></pre>

<p>I just need to drag and drop "Cat 3" above "cat 2" from the category management screen.
So the "order" number of cat2 and cat3 are actually exchanged.</p>

<p>BUT the url index process reindexes ALL products of ALL categories (URL REWRITE index)!
I analyzed the SQL log, and it actually does an INSERT with every single product in the database.
I see insert in core_url_rewrite for "Prod 1", "Prod 2" and "Prod 3".</p>

<p>This is a bug, because "Cat 3" keeps the same parent category, so:
1) there is no need to rewrite products within "Cat 3" (the product name didn 't change, the category name didn't change!!)
2) there is no need to rewrite products linked to other categories</p>

<p>Actually, by doing a select, I can see that the rows of the core_url_rewrite table are the same (for sure as no name changed! and no association between products and any categories above the products changed!)</p>

<p>Here is one SQL query that I see out of the log file wen I move the category:</p>

<pre><code>        SQL: INSERT INTO `core_url_rewrite` (`store_id`,`category_id`,`product_id`,`id_path`,`request_path`,`target_path`,`is_system`) VALUES (?, ?, ?, ?, ?, ?, ?) ON DUPLICATE KEY UPDATE store_id = VALUES(`store_id`), category_id = VALUES(`category_id`), product_id = VALUES(`product_id`), id_path = VALUES(`id_path`), request_path = VALUES(`request_path`), target_path = VALUES(`target_path`), is_system = VALUES(`is_system`)
BIND: array (
  0 =&gt; '1',
  1 =&gt; NULL,
  2 =&gt; '4',
  3 =&gt; 'product/4',
  4 =&gt; 'testun.html',
  5 =&gt; 'catalog/product/view/id/4',
  6 =&gt; 1,
)
AFF: 0
TIME: 0.0005
</code></pre>

<p>Actually, the worse thing is, it does an insert of a row that already exist, so it actually does not insert anything. The insert failed (you can see "AFF: 0" meaning nothing has been inserted)
It is a waste of time to process each product for nothing, and try to insert something that might be already there!!</p>

<p><strong>Second points</strong>
I found another bug/strange behavior.
If I have 2 products with the same name (it can happen), then the url key is the same (by default).
BTW url key is also the same by default when you duplicate a product to create a new one.</p>

<p>So The reindex process becomes crazy.
eg, 2 products with the name "camera" will have the url rewrting like this:</p>

<pre><code>camera-1.html
camera-2.html
</code></pre>

<p>I'm ok with this.
BUT, if now I reindex everything, it becomes crazy.
it will change the url rewriting of those products (even if I didn't change anything related to those products).
it will update the 2 products like this:</p>

<pre><code>UPDATE camera-1.html  =&gt; camera-3.html 
UPDATE camera-2.html  =&gt; camera-4.html 
</code></pre>

<p>and insert redirection if the setting is enabled (so previous links are not lost), somethign like</p>

<pre><code>INSERT camera-1.html , camera-3.html ,RP
INSERT camera-2.html , camera-4.html , RP
</code></pre>

<p>RP options is about permanent redirect.</p>

<p>So 2 useless updates and 2 useless Insert for nothing.
If I reindex again, I wait the end, and reindex immediately, then Magento does 4 updates, 4 inserts etc.
Why?? No change at all with any data between the reindex :-)</p>

<p>If you have 5 000 products with the same name (like I have), then it's 10 000 updates and 10 000 (real) insert for nothing...
Size of core_url_rewrite increase again and again on a daily basis. Suration is extremely high
Note: I have a good reason to have 5 000 products with exactly the same name :-)
Whatever my reason this looks strange.</p>

<p>Have you already checked this?
Quite easy to check with a fresh installation of magento and log files enabled.</p>

<p><strong>Last thing is</strong>, why do we need the core_url_rewrite table?
This is one of the main cause of performance issue with magento!</p>

<p>4 lines of php code+htaccess url rewrite would do exactly the same job, no need of a DB Table for this (except for custom url rewrite or CMS page).
one method to generate dynamically the url of a product (based on name and category if needed) and one to generate the url of a category.
then htaccess to redirect.
you just need a keyword in the url to know whether it is a link to a product or a category, and its ID.
something like:</p>

<pre><code>my-cat/camera-112-p.html
</code></pre>

<p>htacces URL rewrite detects it's a link to a product (because of -p.htm), it gets the product id out of the url (112) and redirect the user accordingly.
having the product ID might looks ugly or an issue with SEO, but I don't think so (not as bad as you can read).
And it has to be balanced with the big benefit:
1) no huge table anymore
2) no need to reindex this table (this takes hours, like 8 hours, with a lot of magento website). This process can cause a lot of timeout issue, locking etc. </p>

<p>at least this should be possible through an option (or a module).
Note also that you don't even need to care about permanent redirection, since the content (text) within the link does not matter! Just the ID matters.</p>

<p>Does it exist? if yes I will definetely buy it to say "bye-bye" to this complex messy mechanism (with bugs)</p>

<p>any feedback will be hight appreciated.
(especially if you find any rational in the way magento behaves, taken into account the poor performance linked to use/manage this table, so the rationnal has to be highly appreciated :-) )</p>

<p>thanks
Rod</p>

## Answers
### Answer ID: 18237321
<p>Point one and two seem to have been addressed see the notes for EE 1.13.0.2 (released today, CE 1.7 coming soon): <a href="http://www.magentocommerce.com/knowledge-base/entry/ee113-later-release-notes#prod-url-unique" rel="nofollow">http://www.magentocommerce.com/knowledge-base/entry/ee113-later-release-notes#prod-url-unique</a></p>

<p>But, it's worth addressing some of your points.</p>

<ul>
<li>Why do/did URL rewrites work this way? Because that's the way they worked - it's just how they were created/evolved, including the racing rewrite bug you noticed when two products have the same <code>url_key</code>.</li>
<li>Based on a lot of benchmarking and experience, I can state that the <code>core_url_rewrite</code> table is <em>not</em> "the main cause of poor performance in Magento". The reindex process can suck though, no doubt.</li>
<li>The URL rewrite table <em>is</em> necessary for custom rewrites <em>in general</em>. Suggesting that manipulation of server config files (e.g. Apache <em><code>.htaccess</code></em>) to add rewrites fails to consider that Magento is an application which can be modified and extended without direct developer knowledge (e.g. by store owner).</li>
<li>The suggestion to use a pretty-urls <code>mod_rewrite</code> pattern is not tenable for any shop concerned with SEO, and I assure you that the URL path is quite important to ranking/relevance.</li>
</ul>

