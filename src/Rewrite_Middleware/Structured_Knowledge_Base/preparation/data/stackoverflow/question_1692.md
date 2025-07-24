# How to display database query results of 100,000 rows or more with HTML?
[Link to question](https://stackoverflow.com/questions/4186384/how-to-display-database-query-results-of-100-000-rows-or-more-with-html)
**Creation Date:** 1289837880
**Score:** 7
**Tags:** python, html, oracle-database, coldfusion
## Question Body
<p>We're rewriting a website used by one of our clients. The user traffic on it is very low, less than 100 unique visitors a week. It's basically just a nice interface to their data in our databases. It allows them to query and filter on different sets of data of theirs.</p>
<p>We're rewriting the site in Python, re-using the same Oracle database that the data is currently on. The current version is written in an old, old version of Coldfusion. One of the things that Coldfusion does well though is displays tons of database records on a single page. It's capable of displaying hundreds of thousands of rows at once without crashing the browser. It uses a Java applet, and it looks like the contents of the rows are perhaps compressed and passed in through the HTML or something. There is a large block of data in the HTML but it's not displayed - it's just rendered by the Java applet.</p>
<p>I've tried several JavaScript solutions but they all hinge on the fact that the data will be present in an HTML table or something along those lines. This causes browsers to freeze and run out of memory.</p>
<p>Does anyone know of any solutions to this situation? Our client loves the ability to scroll through all of this data without clicking a &quot;next page&quot; link.</p>

## Answers
### Answer ID: 4186858
<p>I did something like this a while ago and successfully implemented YUI's data table combined with Django</p>

<p><a href="http://developer.yahoo.com/yui/datatable/" rel="nofollow">http://developer.yahoo.com/yui/datatable/</a></p>

<p>This gives you column sorting, pagination, scrolling and so on. It also allows you to use a variety of data sources such as JSON or XML. </p>

### Answer ID: 4186649
<p>Give a try with Jquery scroll.</p>

<p>Instead of image scroll , you need to have data scroll.</p>

<p>You should poulate data in the divs , instead of images.</p>

<p><a href="http://www.smoothdivscroll.com/#quickdemo" rel="nofollow">http://www.smoothdivscroll.com/#quickdemo</a></p>

<p>It should work. I wish.</p>

<p>You gotta great client anyway  :-)</p>

<p>Something related to your Q</p>

<p><a href="http://www.9lessons.info/2009/07/load-data-while-scroll-with-jquery-php.html" rel="nofollow">http://www.9lessons.info/2009/07/load-data-while-scroll-with-jquery-php.html</a></p>

<p><a href="http://api.jquery.com/scroll/" rel="nofollow">http://api.jquery.com/scroll/</a></p>

### Answer ID: 4186550
<p>I have done just what you are describing using the following (which works very well):</p>

<p><strong><a href="http://www.datatables.net/" rel="noreferrer">jQuery Datatables</a></strong></p>

<p>It enables you to do 'fetch as you scroll' pagination, so you can disable the pagination arrows in favor of a 'forever' scroll.</p>

### Answer ID: 4186534
<p>I'm using <a href="http://www.openrico.org" rel="nofollow">Open Rico</a>'s LiveGrid in a project to display a table with thousands of rows in a page as an endless scrolling table. It has been working really fine so far. The table requests data on demand when you scroll through the rows. The parameters are send as simple GET parameters and the response you have to create on the serverside is simple XML. It should be possible to implement a data backend for a Rico LiveGrid in Python.</p>

### Answer ID: 4186514
<p>Have you tried <a href="http://www.trirand.com/blog/" rel="nofollow">jqGrid</a>?  It can be buggy at times, but overall it's one of the better JavaScript grids.  It's fairly efficient in dealing with large datasets.  It also has a feature whereby the grid retrieves data asynchronously in chunks, but still allows continuous scrolling.  It just asks for more data as the user scrolls down to it.</p>

### Answer ID: 4186505
<p>Most people, in this case, would use a framework. The best documented and most popular framework in Python is Django. It has good database support (including Oracle), and you'll have the easiest time getting help using it since there's such an active Django community.</p>

<p>You can try some other frameworks, but if you're tied to Python I'd recommend Django.</p>

<p>Of course, Jython (if it's an option), would make your job very easy. You could take the existing Java framework you have and just use Jython to build a frontend (and continue to use your Java applet and Java classes and Java server).</p>

<p>The memory problem is an interesting one; I'd be curious to see what you come up with.</p>

