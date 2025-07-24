# PHP MySql Speed optimization in 3 Level menu
[Link to question](https://stackoverflow.com/questions/22349121/php-mysql-speed-optimization-in-3-level-menu)
**Creation Date:** 1394621366
**Score:** 0
**Tags:** php, mysql, performance, menu
## Question Body
<p>I have a nicely working 3 level menu with a HUGE amount of sub-menu points. In the current test version all menu info is read from arrays in PHP and converted into $_GET parameters added to the link of a single display page. On this page the parameters submitted with $_GET are evaluated for the DB Query and the matching content will be displayed. </p>

<p>In order to make the content (including the corresponding menu items) modifyable by the customer, I have to move the menu structure to the database.</p>

<p>Now my question is:</p>

<p>Which is better:</p>

<p>a) On every update of the DB rewrite the file with menu data arrays and keep the menu as it is.</p>

<p>b) Generate temporary arrays of everyxthing when when the menu is displayed</p>

<p>c) generate the submenues only when the higher level is selected</p>

<p>Version a) has proven to have an acceptable page loading for end users (tested with a dummy database online) but not sure about Google ranking (depends much on page loading time). I'm not sure which is faster, reading the menu structure arrays with a MySql Query(version b) or from a file (version a). Data transmitted would be the same, so no difference in loading that. </p>

<p>c) has the advantage of transmitting less data in the beginning, so it would be def faster but would have to reload the page every time the end user selects a menu item. That would produce an annoying delay, which end users are usually not happy about.</p>

<p>Versios b) and c) would produce a lot of DB queries though,  which could be avoided with version a)</p>

<p>So if you have experience with speed optimization - all opinions, comments and suggestions are welcome.</p>

<p>Thank you,
Tina</p>

## Answers
### Answer ID: 22349323
<p>Menu is such a trifle matter that doesn't affect performance at all. Neither for database interaction, nor for amount of data transmitted.</p>

<p>If it's indeed a <em>menu</em> (Not some sort ot nested catalog with 10K+ positions) - just read all the content from database and write all at once.</p>

