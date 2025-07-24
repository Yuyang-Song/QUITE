# Find in Entity Framework multiple OR parameters
[Link to question](https://stackoverflow.com/questions/71043307/find-in-entity-framework-multiple-or-parameters)
**Creation Date:** 1644373759
**Score:** 0
**Tags:** c#, linq, entity-framework-core
## Question Body
<p>Suppose I have a product in my database with the description “white shirt size 50”.</p>
<p>The search parameter would be “shirt 50”. I have a more complex query in which I add several “OR”s and I can't get them to work.</p>
<p>I get the following error:</p>
<blockquote>
<p>The LINQ expression</p>
<p>'DbSet()
.Where(p =&gt; p.IdTienda == __request_IdTienda_0)
.Join(
inner: DbSet(),
outerKeySelector: p =&gt; p.IdArticulo,
innerKeySelector: a =&gt; a.Id,
resultSelector: (p, a) =&gt; new TransparentIdentifier&lt;Publicacion, Articulo&gt;(
Outer = p,
Inner = a
))
.Where(ti =&gt; __arrayrequest_1
.Any(s =&gt; ti.Outer.Descripcion.Contains(s)) || ti.Outer.Codigo == __request_Filtro_SearchText_2 || ti.Inner.Codigo == __request_Filtro_SearchText_2 || ti.Inner.CodigoUniversal == __request_Filtro_SearchText_2 || ti.Inner.CodigoUniversalBulto == __request_Filtro_SearchText_2)'</p>
<p>could not be translated. Either rewrite the query in a form that can be translated, or switch to client evaluation explicitly by inserting a call to 'AsEnumerable', 'AsAsyncEnumerable', 'ToList', or 'ToListAsync'. See <a href="https://go.microsoft.com/fwlink/?linkid=2101038" rel="nofollow noreferrer">https://go.microsoft.com/fwlink/?linkid=2101038</a> for more information.</p>
</blockquote>
<p>My code so far is the following:</p>
<pre><code>var arrayrequest = request.Filtro.SearchText.Split().ToList();

var query = from publicacion in _dbContext.Publicaciones.Where(p =&gt; p.IdTienda == request.IdTienda)
            join articulo in _dbContext.Articulos 
                 on publicacion.IdArticulo equals articulo.Id
            where
                arrayrequest.Any(s =&gt; publicacion.Descripcion.Contains(s))
                                 || publicacion.Codigo == request.Filtro.SearchText
                                 || articulo.Codigo == request.Filtro.SearchText
                                 || articulo.CodigoUniversal == request.Filtro.SearchText
                                 || articulo.CodigoUniversalBulto == request.Filtro.SearchText
            select publicacion;

var publicaciones = await query
                          .Include(p =&gt; p.Articulo)
                          .Include(p =&gt; p.TributoPublicacion)
                          .ToArrayAsync();
</code></pre>
<p>The error occurs in the section</p>
<pre><code>arrayrequest.Any(s =&gt; publicacion.Descripcion.Contains(s))`
</code></pre>
<p>I use Entity Framework Core 5 - any help is welcome</p>

## Answers
### Answer ID: 71055155
<p>Don't want to repeat myself, but it is good to show how it can be solved.</p>
<p>EF do not supports complex predicates with local collections and here you need to build expression tree dynamically. This answer has <a href="https://stackoverflow.com/a/70017345/10646316">GetItemsPredicate</a> function which helps in building needed condition.</p>
<p>Then you can rewrite your query in this way:</p>
<pre class="lang-cs prettyprint-override"><code>var arrayrequest = request.Filtro.SearchText.Split().ToList();

var query = from publicacion in _dbContext.Publicaciones.Where(p =&gt; p.IdTienda == request.IdTienda)
            join articulo in _dbContext.Articulos 
                 on publicacion.IdArticulo equals articulo.Id
            select publicacion;
            
var descriptionPredicate = query.GetItemsPredicate(arrayrequest, (publicacion, s) =&gt; publicacion.Descripcion.Contains(s));

Expression&lt;Func&lt;Publicacion, bool&gt;&gt; otherPredicate = publicacion =&gt; publicacion.Codigo == request.Filtro.SearchText
                                 || articulo.Codigo == request.Filtro.SearchText
                                 || articulo.CodigoUniversal == request.Filtro.SearchText
                                 || articulo.CodigoUniversalBulto == request.Filtro.SearchText;

query = query.Where(descriptionPredicate.CombineOr(otherPredicate)));

var publicaciones = await query
    .Include(p =&gt; p.Articulo)
    .Include(p =&gt; p.TributoPublicacion)
    .ToArrayAsync();
</code></pre>

