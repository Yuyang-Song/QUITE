# Python code executing SQLite query twice against database
[Link to question](https://stackoverflow.com/questions/77044570/python-code-executing-sqlite-query-twice-against-database)
**Creation Date:** 1693917381
**Score:** 0
**Tags:** python, sqlite
## Question Body
<p>I am struggling to understand why my code is producing the query output twice when accessing my database. Essentially I want my query to look up if todays date is present in the database and compare it to the booked_time date part as part of the recorded timestamp. If that is present print that record. As you can see below I encounter a &quot;double output&quot;</p>
<pre><code>from flask import request
import sqlite3

def read_query(query):
    con = sqlite3.connect(&quot;database.db&quot;)
    cur = con.cursor()

    cur.execute(query)
    result = cur.fetchall()
    return result


q1 = &quot;&quot;&quot;
SELECT email,booked_time,strftime('%Y-%m-%d',booked_time) as 'date'
FROM bookings
WHERE date = DATE('2023-09-04');
&quot;&quot;&quot;

print(read_query(q1))
</code></pre>
<p><strong>OUTPUT</strong></p>
<pre><code>devbox:~/web_app_project$ python3 schedule.py 
[('someemail@gmail.com', '2023-09-04 10:00:00', '2023-09-04')]
[('someemail@gmail.com', '2023-09-04 10:00:00', '2023-09-04')]
</code></pre>
<p>I have tried remedying this with con.commit() and con.close() methods I get the same result. I have tried rewriting using the &quot;with&quot; context manager and still get a double output. Has anyone got a solution for this? I am expecting only one record to appear.</p>
<p>As part of @Daviids help troubleshooting:</p>
<pre><code>from flask import Flask, render_template, request
import sqlite3 as sql

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        date = request.form['date']
        hour = request.form['hour']
        minutes = request.form['minutes']

        booked_time = (f&quot;{date} {hour}:{minutes}:00&quot;)
        with sql.connect(&quot;database.db&quot;) as con:
            cur = con.cursor()
            cur.execute(
                &quot;INSERT INTO bookings (name, email, booked_time) VALUES (?, ?, ?)&quot;,
                (name, email, booked_time))
            con.commit()
            msg = &quot;Record successfully added&quot;
    return msg
    con.close()


if __name__ == '__main__':
    app.run
</code></pre>
<p>the data is input through a web form. Below is how the database is created.</p>
<pre><code>import sqlite3

connection = sqlite3.connect('database.db')


with open('schema.sql') as f:
    connection.executescript(f.read())

cur = connection.cursor()


connection.commit()
connection.close()

</code></pre>
<p>The schema file:</p>
<pre><code>CREATE TABLE bookings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    booked_time TIMESTAMP NOT NULL UNIQUE
);
</code></pre>

## Answers
### Answer ID: 77045049
<pre class="lang-py prettyprint-override"><code>import sqlite3

SQLITE_SCRIPT = &quot;&quot;&quot;
-- Create the bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    email TEXT,
    booked_time DATETIME
);

-- Insert some sample data
INSERT INTO bookings (email, booked_time) VALUES
    ('user1@example.com', '2023-09-04 10:00:00'),
    ('user2@example.com', '2023-09-04 14:30:00'),
    ('user3@example.com', '2023-09-05 09:15:00');
&quot;&quot;&quot;

def read_query(query):
    con = sqlite3.connect(&quot;:memory:&quot;)
    # Write the downloaded data into the in-memory database
    con.executescript(SQLITE_SCRIPT)
    cur = con.cursor()

    cur.execute(query)
    result = cur.fetchall()
    return result


q1 = &quot;&quot;&quot;
SELECT email,booked_time,strftime('%Y-%m-%d',booked_time) as 'date'
FROM bookings
WHERE date = DATE('2023-09-04');
&quot;&quot;&quot;

print(read_query(q1))
</code></pre>
<p>I tried this locally and didn't get a double print.
Instead of using a sqlite file I create an in memory database, create the table and insert some data. Can you try this and see if you get the same problem?</p>
<p>Edit: if it still happens I can only think to try from inside the python interpreter</p>
<p>Start it with
<code>devbox:~/web_app_project$ python3</code></p>
<p>then</p>
<pre class="lang-py prettyprint-override"><code>import sqlite3
</code></pre>
<pre class="lang-py prettyprint-override"><code>SQLITE_SCRIPT = &quot;&quot;&quot;
-- Create the bookings table
CREATE TABLE IF NOT EXISTS bookings (
    id INTEGER PRIMARY KEY,
    email TEXT,
    booked_time DATETIME
);

-- Insert some sample data
INSERT INTO bookings (email, booked_time) VALUES
    ('user1@example.com', '2023-09-04 10:00:00'),
    ('user2@example.com', '2023-09-04 14:30:00'),
    ('user3@example.com', '2023-09-05 09:15:00');
&quot;&quot;&quot;
</code></pre>
<pre class="lang-py prettyprint-override"><code>def read_query(query):
    con = sqlite3.connect(&quot;:memory:&quot;)
    # Write the downloaded data into the in-memory database
    con.executescript(SQLITE_SCRIPT)
    cur = con.cursor()

    cur.execute(query)
    result = cur.fetchall()
    return result
</code></pre>
<pre class="lang-py prettyprint-override"><code>q1 = &quot;&quot;&quot;
SELECT email,booked_time,strftime('%Y-%m-%d',booked_time) as 'date'
FROM bookings
WHERE date = DATE('2023-09-04');
&quot;&quot;&quot;
</code></pre>
<pre class="lang-py prettyprint-override"><code>print(read_query(q1))
</code></pre>
<p>Try copying and pasting block by block.</p>

