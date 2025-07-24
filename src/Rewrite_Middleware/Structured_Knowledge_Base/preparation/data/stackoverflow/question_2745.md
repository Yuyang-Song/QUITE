# PDO access.mdb not excape percent during SELECT query in a prepared statement
[Link to question](https://stackoverflow.com/questions/50267794/pdo-access-mdb-not-excape-percent-during-select-query-in-a-prepared-statement)
**Creation Date:** 1525937370
**Score:** 0
**Tags:** php, pdo
## Question Body
<p>I don't know if it's a problem only for PDO connecting to a MDB ACCESS database (and not to MySQL), but i've problem in all SELECT query where I insert a <code>%</code> using prepared statement.</p>

<p>This is my example:</p>

<pre><code>Table.Col1 is a TEXT field
Table.Col2 is a INT field
</code></pre>

<p>When I search inside <code>Col1</code> I want to search exact term (not starting with...or end with...but the exact term I pass)</p>

<p>Example of a compiled Table</p>

<pre><code>| ID | Col1      | Col2 |
-------------------------
| 1  | test      | 23   |
-------------------------
| 2  | apple     | 24   |
-------------------------
| 3  | applejuice| 33   |
-------------------------
| 4  | yellow    | 76   |
-------------------------
| 5  | brown     | 50   |
-------------------------



&lt;?php

$dbName = "Database.mdb";

try{
    $db= new PDO("odbc:DRIVER={Microsoft Access Driver (*.mdb)}; DBQ=$dbName; Uid=; Pwd=;");
    $db-&gt;setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
}catch(PDOException $e){
    echo $e-&gt;getMessage();
    exit();
}

function test($filters = array()) {

    $sql = "SELECT * FROM Table WHERE 1";
    $vars = array();

    //  FILTER BY Col1

    if ( isset($filters['Col1']) &amp;&amp; $filters['Col1'] != "" ) {

        $sql .= " AND [Table].[Col1] LIKE ?";
        $vars[] = $filters['Col1'];

    }

    //  FILTER BY Col2

    if ( isset($filters['Col2']) &amp;&amp; $filters['Col2'] != "" ) {

        $sql .= " AND [Table].[Col2] = ?";
        $vars[] = $filters['Col2'];

    }


        try {
            $s = $db-&gt;prepare($sql);
            $s-&gt;execute($vars);
            $ris = $s-&gt;fetchAll(PDO::FETCH_ASSOC);
            return $ris;
        } catch (PDOException $e) {
            die($e);
        }

}
</code></pre>

<p>Now this is my tests:</p>

<pre><code>var_dump(test(array("Col1" =&gt; "test")));

// OUTPUT CORRECT

array(
  0 =&gt; array(
    "ID" =&gt; 1,
    "Col1" =&gt; test,
    "Col2" =&gt; 23
  )
);

var_dump(test(array("Col1" =&gt; "apple")));

// OUTPUT CORRECT

array(
  0 =&gt; array(
    "ID" =&gt; 2,
    "Col1" =&gt; applejuice,
    "Col2" =&gt; 33
  )
);

 var_dump(test(array("Col1" =&gt; "%")));

// OUTPUT INCORRECT !!!!
// I GET ALL TABLE!!! I WANT TO RETRIEVE A EMPTY RESULT ARRAY

array(
  0 =&gt; array(
    "ID" =&gt; 1,
    "Col1" =&gt; test,
    "Col2" =&gt; 23
  ),
  1 =&gt; array(
    "ID" =&gt; 2,
    "Col1" =&gt; apple,
    "Col2" =&gt; 24
  ),
  2 =&gt; array(
    "ID" =&gt; 3,
    "Col1" =&gt; applejuice,
    "Col2" =&gt; 33
  ),
  3 =&gt; array(
    "ID" =&gt; 4,
    "Col1" =&gt; yellow,
    "Col2" =&gt; 76
  ),
  4 =&gt; array(
    "ID" =&gt; 5,
    "Col1" =&gt; brown,
    "Col2" =&gt; 50
  ),
  0 =&gt; array(
    "ID" =&gt; 2,
    "Col1" =&gt; applejuice,
    "Col2" =&gt; 33
  )
);
</code></pre>

<p>Why prepared statement doesn't work? I've a lot of function where I need to SELECT where I search for a EXACT TEST... How can I solve this problem with <code>%</code> for ALL my tables without rewrite all my function (more than 100 function in my project!!!)?</p>

