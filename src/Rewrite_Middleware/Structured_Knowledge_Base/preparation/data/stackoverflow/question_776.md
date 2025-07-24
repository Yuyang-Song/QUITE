# global varible in class functions
[Link to question](https://stackoverflow.com/questions/41833449/global-varible-in-class-functions)
**Creation Date:** 1485275545
**Score:** -1
**Tags:** php, oop, global
## Question Body
<ol>
<li>I got some old code to deal with, it's to large to rewrite</li>
<li>I need to extend and/or replace some pieces of it</li>
<li><p>In the code, there is a declared variable <code>$table_prefix</code> (not global) used in SQL queries like this:</p>

<pre><code>$sql="SELECT * FROM {$table_prefix}table WHERE id = %d";
</code></pre></li>
<li><p><code>$table_prefix</code> changes depending on some conditions (i.e host, remote ip etc)</p></li>
</ol>

<p><strong>The problem</strong> </p>

<p>to get my goals  I created a class with many functions reading/writing data to SQL. For now I had to repeat <code>global $table_prefix</code> in every function. It looks similar to this:</p>

<pre><code>class MyClass {

    function loadData($id=0){

        global $table_prefix;

        $sql = "SELECT * FROM {$table_prefix}table WHERE id = %d;";
        [...]
    }

    function saveData($id=0, $data){

        global $table_prefix;

        if(is_array($data) [...] ){
            $sql = "UPDATE
                 {$table_prefix}table
                SET
                    data_1= %s,
                    data_2 = %d
                WHERE id = %d;";
            [...]
        }
    }
}
</code></pre>

<p><strong>QUESTION</strong> 
Is there any way to declare this <code>$table_prefix</code> once and use it in every class function without repeating it. </p>

<p><strong><em>protip</strong> If you see an mistake in my English, feel free to write me about it - i'm still learning, and learning, and learning... It seems it's been that way forever, and not only with my language skills, becouse people learn whole life :)</em></p>

## Answers
### Answer ID: 41834146
<p>Do this in the constructor of your class:</p>

<pre><code> class MyClass {
     private $table_prefix;

     public function __construct($table_prefix) {
            $this-&gt;table_prefix = $table_prefix;
     }
     private function table($name) {
           return $this-&gt;table_prefix.$name;
     }
     function loadData($id=0){             
        $sql = "SELECT * FROM ".$this-&gt;table("table")." WHERE id = %d;";
        //Or you can not define the function and do the following:
        //$sql = "SELECT * FROM ".$this-&gt;table_prefix."table WHERE id = %d;";
        [...]
    }

     ...         

}
</code></pre>

<p>You will then need to construct your class differently:</p>

<pre><code> $class = new MyClass($tablePrefix); //Where $tablePrefix is the prefix you've computed
</code></pre>

### Answer ID: 41833583
<p>I would suggest you to use the <code>Define</code> function in your configuration phase to define <code>table_prefix</code> globally. </p>

<p>Sample code:</p>

<p>config.php</p>

<pre><code>&lt;?php define('table_prefix','prefix_');
</code></pre>

<p>MyClass.php</p>

<pre><code>$sql = "UPDATE " . table_prefix . "...";
</code></pre>

<p>Source: <a href="http://php.net/manual/en/function.define.php" rel="nofollow noreferrer">http://php.net/manual/en/function.define.php</a></p>

