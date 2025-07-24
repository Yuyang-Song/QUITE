# Linq to SQL, Join memory list with database result with contains or rewrite query
[Link to question](https://stackoverflow.com/questions/13401707/linq-to-sql-join-memory-list-with-database-result-with-contains-or-rewrite-quer)
**Creation Date:** 1352996321
**Score:** 1
**Tags:** sql, linq, linq-to-sql
## Question Body
<p>Hi guys I have the following query and I trying to write it in linq to sql:</p>

<pre><code>Select * from PlazaI pi
join (
    Select * from PlazaE pe where 
    NOT EXISTS(SELECT 1 FROM PlazaE pe1 
    WHERE pe.Id_plaza = pe1.Id_plaza AND pe1.Fecha &gt; pe.Fecha AND pe1.Fecha &lt; GETDATE() and pe1.Id_Emp != 0) 
) pe on pe.Id_plaza = pieepo.Id_plaza
join Emp e on pe.Id_Emp = e.Id_Emp
join View ct on ct.Id_Nodo = pe.id_nodo
where pi.PlazaIe in ('some value')
</code></pre>

<p>Query is working correctly.</p>

<p>Right now I break into two pieces the queries, 1 for the subquery and other for the joining and with the others tables.</p>

<pre><code> var q1 = (from pe in db.PlazaEmpleados 
                        where !db.PlazaEmpleados.Any
                        (
                         pe1 =&gt; (pe1.Id_plaza.Equals(pe.Id_plaza) &amp;&amp; pe1.Fecha &gt; pe.Fecha &amp;&amp; pe1.Id_Emp != 0 &amp;&amp; pe1.Fecha &gt; DateTime.Now)
                        ) select pe).ToList();
</code></pre>

<p>and for testing purpose I'm joining the first subquery with just one table.</p>

<pre><code>    var q2 = (from pi in db.Context
              join pe in (q1) on pi.Id_plaza equals pe.Id_plaza
              select new MvcApplication1.Models.EmpleadoModel.EmpleadoPlazaVO
              {
                  Id_Nodo = pe.id_nodo,

                  Id_plaza = pi.PlazaSome,
                  Num_Plaza = pi.Id_plaza,
              }); 
</code></pre>

<p>THE PROBLEM is that after I research I realize that Im trying to join a memory table with database table and I'm getting the exception: <strong>“Local sequence cannot be used in LINQ to SQL”</strong> <a href="https://stackoverflow.com/questions/3132981/linq2sql-local-sequence-cannot-be-used-in-linq-to-sql-error">Linq2SQL &quot;Local sequence cannot be used in LINQ to SQL&quot; error</a> , </p>

<p>In some post they are suggesting to Change the ANY method (which I'm using in the first query) for the CONTAINS method, the problem is that I'm comparing some value with the same table, So basically I dont know how to translate my actual query using the Contain.</p>

<p>So, I need help in rewrite the linq to sql query in a better approach or help me building the query with the CONTAING method, Im new in this world of Linq to Sql so I know I have issues with this.</p>

<p>Thanks in advance</p>

<p>--------- EDIT ------</p>

<p>Removing the ToList() Method solve the Exception problem, But now I think my translation is did wrong because I'm getting different result from my SQL query than from Linq2SQL. Any can help me checking this.??? as @ean5533 suggested me I'm creating a new question for the SQL query. <a href="https://stackoverflow.com/questions/13402216/linq-translation-doesnt-give-the-same-results-as-my-sql-query">LINQ translation doesn&#39;t give the same results as my SQL query</a></p>

## Answers
### Answer ID: 13401802
<p>Short answer: remove the <code>.ToList()</code> call from the end of your first query declaration (<code>q1</code>).</p>

<p>When you call <code>ToList()</code> you're materializing the results of that query. Or rather, you're enumerating them. If you remove the <code>ToList</code> call then instead of <code>q1</code> being a <code>List</code> of data, you will instead have an <code>IEnumerable</code> of data, which LINQ can further optimize if joined in another query.</p>

