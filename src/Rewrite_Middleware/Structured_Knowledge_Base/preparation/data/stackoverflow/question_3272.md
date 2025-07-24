# Automatically filter SQLAlchemy Query on certain fields
[Link to question](https://stackoverflow.com/questions/74826902/automatically-filter-sqlalchemy-query-on-certain-fields)
**Creation Date:** 1671206450
**Score:** 0
**Tags:** python, sqlalchemy
## Question Body
<p>We are working on implementing SQLAlchemy ORM in our existing app. We used to use SQLAlchemy Core but introduced some much additional complexity on top that we ended up rewriting most of the Core components, which was hard to maintain and not scalable.</p>
<p>We are now implementing SQLAlchemy ORM and do not want to make the same mistakes. Currently we are stuck on what the best design pattern is to automatically filter each Query on certain Base attributes. I will elaborate with a minimum working example below.</p>
<p>Assume that we have the following Base class and Entity model, where client_id is assumed to be a valid client ID that is set on each record that is committed to the database. This is the part that works as expected, when we retrieve all records, client_ids are reflected properly.</p>
<pre><code>from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base


class Base:
    __abstract__ = True

    client_id = Column('client_id', Integer)  # assume the client_id has a valid ID for the logged in user at the time a model was initiated and the record stored in the database
    

base = declarative_base(cls=Base, constructor=None)


class Entity(Base):
    __tablename__ = 'entity'

    name = Column(String, nullable=False)

</code></pre>
<p>To filter records for a valid client, we would do something like</p>
<pre><code>session.query(Entity).filter(client_id=1)
</code></pre>
<p>In essence, this works. However, we do not want to bother our programmers with having to filter each resultset on the client_id, since that should happen on each and every query. If our programmers have to do this manually on each query this would also introduce a security issue if this is forgotten and the reviewer didn't pick it up.</p>
<p>What is the best pattern to achieve automatic filtering of the results on a client_id, so that we can do:</p>
<pre><code>session.query(Entity)
</code></pre>
<p>and it would behave exactly as if we specified the filter ourselves?</p>
<p>We have considered overwriting the query method on the session, e.g. as such (pseudo)</p>
<pre><code>def query(...):
   return session.query(Entity).filter(client_id=id)
</code></pre>
<p>We also considered adding a query method to each data model, as such:</p>
<pre class="lang-py prettyprint-override"><code>class Base:
   ... # identical to above

   def query(...):
       return session.query(self).filter(self.client_id=id)
</code></pre>
<p>However both of these solutions don't feel right, as in (1) we have to overwrite Session and in (2) we have to call query on a model instead of a session, which feels like it is not in line with SQLAlchemy best practice.</p>
<p>Are there any patterns we can consider that will enable us to do this without overriding SQLAlchemy components so as to improve maintainability?</p>

