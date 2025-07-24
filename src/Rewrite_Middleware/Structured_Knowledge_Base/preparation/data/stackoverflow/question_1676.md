# Adding another db connection to function
[Link to question](https://stackoverflow.com/questions/3584139/adding-another-db-connection-to-function)
**Creation Date:** 1282912486
**Score:** 0
**Tags:** php, mysql
## Question Body
<p>I have a set of functions that handle the db connection.  I want to add another connection here so I can access a different database at the same time as the current one.  Any Suggestions? </p>

<p>The reason I'm looking for a solution is because the script I'm using has very complicated Queries and I would like to be able to simply add the database name in front of it, instead of re-writing the many complicated queries.   </p>

<p>Here are the functions that connect to the database: </p>

<pre><code>function db(){

    $this-&gt;host = DATABASE_HOST;
    $this-&gt;port = DATABASE_PORT;
    $this-&gt;socket = DATABASE_SOCK;
    $this-&gt;dbname = DATABASE_NAME;
    $this-&gt;user = DATABASE_USER;
    $this-&gt;password = DATABASE_PASS;
    $this-&gt;current_arr_type = MYSQL_ASSOC;

    //  connect to db automatically
    if (empty($GLOBALS['bx_db_link'])) {
        $this-&gt;connect();
        $GLOBALS['gl_db_cache'] = array();
        $GLOBALS['bx_db_param'] = array();
    }
    else
        $this-&gt;link = $GLOBALS['bx_db_link'];

    if(empty($GLOBALS['bx_db_param']))
        $GLOBALS['bx_db_param'] = new BxDolParams($this);

    $this-&gt;oParams = &amp;$GLOBALS['bx_db_param'];
}

/**
 * connect to database with appointed parameters
 */
function connect()
{
    $full_host = $this-&gt;host;
    $full_host .= $this-&gt;port ? ':'.$this-&gt;port : '';
    $full_host .= $this-&gt;socket ? ':'.$this-&gt;socket : '';

    $this-&gt;link = @mysql_pconnect($full_host, $this-&gt;user, $this-&gt;password);
    if (!$this-&gt;link)
        $this-&gt;error('Database connect failed', true);

    if (!$this-&gt;select_db())
        $this-&gt;error('Database select failed', true);

    $this-&gt;res("SET NAMES 'utf8'");
    $this-&gt;res("SET sql_mode = ''");

    $GLOBALS['bx_db_link'] = $this-&gt;link;
}

function select_db()
{
    return @mysql_select_db($this-&gt;dbname, $this-&gt;link) or $this-&gt;error('Cannot complete query (select_db)');
}

/**
 * close mysql connection
 */
function close()
{
    mysql_close($this-&gt;link);
}   
</code></pre>

<p>Here is an example Query that I don't want to rewrite.  I only need to connect to the <code>Profiles</code> Table on a separate database:</p>

<pre><code>$sQuery = "
    SELECT
        `tp`.`ID` as `id`,
        `tp`.`NickName` AS `username`,
        `tp`.`Headline` AS `headline`,
        `tp`.`Sex` AS `sex`,
        `tp`.`DateOfBirth` AS `date_of_birth`,
        `tp`.`Country` AS `country`,
        `tp`.`City` AS `city`,
        `tp`.`DescriptionMe` AS `description`,
        `tp`.`Email` AS `email`,
        DATE_FORMAT(`tp`.`DateReg`,  '" . $sDateFormat . "' ) AS `registration`,
        DATE_FORMAT(`tp`.`DateLastLogin`,  '" . $sDateFormat . "' ) AS `last_login`,
        `tp`.`Status` AS `status`,
        IF(`tbl`.`Time`='0' OR DATE_ADD(`tbl`.`DateTime`, INTERVAL `tbl`.`Time` HOUR)&gt;NOW(), 1, 0) AS `banned`, 
        `tl`.`ID` AS `ml_id`, 
        IF(ISNULL(`tl`.`Name`),'', `tl`.`Name`) AS `ml_name`
        " . $sSelectClause . "
    FROM `Profiles` AS `tp` 
    LEFT JOIN `sys_admin_ban_list` AS `tbl` ON `tp`.`ID`=`tbl`.`ProfID`
    LEFT JOIN `sys_acl_levels_members` AS `tlm` ON `tp`.`ID`=`tlm`.`IDMember` AND `tlm`.`DateStarts` &lt; NOW() AND (`tlm`.`DateExpires`&gt;NOW() || ISNULL(`tlm`.`DateExpires`))  
    LEFT JOIN `sys_acl_levels` AS `tl` ON `tlm`.`IDLevel`=`tl`.`ID` 
    " . $sJoinClause . "
    WHERE
        1 AND (`tp`.`Couple`=0 OR `tp`.`Couple`&gt;`tp`.`ID`)" . $sWhereClause . "
    " . $sGroupClause . "
    ORDER BY `tp`.`" . $aParams['view_order'] . "` " . $aParams['view_order_way'] . "
    LIMIT " . $aParams['view_start'] . ", " . $aParams['view_per_page'];
</code></pre>

## Answers
### Answer ID: 3584247
<p>You could remodel the class to hold an array of connections, and then add the connection index to each method in your class.</p>

<pre><code>$db-&gt;query(1, ".....");
$db-&gt;connect(1, "localhost", "username", "password");
</code></pre>

<p>An sleek method could be introducing a <code>getConnection()</code> method that selects one of the database connections as the current connection, and then executes your query like so:</p>

<pre><code>$db-&gt;getConnection(1)-&gt;connect("localhost", "username", "password", "database");
$db-&gt;getConnection(1)-&gt;query(".....");
</code></pre>

<p>the method would have to look something like this:</p>

<pre><code>function getConnection($conn)
 {
  $this-&gt;useConnection = $conn;
  return $this;
 }
</code></pre>

<p>obviously, for this method, every method in your class would have to be made sensitive of the <code>useConnection</code> property.</p>

