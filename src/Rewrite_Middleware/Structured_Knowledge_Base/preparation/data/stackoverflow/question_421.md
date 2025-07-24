# Creating a query with few related tables in Pyramid with SQLAlchemy
[Link to question](https://stackoverflow.com/questions/25529546/creating-a-query-with-few-related-tables-in-pyramid-with-sqlalchemy)
**Creation Date:** 1409148886
**Score:** 2
**Tags:** python, sql, postgresql, sqlalchemy, pyramid
## Question Body
<p>I have defined few tables in Pyramid like this:</p>

<pre><code># coding: utf-8
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Integer, Float, DateTime, ForeignKey, ForeignKeyConstraint, String, Column
from sqlalchemy.orm import scoped_session, sessionmaker, relationship, backref,
from zope.sqlalchemy import ZopeTransactionExtension

DBSession = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))
Base = declarative_base()


class Codes(Base):
    __tablename__ = 'Code'
    __table_args__ = {u'schema': 'Locations'}

    id = Column(Integer, nullable=False)
    code_str = Column(String(9), primary_key=True)
    name = Column(String(100))

    incoming = relationship(u'Voyages', primaryjoin='Voyage.call == Codes.code_str', backref=backref('Code'))


class Locations(Base):
    __tablename__ = 'Location'
    __table_args__ = {u'schema': 'Locations'}

    unit_id = Column(ForeignKey(u'Structure.Definition.unit_id', ondelete=u'RESTRICT', onupdate=u'CASCADE'), primary_key=True, nullable=False)
    timestamp = Column(DateTime, primary_key=True, nullable=False)
    longitude = Column(Float)
    latitude = Column(Float)


class Voyages(Base):
    __tablename__ = 'Voyage'
    __table_args__ = (ForeignKeyConstraint(['unit_id', 'Voyage_id'], [u'Locations.Voyages.unit_id', u'Locations.Voyages.voyage_id'], ondelete=u'RESTRICT', onupdate=u'CASCADE'), {u'schema': 'Locations'}
    )

    uid = Column(Integer, primary_key=True)
    unit_id = Column(Integer)
    voyage_id = Column(Integer)
    departure = Column(ForeignKey(u'Locations.Code.code_str', ondelete=u'RESTRICT', onupdate=u'CASCADE'))
    call = Column(ForeignKey(u'Locations.Code.code_str', ondelete=u'RESTRICT', onupdate=u'CASCADE'))
    departure_date = Column(DateTime)

    voyage_departure = relationship(u'Codes', primaryjoin='Voyage.departure == Codes.code_str')
    voyage_call = relationship(u'Codes', primaryjoin='Voyage.call == Codes.code_str')


class Definitions(Base):
    __tablename__ = 'Definition'
    __table_args__ = {u'schema': 'Structure'}

    unit_id = Column(Integer, primary_key=True)
    name = Column(String(90))
    type = Column(ForeignKey(u'Structure.Type.id', ondelete=u'RESTRICT', onupdate=u'CASCADE'))

    locations = relationship(u'Locations', backref=backref('Definition'))
    dimensions = relationship(u'Dimensions', backref=backref('Definition'))
    types = relationship(u'Types', backref=backref('Definition'))
    voyages = relationship(u'Voyages', backref=backref('Definition'))


class Dimensions(Base):
    __tablename__ = 'Dimension'
    __table_args__ = {u'schema': 'Structure'}

    unit_id = Column(ForeignKey(u'Structure.Definition.unit_id', ondelete=u'RESTRICT', onupdate=u'CASCADE'), primary_key=True, nullable=False)
    length = Column(Float)


class Types(Base):
    __tablename__ = 'Type'
    __table_args__ = {u'schema': 'Structure'}

    id = Column(SmallInteger, primary_key=True)
    type_name = Column(String(255))
    type_description = Column(String(255))
</code></pre>

<p>What I am trying to do here is to find a specific row from <code>Codes</code> table (filter it by <code>code_str</code>) and get all related tables in return, but under the condition that <code>Location</code> table returns only the last row by <code>timestamp</code>, <code>Voyage</code> table must return only the last row by <code>departure</code>, and it must have all information from <code>Definitions</code> table.</p>

<p>I started to create a query from the scratch and came across something like this:</p>

<pre><code>string_to_search = request.matchdict.get('code')

sub_dest = DBSession.query(func.max(Voyage.departure).label('latest_voyage_timestamp'), Voyage.unit_id, Voyage.call.label('destination_call')).\
    filter(Voyage.call== string_to_search).\
    group_by(Voyage.unit_id, Voyage.call).\
    subquery()

query = DBSession.query(Codes, Voyage).\
    join(sub_dest, sub_dest.c.destination_call == Codes.code_str).\
    outerjoin(Voyage, sub_dest.c.latest_voyage_timestamp == Voyage.departure_date)
</code></pre>

<p>but I have notice that when I iterate through my results (like <code>for code, voyage in query</code>) I am actually iterating every <code>Voyage</code> I get in return. In theory it is not a big problem for me but I am trying to construct some json response with basic information from <code>Codes</code> table which would include all possible <code>Voyages</code> (if there is any at all).
For example:</p>

<pre><code>code_data = {}
all_units = []

for code, voyage in query:
    if code_data is not {}:
        code_data = {
            'code_id': code.id,
            'code_str': code.code_str,
            'code_name': code.name,
        }

    single_unit = {
        'unit_id': voyage.unit_id,
        'unit_departure': str(voyage.departure_date) if voyage.departure_date else None,
    }
    all_units.append(single_unit)

return {
    'code_data':  exception.message if exception else code_data,
    'voyages': exception.message if exception else all_units,
}
</code></pre>

<p>Now, this seems a bit wrong because I don't like rewriting this <code>code_data</code> in each loop, so I put <code>if code_data is not {}</code> line here, but I suppose it would be much better (logical) to iterate in a way similar to this:</p>

<pre><code>for code in query:
    code_data = {
        'code_id': code.id,
        'code_str': code.code_str,
        'code_name': code.name,
    }
    for voyage in code.voyages:
        single_unit = {
            'unit_id': voyage.unit_id,
            'unit_departure': str(voyage.departure) if voyage.departure else None,
        }
        all_units.append(single_unit)

return {
    'code_data':  exception.message if exception else code_data,
}
</code></pre>

<p>So, to get only single <code>Code</code> in return (since I queried the db for that specific <code>Code</code>) which would then have all <code>Voyages</code> related to it as a nested value, and of course, in each <code>Voyage</code> all other information related to <code>Definition</code> of the particular <code>Unit</code>...</p>

<p>Is my approach good at all in the first place, and how could I construct my query in order to iterate it in this second way?</p>

<p>I'm using Python 2.7.6, SQLAlchemy 0.9.7 and Pyramid 1.5.1 with Postgres database.</p>

<p>Thanks!</p>

## Answers
### Answer ID: 25570355
<p>Try changing the outer query like so:</p>

<pre><code>query = DBSession.query(Codes).options(contains_eager('incoming')).\
    join(sub_dest, sub_dest.c.destination_call == Codes.code_str).\
    outerjoin(Voyage, sub_dest.c.latest_voyage_timestamp == Voyage.departure_date)
</code></pre>

<p>In case of problems, try calling the options(...) part like so:</p>

<pre><code>(...) .options(contains_eager(Codes.incoming)). (...)
</code></pre>

<p>This should result in a single <code>Codes</code> instance being returned with <code>Voyages</code> objects accessible via the relationship you've defined (<code>incoming</code>), so you could proceed with:</p>

<pre><code>results = query.all()
for code in results:
    print code 
    # do something with code.incoming
    # actually, you should get only one code so if it proves to work, you should 
    # use query.one() so that in case something else than a single Code is returned,
    # an exception is thrown
</code></pre>

<p>of course you need an import, e.g.: <code>from sqlalchemy.orm import contains_eager</code></p>

