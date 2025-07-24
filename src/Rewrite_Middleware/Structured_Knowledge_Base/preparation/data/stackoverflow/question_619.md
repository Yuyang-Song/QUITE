# php breadcrumbs from url and query database
[Link to question](https://stackoverflow.com/questions/3383520/php-breadcrumbs-from-url-and-query-database)
**Creation Date:** 1280692467
**Score:** 0
**Tags:** php, database, breadcrumbs
## Question Body
<p>I have a php function that works for what i need but now i've found that there is chance for it to fail.  I use mod rewrite to rewrite urls and this function needs urls to be rewritten for it to work.  If i have 2 pages that have been rewritten as the same even though they are not the same, it could fail.</p>

<p>The function reads the url and splits it into parts using the / as the separator.</p>

<p>What i want to be able to do is check if the url has the word 'forum' in it and if it does query the database using the following url parts in the query.</p>

<p>Say i have a url like <a href="http://www.mydomain.com/forum/1/2/6" rel="nofollow noreferrer">http://www.mydomain.com/forum/1/2/6</a> i would like to get the 1 and 2 for my query which would be the boardid and topicid.  The last bit would be the page number.</p>

<p>This is a rewritten url which would normally look like <a href="http://www.mydomain.com/topic.php?boardid=1&amp;topicid=2&amp;pagenum=6" rel="nofollow noreferrer">http://www.mydomain.com/topic.php?boardid=1&amp;topicid=2&amp;pagenum=6</a> but using the function I wouldn't be able to split becuase there are no /.</p>

<p>The query i can do easy enough, it's just checking the url to make sure that 'forum' is in there then do the query.  If it's not in the url then carry on as normal.</p>

<p>here is the code for my php breadcrumb</p>

<pre><code>function breadcrumb(
                    $home = 'Home', // Name of root link
                    $division = ' / ', // Divider between links
                    $hidextra = true, // Toggle hide/show get data and fragment in text
                    $index = false,  // Toggle show/hide link to directory if it does not contain a file
                    $indexname = 'index.php' // The definition of the file the directory must contain
        ) {

            $breadcrumb="";

            // Requested addons...
            $extension = '.php'; // Extension to cut off the end of the TEXT links
            $ifIndex = 'index.php'; // Filename of index/default/home files to not display
            // End requested addons

            $whole = $_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI'];

            if(stristr($whole,"contact-bidder")) {
                $whole = substr($whole,0,strrpos($whole,'/'));
            }

            $parts = explode('/', $whole);
            $parts[0] = 'http://'.$parts[0];

            $array = array('-', '%20');

            $breadcrumb .=  "&lt;a href=\"{$parts[0]}\"&gt;{$home}&lt;/a&gt;{$division}";
            $k = 1;
            for ($i=1;$i &lt; sizeof($parts);$i++) {
                $uri = '/';
                while ($k &lt;= $i) {
                        $uri .= $parts[$k];
                        if ($k != (sizeof($parts)-1)) $uri .= '/';
                        $k++;
                 }
                  if (($index &amp;&amp; is_dir($_SERVER['DOCUMENT_ROOT'].$uri) &amp;&amp; is_file($_SERVER['DOCUMENT_ROOT'].$uri.$indexname) 
                || !$index 
                || !is_dir($_SERVER['DOCUMENT_ROOT'].$uri)) &amp;&amp; $parts[$i] != $ifIndex) {
                    $breadcrumb .= "&lt;a href=\"$uri\"&gt;";
                    if ($hidextra) {
                        $breadcrumb .= rtrim(preg_replace("/\?.*$/", '', ucwords(str_replace($array," ",$parts[$i]))), $extension);
                    }
                    else {
                        $breadcrumb .= rtrim(ucwords($parts[$i]), $extension);
                    }
                    $breadcrumb .= '&lt;/a&gt;';
                }
                else {
                    $breadcrumb .= ucwords(str_replace($array," ",$parts[$i]));
                }

                  if (isset($parts[($i+1)])) {
                    $breadcrumb .= $division;
                }
                  $k = 1;
            }
            return $breadcrumb;
        }
</code></pre>

<p>If that isn't possible or easy, is there a way i can split on the ? and &amp; and get only what is before the ? and after = for each variable in the url</p>

## Answers
### Answer ID: 3390430
<p>I managed to fix it how i needed and it wasn't that hard</p>

<pre><code>function breadcrumb(
                $home = 'Home', // Name of root link
                $division = ' / ', // Divider between links
                $hidextra = true, // Toggle hide/show get data and fragment in text
                $index = false,  // Toggle show/hide link to directory if it does not contain a file
                $indexname = 'index.php' // The definition of the file the directory must contain
    ) {
        global $host,$dbUser,$dbPass,$dbName;

        require_once("php/database/connection.php");
        require_once("php/database/MySQL.php");

        // Connect to the database and grab the email
        $db = &amp; new MySQL($host,$dbUser,$dbPass,$dbName);

        $breadcrumb="";

        // Requested addons...
        $extension = '.php'; // Extension to cut off the end of the TEXT links
        $ifIndex = 'index.php'; // Filename of index/default/home files to not display
        // End requested addons

        $whole = $_SERVER['HTTP_HOST'].$_SERVER['REQUEST_URI'];

        $parts = explode('/', $whole);
        $parts[0] = 'http://'.$parts[0];

        $array = array('-', '%20');

        $breadcrumb .=  "&lt;a href=\"{$parts[0]}\"&gt;{$home}&lt;/a&gt;{$division}";
        $k = 1;
        for ($i=1;$i &lt; sizeof($parts);$i++) {
            $uri = '/';
            while ($k &lt;= $i) {
                    $uri .= $parts[$k];
                    if ($k != (sizeof($parts)-1)) $uri .= '/';
                    $k++;
             }
              if (($index &amp;&amp; is_dir($_SERVER['DOCUMENT_ROOT'].$uri) &amp;&amp; is_file($_SERVER['DOCUMENT_ROOT'].$uri.$indexname) 
            || !$index 
            || !is_dir($_SERVER['DOCUMENT_ROOT'].$uri)) &amp;&amp; $parts[$i] != $ifIndex) {
                $breadcrumb .= "&lt;a href=\"$uri\"&gt;";
                if ($hidextra) {
                    if($parts[$i-1]=="forum") {
                        $board = substr($parts[$i],6);
                        $sql = "SELECT boardname FROM boards WHERE boardid='".$board."'";
                        $result = $db-&gt;query($sql);

                        while($row=$result-&gt;fetch()) {
                            extract($row, EXTR_PREFIX_INVALID, '_');
                            $breadcrumb .= $boardname;
                        }
                    } 
                    else if($parts[$i-2]=="forum") {
                        $topic = substr($parts[$i],10);
                        $sql = "SELECT topicname FROM topics WHERE topicid='".$topic."'";
                        $result = $db-&gt;query($sql);

                        while($row=$result-&gt;fetch()) {
                            extract($row, EXTR_PREFIX_INVALID, '_');
                            $breadcrumb .= $topicname;
                        }
                    }
                    else {
                        $breadcrumb .= rtrim(preg_replace("/\?.*$/", '', ucwords(str_replace($array," ",$parts[$i]))), $extension);
                    }
                }
                else {
                    $breadcrumb .= rtrim(ucwords($parts[$i]), $extension);
                }
                $breadcrumb .= '&lt;/a&gt;';
            }
            else {
                $breadcrumb .= ucwords(str_replace($array," ",$parts[$i])); 
            }

              if (isset($parts[($i+1)])) {
                $breadcrumb .= $division;
            }
              $k = 1;
        }
        return $breadcrumb;
    }
</code></pre>

<p>I had to check on the current part if the previous was 'forum', make a connection to the database, grab the info i needed then replace what is in the breadcrumb at that point.  It was the same for the next breadcrumb.</p>

<p>It now works how it should.</p>

### Answer ID: 3384371
<p>The string of variables after the URL is called the query string. The best way to check for the existence of variables in the query string is to look in the $_GET array.</p>

<p>So... if you have:</p>

<p><a href="http://google.com/?key=value&amp;another_key=another_value&amp;forum=22" rel="nofollow noreferrer">http://google.com/?key=value&amp;another_key=another_value&amp;forum=22</a></p>

<p>You would check for the variable 'forum' like this:</p>

<pre><code>if (isset($_GET['forum'])){

  // 'forum' has been set in the query string, do something...

} else {

  // 'forum' has NOT been set.
}
</code></pre>

