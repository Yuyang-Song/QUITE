# How do I properly test my database performance with high load demand?
[Link to question](https://stackoverflow.com/questions/1602475/how-do-i-properly-test-my-database-performance-with-high-load-demand)
**Creation Date:** 1256147833
**Score:** 4
**Tags:** database-performance, sybase-asa
## Question Body
<p>I have found a lot of topics about stress-testing web application.</p>

<p>My goals are different, it's to test only database (sybase sql anywhere 9).</p>

<p><strong>What I need:</strong></p>

<ul>
<li>Some tool to give a diagnostic of all sqls and find a bottleneck. I wish I could macro-view the entire system easily.</li>
<li>Best practices to design/build a good sql queries.</li>
</ul>

<p><strong>The system issues are:</strong></p>

<ul>
<li>20GB database size.</li>
<li>2-5 request per second</li>
<li>Thousands sql spread in the code (this messy can be solved only rewriting the system).</li>
</ul>

## Answers
### Answer ID: 1603121
<p>The quickest way would actually be to upgrade your SQL Anywhere to v10 or (better) v11, as the latest releases include a complete performance diagnostic toolset. See the documentation <a href="http://dcx.sybase.com/1101en/dbusage_en11/perform-s-4478058.html" rel="nofollow noreferrer">here</a> for more details.</p>

### Answer ID: 1602546
<p>several open source tools are listed here:</p>

<p><a href="http://www.opensourcetesting.org/performance.php" rel="nofollow noreferrer">http://www.opensourcetesting.org/performance.php</a></p>

