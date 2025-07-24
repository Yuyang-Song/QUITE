# Triggering Python (from PHP) via MySQL
[Link to question](https://stackoverflow.com/questions/8399677/triggering-python-from-php-via-mysql)
**Creation Date:** 1323173556
**Score:** 4
**Tags:** python, mysql, triggers
## Question Body
<h2>Background</h2>

<p>I am considering various architecture options. While I have used SQL over the years as a query language, I have limited experience with triggers and stored procedures.</p>

<h2>The Problem: Integrating PHP and Python via MySQL</h2>

<p>In the red corner of the boxing ring, I have some off-the-shelf PHP which processes some XML pushed to the server via HTTP, and records it into a MySQL database.</p>

<p>In the blue corner of the ring, I have a daemon written in Python, that is keen to promptly learn of the data that has been pushed, so it can process it, in real time.</p>

<p>The boxing ring itself is Ubuntu (and probably Apache, but not yet confirmed).</p>

<h2>Possible Solutions</h2>

<p>I am considering three different ways of communicating between the processes.</p>

<ol>
<li><p>Totally rewrite the PHP to Python. Probably will take too long to be viable.</p></li>
<li><p>Patch the PHP to have it also write the XML to a socket. Have a Python thread listening to the socket. This seems feasible. It will need to be rewritten every time a new version of the PHP is released. It also seems a little ugly.</p></li>
<li><p>Write an SQL trigger that informs the Python code that the database has been updated, and it can fetch the latest through normal SQL queries. This is a technology I am not familiar with, and hence this question:</p></li>
</ol>

<h2>The Question</h2>

<p><strong>Is there a standard idiom for notifying a running Python program that another process has updated a MySQL table?</strong></p>

<h2>Possible Answers?</h2>

<p>I assume the answer will include MySQL Triggers, but I am happy to be told I am barking up the wrong tree.</p>

<p>From my research so far, I believe one answer would be to trigger the <a href="http://forge.mysql.com/projects/project.php?id=211" rel="nofollow">execution of an arbitrary executable</a> which could then talk via a socket to the main process, but I was hoping there might be something a little more direct - like a call to the SQL API that blocks until a trigger is fired.</p>

## Answers
### Answer ID: 8399763
<p><strong>Solution 4</strong>: Let Python publish a webservice (XMLRPC or SOAP) containing a webmethod that can be called by PHP to tell Python that new data is available. </p>

<p><em>(<a href="http://docs.python.org/library/xmlrpclib.html" rel="nofollow">Python XMLRPC</a> is very ease to use)</em></p>

