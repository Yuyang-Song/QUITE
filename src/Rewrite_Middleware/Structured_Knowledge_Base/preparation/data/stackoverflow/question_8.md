# How to intercept &amp; replace SQL in jdbc driver?
[Link to question](https://stackoverflow.com/questions/10210560/how-to-intercept-replace-sql-in-jdbc-driver)
**Creation Date:** 1334756209
**Score:** 1
**Tags:** sql, jdbc, intercept
## Question Body
<p>I have a Java application that I can't change and SQL queries thet it sends to Oracle database leaves much to be desired (to say the least) in terms of performance.</p>

<p>Is there any way to modify SQL before it is sent to DB? </p>

<p>E.g. some jdbc-proxy that would allow to intercept and modify SQL?
Similar question on the net is <a href="http://www.dbforums.com/microsoft-sql-server/1644179-source-code-jdbc.html" rel="nofollow">http://www.dbforums.com/microsoft-sql-server/1644179-source-code-jdbc.html</a> and I've found example of such proxy here <a href="http://code.google.com/p/log4jdbc/" rel="nofollow">http://code.google.com/p/log4jdbc/</a></p>

<p>Is there any better way to intercept and rewrite SQL if I can't change the application itself?</p>

## Answers
### Answer ID: 10210813
<p>I personally haven't tried this but P6spy (http://sourceforge.net/projects/p6spy/) appears to address your needs.</p>

