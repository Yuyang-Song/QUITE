# php mysql building a search query at ten tables + different columns
[Link to question](https://stackoverflow.com/questions/13878691/php-mysql-building-a-search-query-at-ten-tables-different-columns)
**Creation Date:** 1355488022
**Score:** 1
**Tags:** php, mysql
## Question Body
<p>I am trying to develop a search page for a website, but cannot come up with a single query.</p>

<p>Here is a list of those ten tables and their fields</p>

<ol>
<li><p><strong>tmp_auction_auto</strong></p>

<p>id order category manufacturer model price price_type location year run run_type doors airbags gear engine horsepower cylinders drivetype fuel color abs electronicwindows climatcontrol disks hatch boardcomputer alarm rightsteer turbo parkingcontrol conditioner leathersalon navigation centrallock chairwarm hydraulics noprice rent exchange customclearance status other contact </p></li>
<li><p><strong>tmp_auction_estate</strong> 
id order type transaction price price_type price_sqm noprice city address area height repair condition project destination land veranda mansard conference stairs_total stair rooms bedrooms balcony sanitary_arr loggia fireplace conditioner garage parking land_destination buildings distance_central_street distance_tbilisi storeroom jacuzzi bathroom shower sauna furniture technique telephone internet generator pool businesscenter ate network inventory wardobe elevator gas hotwater heating intercom cabletv alarmsystem entrancesecurity windowguards security duplex triplex satelite kitchen showcase land_railway land_electricity land_gas land_water land_drainage status other contact </p></li>
<li><p><strong>tmp_auction_other</strong> 
id order title price price_type noprice info contact </p></li>
<li><strong>tmp_branch</strong> 
id lang title content x y </li>
<li><strong>tmp_comments</strong> 
id reply_id path username email title content likes dislikes time admin </li>
<li><p><strong>tmp_news</strong> 
id lang title content date </p></li>
<li><p><strong>tmp_pages</strong>
id lang title content date </p></li>
<li><p><strong>tmp_polls</strong>
id name question answers ip </p></li>
<li><p><strong>tmp_presentation</strong> 
id lang title order </p></li>
<li><p><strong>tmp_sitemap</strong> 
id parent lang title link order</p></li>
</ol>

<p>I know I can write multiple queries for each table with any order (bad practice) and then combine it to a PHP array for output, but I rather need a professional approach to this subject.</p>

<p>P.S. I don't want to use memcache, solr, sphinxs and such libs (server won't support those)</p>

<ul>
<li>I will also appreciate other seach suggestions like content search,etc (website is written in php in mvc pattern with url rewrites and relies on mysql database though)</li>
</ul>

## Answers
### Answer ID: 13878983
<pre><code>I guess you can join these tables and create a view into which the data obtained fom the joined tables can be saved. Now the search must be conducted on this view which will speed up the search.
For eg.
mysql&gt; SELECT CONCAT(UPPER(supplier_name), ' ', supplier_address) FROM suppliers;
+-----------------------------------------------------+
| CONCAT(UPPER(supplier_name), ' ', supplier_address) |
+-----------------------------------------------------+
| MICROSOFT 1 Microsoft Way                           |
| APPLE, INC. 1 Infinate Loop                         |
| EASYTECH 100 Beltway Drive                          |
| WILDTECH 100 Hard Drive                             |
| HEWLETT PACKARD 100 Printer Expressway              |
+-----------------------------------------------------+
CREATE VIEW suppformat AS 
SELECT CONCAT(UPPER(supplier_name), ' ', supplier_address) FROM suppliers;

mysql&gt; SELECT * FROM suppformat;
+-----------------------------------------------------+
| CONCAT(UPPER(supplier_name), ' ', supplier_address) |
+-----------------------------------------------------+
| MICROSOFT 1 Microsoft Way                           |
| APPLE, INC. 1 Infinate Loop                         |
| EASYTECH 100 Beltway Drive                          |
| WILDTECH 100 Hard Drive                             |
| HEWLETT PACKARD 100 Printer Expressway              |
+-----------------------------------------------------+


Please check this link which will give you some idea of views
[http://www.techotopia.com/index.php/An_Introduction_to_MySQL_Views][1]


  [1]: http://www.techotopia.com/index.php/An_Introduction_to_MySQL_Views
</code></pre>

