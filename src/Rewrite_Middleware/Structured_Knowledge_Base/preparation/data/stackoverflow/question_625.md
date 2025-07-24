# &quot;No database selected&quot; just in the second and following queries - PHP - MySQL
[Link to question](https://stackoverflow.com/questions/34032557/no-database-selected-just-in-the-second-and-following-queries-php-mysql)
**Creation Date:** 1449014298
**Score:** 0
**Tags:** php, mysql, mysqli
## Question Body
<p>I have a weird error, I can execute <code>mysql_query()</code> just one time. When I execute the following queries I get <code>No database selected</code>.</p>

<p>The point is, first query always is executed (<code>insertar()</code>) but the following queries fail (<code>consultar()</code>) saying that there is not a database selected.
I've rewrited the code to use MyQSLi instead, but curiously, the first query always works again and the following queries just fail with this error: <code>Warning: mysqli::mysqli(): (HY000/1044): Access denied for user ''@'localhost' to database 'mysql'</code>.
I've also tried to remove the <code>insert</code> and just execute the both <code>selects</code> and guess what, just the first <code>select</code> is being executed, the next fails.</p>

<p>Note: I know I'm not returning anything from <code>consultar()</code>, the error is not there, it's triggered before to reach that statement.</p>

<p>This is the code where I call functions <code>queries.php</code>:</p>

<pre><code>insertar($nombre, $respuestas, $fallos, $tiempoTotal);

$puntuacionesTiempo = consultar("tiempo");
$puntuacionesFallos = consultar("fallos");
</code></pre>

<p>This is my <code>model.php</code>:</p>

<pre><code>&lt;?php 

function conectar(){

    $data = include_once('configDB.php');
    $c = mysql_connect($data["server"], $data["user"], $data["pass"]);
    mysql_select_db("mysql", $c);

    if ($c)
        return $c;
    else
        exit("fail");
}

function insertar($nombre, $resultados, $tiempo){

    $conexion = conectar();

    $consulta = "INSERT INTO juegopreguntas (nombre, p1, p2, p3, p4, p5, tiempo) VALUES 
('".$nombre."',".$resultados[0].",".$resultados[1].",".$resultados[2].",".$resultados[3]
.",".$resultados[4].",'".$tiempo."')";

    $conexion-&gt;query($consulta);

    cerrarConexion($conexion);

}

function consultar($filtro){

    $conexion = conectar();

    $consulta = "SELECT * FROM juegopreguntas ORDER BY tiempo LIMIT 5";

    $re = mysql_query($consulta, $conexion);

    if(!$re)
        echo "Hubo un fallo al consultar -&gt; ".mysql_error();

    cerrarConexion($conexion);
}

function cerrarConexion($conexion){

    mysql_close($conexion);
}
?&gt;
</code></pre>

## Answers
### Answer ID: 34032647
<pre><code>&lt;?php 

    $data = include_once('configDB.php');
    $conexion  = mysql_connect($data["server"], $data["user"], $data["pass"]);
    mysql_select_db("mysql", $c);

    if ($c)
        return $c;
    else
        exit("fail");


function insertar($nombre, $resultados, $tiempo){

    global $conexion;

    $consulta = "INSERT INTO juegopreguntas (nombre, p1, p2, p3, p4, p5, tiempo) VALUES 
('".$nombre."',".$resultados[0].",".$resultados[1].",".$resultados[2].",".$resultados[3]
.",".$resultados[4].",'".$tiempo."')";

    $conexion-&gt;query($consulta);

    cerrarConexion($conexion);

}

function consultar($filtro){

      global $conexion;

    $consulta = "SELECT * FROM juegopreguntas ORDER BY tiempo LIMIT 5";

    $re = mysql_query($consulta, $conexion);

    if(!$re)
        echo "Hubo un fallo al consultar -&gt; ".mysql_error();

    cerrarConexion($conexion);
}

function cerrarConexion($conexion){

    mysql_close($conexion);
}
?&gt;
</code></pre>

