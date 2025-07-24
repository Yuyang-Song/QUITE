# JQuery .post function not executing properly
[Link to question](https://stackoverflow.com/questions/27259537/jquery-post-function-not-executing-properly)
**Creation Date:** 1417556572
**Score:** 1
**Tags:** jquery, post
## Question Body
<p>I'm trying to post some variables to a PHP script based whatever item the user selects, then load the selection into the current page without redirecting the user. However, when I click a button to submit data, return false doesn't fire, and I get redirected to the action specified in the form. Can someone tell me where the problem in my code is? </p>

<pre><code> &lt;!DOCTYPE html&gt;
    &lt;html&gt;
    &lt;head&gt;
    &lt;title&gt; Today's Clients&lt;/title&gt;

    &lt;link href="../_css/jquery-ui.min.css"&gt;
    &lt;script src="../_js/jquery.min.js"&gt;&lt;/script&gt;
    &lt;script src="../_js/jquery-ui.min.js"&gt;&lt;/script&gt;

    &lt;script&gt;
    $(document).ready(function(){
        $("#clientSubmit").submit(function(event) {
            var clientInformation = $(this).serialize();
            $.post('IRCpopulatecheckin.php',clientinformation,clientForm);
            function clientForm(data) {
                if (data!='') {
                    $('#clientform').load("IRCpopulatecheckin.php");
                } else {
                    alert("your data returned nothing!!! rewrite the code...");
                }
            } // end clientForm
         return false;
        }); // end .submit
    }); // end ready

    &lt;/script&gt;

    &lt;style&gt;

    /* css to style and remove everything but text */
        #hiddenInput {
                    position    :relative;
                    width       :0px;
                    height      :8px;
                    top         :-40px;
                    left        :-230px;260
                    }
        input[name="dailyClient"] {
                    background-color: white;
                    border: none;
                    font-weight :bold;
                    font-family :sans-serif;
                    font-size: 15px;  
                    color: black;
                    cursor: default;
                    line-height: normal;
                    padding: 6px;
                    text-align: center;
                    text-shadow: none;
                    white-space: pre;
                    }

        input[name="dailyClient"]:hover {
                    color: blue;
                    }
    &lt;/style&gt;                
    &lt;body&gt;
    &lt;div id="clientform"&gt;&lt;/div&gt;

    &lt;?php 

    ini_set('display_errors',1);  error_reporting(E_ALL);

    if(isset($_POST['DATE'])) {
        $DATE = $_POST['DATE'];
        }else{
            $DATE = date('Y-m-d');
             }

    require_once 'IRCconfig.php';

    $connection = new mysqli($db_hostname, $db_username, $db_password, $db_database);
        if ($connection-&gt;connect_error) die($connection-&gt;connect_error);

    $query  = "SELECT * FROM CLIENT_CHECKIN WHERE DATE&gt;='$DATE' ORDER BY F_NAME ASC";
        $result = $connection-&gt;query($query);

    if (!$result) die ("Database access failed: " . $connection-&gt;error);

    $rows = $result-&gt;num_rows;

    for ($j = 0 ; $j &lt; $rows ; ++$j)
        {
            $result-&gt;data_seek($j);
            $row = $result-&gt;fetch_array(MYSQLI_NUM);

            echo &lt;&lt;&lt;_END
            &lt;pre&gt;
                &lt;div id="hiddenInput"&gt;&lt;div style="display:none"&gt;
                &lt;form id="clientSubmit" action="IRCpopulatecheckin.php" method="post"&gt;&lt;input id="date" type="hidden" name="DATE" value="$row[0]"&gt;&lt;input id="first" type="hidden" name="F_NAME" value="$row[1]"&gt;&lt;input id="middle" type="hidden" name="M_NAME" value="$row[2]"&gt;&lt;input id="last" type="hidden" name="L_NAME" value="$row[3]"&gt;&lt;/div&gt;
                &lt;input type="submit" name="dailyClient" value="$row[1] $row[2] $row[3]"&gt;&lt;/form&gt;
                &lt;/pre&gt;
    _END;
        }

    ?&gt;
    &lt;/body&gt;
    &lt;/html&gt;
</code></pre>

## Answers
### Answer ID: 27259713
<p>The problem seems to be with the fact that you create multiple forms with the same <code>clientSubmit</code> id. (<em>so it most likely works correct for the first form in your page</em>)</p>

<p>Id's <strong>must</strong> be unique in the page.</p>

<p>You should use a class if you want to apply the same functionality to multiple elements.</p>

<p>So change your forms to <code>&lt;form class="clientSubmit" action=...</code></p>

<p>and your script to</p>

<pre><code>$(document).ready(function(){
    $(".clientSubmit").submit(function(event) {
        var self = $(this),
            clientInformation = self.serialize();
        $.post('IRCpopulatecheckin.php',clientinformation,clientForm);
        function clientForm(data) {
            if (data!='') {
                self.load("IRCpopulatecheckin.php");
            } else {
                alert("your data returned nothing!!! rewrite the code...");
            }
        } // end clientForm
     return false;
    }); // end .submit
}); // end ready
</code></pre>

### Answer ID: 27259625
<p>Rather than <code>return false</code> use <code>event.preventDefault</code>. Notice how you already have the parameter in the <code>onsubmit</code>:</p>

<pre><code>$(document).ready(function(){
    $("#clientSubmit").submit(function(event) {
        event.preventDefault();
        var clientInformation = $(this).serialize();
        $.post('IRCpopulatecheckin.php',clientinformation,clientForm);
        function clientForm(data) {
            if (data!='') {
                $('#clientform').load("IRCpopulatecheckin.php");
            } else {
                alert("your data returned nothing!!! rewrite the code...");
            }
        } // end clientForm
    }); // end .submit
}); 
</code></pre>

