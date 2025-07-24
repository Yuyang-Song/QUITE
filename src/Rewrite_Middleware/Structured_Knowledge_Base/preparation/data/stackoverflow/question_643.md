# Insert multiple rows to database without using looping
[Link to question](https://stackoverflow.com/questions/34853584/insert-multiple-rows-to-database-without-using-looping)
**Creation Date:** 1453116327
**Score:** 4
**Tags:** python, postgresql, psql
## Question Body
<p>I have following psql query to insert data to database <br/></p>

<pre><code>sql = ("INSERT INTO kart_user (custid,token,cycle,userid,proxyid,salesrepid,users,buyer,salesrep,validfrom,validto,discount,category,ratioOnly,proxy,notified) ""VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s,%s, %s, %s, %s)")
result = self.cur.execute(sql,data)
self.dbconn.commit()
return result
</code></pre>

<p>Now, the problem I facing ,in some case data may contain multiple rows.in this case how can i rewrite my code. 
Note: I don't like to use for loop for data iteration ,please suggest better way to solve this issue.</p>

## Answers
### Answer ID: 34853602
<p><a href="http://initd.org/psycopg/docs/cursor.html#cursor.executemany" rel="nofollow"><code>executemany()</code></a> would help:</p>

<pre><code>result = self.cur.executemany(sql, data)
</code></pre>

<p><code>data</code> in this case should be a list of lists or a list of tuples.</p>

