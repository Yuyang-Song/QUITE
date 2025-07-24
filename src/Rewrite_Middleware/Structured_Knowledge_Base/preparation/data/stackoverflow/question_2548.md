# Pagination not working with htaccess
[Link to question](https://stackoverflow.com/questions/39477332/pagination-not-working-with-htaccess)
**Creation Date:** 1473793774
**Score:** 0
**Tags:** .htaccess, mod-rewrite, pagination
## Question Body
<p>I have this code for a category page rewrite:</p>

<pre><code>RewriteCond %{THE_REQUEST} /category\.php\?catid=([a-zA-Z0-9_-]+) [NC]
RewriteRule ^/store/%1? [R=302,L,NE]
RewriteRule ^store/([a-zA-Z0-9_-]+)/?$ category.php?catid=$1 [L,QSA,NC]
</code></pre>

<p>So <code>www.example.com/store</code>
is the rewrite for <code>store.php</code></p>

<p>and <code>www.example.com/store/lights</code>
is the rewrite for <code>category.php</code></p>

<p>Filters with results are working ok in the search query both for store and category, ex:</p>

<pre><code>http://www.example.com/store/lights?title=phillips&amp;searching=
</code></pre>

<p>The problem is that in the pagination links in both pages are going to the root folder, the href link is like this for both store and category:</p>

<pre><code>http://www.example.com/?title=phillips&amp;searching=&amp;pag=2 
</code></pre>

<p>How can i solve this?</p>

<pre><code>Pagination function:
function paginationStore($query,$per_page=10,$page=1,$url='?'){  
    global $dbc;
    $query = "SELECT COUNT(*) as `num` FROM {$query} as t WHERE prod_activo ='1'";
    $row = mysqli_fetch_array(mysqli_query($dbc,$query));
    $total = $row['num'];
    $adjacents = "2";

    $prevlabel = "&amp;lsaquo; Anterior";
    $nextlabel = "Siguiente &amp;rsaquo;";

    $page = ($page == 0 ? 1 : $page); 
    $start = ($page - 1) * $per_page;                             

    $prev = $page - 1;                       
    $next = $page + 1;

    $lastpage = ceil($total/$per_page);

    $lpm1 = $lastpage - 1; // //last page minus 1

    $pagination = "";
    if($lastpage &gt; 1){  
        $pagination .= "&lt;ul class='pagination pull-right' style='clear:both;'&gt;";
        //$pagination .= "&lt;li class='page_info'&gt;Page {$page} of {$lastpage}&lt;/li&gt;";

            if ($page &gt; 1) $pagination.= "&lt;li&gt;&lt;a href='{$url}pag={$prev}'&gt;{$prevlabel}&lt;/a&gt;&lt;/li&gt;";

        if ($lastpage &lt; 7 + ($adjacents * 2)){  
            for ($counter = 1; $counter &lt;= $lastpage; $counter++){
                if ($counter == $page)
                    $pagination.= "&lt;li class='active'&gt;&lt;a&gt;{$counter}&lt;/a&gt;&lt;/li&gt;";
                else
                    $pagination.= "&lt;li&gt;&lt;a href='{$url}pag={$counter}'&gt;{$counter}&lt;/a&gt;&lt;/li&gt;";                
            }

        } elseif($lastpage &gt; 5 + ($adjacents * 2)){

            if($page &lt; 1 + ($adjacents * 2)) {

                for ($counter = 1; $counter &lt; 4 + ($adjacents * 2); $counter++){
                    if ($counter == $page)
                        $pagination.= "&lt;li class='active'&gt;&lt;a&gt;{$counter}&lt;/a&gt;&lt;/li&gt;";
                    else
                        $pagination.= "&lt;li&gt;&lt;a href='{$url}pag={$counter}'&gt;{$counter}&lt;/a&gt;&lt;/li&gt;";                
                }
                $pagination.= "&lt;li class='disabled'&gt;&lt;a href='#'&gt;...&lt;/a&gt;&lt;/li&gt;";
                $pagination.= "&lt;li&gt;&lt;a href='{$url}pag={$lpm1}'&gt;{$lpm1}&lt;/a&gt;&lt;/li&gt;";
                $pagination.= "&lt;li&gt;&lt;a href='{$url}pag={$lastpage}'&gt;{$lastpage}&lt;/a&gt;&lt;/li&gt;"; 

            } elseif($lastpage - ($adjacents * 2) &gt; $page &amp;&amp; $page &gt; ($adjacents * 2)) {

                $pagination.= "&lt;li&gt;&lt;a href='{$url}pag=1'&gt;1&lt;/a&gt;&lt;/li&gt;";
                $pagination.= "&lt;li&gt;&lt;a href='{$url}pag=2'&gt;2&lt;/a&gt;&lt;/li&gt;";
                $pagination.= "&lt;li class='disabled'&gt;&lt;a href='#'&gt;...&lt;/a&gt;&lt;/li&gt;";
                for ($counter = $page - $adjacents; $counter &lt;= $page + $adjacents; $counter++) {
                    if ($counter == $page)
                        $pagination.= "&lt;li class='active'&gt;&lt;a&gt;{$counter}&lt;/a&gt;&lt;/li&gt;";
                    else
                        $pagination.= "&lt;li&gt;&lt;a href='{$url}pag={$counter}'&gt;{$counter}&lt;/a&gt;&lt;/li&gt;";                
                }
                $pagination.= "&lt;li class='disabled'&gt;&lt;a href='#'&gt;...&lt;/a&gt;&lt;/li&gt;";
                $pagination.= "&lt;li&gt;&lt;a href='{$url}pag={$lpm1}'&gt;{$lpm1}&lt;/a&gt;&lt;/li&gt;";
                $pagination.= "&lt;li&gt;&lt;a href='{$url}pag={$lastpage}'&gt;{$lastpage}&lt;/a&gt;&lt;/li&gt;";    

            } else {

                $pagination.= "&lt;li&gt;&lt;a href='{$url}pag=1'&gt;1&lt;/a&gt;&lt;/li&gt;";
                $pagination.= "&lt;li&gt;&lt;a href='{$url}pag=2'&gt;2&lt;/a&gt;&lt;/li&gt;";
                $pagination.= "&lt;li class='disabled'&gt;&lt;a href='#'&gt;...&lt;/a&gt;&lt;/li&gt;";
                for ($counter = $lastpage - (2 + ($adjacents * 2)); $counter &lt;= $lastpage; $counter++) {
                    if ($counter == $page)
                        $pagination.= "&lt;li class='active'&gt;&lt;a&gt;{$counter}&lt;/a&gt;&lt;/li&gt;";
                    else
                        $pagination.= "&lt;li&gt;&lt;a href='{$url}pag={$counter}'&gt;{$counter}&lt;/a&gt;&lt;/li&gt;";                
                }
            }
        }

            if ($page &lt; $counter - 1) $pagination.= "&lt;li&gt;&lt;a href='{$url}pag={$next}'&gt;{$nextlabel}&lt;/a&gt;&lt;/li&gt;";

        $pagination.= "&lt;/ul&gt;";     
    }

    return $pagination;
}
</code></pre>

<p>Database query script for the categories:</p>

<pre><code>&lt;?php
require_once ('inc/db.php');
include_once ('inc/funciones.php');


$category = str_replace("-"," ",$_GET["catid"]);

$catquery = mysqli_query($dbc,"SELECT * FROM tienda_categorias WHERE cat_nombre='{$category}'");    

while ($raw = mysqli_fetch_array($catquery, MYSQLI_ASSOC)){
            $cat = $raw['cat_id'];
        }           


$page = (int)(!isset($_GET["pag"]) ? 1 : $_GET["pag"]);
if ($page &lt;= 0) $page = 1;

$per_page = 4; // Set how many records do you want to display per page.

$startpoint = ($page * $per_page) - $per_page;

$statement = "tienda_prod";

$filtros = '';
$url_filtros = '?';

if(isset($_GET['searching'])) {
    //VALIDACION TITULO
    if (isset($_GET['title'])) {
        $title = trim($_GET["title"]);

        $title = str_replace('%','', $title);
        $title = str_replace('_','', $title);
        $title = str_replace('+','', $title);
        if (preg_match ("([^ñÑa-zA-Z0-9\s]|)", $title) &amp;&amp; strlen($title) &gt;= 0) {
            $filtros = " AND prod_titulo LIKE '%{$title}%'";
            $url_filtros .= 'title='.$title;

        } else {
            echo '&lt;p class="alert alert-danger"&gt;Ingrese un titulo correcto&lt;/p&gt;';
        }
    }
    if(isset($_GET['subcat']) &amp;&amp; $_GET['subcat'] != 0){
        $subcategoria = $_GET['subcat'];
        $filtros .= " AND t.subcat_id ={$subcategoria}";
        if (isset($_GET['title'])) $url_filtros .= '&amp;';
        $url_filtros .= 'subcategoria='.$subcategoria;
    }
    if(isset($_GET['condicion']) &amp;&amp; $_GET['condicion'] != ''){
        $condicion = $_GET['condicion'];
        $condicion = isset($_GET["condicion"]) ? $_GET["condicion"] : "";
        $filtros .= " AND prod_condicion ='{$condicion}'";
        if (isset($_GET['title'])) $url_filtros .= '&amp;';
        $url_filtros .= 'condicion='.$condicion;
    }
    //Validacion de provincia
    if(isset($_GET['permuta']) &amp;&amp; $_GET['permuta'] != 0){
        $permuta = $_GET['permuta'];
        $filtros .= " AND prod_permuta='{$permuta}'";
        if (isset($_GET['title']) || isset($_GET['permuta'])) $url_filtros .= '&amp;';
        $url_filtros .= 'permuta='.$permuta;
    }
    $url_filtros .= '&amp;searching=&amp;';
}

$results = mysqli_query($dbc,"SELECT t.prod_id, t.cat_id, t.subcat_id, t.prod_titulo, t.prod_descripcion, t.prod_precio, t.prod_moneda, t.prod_condicion, t.prod_permuta, t.prod_marca_id, t.prod_destacado, m.marca_nombre, DATE_FORMAT(t.prod_fechacreado, '%d/%m/%Y') AS fc FROM {$statement} AS t LEFT JOIN tienda_marcas AS m ON t.prod_marca_id = m.marca_id WHERE t.prod_activo ='1' AND t.cat_id = {$cat} {$filtros} ORDER BY t.prod_fechacreado DESC LIMIT {$startpoint} , {$per_page}");

$totalRows = mysqli_num_rows($results);
if ($totalRows == 0){ // Si no encuentra registros, muestra la notificacion correspondiente
    echo '&lt;div class="alert alert-success" role="alert"&gt;&lt;span&gt;No existen articulos en venta para esta categoría&lt;/span&gt;&lt;div class="col-separador-m"&gt;&lt;/div&gt;&lt;span&gt;&lt;button class="btn btn-success btn-block"&gt;Publica tu venta &lt;strong&gt;GRATIS&lt;/strong&gt;&lt;/button&gt;&lt;/span&gt;&lt;/div&gt;';
}

while ($row = mysqli_fetch_array($results, MYSQLI_ASSOC)){
//var_dump($row);
if($row['prod_precio']==1){
    $moneda = 'U$D';
}else{
    $moneda = '$';
};
if($row['prod_condicion']==0){
    $condicion = 'nuevo';
}else{
    $condicion = 'usado';
}
if($row['prod_destacado']==1){
    $destacado = '&lt;div id="badge"&gt;
              &lt;div class="gem-top-right"&gt;&lt;/div&gt;
              &lt;div class="gem-top-left"&gt;&lt;/div&gt;
              &lt;div class="gem-bottom-right"&gt;&lt;/div&gt;
              &lt;div class="gem-bottom-left"&gt;&lt;/div&gt;
            &lt;/div&gt;';
}else{
    $destacado = '';
}

  echo '&lt;div class="col-xs-6 col-md-4 column productbox"&gt;
            '. $destacado .'
            &lt;div class="ribbon-wrapper"&gt;&lt;div class="ribbon-'.$condicion.'"&gt;'.$condicion.'&lt;/div&gt;&lt;/div&gt;
            &lt;a href="store/' . $row['cat_id'] . '-' . sanitizarURL($row['prod_titulo']) .'-da' . $row['prod_id'] . '"&gt;
                &lt;img src="https://unsplash.it/270/270/?random=0" class="img-responsive"&gt;
            &lt;/a&gt;
            &lt;div class="product-info"&gt;
                &lt;div class="product-title"&gt;
                    &lt;a href="store/' . $row['cat_id'] . '-' . sanitizarURL($row['prod_titulo']) .'-da' . $row['prod_id'] . '"&gt;'. $row['prod_titulo'] . '&lt;/a&gt;
                &lt;/div&gt;
                &lt;div class="product-price"&gt;
                    &lt;div class="pull-right"&gt;
                        &lt;a href="store/' . $row['cat_id'] . '-' . sanitizarURL($row['prod_titulo']) .'-da' . $row['prod_id'] . '" class="btn btn-info btn-sm" role="button"&gt;Ver&lt;/a&gt;
                    &lt;/div&gt;

                    &lt;div class="pricetext"&gt;'.$moneda.''. $row['prod_precio'] . '&lt;/div&gt;
                &lt;/div&gt;
                &lt;div class="col-separador-s"&gt;&lt;/div&gt;
            &lt;/div&gt;
        &lt;/div&gt;';

    }   
    echo paginationStore( $statement, $per_page,$page, $url_filtros, $filtros);
?&gt;
</code></pre>

