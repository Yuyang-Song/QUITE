# SQLAlchemy query/filter does not work
[Link to question](https://stackoverflow.com/questions/46377715/sqlalchemy-query-filter-does-not-work)
**Creation Date:** 1506155981
**Score:** -1
**Tags:** python, postgresql, sqlalchemy
## Question Body
<p>I have created a database called <code>websites2014</code> and three tables <code>cand_elec</code>, <code>sites</code>, and <code>pages</code> under this database through Postgresql. I am now trying to query the table <code>pages</code> and filter by one of its columns <code>uuid</code> but it doesn't work. Below is the code:</p>

<pre><code>import sqlalchemy
from sqlalchemy import create_engine  
from sqlalchemy import Column, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect 

db_string = "postgres://usr:passwd@localhost:5432/websites2014"

db = create_engine(db_string)
Session = sessionmaker(db)  
session = Session()

pages = session.query('pages')  
</code></pre>

<p>The codes above work fine until the next line:</p>

<pre><code>test = pages.filter_by(uuid="1234").first()
</code></pre>

<p>It doesn't work if I change the code to:</p>

<pre><code>test = pages.filter_by("uuid"="1234").first()
</code></pre>

<p>I am new to Postgresql and SQLAlchemy. Can anyone help? Thanks!</p>

<hr>

<h1>EDIT 1</h1>

<p>Below are the new codes I revised:</p>

<pre><code>import sqlalchemy
from sqlalchemy import create_engine  
from sqlalchemy import Column, String  
from sqlalchemy.ext.declarative import declarative_base  
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect

db_string = "postgres://usr:passwd@localhost:5432/websites2014"

db = create_engine(db_string)
Session = sessionmaker(db)  
session = Session()

Base = declarative_base()

class Page(Base):
    __tablename__ = 'polls_question'

    uuid =  Column(String, primary_key=True)  

pages = session.query(Page)  
test = pages.filter_by(uuid=1234).first()
</code></pre>

<p>However, it gives me an error message as: <code>InternalError: (psycopg2.InternalError) current transaction is aborted, commands ignored until end of transaction block
 [SQL: 'SELECT polls_question.uuid AS polls_question_uuid \nFROM polls_question \nWHERE polls_question.uuid = %(uuid_1)s \n LIMIT %(param_1)s'] [parameters: {'uuid_1': 1234, 'param_1': 1}]
</code></p>

<p>If I change the last line to: <code>session.execute("""SELECT * from page WHERE uuid = '1234'""").first()</code></p>

<p>It shows another error message as :<code>InternalError: (psycopg2.InternalError) current transaction is aborted, commands ignored until end of transaction block
 [SQL: "SELECT * from page WHERE uuid = '1234'"]
</code></p>

<p>Thanks for the help again!</p>

<hr>

<h1>EDIT 2</h1>

<p>As the comments below the answer, if I rewrite the codes as:</p>

<pre><code>class Pages(Base):
    __tablename__ = 'pages'

    uuid =  Column(String, primary_key=True)
</code></pre>

<p>so the class' name and the tablename are defined as I defined when creating the table. It should work and the error message will disappear.</p>

## Answers
### Answer ID: 60708016
<p>You are not using the uuid correctly.
Please follow the declaration below.</p>

<pre><code>from sqlalchemy.dialects.postgresql import UUID

...

    uuid = db.Column(
        UUID(as_uuid=True),
        nullable=False,
        index=True,
        unique=True,
        server_default=text("uuid_generate_v4()")
    )

</code></pre>

### Answer ID: 46378287
<p>You are trying to use a query object, but it seems you didn't create a mapped class to instantiate it.</p>

<p><a href="http://docs.sqlalchemy.org/en/latest/orm/query.html?highlight=filter_by#the-query-object" rel="nofollow noreferrer">Query documentation</a></p>

<p><a href="http://docs.sqlalchemy.org/en/latest/orm/tutorial.html#declare-a-mapping" rel="nofollow noreferrer">Mapping documentation</a></p>

<p>You should declare a class <code>Page</code> like the following to use this tool :</p>

<pre><code>from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
Base = declarative_base()

class Page(Base):
    __tablename__ = 'pages'

    uuid =  Column(String, primary_key=True) 
</code></pre>

<p>It doesn't need all columns defined in your table, at least the primary key and the columns you will use after in the filter, or in the output you want to create.</p>

<p>Then you can use it to build the <code>session.query</code> :</p>

<pre><code>pages = session.query(Page)  
test = pages.filter_by(uuid="1234").first()
</code></pre>

<hr>

<p>Maybe it can be easier to create a simple <code>SELECT</code> query statement ?</p>

<pre><code>session.execute("""SELECT * from pages WHERE uuid = '1234'""").first()
</code></pre>

