# SelectMany converts query to Enumerable List. How to avoid it?
[Link to question](https://stackoverflow.com/questions/51903250/selectmany-converts-query-to-enumerable-list-how-to-avoid-it)
**Creation Date:** 1534542387
**Score:** 1
**Tags:** c#, entity-framework, entity-framework-6
## Question Body
<p>I have a MVC controller action that does a database query this way: </p>

<pre><code>var marcaciones = db.Marcacion
</code></pre>

<p>where db is the database context in Entity Framework, and Marcacion is a database table. After that instruction, <code>marcaciones</code> type becomes</p>

<pre><code>System.Data.Entity.DbSet`1[CasinosCloud.Models.Marcacion]
</code></pre>

<p>That allows to add any filter before framework actually executes the query in database.</p>

<p>So far, so good.</p>

<p>However, depending on certain condition, <code>marcaciones</code> variable is assigned in a different way.</p>

<p>The database model is such that <code>marcaciones</code> entity in database is a child of another entity. To get that <code>marcaciones</code> list, I can do this:</p>

<pre><code>var marcaciones = trabajador.ServicioSupervisado.SelectMany(s =&gt; s.Marcacion).AsQueryable();
</code></pre>

<p>As you can infer from instruction above, <code>trabajador</code> is a parent database entity that have many <code>ServicioSupervisado</code> entities, which, in turn, can have many <code>Marcacion</code> entities.</p>

<p>Since <code>marcaciones</code> variable is the same as the <code>marcaciones</code> variable I showed before, I have to convert to <code>Queryable</code>.</p>

<p>After executing the above instruction, <code>marcaciones</code> type becomes;</p>

<pre><code>{System.Linq.Enumerable+&lt;SelectManyIterator&gt;d__17`2
    [CasinosCloud.Models.Servicio,CasinosCloud.Models.Marcacion]}
</code></pre>

<p>That mean query is actually converted to an Enumerable List. </p>

<p>All that works when no other filter is applied. When I add query filter I got problems with the second form. First, the whole web page is slower because all filters are applied in a memory list, not in the database, and second, I have problems with string comparisons, specially when I try to find a text in lowercase when in database is stored in uppercase. Of course, nothing is found in such a case.</p>

<p>I think the problem is reduced by solving the type issue. Why after calling <code>SelectMany</code>, the query is actually executed and converted to an Enumerable List? Is there a way to avoid this and all that to be executed in database? Maybe I should rewrite that instruction not using <code>SelectMany</code>. I tried by using <code>db.Marcacion.Insersect()</code> to do the intersection with this code, but the same problem occurs:</p>

<pre><code>trabajador.ServicioSupervisado.SelectMany(s =&gt; s.Marcacion)
</code></pre>

<p>EDIT: </p>

<p>Query I want to execute in database takes the following form:</p>

<p>For the first way:</p>

<pre><code>SELECT m.*
FROM Marcacion m
</code></pre>

<p>For the second way:</p>

<pre><code>SELECT m.*
FROM Marcacion m
INNER JOIN Servicio s ON s.ServicioId = m.ServicioId
INNER JOIN Trabajador t ON t.TrabajadorId = s.TrabajadorId
WHERE t.TrabajadorId = 1069
</code></pre>

<p>EDIT 2:</p>

<p>For the second way, I tried with:</p>

<pre><code>marcaciones = marcaciones.Where(m =&gt; trabajador.ServicioSupervisado.Any(s =&gt; s.ServicioId == m.ServicioId));
</code></pre>

<p>After that, when query is actually executed in database, this error happens:</p>

<blockquote>
  <p>System.NotSupportedException: 'Unable to create a constant value of type 'CasinosCloud.Models.Servicio'. Only primitive types or enumeration types are supported in this context.'</p>
</blockquote>

## Answers
### Answer ID: 51903612
<p>I solved it by writing the query this way:</p>

<pre><code>var servicios = trabajador.ServicioSupervisado.Select(s =&gt; s.ServicioId);
marcaciones = marcaciones.Where(m =&gt; servicios.Any(s =&gt; s == m.ServicioId));
</code></pre>

<p>That way query is executed when I call <code>ToList()</code>, and works in both cases I told about, being very fast in both since query is run directly in database with all filters applied.</p>

<p>By seeing the database log, the final query executed by Entity Framework was:</p>

<pre><code>SELECT 
    [Extent1].[MarcacionId] AS [MarcacionId], 
    [Extent1].[MonitorId] AS [MonitorId], 
    [Extent1].[TrabajadorId] AS [TrabajadorId], 
    [Extent1].[EmpresaId] AS [EmpresaId], 
    [Extent1].[ServicioId] AS [ServicioId], 
    [Extent1].[MarcacionFechaHora] AS [MarcacionFechaHora], 
    [Extent1].[MarcacionEntradaSalida] AS [MarcacionEntradaSalida], 
    [Extent1].[MarcacionChecksum] AS [MarcacionChecksum], 
    [Extent1].[MarcacionEquipo] AS [MarcacionEquipo], 
    [Extent1].[MarcacionEsManual] AS [MarcacionEsManual], 
    [Extent1].[MarcacionCreadoEn] AS [MarcacionCreadoEn], 
    [Extent1].[MarcacionActualizadoEn] AS [MarcacionActualizadoEn], 
    [Extent1].[MarcacionIndice] AS [MarcacionIndice]
FROM  [dbo].[Marcacion] AS [Extent1]
INNER JOIN [dbo].[Trabajador] AS [Extent2] ON [Extent1].[TrabajadorId] = [Extent2].[TrabajadorId]
WHERE ( EXISTS (SELECT 
    1 AS [C1]
    FROM  ( SELECT 1 AS X ) AS [SingleRowTable1]
    WHERE 3 = [Extent1].[ServicioId]
)) AND ([Extent2].[TrabajadorNombres] + N' ' + [Extent2].[TrabajadorApellidos] LIKE @p__linq__0 ESCAPE N'~') AND ([Extent1].[MarcacionFechaHora] &gt;= @p__linq__1) AND ([Extent1].[MarcacionFechaHora] &lt;= @p__linq__2)
</code></pre>

