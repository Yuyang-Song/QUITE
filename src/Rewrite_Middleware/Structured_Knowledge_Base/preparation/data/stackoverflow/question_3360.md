# Edit SQL query to include aliases, using Python
[Link to question](https://stackoverflow.com/questions/77148178/edit-sql-query-to-include-aliases-using-python)
**Creation Date:** 1695282429
**Score:** 2
**Tags:** python, sql, parsing
## Question Body
<p>I want to use <a href="https://cosette.cs.washington.edu/" rel="nofollow noreferrer">Cosette</a> on a set of SQL queries (let's assume standard SQL, no specific database features).
Unfortunately, Cosette's documentation says:</p>
<blockquote>
<p>Cosette’s SQL syntax are more restricted (say compared to that of MySQL or T-SQL). These restrictions are helpful to precisely express query semantics:</p>
<p>In the select clause, each projected attribute must be named using  as  such as (x.x + x.x) as ax.
In the from clause, each table or subquery is of the form   such as a x.
Each attribute reference must be fully qualified with . such as x.x.</p>
</blockquote>
<p>So I need to find a way to take existing SQL queries and add aliases to all of the tables and columns.</p>
<p>An approach I was thinking about is using one of many different SQL parser Python packages (<a href="https://pypi.org/project/sqlparse/" rel="nofollow noreferrer">sqlparse</a>, <a href="https://pypi.org/project/sqlglot/" rel="nofollow noreferrer">sqlglot</a>, <a href="https://pypi.org/project/sqloxide/" rel="nofollow noreferrer">sqloxide</a>, ...) in order to find the tables and columns (and the structure), and then use one of the SQL query builder Python packages (<a href="https://pypi.org/project/PyPika/" rel="nofollow noreferrer">pypika</a>, <a href="https://pypi.org/project/python-sql/" rel="nofollow noreferrer">python-sql</a>, ...) in order to rewrite the query as is, but with aliases.</p>
<p>However, this approach sounds complicated to implement and with many edge cases. Is there a better direction I can go with?</p>

## Answers
### Answer ID: 77153809
<p>The solution below uses <a href="https://github.com/tobymao/sqlglot/tree/main" rel="nofollow noreferrer"><code>sqlglot</code></a> to convert a SQL query into an abstract syntax tree. The tree is then traversed and at each step, the code performs several checks which form the basis of the alias creation. Please see the commented code below for more details:</p>
<pre class="lang-py prettyprint-override"><code>import sqlglot, string
import sqlglot.expressions as s_ex

def generate_aliases(ast):
   '''
   Take in the SQL AST and generate an infinite stream of possible alias names.
   At each iteration, check if the candidate name does not already exist in the AST
   '''
   ignore = [i.this for i in ast.find_all(s_ex.Identifier)]
   q = ['']
   while q:
     if(current:=q.pop(0)) not in ignore and current: yield current
     for i in string.ascii_lowercase: q += [current + i]

def add_aliases(tree, alias_stream, default_scope = None, scopes = {}):
   def handle_subquery(subquery):
      # function to add alias to subqueries in &quot;from&quot; clause
      if not subquery.alias:
         subquery.args['alias'] = s_ex.TableAlias(this = s_ex.to_identifier(next(alias_stream)))
      add_aliases(subquery.this, alias_stream, default_scope, scopes)
   def handle_table(root):
      # function to add alias to table specified in &quot;from&quot; clause
      scopes[root.this.this] = root.alias if root.alias else next(alias_stream)
      if not root.alias:
          root.args['alias'] = s_ex.TableAlias(this = s_ex.to_identifier(scopes[root.this.this]))
          return root.this.this
   if isinstance(tree, s_ex.Select): # check if tree is a select statement
      if isinstance(root:=tree.args['from'].this, s_ex.Table):
          # if the &quot;from&quot; clause is a table, add alias (if one does not exist)
          default_scope = handle_table(root)
      elif isinstance(root, s_ex.Subquery):
          # if the &quot;from&quot; clause is a subquery, add an alias and traverse it
          handle_subquery(root)
      for i in tree.args.get('joins', []):
          #loop over all table joins, adding aliases and traversing
          if isinstance(i.this, s_ex.Table):
             _ = handle_table(i.this)
          else:
             handle_subquery(i.this)
   if isinstance(tree, s_ex.Column):
      # check if column reference has an alias. If not, add one
      if 'table' not in tree.args:
         tree.args['table'] = s_ex.to_identifier(default_scope if default_scope is not None else next(alias_stream))
      tree.args['table'] = s_ex.to_identifier(scopes.get(tree.args['table'].this, tree.args['table'].this))
   for i, a in enumerate(tree.args.get('expressions', [])):
      if not isinstance(a, sqlglot.expressions.Column) and isinstance(tree, s_ex.Select):
         # check that expression, such as a + b or my_fun(a, b) has an alias
         # if not, add an alias
         tree.args['expressions'][i] = s_ex.Alias(this = a, alias = next(alias_stream))
      add_aliases(a, alias_stream, default_scope, scopes)
   for a, b in getattr(tree, 'args', {}).items():
      # traverse the rest of the tree
      if a not in ['from', 'expressions']:
         for i in ([b] if not isinstance(b, list) else b):
             if not isinstance(i, s_ex.Expression): continue
             add_aliases(i, alias_stream, default_scope, scopes)
</code></pre>
<hr />
<pre><code>def to_cosette(s):
    ast = sqlglot.parse(s)[0]
    add_aliases(ast, generate_aliases(ast))
    return ast.sql()

s1 = &quot;&quot;&quot;
 select a, b, c from tbl where a &gt; 1
&quot;&quot;&quot;
s2 = &quot;&quot;&quot;
 select a, count(*) from tbl where my_fun(b + 1) &gt; a + 3 group by a
&quot;&quot;&quot;
s3 = &quot;&quot;&quot;
 select tbl1.a + tbl2.b * 2, from tbl1 join tbl2 on tbl1.c = tbl2.d
&quot;&quot;&quot;
s4 = &quot;&quot;&quot;
 select a + 1 from (select 1 from generate_series(1, 10, 1)) order by a
&quot;&quot;&quot;
s5 = &quot;&quot;&quot;
select name, sum(status in ('. On', '. Off')) from tbl group by name
&quot;&quot;&quot;
s6 = &quot;&quot;&quot;
with cte as (
  select employee_id, starttime, max(endtime) from time_records
  group by employee_id, starttime
)
select employee_id, starttime, m, array_agg(id)
from cte join time_records on cte.starttime &lt;= time_records.starttime and time_records.endtime &lt;= cte.m
where not exists (select 1 from cte where employee_id = employee_id and starttime &lt; starttime and m &lt;= m)
group by employee_id, starttime, m
&quot;&quot;&quot;

print(to_cosette(s1))
print(to_cosette(s2))
print(to_cosette(s3))
print(to_cosette(s4))
print(to_cosette(s5))
print(to_cosette(s6))
</code></pre>
<p>Output:</p>
<pre><code>SELECT d.a, d.b, d.c FROM tbl AS d WHERE d.a &gt; 1
SELECT c.a, COUNT(*) AS d FROM tbl AS c WHERE MY_FUN(c.b + 1) &gt; c.a + 3 GROUP BY c.a
SELECT e.a + f.b * 2 AS g FROM tbl1 AS e JOIN tbl2 AS f ON e.c = f.d
SELECT f.a + 1 AS e FROM (SELECT 1 AS d FROM GENERATE_SERIES(1, 10, 1) AS c) AS b
SELECT a.name, SUM(a.status IN ('. On', '. Off')) AS b FROM tbl AS a GROUP BY a.name
WITH cte AS (SELECT f.employee_id, f.starttime, MAX(f.endtime) AS g FROM time_records AS f GROUP BY f.employee_id, f.starttime) SELECT a.employee_id, a.starttime, a.m, ARRAY_AGG(a.id) AS c FROM cte AS a JOIN time_records AS b ON a.starttime &lt;= b.starttime AND b.endtime &lt;= a.m WHERE NOT EXISTS(SELECT 1 AS e FROM cte AS d WHERE d.employee_id = d.employee_id AND d.starttime &lt; d.starttime AND d.m &lt;= d.m) GROUP BY d.employee_id, d.starttime, d.m
</code></pre>

