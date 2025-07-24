# Create a fetch query in a file and show it in another file
[Link to question](https://stackoverflow.com/questions/53697772/create-a-fetch-query-in-a-file-and-show-it-in-another-file)
**Creation Date:** 1544398317
**Score:** -1
**Tags:** php, mysql, oop
## Question Body
<p>I  have a question with OOP on PHP and MySQL.   </p>

<p>I'm working with PHP 7 using OOP, I want make a class Connection. In these class<br>
I have a method that generates a query to the database and store it in an array. I want the result of that array to be opened in another class of another file.
If I use an if statement, a single value is sent, if I use a while loop, nothing is shown when I request the vector in the other file.
I want to create this method to avoid having to rewrite the calls to the connection with the database.</p>

<p>This is the code that will inherit the class that shows the data.</p>

<pre><code>public function open_connection()
{ 
    $this-&gt;connect = new mysqli( self::$SERVER, self::$USER, self::$PASS, $this-&gt;DB ) or die ( "Error" ); 
} 

public function close_connection()
{ 
    mysqli_close( $this-&gt;connect ); 
}

protected function execute_a_fetch_query( )
{
    $this-&gt;open_connection();
    $orderA = $this-&gt;connect-&gt;query( $this-&gt;query );
    $orderB = $this-&gt;connect-&gt;query( $this-&gt;query );
    if ( $this-&gt;rows = mysqli_fetch_array( $orderA ) ) { //this sentence avoid a duplicate result from the query
        if ( $this-&gt;rows = mysqli_fetch_array( $orderB ) );
    }
    $this-&gt;close_connection();
}
</code></pre>

<p>And here the another method in the Show class</p>

<pre><code>public function data( $attributes = array() )
{
    $this-&gt;query = 'select * from Supplier';
    $this-&gt;execute_a_fetch_query();

    echo '&lt;tr&gt;';

    for ( $i = 0; $i &lt; count( $this-&gt;_attributes ); $i++ ) {
        echo 
            '&lt;td&gt;'. $this-&gt;rows[ $attributes[ $i ] ]. '&lt;/td&gt;'; 
    }
</code></pre>

## Answers
### Answer ID: 53698053
<p>In OOP you have a constructor that can help you out by establishing that connection when you instantiate that object so you wont have to use <code>$this-&gt;open_connection();</code> in every query. </p>

<p>Instead of creating an <code>open_connection()</code> function use</p>

<pre><code>function __ construct(){
  $this-&gt;connect = new mysqli( self::$SERVER, self::$USER, self::$PASS, $this-&gt;DB ) or 
    die ( "Error" );
 }
</code></pre>

<p>so <code>$obj = new BaseClass();</code> will open up a connection. </p>

<p>you can also have a private variable in the same class </p>

<p><code>private $dataObject</code> which can be set in your query <code>$this-&gt;$dataObject = $result;</code></p>

<p>and a public function which can be called to return the variable.</p>

<pre><code>public function getData()
{
  return $this-&gt;$dataObject;
}
</code></pre>

