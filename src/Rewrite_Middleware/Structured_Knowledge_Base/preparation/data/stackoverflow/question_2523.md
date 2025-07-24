# Convert datetime to unix timestamp in SQLAlchemy model before executing query?
[Link to question](https://stackoverflow.com/questions/38357352/convert-datetime-to-unix-timestamp-in-sqlalchemy-model-before-executing-query)
**Creation Date:** 1468428104
**Score:** 9
**Tags:** python, sqlalchemy
## Question Body
<p>I am using SQLAlchemy to work with a remote database that uses a strange timestamp format--it stores timestamps as double-precision milliseconds since epoch. I'd like to work with python datetime objects, so I wrote getter/setter methods in my model, following <a href="https://gist.github.com/luhn/4170996" rel="noreferrer">this gist</a>:</p>

<pre><code>from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import synonym
from sqlalchemy.dialects.mysql import DOUBLE
import datetime

Base = declarative_base()
class Table(Base):
    __tablename__ = "table"

    id = Column(Integer, primary_key=True)
    _timestamp = Column("timestamp", DOUBLE(asdecimal=False))

    @property
    def timestamp(self):
        return datetime.datetime.utcfromtimestamp(float(self._timestamp)/1000.)

    @timestamp.setter
    def timestamp(self, dt):
        self._timestamp = float(dt.strftime("%s"))*1000.

    timestamp = synonym('_timestamp', descriptor=timestamp)
</code></pre>

<p>This works great for inserting new rows into the table and working with objects from the table:</p>

<pre><code>&gt;&gt;&gt; table = session.query(Table).first()
&lt;Table id=1&gt;
&gt;&gt;&gt; table.timestamp
datetime.datetime(2016, 6, 27, 16, 9, 3, 320000)
&gt;&gt;&gt; table._timestamp
1467043743320.0
</code></pre>

<p>However, it breaks down when I try to use a datetime in a filter expression:</p>

<pre><code>&gt;&gt;&gt; july = datetime.datetime(2016, 7, 1)
&gt;&gt;&gt; old = session.query(Table).filter(Table.timestamp &lt; july).first()
/lib/python2.7/site-packages/sqlalchemy/engine/default.py:450: Warning: Truncated incorrect DOUBLE value: '2016-07-01 00:00:00'
&gt;&gt;&gt; july_flt = float(july.strftime("%s"))*1000.
&gt;&gt;&gt; old = session.query(Table).filter(Table.timestamp &lt; july_flt).first()
&lt;Table id=1&gt;
</code></pre>

<p>I assume this is because my getter/setter methods apply to instances of the table class, but don't change the behavior of the class itself. I've tried rewriting using a hybrid property instead of a synonym:</p>

<pre><code>from sqlalchemy.ext.hybrid import hybrid_property

class Table(Base):
    __tablename__ = "table"

    id = Column(Integer, primary_key=True)
    _timestamp = Column("timestamp", DOUBLE(asdecimal=False))

    @hybrid_property
    def timestamp(self):
        return datetime.datetime.utcfromtimestamp(float(self._timestamp)/1000.)

    @timestamp.setter
    def timestamp(self, dt):
        self._timestamp = float(dt.strftime("%s"))*1000.
</code></pre>

<p>Again, this works with Table instances, but fails on a query--now it's hitting my getter method when I run the query:</p>

<pre><code>&gt;&gt;&gt; july = datetime.datetime(2016, 7, 1)
&gt;&gt;&gt; old = session.query(Table).filter(Table.timestamp &lt; july).first()
Traceback:
  File "models.py", line 42, in timestamp
    return datetime.datetime.utcfromtimestamp(float(self._timestamp)/1000.)
TypeError: float() argument must be a string or a number
</code></pre>

<p>With the debugger, I can see that the getter is receiving the Table._timestamp class (not a specific Table._timestamp, and not 'july').</p>

<p>I see that I could use the <a href="http://docs.sqlalchemy.org/en/latest/orm/extensions/hybrid.html" rel="noreferrer">hybrid_property.expression</a> decorator to define a SQL expression for converting timestamps into datetime, but what I'd really like is to convert the datetime into a timestamp on the python side, then run the query using timestamps. In other words, I'd like to use datetimes everywhere (including in queries), but have everything done with the microsecond timestamps on the SQL side. How can I do this?</p>

## Answers
### Answer ID: 38360432
<p>You have to use a custom type, which isn't as scary as it sounds.</p>

<pre><code>from sqlalchemy.types import TypeDecorator


class DoubleTimestamp(TypeDecorator):
    impl = DOUBLE

    def __init__(self):
        TypeDecorator.__init__(self, as_decimal=False)

    def process_bind_param(self, value, dialect):
        return value.replace(tzinfo=datetime.timezone.utc).timestamp() * 1000

    def process_result_value(self, value, dialect):
        return datetime.datetime.utcfromtimestamp(value / 1000)
</code></pre>

<p>Then <code>Table</code> becomes:</p>

<pre><code>class Table(Base):
    __tablename__ = "table"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DoubleTimestamp)
</code></pre>

<p>And then everything you mention works. You insert, select and compare with <code>datetime</code>s but it's stored as a <code>DOUBLE</code>.</p>

<p>Here I've used different logic for converting between timestamps since <code>strftime('%s')</code> isn't the correct solution. It's a different question which has been <a href="https://stackoverflow.com/questions/8777753/converting-datetime-date-to-utc-timestamp-in-python/8778548#8778548">answered correctly here</a>. Oh and I noticed you said microseconds but only convert to milliseconds in the code you posted, unless it was a slip of the tongue 😉.</p>

