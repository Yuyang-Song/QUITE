# SQLAlchemy Core select query significantly slower than raw SQL
[Link to question](https://stackoverflow.com/questions/52224945/sqlalchemy-core-select-query-significantly-slower-than-raw-sql)
**Creation Date:** 1536331605
**Score:** 3
**Tags:** python, sql-server, performance, sqlalchemy
## Question Body
<p>I've been running a Jupyter Notebook with Python3 code for quite some time. It uses a combination of pyodbc and SQLAlchemy to connect to a few SQL Server databases on my company intranet. The purpose of the notebook is to pull data from an initial SQL Server database and store it in memory as a Pandas dataframe. The file then extracts specific values from one of the columns and sends that list of values through to two different SQL Server databases to pull back a mapping list.</p>

<p>All of this has been working great until I decided to rewrite the raw SQL queries as SQLAlchemy Core statements. I've gone though the process of validating that the SQLAlchemy queries compile to match the raw SQL queries. However, the queries run unimaginably slow. For instance, the initial raw SQL query runs in 25 seconds and the same query rewritten in SQLAlchemy Core runs in 15 minutes! The remaining queries didn't finish even after letting them run for 2 hours.</p>

<p>This could have something to do with how I'm reflecting the existing tables. I even took some time to override the ForeignKey and primary_key on the tables hoping that'd help improve performance. No dice.</p>

<p>I also know "if it ain't broke, don't fix it." But SQLAlchemy just looks so much nicer than a nasty block of hard coded SQL.</p>

<p>Can anyone explain why the SQLAlchemy queries are running so slowly. The SQLAlchemy docs don't give much insight. I'm running SQLAlchemy version 1.2.11.</p>

<pre><code>import sqlalchemy
sqlalchemy.__version__
'1.2.11'
</code></pre>

<p>Here are the relevant lines. I'm excluding the exports for brevity but in case anyone needs to see that I'll be happy to supply it.</p>

<pre><code>engine_dr2 = create_engine("mssql+pyodbc://{}:{}@SER-DR2".format(usr, pwd))
conn = engine_dr2.connect()

metadata_dr2 = MetaData()
bv = Table('BarVisits', metadata_dr2, autoload=True, autoload_with=engine_dr2, schema='livecsdb.dbo')
bb = Table('BarBillsUB92Claims', metadata_dr2, autoload=True, autoload_with=engine_dr2, schema='livecsdb.dbo')

mask = data['UCRN'].str[:2].isin(['DA', 'DB', 'DC'])
dr2 = data.loc[mask, 'UCRN'].unique().tolist()

sql_dr2 = select([bv.c.AccountNumber.label('Account_Number'),
                  bb.c.UniqueClaimReferenceNumber.label('UCRN')])
sql_dr2 = sql_dr2.select_from(bv.join(bb, and_(bb.c.SourceID == bv.c.SourceID,
                                               bb.c.BillingID == bv.c.BillingID)))
sql_dr2 = sql_dr2.where(bb.c.UniqueClaimReferenceNumber.in_(dr2))

mapping_list = pd.read_sql(sql_dr2, conn)
conn.close()
</code></pre>

<p>The raw SQL query that should match <code>sql_dr2</code> and runs lickety split is here:</p>

<pre><code>"""SELECT Account_Number = z.AccountNumber, UCRN = y.UniqueClaimReferenceNumber 
FROM livecsdb.dbo.BarVisits z 
INNER JOIN 
livecsdb.dbo.BarBillsUB92Claims y
ON 
y.SourceID = z.SourceID 
AND 
y.BillingID = z.BillingID
WHERE
y.UniqueClaimReferenceNumber IN ({0})""".format(', '.join(["'" + acct + "'" for acct in dr2]))
</code></pre>

<p>The list <code>dr2</code> typically contains upwards of 70,000 elements. Again, the raw SQL handles this in one minute or less. The SQLAlchemy rewrite has been running for 8+ hours now and still not done.</p>

<p><strong>Update</strong>
Additional information is provided below. I don't own the database or the tables and they contain protected health information so it's not something I can directly share but I'll see about making some mock data.</p>

<pre><code>tables = ['BarVisits', 'BarBillsUB92Claims']
for t in tables:
    print(insp.get_foreign_keys(t))
[], []

for t in tables:
    print(insp.get_indexes(t))
[{'name': 'BarVisits_SourceVisit', 'unique': False, 'column_names': ['SourceID', 'VisitID']}]
[]

for t in tables:
    print(insp.get_pk_constraint(t))
{'constrained_columns': ['BillingID', 'SourceID'], 'name': 'mtpk_visits'}
{'constrained_columns': ['BillingID', 'BillNumberID', 'ClaimID', 'ClaimInsuranceID', 'SourceID'], 'name': 'mtpk_insclaim'}
</code></pre>

<p>Thanks in advance for any insight.</p>

## Answers
### Answer ID: 76222213
<p>I had a similar problem, and was able to fix it by <em>casting the placeholders</em> so the query optimizer knows what to do with them.</p>
<p>In my case, the raw SQL string was faster not because it was itself a raw SQL string but because the parameter was put right into the query and thus the query optimizer was able to infer its type in the process of creating the query plan.</p>
<p>Placeholders, at least in SQL Server, appear to be untyped that is my hunch why queries with them tend to have bad query plans. However, using literal strings isn't a good alternative for security purposes.</p>
<p>My workaround? Casting the parameter in the query itself so the optimizer knows what datatype it is.</p>
<p>So, going from:</p>
<pre><code>select * from mytable where indexed_col = ?
</code></pre>
<p>to</p>
<pre><code>select * from mytable where indexed_col = (cast ? as varchar(100))
</code></pre>
<p>improved performance significantly, matching that of the string literal version.</p>
<p>This also works in SQLAlchemy-built queries, e.g.:</p>
<pre><code>.where(MyTable.indexed_col == cast(&lt;pythonvar&gt; as String(100))
</code></pre>

### Answer ID: 53122737
<p>I figured out how to make the query run fast but have no idea why it's needed with this server and not any others.</p>

<p>Taking</p>

<pre><code>sql_dr2 = str(sql.compile(dialect=mssql.dialect(), compile_kwargs={"literal_binds": True}))
</code></pre>

<p>and sending that through</p>

<pre><code>pd.read_sql(sql_dr2, conn)
</code></pre>

<p>performs the query in about 2 seconds.</p>

<p>Again, I have no idea why that works but it does.</p>

