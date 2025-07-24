# Creating dataframes from a list of queries with a defined list of names
[Link to question](https://stackoverflow.com/questions/69083754/creating-dataframes-from-a-list-of-queries-with-a-defined-list-of-names)
**Creation Date:** 1630998413
**Score:** 1
**Tags:** python, dataframe
## Question Body
<p>I am trying to run a query which changes the name of different dataframes pulled from an SQL database. I have developed a simple definition to run the query given the name of the SQL file. the for loop is running properly but it will rewrite <strong>Query</strong> to the last observed dataframe from the report function.</p>
<pre><code>def report(query_name):

   df = []

   filename = query_name +'.sql'

   # read the sql file 
   with open(filename, 'r') as query:

        
       connection = sql_server_connection(server = &quot;server&quot;, database = &quot;database&quot;)
       with connection:
            df = pd.read_sql_query(query.read(), connection)
  
   return df

queries = ['name1','name2','name3']

for query in queries:
    query = report(query)
</code></pre>
<p>What I wish to see from this is</p>
<p>name1 = data from report(name1)</p>
<p>name2 = data from report(name2)</p>
<p>name3 = data from report(name3)</p>
<p>Any assistance would be greatly appreciated.</p>

## Answers
### Answer ID: 69084483
<p>Try this</p>
<pre><code>queries = ['name1','name2','name3']
querie_data = {}

for query in queries:
    querie_data[query] = report(query)
</code></pre>
<p>To access the data</p>
<pre><code>querie_data['name1']
</code></pre>

