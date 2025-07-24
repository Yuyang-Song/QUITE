# Is the PDO Library faster than the native MySQL Functions?
[Link to question](https://stackoverflow.com/questions/9770560/is-the-pdo-library-faster-than-the-native-mysql-functions)
**Creation Date:** 1332161612
**Score:** 12
**Tags:** php, mysql, sql, pdo
## Question Body
<p>I have read several questions regarding this but I fear they may be out of date as newer versions of the PDO libraries have been released since these questions were answered.</p>

<p>I have written a MySQL class that builds queries and escapes parameters, and then returns results based on the query. Currently this class is using the built-in mysql functions.</p>

<p>I am well aware of the advantages of using the PDO Library, e.g. it is compatible with other databases, stored procedures are easier to execute etc... <strong>However, what I would like to know is simply; is using the PDO Library faster then using the mysql built-in functions?</strong></p>

<p>I have just written the equivalent class for MsSQL, so rewriting it to work with all databases would not take me long at all. Is it worth it or is the PDO library slower?</p>

## Answers
### Answer ID: 26290791
<p>My observation is that PDO seems to be less tolerate of many consecutive connections - that is connections being created in a loop.  I know this is bad practice it the first place.  When I was using mysql_* my looped queries seemed to be reasonably fast. However when I switched to PDO I noticed much longer response times for these types of queries.</p>

<p>TL;DR; - If you switch to PDO and you call queries in a PHP loop you may need to rewrite the application to call one single query rather than many consecutive queries.</p>

### Answer ID: 9771068
<p>I found PDO in many situation/projects to be even faster than the more native modules.<br>
Mainly because many patterns/building blocks in a "PDO-application" require less php script driven code and more code is executed in the compiled extension and there <em>is</em> a speed penalty when doing things in the script. Simple, synthetic tests without data and error handling often do not cover this part, which is why (amongst other problems like e.g. measuring inaccuracies) I think "10000x SELECT x FROM foo took 10ms longer" conclusions are missing the point more often than not .<br>
I can't provide you with solid benchmarks and the outcome depends on how the surrounding application handles the data but even synthetic tests usually only show differences so negligible that you better spend your time on optimizing your queries, the MySQL server, the network, ... instead of worrying about PDO's raw performance. Let alone security and error handling ...</p>

