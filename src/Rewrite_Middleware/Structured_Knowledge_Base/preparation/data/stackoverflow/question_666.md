# Refer to the variable
[Link to question](https://stackoverflow.com/questions/36515779/refer-to-the-variable)
**Creation Date:** 1460199072
**Score:** 0
**Tags:** php, mysqli
## Question Body
<p>I want to rewrite the script on an object PHP.
I created script login to the database (database connection work).</p>

<p>The problem has arisen when you send a query to the database which checks whether the user exists.</p>

<pre><code>&lt;?php
//DANE DO LOGOWANIA DO BD
define("DB_HOST", 'localhost');
define("DB_USER", 'michal');
define("DB_PASSWORD", '');
define("DB_DATABSE", 'kurs_php');
?&gt;

&lt;?php
//PLIK LOGOWANIA DO BD I SPRAWDZANIA POLACZENIA Z BD
class dbConnect {
    function __construct() {
        require_once 'config.php';
        $db_mysqli = mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABSE);
        //$db_mysqli-&gt;query('SET NAMES utf8');
        if (!$db_mysqli) {
            die('Błąd połączenia (' . mysqli_connect_errno() . ') '
                . mysqli_connect_error());
        } else {
            echo '&lt;font size="2px" color="red"&gt;Info: Połączono z bazą danych.&lt;/font&gt;&lt;br /&gt;';
        }
    }
    public function CloseDb() {
        mysqli_close();
    }
}
?&gt;

&lt;?php
// KLASA Z FUNKCJAMI LOGOWANIE UŻYTKOWNIKA
class Functions {

    function __construct() {

        // connecting to database
        $db_mysqli = new dbConnect();

    }
    function __destruct() {

    }

    public function Login($login, $hasloSha1) {
        $result = $db_mysqli-&gt;prepare("SELECT haslo FROM uzytkownicy WHERE login=? AND haslo=?");
        $result-&gt;bind_param('ss', $login, $hasloSha1);
        $result-&gt;execute();
        $result-&gt;store_result();
        $row = mysqli_fetch_assoc($result);
        $kodAktywowany = $row['kod'];

//sprawdzenie czy taki uzytkownik istnieje
        if ($result-&gt;num_rows == 1) {
            $_SESSION['logowanie'] = $login;
            return TRUE;
        } else {
            return FALSE;
        }
    }

}
?&gt;
</code></pre>

<p><a href="https://i.sstatic.net/11def.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/11def.png" alt="enter image description here"></a></p>

## Answers
### Answer ID: 36515888
<p>It's good to learn. You may want to start with the basics. Your PHP class lacks member property to store/access your db connection...</p>

<p><a href="http://code.tutsplus.com/tutorials/object-oriented-php-for-beginners--net-12762" rel="nofollow">http://code.tutsplus.com/tutorials/object-oriented-php-for-beginners--net-12762</a></p>

### Answer ID: 36515873
<p>Declare $db_mysqli; as a class variable and access it using $this->db_mysqli;      </p>

<pre><code>&lt;?php
        //DANE DO LOGOWANIA DO BD
        define("DB_HOST", 'localhost');
        define("DB_USER", 'michal');
        define("DB_PASSWORD", '');
        define("DB_DATABSE", 'kurs_php');
        ?&gt;

        &lt;?php
        //PLIK LOGOWANIA DO BD I SPRAWDZANIA POLACZENIA Z BD
        class dbConnect {
            function __construct() {
                require_once 'config.php';
                $db_mysqli = mysqli_connect(DB_HOST, DB_USER, DB_PASSWORD, DB_DATABSE);
                //$db_mysqli-&gt;query('SET NAMES utf8');
                if (!$db_mysqli) {
                    die('Błąd połączenia (' . mysqli_connect_errno() . ') '
                        . mysqli_connect_error());
                } else {
                    echo '&lt;font size="2px" color="red"&gt;Info: Połączono z bazą danych.&lt;/font&gt;&lt;br /&gt;';
                }
            }
            public function CloseDb() {
                mysqli_close();
            }
        }
        ?&gt;
       // Declare a class variable to $db_mysqli;
    &lt;?php
    // KLASA Z FUNKCJAMI LOGOWANIE UŻYTKOWNIKA
    class Functions {
        var $db_mysqli;
        function __construct() {

            // connecting to database
            $this-&gt;db_mysqli = new dbConnect();

        }
        function __destruct() {

        }

        public function Login($login, $hasloSha1) {
            $result = $this-&gt;db_mysqli-&gt;prepare("SELECT haslo FROM uzytkownicy WHERE login=? AND haslo=?");
            $result-&gt;bind_param('ss', $login, $hasloSha1);
            $result-&gt;execute();
            $result-&gt;store_result();
            $row = mysqli_fetch_assoc($result);
            $kodAktywowany = $row['kod'];

    //sprawdzenie czy taki uzytkownik istnieje
            if ($result-&gt;num_rows == 1) {
                $_SESSION['logowanie'] = $login;
                return TRUE;
            } else {
                return FALSE;
            }
        }

    }
    ?&gt;
</code></pre>

