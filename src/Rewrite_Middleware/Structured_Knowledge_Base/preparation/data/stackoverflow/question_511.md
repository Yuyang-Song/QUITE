# Postgresql Python: ignore duplicate key exception
[Link to question](https://stackoverflow.com/questions/29186112/postgresql-python-ignore-duplicate-key-exception)
**Creation Date:** 1426960878
**Score:** 4
**Tags:** python, sql, postgresql, psycopg2
## Question Body
<p>I insert items using psycopg2 in the following way:</p>

<pre><code>cursor = connection.cursor()
for item in items:
    try:
        cursor.execute(
            "INSERT INTO items (name, description) VALUES (%s, %s)  RETURNING id",
            (item[0], item[1])
        )
        id = cursor.fetchone[0]
        if id is not None:
            cursor.execute(
                "INSERT INTO item_tags (item, tag) VALUES (%s, %s)  RETURNING id",
                (id, 'some_tag')
            )    
    except psycopg2.Error:
        connection.rollback()
        print("PostgreSQL Error: " + e.diag.message_primary)
        continue
    print(item[0])
connection.commit()
</code></pre>

<p>Obviously, when an item is already in the database, the <code>duplicate key exception</code> is being thrown. Is there a way to ignore the exception? Is the whole transaction is going to be aborted when the exception is thrown? If yes, then what is the best option to rewrite the query, maybe using batch inserting?</p>

## Answers
### Answer ID: 29564712
<p>from <a href="https://stackoverflow.com/questions/8497886/graceful-primary-key-error-handling-in-python-psycopg2">Graceful Primary Key Error handling in Python/psycopg2</a>:</p>

<blockquote>
  <p>You should rollback transaction on error.</p>
  
  <p>I've added one more try..except..else construction in the code bellow
  to show the exact place where exception will occur.</p>
</blockquote>

<pre><code>try:
    cur = conn.cursor()

    try:
        cur.execute( """INSERT INTO items (name, description) 
                      VALUES (%s, %s)  RETURNING id""", (item[0], item[1]))
    except psycopg2.IntegrityError:
        conn.rollback()
    else:
        conn.commit()

    cur.close() 
except Exception , e:
    print 'ERROR:', e[0]
</code></pre>

