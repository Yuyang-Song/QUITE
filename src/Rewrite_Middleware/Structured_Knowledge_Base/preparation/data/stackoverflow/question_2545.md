# Datetime Picker value won&#39;t update in database on post
[Link to question](https://stackoverflow.com/questions/39166248/datetime-picker-value-wont-update-in-database-on-post)
**Creation Date:** 1472214125
**Score:** 0
**Tags:** php, jquery, mysql, datetimepicker
## Question Body
<p>Trying to use the jquery datetimepicker and I can get the addon to work, however, when I post the data it doesn't update in the database. Everything else updates, but the date/time.</p>

<p>Note: I realize some of this is still mysql, I'm working to update the entire site.</p>

<p>edit_release_form.php, I have </p>

<pre><code>&lt;script src="https://code.jquery.com/jquery-1.12.4.js"&gt;&lt;/script&gt;
&lt;script src="https://code.jquery.com/ui/1.12.0/jquery-ui.js"&gt;&lt;/script&gt;
&lt;script type="text/javascript" src="http://vmcnucmed.cvm.umn.edu/includes/js/jquery-ui-timepicker-addon.js"&gt;&lt;/script&gt;
&lt;link rel="stylesheet" href="http://vmcnucmed.cvm.umn.edu/includes/jquery-ui-timepicker-addon.css"&gt;
&lt;link rel="stylesheet" href="//code.jquery.com/ui/1.12.0/themes/base/jquery-ui.css"&gt;
&lt;script&gt;
  $( function() {
    $('#datetime_released').datetimepicker({
    controlType: 'select',
    oneLine: true,
    timeFormat: 'hh:mm:ss tt'
});
  } );
  &lt;/script&gt;
</code></pre>

<p>My input:</p>

<pre><code> &lt;input tabindex="1" id="datetime_released" type="text" name="datetime_released" &gt;
</code></pre>

<p>post.php</p>

<pre><code>&lt;?php
// Database Conection Parameters
define('DB_SERVER', "hostname");
define('DB_USER', "username");
define('DB_PASSWORD', "password");
define('DB_TABLE', "database");

// Connection to the Database
$mysqli = mysqli_connect(DB_SERVER, DB_USER, DB_PASSWORD, DB_TABLE);
$mysqli-&gt;set_charset("utf8");
$mysqli-&gt;query("SET NAMES 'utf8'");

if (mysqli_connect_errno($mysqli)) {
    trigger_error('Database connection failed: '  . mysqli_connect_error(), E_USER_ERROR);
}

$datetime_released = $_POST['datetime_released']; 
$release_probeSN = $_POST['release_probeSN']; 
$release_reading = $_POST['release_reading'];
$release_reading_loc = $_POST['release_reading_loc'];
$releasedby = $_POST['releasedby'];
$id = $_POST['id'];


// Query
$sql = "
UPDATE xxx
SET datetime_released=?, 
release_probeSN=?, 
release_reading=?, 
release_reading_loc=?,
releasedby=?

WHERE patientdoseID=?";
if(!($stmt = $mysqli-&gt;prepare($sql)))
{
  die("Unable to prepare statement");
}
else
{
  $stmt-&gt;bind_param("sissii", $datetime_released, $release_probeSN, $release_reading, $release_reading_loc, $releasedby, $id);    
  if($stmt-&gt;execute())
  {
    echo 'Patient Updated Successfully. &lt;br /&gt;&lt;br /&gt;Database ID: &lt;br&gt;';
          header('Location: http://vmcnucmed.cvm.umn.edu', 
            TRUE, // rewrite existing Location header
            302 // set status code
);
  }
  else
  {
    die("Update failed");
  }
}

mysqli_close($mysqli);

?&gt;
</code></pre>

## Answers
### Answer ID: 39193663
<p>This is how you can convert a posted js date into mysql format.
The PHP DateTime object can accept various formats and usually converts them correctly.
You could easily package this into a function - for readability.</p>

<pre><code>&lt;?php
// set your timezone somewhere prior to creating a DateTime object
// to prevent local vs UTC issues
date_default_timezone_set('America/Chicago');

// mysql date format
$format = "Y-m-d H:i:s";

// an example input
$input = '08/25/2016 05:19:20 am';

// convert input date into a PHP DateTime object
$my_date = new DateTime($input);

// create a string in the desired mysql format
$output = $my_date-&gt;format($format);

echo $output;

// outputs  2016-08-25 05:19:20  - just the way mysql likes it
</code></pre>

