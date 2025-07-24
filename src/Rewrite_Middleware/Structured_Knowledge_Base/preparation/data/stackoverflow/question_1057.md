# How can I convert Sqlalchemy ORM query results into a single joined table including relationships?
[Link to question](https://stackoverflow.com/questions/56940978/how-can-i-convert-sqlalchemy-orm-query-results-into-a-single-joined-table-includ)
**Creation Date:** 1562611949
**Score:** 2
**Tags:** python, sqlalchemy
## Question Body
<p>I am woking on an existing Python API for a web app database and would like to give users formatting options for the results of their queries. In some cases, JSON is appropriate and in others CSV. The API is built around the SQLAlchemy declarative ORM and queries in the system generally return ORM instances or lists of instances along with their relationships. Converting this to JSON is straightforward, however I am having trouble retrieving a table-like view to convert the results to CSV. Using SQLAlchemy core operations, or with plain SQL, it is easy to get back the joined table view. I know that behind the scenes SQLAlchemy is constructing the necessary SQL statements and joins to do what I am asking, but it's hidden behind the mapper.</p>

<p>Given that the API I am working with is already set up to query everything declaratively, using ORM classes, how can I get back the rows that were returned by the database before SQLAlchemy performs its magic to map everything back to objects?</p>

<pre class="lang-py prettyprint-override"><code>user_addresses = Table("user_addresses", Base.metadata,
    Column("user_id", Integer, ForeignKey("user.id")),
    Column("address_id", Integer, ForeignKey("address.id"))
)

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    addresses = relationship("Address", secondary=user_addresses, back_populates="users")


class Address(Base):
    __tablename__ = "address"
    id = Column(Integer, primary_key=True, autoincrement=True)
    number = Column(Integer)
    street = Column(String)
    city = Column(String)
    state = Column(String)
    zip = Column(Integer)
    users = relationship("User", secondary=user_addresses, back_populates="addresses")


## configure session, engine, etc.
# get all relationships loaded together
statement = session.query(User).options(joinedload("*"))
# normal orm classes
results = statement.all()
# I want something like
flat_results = statement.table()
</code></pre>

<p>I think something like the above would have to interact with the pre-mapped tables directly, but I'm not sure how to get back to the tables without rewriting the query API for the backend.</p>

## Answers
### Answer ID: 56943176
<p><em>Giving a possible answer to my own question, so if you have something better feel free to respond.</em></p>

<p>The easiest way I have found to achieve this so far is by extracting the actual SQL statement that will be executed by the <code>Session</code> and executing it directly using the <code>execute</code> method:</p>

<pre class="lang-py prettyprint-override"><code>statement = session.query(User).options(joinedload("*"))
results = session.execute(str(statement))
colnames = results.keys()
rows = results.fetchall()
</code></pre>

<p>This way, you can take advantage of all the automatic joinery by SQLAlchemy and still get the full table view of the data.</p>

<p><strong>Edit</strong>:
As pointed out by @IljaEverilä, it is better to call <code>Query.statement</code> to get the final SQL commands with all of the correct argument substitutions and backend specific functionality:</p>

<pre class="lang-py prettyprint-override"><code>statement = session.query(User).options(joinedload("*")).statement
results = session.execute(statement)
colnames = results.keys()
rows = results.fetchall()
</code></pre>

