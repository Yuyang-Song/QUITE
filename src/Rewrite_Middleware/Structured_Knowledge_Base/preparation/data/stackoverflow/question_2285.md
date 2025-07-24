# filter sqlalchemy joined query, constructed on parsed input
[Link to question](https://stackoverflow.com/questions/27532525/filter-sqlalchemy-joined-query-constructed-on-parsed-input)
**Creation Date:** 1418841634
**Score:** 3
**Tags:** python, sqlalchemy, pyparsing
## Question Body
<p>I'm stuck with this one: I have adopted <a href="http://github.com/mfrasca/bauble.classic" rel="nofollow">bauble (a program on github)</a> and part of it is meant to specify a query on an sql database. the query language is really three different languages, one of which (filtering as in an SQL query) I am rewriting.</p>

<p>the original author had chosen for pyparsing and I have no reasons for reviewing that choice, other than I do not know pyparsing and I have always had fun with lex and yacc... but I decided I will keep pyparsing, so I'm learning it.</p>

<p>I have (re)written a parser that recognizes the given query, and most grammar categories translate to classes. I suppose the parsing part is quite fine, the point where I'm stuck is where the objects I've created with pyparsing need use SQLAlchemy to query the database, in particular when I'm filtering based on attributes from joined tables.</p>

<p>the relevant part of the grammar, in pyparsing format:</p>

<pre><code>query_expression = Forward()
identifier = Group(delimitedList(Word(alphas, alphanums+'_'),
                                 '.')).setParseAction(IdentifierToken)
ident_expression = (
    Group(identifier + binop + value).setParseAction(IdentExpressionToken)
    | (
        Literal('(') + query_expression + Literal(')')
    ).setParseAction(ParenthesisedQuery))
query_expression &lt;&lt; infixNotation(
    ident_expression,
    [ (NOT_, 1, opAssoc.RIGHT, SearchNotAction),
      (AND_, 2, opAssoc.LEFT,  SearchAndAction),
      (OR_,  2, opAssoc.LEFT,  SearchOrAction) ] )
</code></pre>

<p>and the corresponding classes (the <code>evaluate</code> method of the last two ones is what I don't yet know how to write):</p>

<pre><code>class BinaryLogical(object):
    ## abstract base class. `name` is defined in derived classes
    def __init__(self, t):
        self.op = t[0][1]
        self.operands = t[0][0::2]  # every second object is an operand

    def __repr__(self):
        return "(%s %s %s)" % (self.operands[0], self.name, self.operands[1])


class SearchAndAction(BinaryLogical):
    name = 'AND'

    def evaluate(self, domain, session):
        return self.operands[0].evaluate(domain, session).intersect_all(
            map(lambda i: i.evaluate(domain, session), self.operands[1:]))


class SearchOrAction(BinaryLogical):
    name = 'OR'

    def evaluate(self, domain, session):
        return self.operands[0].evaluate(domain, session).union_all(
            map(lambda i: i.evaluate(domain, session), self.operands[1:]))


class SearchNotAction(object):
    name = 'NOT'

    def __init__(self, t):
        self.op, self.operand = t[0]

    def evaluate(self, domain, session):
        return session.query(domain).except_(self.operand.evaluate(domain, session))

    def __repr__(self):
        return "%s %s" % (self.name, str(self.operand))



class ParenthesisedQuery(object):
    def __init__(self, t):
        self.query = t[1]

    def __repr__(self):
        return "(%s)" % self.query.__repr__()

    def evaluate(self, domain, session):
        return self.query.evaluate(domain, session)


class IdentifierToken(object):
    def __init__(self, t):
        self.value = t[0]

    def __repr__(self):
        return '.'.join(self.value)

    def evaluate(self, domain, session):
        q = session.query(domain)
        if len(self.value) &gt; 1:
            q = q.join(self.value[:-1], aliased=True)
        return q.subquery().c[self.value[-1]]


class IdentExpressionToken(object):
    def __init__(self, t):
        self.op = t[0][1]
        self.operation = {'&gt;': lambda x,y: x&gt;y,
                          '&lt;': lambda x,y: x&lt;y,
                          '&gt;=': lambda x,y: x&gt;=y,
                          '&lt;=': lambda x,y: x&lt;=y,
                          '=': lambda x,y: x==y,
                          '!=': lambda x,y: x!=y,
                      }[self.op]
        self.operands = t[0][0::2]  # every second object is an operand

    def __repr__(self):
        return "(%s %s %s)" % ( self.operands[0], self.op, self.operands[1])

    def evaluate(self, domain, session):
        return session.query(domain).filter(self.operation(self.operands[0].evaluate(domain, session),
                                                           self.operands[1].express()))
</code></pre>

<p>the complete and most up-to-date code for the above snippets is <a href="https://github.com/mfrasca/bauble.classic/blob/master/bauble/test/test_search2.py" rel="nofollow">here</a>.</p>

<p>a couple possible queries:</p>

<pre><code>results = mapper_search.search("plant where accession.species.id=44")
results = mapper_search.search("species where genus.genus='Ixora'")
results = mapper_search.search("species where genus.genus=Maxillaria and not genus.family=Orchidaceae")
</code></pre>

## Answers
### Answer ID: 27730945
<p>I suppose I found a temporarily acceptable answer, but it uses internal information (an underscore-prefixed field) from SQLAlchemy.</p>

<p>the core of the problem was that since I was working with parsed information from the user, I started with something <em>looking like</em> the name of a class, and the <em>name</em> of the relations to navigate. for example in <code>plant where accession.species.id=44</code>, the class name is <code>Plant</code>, and I am filtering on the <code>id</code> of the connected <code>Species</code> object.</p>

<p>the above example might lead one to think that things are rather easy, just a capitalization problem. but we still need to know in which module the <code>Plant</code>, <code>Accession</code>, and <code>Species</code> are to be found.</p>

<p>an other example: <code>family where genera.id!=0</code>. in general, the name of the relation does not need be equal to the name of the class referred to.</p>

<p>The grammar was ok, and I did not need alter it further. the point was (and still partially is) in the interaction with SQLAlchemy, so I had to correct the <code>evaluate</code> methods in the classes <code>IdentifierToken</code> and <code>IdentExpressionToken</code>.</p>

<p>my solution includes this code:</p>

<pre><code>class IdentifierToken(object):
....
    def evaluate(self, env):
        """return pair (query, attribute)

        the value associated to the identifier is an altered query where the
        joinpoint is the one relative to the attribute, and the attribute
        itself.
        """

        query = env.session.query(env.domain)
        if len(self.value) == 1:
            # identifier is an attribute of the table being queried
            attr = getattr(env.domain, self.value[0])
        elif len(self.value) &gt; 1:
            # identifier is an attribute of a joined table
            query = query.join(*self.value[:-1], aliased=True)
            attr = getattr(query._joinpoint['_joinpoint_entity'], self.value[-1])
        return query, attr

class IdentExpressionToken(object):
...
    def evaluate(self, env):
        q, a = self.operands[0].evaluate(env)
        clause = lambda x: self.operation(a, x)
        return q.filter(clause(self.operands[1].express()))
</code></pre>

<p>some points:</p>

<ul>
<li>it was initially not clear to me that the query method did not alter the query invoking it, but that I had to use the returned value.</li>
<li>I'm aliasing the joined query so that it is easy to retrieve the "destination" class of the join operation.</li>
<li>of the aliased joined query, I'm using the field <code>_joinpoint</code>, which looks like non-exposed information.</li>
<li><p><code>query._joinpoint['_joinpoint_entity']</code> is a reference to the class from which I need retrieve the field named in the parsed query. the <code>_joinpoint</code> dictionary looks different on non-aliased queries.</p></li>
<li><p>the still open part of the question is whether there is an 'official' SQLAlchemy way to retrieve this information.</p></li>
</ul>

### Answer ID: 27536824
<p>It seems like the previous developer went to a lot of trouble to create those classes - this is in fact a "best practice" when using pyparsing.  The intent is that these classes, as the output of the parsing process, usually support some behavior of their own, using the parsed elements. In this case, the elements are accessible by name also (another pyparsing "best practice"). Once these classes have been constructed during the parsing process, pyparsing is pretty much out of the picture - any further processing is purely a function of these classes.</p>

<p>I think the goal probably was much as you posit, that there is a method on these classes like <code>results.statement.invoke()</code>.  Look at the methods on these classes and see what they provide for you, especially the top level StatementAction class.  If there is no such method, then that is probably the next step, for you to apply the parsed values in a way that is meaningful to your SQLAlchemy database wrapper.</p>

