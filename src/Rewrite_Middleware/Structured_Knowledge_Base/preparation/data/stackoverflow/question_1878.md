# PostgreSQL/performance one general cursor or create for every query
[Link to question](https://stackoverflow.com/questions/10773372/postgresql-performance-one-general-cursor-or-create-for-every-query)
**Creation Date:** 1338115878
**Score:** 1
**Tags:** python, postgresql, cursor, python-db-api
## Question Body
<p>I am building a script to store some data in a database. First time I'm using PostgeSQL and everything goes well and as planned. I was thinking about the usage of the Cursor in PostgreSQl and what if I am making a lot of them while one is enough. But I don't want to pass the cursor to all my SQL functions.</p>

<p>Here's my simplified example.</p>

<pre><code>dbConn, dbCurs = openDataBase(config)
doSomeThing(dbCurs, name, age, listOfJohns)

def doSomething(dbCurs, name, age, listOfPoeple):
  listOfPoeple SQLnrOfPeopleNamed(dbCurs, name, age)
  #here some fine checking if there's a list
  #room for more code. etc. etc.

def SQLnrOfPeopleNamed(dbCurs, inpName, inpAge)
  dbCurs.execute(Some SQL-thingy)
  #check and return result
</code></pre>

<p>dbCurs is the value that is passed on to every function that contains the SQL-query. Now is the dbCurs very PostgreSQL specific. Whenever I change this database to e.q. MySQL I have to rewrite the query function SQLnrOfPeople, and the interfacing to these functions.</p>

<p>I want to have the situation I only have to rewrite the functionality of the SQL function. So, I was thinking about creating a Cursor class in every SQL function and close it. This will result in a more generic interface where only the connection is needed.</p>

<pre><code>dbConn = openDataBase(config)
doSomeThing(dbConn, name, age, listOfJohns)

def doSomething(dbConn, name, age, listOfPoeple):
  listOfPoeple SQLnrOfPeopleNamed(dbConn, name, age)
  #here some fine checking if there's a list
  #room for more code. etc. etc.

def SQLnrOfPeopleNamed(dbConn, inpName, inpAge)
   dbCurs = dbConn.cursor()
   dbCurs.execute(Some SQL-thingy)
   #check and return result
</code></pre>

<p>But I will create and close more cursors. I read in the manual that should be okay and I think this is a good solution. But I am still a bit doubtful about it.</p>

## Answers
### Answer ID: 15761645
<p>In general there's no problem at all with opening and closing multiple cursors sequentially.  You can think of the cursor as basically a pointer to a query result set (and it is a set of pointers to cached data).  Opening a cursor allocates a pointer and closing one frees the memory.</p>

<p>In general I think that logical cleanliness is best here so having one cursor per query is the way to go.</p>

