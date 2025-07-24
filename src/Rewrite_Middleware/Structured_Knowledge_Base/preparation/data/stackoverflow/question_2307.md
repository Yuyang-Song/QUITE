# Best OOP design pattern for static class DbTable
[Link to question](https://stackoverflow.com/questions/28380912/best-oop-design-pattern-for-static-class-dbtable)
**Creation Date:** 1423304057
**Score:** 1
**Tags:** php, oop, design-patterns
## Question Body
<p>I have class DbTable, which implements all db queries to database such as insertRecord, updateRecord, ... But variable is not rewriting.</p>

<pre><code>abstract class DbTable {
    public static $table;

    public static function insertRecord($data) {
       // here I add some values to data, but that's not important
       my_db::insert(self::$table, $data);
    }
}

class User extends DbTable {
    public static $table = 'table_users';
}

// everywhere I can call
User::insertRecord($data);
</code></pre>

<p>I know I can call</p>

<pre><code>$c = get_called_class();
my_db::insert($c::$table, $data);
</code></pre>

<p>but I think that's not best solution at all.</p>

<p>Method and variables can be non static, I just use them because it is comfortable to write <code>User::insertRecord</code> instead of <code>$user = new User(); $user-&gt;insertRecord($data);</code></p>

## Answers
### Answer ID: 28381228
<p>Use static variables are unnecessary in this case. You just need dynamically create <code>User</code> object and them call method.</p>

<pre><code>abstract class DbTable
{
    protected $tableName;

    public static function insertRecord($data) 
    {
        $object = static::newInstance();
        $object-&gt;insert($data);
    }

    public static function newInstance()
    {
        $className = get_called_class();
        return new $className();
    }

    public function insert($data)
    {
        my_db::insert($this-&gt;tableName, $data);
    }
}

class User extends DbTable 
{
    public function __construct()
    {
        $this-&gt;tableName = 'table_users';
    }
}
</code></pre>

<p>You can now call:</p>

<pre><code>User::insertRecord(['col1' =&gt; 'val1']);
</code></pre>

<p>But also you can insert rows from instated object:</p>

<pre><code>$user = new User();
$user-&gt;insert(['col1' =&gt; 'val1']);
</code></pre>

### Answer ID: 28381175
<p>When you're working with static classes you need to specify your variable source, in this case you're scoping to both classes and not on single class, this makes a difference, because <code>self</code> is scoping to concurrent class and when you want to scope for both classes you have to use <code>static</code>.</p>

<pre><code>/**
* For testing
*/
class my_db {
    public static function insert($table, $data){
        echo $table;
    }
}
abstract class DbTable {
    public static $table = null;

    public static function insertRecord($data) {

        //self::$table is empty
        //static::$table has 'table_users'

        // here I add some values to data, but that's not important
        my_db::insert(static::$table, $data);
    }
}

class User extends DbTable {
    public static $table = 'table_users';
}

// everywhere I can call
User::insertRecord(['Hi']);
</code></pre>

<p><code>self::$table</code> is <strong>empty</strong></p>

<p><code>static::$table</code> has <strong>'table_users'</strong></p>

<p>You can read more about this here: <a href="https://stackoverflow.com/a/5197655/2529486">SO Answer</a> and <a href="http://php.net/manual/en/language.oop5.static.php" rel="nofollow noreferrer">PHP Documentation</a></p>

