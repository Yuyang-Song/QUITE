# SQLAlchemy: how to extend hybrid attributes?
[Link to question](https://stackoverflow.com/questions/52662760/sqlalchemy-how-to-extend-hybrid-attributes)
**Creation Date:** 1538732718
**Score:** 2
**Tags:** python, sql-server, sqlalchemy
## Question Body
<p>I'm working with a MSSQL database with no control over the DB setup nor the (read-only) data in it. One table is represented in SQLAlchemy like this:</p>

<pre><code>class pdAnlage(pdBase):
    __tablename__ = "Anlage"
    typ = Column(CHAR(4), primary_key=True)
    nummer = Column(CHAR(4), primary_key=True)
</code></pre>

<p>In accessing the database, I need a property "name" that is just a concatenation of "typ" and "nummer" with a dot between them. So I did this:</p>

<pre><code>    @hybrid_property
    def name(self):
        return self.typ + '.' + self.nummer
</code></pre>

<p>Looks simple and works as expected. There are two caveats though, one general and one special. The general one: The table is quite big, and i'd like to make  queries against Anlage.name, like this:</p>

<pre><code>db.query(Anlage).filter(Anlage.name.like('A%.B'))
db.query(Anlage).filter(Anlage.name == 'X.Y')
</code></pre>

<p>This works but it is inefficient as the SQL server first has to concatenate all "typ" and "nummer" columns of the (large) table before doing the test. So I've defined a classmethods like this one:</p>

<pre><code>    @classmethod
    def name_like(self, pattern):
        p = pattern.split('.', 2)
        if len(p) == 1 or not p[1]:
            return self.typ.like(p[0])
        else:
            return and_(self.typ.like(p[0]), self.nummer.like(p[1]))
</code></pre>

<p>This isn't elegant, but it does the job just fine. It would be nicer to overload "==" and "like()", is there a way to do that?</p>

<p>Now to the special case: Both name and typ columns can contain trailing spaces in the DB. But the name property must not have spaces, especially not before the dot. So I tried to rewrite the name hybrid property like this:</p>

<pre><code>    @hybrid_property
    def name(self):
        return self.typ.rstrip() + '.' + self.nummer.rstrip()
</code></pre>

<p>This doesn't work because SQLAlchemy doesn't know how to translate the rstrip() python method to the MSSQL RTRIM() function. How can I accomplish that?</p>

## Answers
### Answer ID: 52665081
<p>You could implement a <a href="https://docs.sqlalchemy.org/en/latest/orm/extensions/hybrid.html#building-custom-comparators" rel="nofollow noreferrer">custom comparator</a> that handles string operands in a special way (and others as necessary):</p>

<pre><code>from sqlalchemy.ext.hybrid import Comparator

_sep = '.'


def _partition(s):
    typ, sep, nummer = s.partition(_sep)
    return typ, nummer


class NameComparator(Comparator):

    def __init__(self, typ, nummer):
        self.typ = typ
        self.nummer = nummer
        super().__init__(func.rtrim(typ) + _sep + func.rtrim(nummer))

    def operate(self, op, other, **kwgs):
        if isinstance(other, str):
            typ, nummer = _partition(other)
            expr = op(self.typ, typ, **kwgs)

            if nummer:
                expr = and_(expr, op(self.nummer, nummer, **kwgs))

            return expr

        else:
            # Default to using the "slow" method of concatenating first that
            # hides the columns from the index created for the primary key.
            return op(self.__clause_element__(), other, **kwgs)
</code></pre>

<p>and use it with your hybrid attribute:</p>

<pre><code>class pdAnlage(Base):
    __tablename__ = "Anlage"
    typ = Column(CHAR(4), primary_key=True)
    nummer = Column(CHAR(4), primary_key=True)

    @hybrid_property
    def name(self):
        return self.typ.rstrip() + _sep + self.nummer.rstrip()

    @name.comparator
    def name(cls):
        return NameComparator(cls.typ, cls.nummer)
</code></pre>

