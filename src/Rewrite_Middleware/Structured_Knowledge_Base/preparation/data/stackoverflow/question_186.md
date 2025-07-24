# PHP, MySQL, FastCGI - best way to handle many queries
[Link to question](https://stackoverflow.com/questions/16025541/php-mysql-fastcgi-best-way-to-handle-many-queries)
**Creation Date:** 1366063839
**Score:** 0
**Tags:** php, mysql, pdo
## Question Body
<p>I am trying to figure out the best way to handle db communication in PHP, MySQL setup through FastCGI and usig PHP-FPM; This is for a relatively heavy use site where there is anywhere from 100 to 1,000 SQL queries a second so I would like to make things as efficient as possible.  </p>

<p>I am rewriting parts of the website and in the new code I am utilizing PDO and have the below class to handle DB queries and connections by doing database::insertEmployee($name, $SIN, $DOB, $position).  My concern is that with every query a new PDO connection is established.  Should I be trying to set up a persistent connection???</p>

<pre><code>class database
{
    protected $dbh;
    protected static $instance;

    private function __construct()
    {
        try {
        // building data source name from config
            $dsn = 'mysql:=' . DB_Config::read('db.host') .
                   ';dbname='  . DB_Config::read('db.name');
            $user = DB_Config::read('db.user');
            $password = DB_Config::read('db.password');
            $this-&gt;dbh = new PDO($dsn, $user, $password);
            $this-&gt;dbh-&gt;setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
        } catch (PDOException $e) {
            //@TODO-KP: log and alert
            print "Error!: " . $e-&gt;getMessage() . "&lt;br/&gt;";
            die();
        }

    }

    public static function getInstance()
    {
        if (!isset(self::$instance)) {
            $object = __CLASS__;
            self::$instance = new $object;
        }
        return self::$instance;
    }

    public static function insertEmployee($name, $position, $SIN, $DOB)
    {
        $dbi = self::getInstance();

        try {
            $sthEmployee = $dbi-&gt;dbh-&gt;prepare('INSERT INTO employees SET
                                                name = :name
                                                , position = :position
                                                , SIN = :SIN
                                                , DOB = :DOB'
            );

            $sthEmployee-&gt;bindParam(':name', $name);
            $sthEmployee-&gt;bindParam(':position', $position);
            $sthEmployee-&gt;bindParam(':SIN', $SIN);
            $sthEmployee-&gt;bindParam(':DOB', date('Y-m-d G:i:s', $DOB));

            return $sthEmployee-&gt;execute();

        } catch (PDOException $e) {
            //@FIXME-KP: log and alert
            print "Error!: " . $e-&gt;getMessage() . "-- name [$name]";
            return '';
        }
    }
}
</code></pre>

<p>Any thoughts on most efficient approach would be very, very appreciated!</p>

<p>Kathryn.</p>

## Answers
### Answer ID: 16025598
<blockquote>
  <p>My concern is that with every query a new PDO connection is established.</p>
</blockquote>

<p>Well, verify your concern, because I would say this is likely not the case.</p>

<p>For performance reasons, take care you're using the mysql native driver under the hood as this allows extended metrics of the interaction from PHP with the database.</p>

<p>Also get a professional support plan from Oracle for Mysql, they have nice monitoring tools and very good support that should help you to get your database and PHP code ready for the traffic to handle.</p>

