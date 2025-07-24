# querying and posting to mysql from php. Serialize array and save it to database or create about 15 different columns?
[Link to question](https://stackoverflow.com/questions/12239314/querying-and-posting-to-mysql-from-php-serialize-array-and-save-it-to-database)
**Creation Date:** 1346616044
**Score:** 0
**Tags:** php, mysql, database, database-design
## Question Body
<p>The data will consist of 1 or 2 digit numbers and I can either make a (to my experience) a hectic looking database full of all the primary data plus these extra 15 columns or I could use the serialization function on the array which I'm already going to be keeping these numbers to save room and tidy up the database.</p>

<p><strong>Questions you may have:</strong></p>

<ul>
<li><p>Every query that changes one of these numbers will affect the rest of them.</p></li>
<li><p>I am using php right now along with possibly javascript and ajax, however I will eventually rewrite the project fully or partially in python and or C.  So that serialization function may make things a bit sticky there...</p></li>
<li><p>The information in the database is going to be read and written to by 2 individuals using separate internet connections.  </p></li>
</ul>

<p>If you need an example it would play out as follows:  </p>

<pre><code>row in database is created by php. 
user_1 &amp;&amp; user_2 read. 
user_1 writes. 
user_1 &amp;&amp; user_2 read. 
user_2 writes. 
user_1 &amp;&amp; user_2 read. 
</code></pre>

<p>And so on...  next user_1 would write again.</p>

<p>So if anyone could please give me any assistance..  I am majorly concerned about whether mysql is the best choice for this project; it is basically my only free option.  And to serialize or not to serialize..? (given my personal situation).</p>

<p>Thank you all so much in advanced.</p>

## Answers
### Answer ID: 12241875
<p>PostgreSQL  has great  array support.  You make an  column that is  an array of integer</p>

