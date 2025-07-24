# Mysql INSERT statement FAILING when POSTING large array
[Link to question](https://stackoverflow.com/questions/28235423/mysql-insert-statement-failing-when-posting-large-array)
**Creation Date:** 1422618994
**Score:** 0
**Tags:** php, mysql, oop, pdo
## Question Body
<p>I've been searching the internet and "pulling my hair out" for days over this.  It works fine on my XAMPP localhost and was working fine on my online testing server until I updated the PHP version and had to rewrite the code due to deprecated syntax.</p>

<p>Basically, I'm making a backend database for photography clients.  One of the tables is designed to store image information.  I haven't tried to store an actual image (BLOB of some sorts), I'm just looking to store "what and where".</p>

<p>What seems to be happening is if I try entering the contents of a shoot directory with several hundred images, when I hit input the screen changes, then instead of telling me how many were entered, it goes to a "418 unused" page saying</p>

<blockquote>
  <p>The server encountered an internal error or misconfiguration and was unable to complete your request.</p>
</blockquote>

<p>I've been trying to narrow down which buffers to increase or variables like "max_allowed_packet", "max_input_vars"... still no luck.  I've even tried comparing the phpinfo between the two servers to find out why one works and the other doesn't...</p>

<p>Here's what I'm doing... the listpage</p>

<pre><code>&lt;?php
// set page headers
$page_title = "Enter Images into Database";
include_once 'auth.php';

// get database connection
include_once 'config/fpaddb.php';
include_once 'objects/clients.php';
include_once 'objects/photoshoots.php';
include_once 'objects/images.php';

$database = new Database();
$db = $database-&gt;getConnection();

$colname_chk_Images = "-1";
if (isset($_GET['ShootId'])) {
  $colname_chk_Images = $_GET['ShootId'];
}
$colname1_chk_Images = "NULL";
if (isset($_GET['ShootFolder'])) {
  $colname1_chk_Images = $_GET['ShootFolder'];
}

$colname_get_Images = "-1";
if (isset($_SESSION['cID'])) {
  $colname_get_Images = $_SESSION['cID'];
}
$entered=0; //check for already entered images

?&gt;
&lt;?php
$dirname=$_SESSION['cIFolder'];
$Clogin=$_SESSION['Clogin'];
$ClientID=$_SESSION['cID'];
$_SESSION['CURR_CLIENT_ID'] = $ClientID;
$maindir=$_GET['ShootFolder'];
$ShootId=$_GET['ShootId'];
$dir=$_SERVER['DOCUMENT_ROOT'].dirname($_SERVER['PHP_SELF'])."protect/clientfolders/".$Clogin."/users/".$Clogin."/images/".$maindir;
$_SESSION['dir']=$dir;
$dir2="/protect/clientfolders/".$Clogin."/users/".$Clogin."/images/".$maindir;
$dirt= "/phpThumb-master/";
$dirn= dirname($_SERVER['PHP_SELF']);
$filesArray=array_map('basename', glob($dir."/*.jpg"));
$lightbox_data= "FPAD_Lightbox";
$thumb =    "$dir2/";
$notThumb =   "$dir2/";
$ic = count($filesArray);
$_SESSION['SESS_TOTNUM'] = $ic;
$_SESSION['sID'] = $ShootId;
$sID = $_SESSION['sID'];

include_once 'header_a.php';
?&gt;
&lt;div class="container"&gt;
&lt;?php
echo $_SESSION['SESS_TOTNUM']." images found ";
echo "for Shoot ID#: ".$_SESSION['sID']."&lt;br&gt;";
echo "*Note* - if input boxes come up GREEN, then images are already loaded into the database";
?&gt;
&lt;p&gt;
&lt;?php

$images1 = new Image($db);

$images1-&gt;ShootId = $colname_chk_Images;
$images1-&gt;directory = $colname1_chk_Images;
$images1-&gt;ClientID = $colname_get_Images;
$chk_Images = $images1-&gt;checkImages();
$get_Images = $images1-&gt;getImages();

$Images = array();

while ($row_get_Images = $get_Images-&gt;fetch(PDO::FETCH_ASSOC))
    {
        $Images[] = $row_get_Images['image_name'];
    }
?&gt;&lt;/p&gt;
&lt;form method="POST" name="form1" id="form1" action="input.php"&gt;
    &lt;table id="clientshoots" class="table table-condensed table-bordered table-small"&gt;
  &lt;tr&gt;
    &lt;th&gt;image_id&lt;/th&gt;
    &lt;th&gt;image_name&lt;/th&gt;
    &lt;th&gt;image_path&lt;/th&gt;
    &lt;th&gt;image_path_root&lt;/th&gt;
    &lt;th&gt;image_size&lt;/th&gt;
    &lt;th&gt;directory&lt;/th&gt;
    &lt;th width="auto"&gt;ShootId&lt;/th&gt;
    &lt;th width="auto"&gt;ClientID&lt;/th&gt;
    &lt;th&gt;ClientName&lt;/th&gt;
    &lt;th&gt;login&lt;/th&gt;
  &lt;/tr&gt;
  &lt;?php $ic=0;
   for($i=0;$i&lt;count($filesArray);$i++) { 
        $fileinfo = $filesArray[$i];
        $fname=$dir."/".$fileinfo;
        $fname2=$dir2."/".$fileinfo;
        $size = filesize($fname);
        $atime = date("F d, Y H:i:s", fileatime($fname));
        $mtime= date("F d, Y H:i:s", filemtime($fname));
        $perms=decoct(fileperms($fname) &amp; 0777);
        $type=filetype($fname);
        $pth=realpath($fname);
        $name=basename($fname);
        $dn=dirname($fname2);
        if (in_array($fileinfo, $Images)) {
        $entered=1;    
        echo "&lt;style type=\"text/css\"&gt;\n";
        echo "input {\n";
        echo "background-color:#00FF33;\n";
        echo "}\n";
        echo "&lt;/style&gt;";
        } 
    ?&gt;
    &lt;tr&gt;
    &lt;td&gt;&amp;nbsp;&lt;/td&gt;
      &lt;td&gt;&lt;input type="text" name="image_name[]" value="&lt;?php echo $fileinfo; ?&gt;" readonly/&gt;&lt;/td&gt;
      &lt;td&gt;&lt;input type="text" name="image_path[]" value="&lt;?php echo $dir; ?&gt;" readonly/&gt;&lt;/td&gt;
      &lt;td&gt;&lt;input type="text" name="image_path_root[]" value="&lt;?php echo $dir2; ?&gt;" readonly/&gt;&lt;/td&gt;
      &lt;td&gt;&lt;input type="number" name="image_size[]" value="&lt;?php echo $size; ?&gt;" readonly/&gt;&lt;/td&gt;
      &lt;td&gt;&lt;input type="text" name="directory[]" value="&lt;?php echo $maindir; ?&gt;" readonly/&gt;&lt;/td&gt;
      &lt;td&gt;&lt;input type="number" name="ShootId[]" value="&lt;?php echo $ShootId; ?&gt;" readonly/&gt;&lt;/td&gt;
      &lt;td&gt;&lt;input type="number" name="ClientID[]" value="&lt;?php echo $ClientID; ?&gt;" readonly/&gt;&lt;/td&gt;
      &lt;td&gt;&lt;input type="text" name="ClientName[]" value="&lt;?php echo $_SESSION['cName']; ?&gt;" readonly/&gt;&lt;/td&gt;
      &lt;td&gt;&lt;input type="text" name="login[]" value="&lt;?php echo $Clogin; ?&gt;" readonly/&gt;&lt;/td&gt;
    &lt;/tr&gt;
    &lt;?php next($filesArray);
    $ic=$ic+1;
    } 

    $_SESSION['SESS_IC'] = $ic;?&gt;
&lt;/table&gt;
&lt;?php if ($entered == 1){
  echo  "&lt;a href=\"viewClient.php?ClientID=".$ClientID."\" class=\"btn btn-primary active\"&gt;Return&lt;/a&gt;";
} else { 
  echo  "&lt;input class=\"btn-primary\" style=\"background-color:\" id=\"Insert records\" type=\"submit\" value=\"Insert records\"&gt;";
}?&gt;
&lt;input type="hidden" name="MM_insert" value="form1"&gt;
&lt;input type="hidden" name="sID" value="&lt;?php echo $sID; ?&gt;"&gt;
&lt;/form&gt;
&lt;/div&gt;
&lt;br&gt;
  &lt;!-- /container --&gt;
 &lt;?php include 'footer_b.php'; ?&gt;
</code></pre>

<p>and then the input.php page...</p>

<pre><code>&lt;?php
// set page headers
$page_title = "Enter Images into Database";
include_once 'auth.php';

// get database connection
include_once 'config/fpaddb.php';
include_once 'objects/clients.php';
include_once 'objects/photoshoots.php';
include_once 'objects/images.php';
include_once 'objects/ratings.php';

$database = new Database();
$db = $database-&gt;getConnection();

$sID = $_SESSION['sID'];
$ic = $_SESSION['SESS_IC'];
$ma = $_SESSION['SESS_CLIENT_MULTI'];
$gn = $_SESSION['SESS_CLIENT_GRPNO'];
$cID = $_SESSION['cID'];

$editFormAction = $_SERVER['PHP_SELF'];
if (isset($_SERVER['QUERY_STRING'])) {
  $editFormAction .= "?" . htmlentities($_SERVER['QUERY_STRING']);
}

    //Function to sanitize values received from the form. Prevents SQL injection

        function clean($str) {
        $str = filter_var(($str), FILTER_SANITIZE_STRING);
        return ($str);
    }

$image1 = new Image($db);   

$count = count($_POST['image_name']);
$fileinfo = clean($_POST['image_name']);

    //Check for duplicates
    if($fileinfo != '') {
            for($i=0;$i&lt;$count;$i++) { 
            $fileinfo = clean($_POST['image_name'][$i]);
            //echo $fileinfo;
            $image1-&gt;image_name = $fileinfo;
            $result = $image1-&gt;check4Dup(); 
            if($result) {
                if(count($result) &gt; 0) {
                    $errmsg_arr[] = 'Image already entered into Database';
                    $errflag = true;
                }
                $result = NULL;
            }
            else {
                die($e-&gt;getMessage());
            }
            next($count);   
            }
        }
$image1-&gt;ic = $ic;
$num = $image1-&gt;create();   

$colname_newImages = "-1";
if (isset($sID)) {
  $colname_newImages = $sID;
}
$image1-&gt;ShootId = $sID;
$newImages = $image1-&gt;countOneShoot();
$row_newImages = $newImages-&gt;fetch(PDO::FETCH_ASSOC);
$totalRows_newImages = $newImages-&gt;rowCount();
$ic2 = $totalRows_newImages;
$_SESSION['SESS_TOTNUM_ENT'] = $ic2;
header("Location: rs_images.php"); 


include_once 'header_a.php';
?&gt;
&lt;div class="container"&gt;
&lt;?php 
echo "Success! Number of images entered is ".$ic2; ?&gt;
&lt;br&gt;&lt;br&gt;
&lt;p&gt;&lt;input name="Verify" type="button" value="Verify Inputs" onclick="MM_goToURL('parent','rs_images.php');return document.MM_returnValue"/&gt;&lt;/p&gt;
&lt;/div&gt;
 &lt;?php include 'footer_b.php'; ?&gt;
</code></pre>

<p>And the Class file...</p>

<pre><code>&lt;?php

class Image{

        // database connection and table name
    private $dbh;
    private $table_name = "images";

    // object properties
    public $image_id;
    public $image_name;
    public $image_path;
    public $image_path_root;
    public $image_size;
    public $directory;
    public $ShootId;
    public $ClientID;
    public $ClientName;
    public $login;
    public $ic;

    public function __construct($db){
        $this-&gt;dbh = $db;
    }

    // Clean Function
    function clean($str){
        $str = filter_var(($str), FILTER_SANITIZE_STRING);
        return ($str);
    }

    // test function
    function test(){

        $ic = $this-&gt;ic;

        $i=1;
        $j=1;
        foreach ($_POST['image_name'] as $row=&gt;$iname)
        {
            $image_name = clean($iname);
            $image_path = clean($_POST['image_path'][$row]);
            $image_path_root = clean($_POST['image_path_root'][$row]);
            $image_size = clean($_POST['image_size'][$row]);
            $directory = clean($_POST['directory'][$row]);
            $ShootId = clean($_POST['ShootId'][$row]);
            $ClientID = clean($_POST['ClientID'][$row]);
            $ClientName = clean($_POST['ClientName'][$row]);
            $login = clean($_POST['login'][$row]);
            $Clogin = $login."');";

            $i=$i+1;
            $j=$j+1;

            $qry1st = "INSERT INTO `images` (image_name, image_path, image_path_root, image_size, directory, ShootId, ClientID, ClientName, login) VALUES ";
            $sql_array = "('".$image_name."', '".$image_path."', '".$image_path_root."', ".$image_size.", '".$directory."', ".$ShootId.", ".$ClientID.", '".$ClientName."', '".$Clogin;
            //$stmt = $this-&gt;dbh-&gt;prepare($qry1st.$sql_array);
            //$stmt-&gt;execute();
            echo $qry1st.$sql_array;
        }

    }

     // create function
    function create(){

        $ic = $this-&gt;ic;
        $qry1st = "INSERT INTO `images` (image_name, image_path, image_path_root, image_size, directory, ShootId, ClientID, ClientName, login) VALUES ";

        $sql_array = array(); // This is where we'll queue up the rows

        $queue_num = 50; // How many rows should be queued at once?
        $i=1;       
        foreach ($_POST['image_name'] as $row=&gt;$iname)
        {
        $image_name = clean($iname);
        $image_path = clean($_POST['image_path'][$row]);
        $image_path_root = clean($_POST['image_path_root'][$row]);
        $image_size = clean($_POST['image_size'][$row]);
        $directory = clean($_POST['directory'][$row]);
        $ShootId = clean($_POST['ShootId'][$row]);
        $ClientID = clean($_POST['ClientID'][$row]);
        $ClientName = clean($_POST['ClientName'][$row]);
        $login = clean($_POST['login'][$row]);
        if ($i==($_SESSION['SESS_TOTNUM'])) {
        $login_term = $login."');";
        }
        else
        {
        $login_term = $login."')";
        $i=$i+1;
        }

        $sql_array[] = "('".$image_name."', '".$image_path."', '".$image_path_root."', ".$image_size.", '".$directory."', ".$ShootId.", ".$ClientID.", '".$ClientName."', '".$login_term;

        // Add a new entry to the queue
        $c=0;
        if (count($sql_array) &gt;= $queue_num)
        { // Reached the queue limit

        $addImages = $this-&gt;dbh-&gt;query($qry1st . implode(', ', $sql_array)); // Insert those that are queued up
        $addImages-&gt;execute();

        $sql_array = array(); // Erase the queue
        }//End if 

        }//end foreach

        if (count($sql_array) &gt; 0) // There are rows left over
        {
        $addImages = $this-&gt;dbh-&gt;query($qry1st . implode(', ', $sql_array));
        $addImages-&gt;execute();
        }
    }

    function checkImages(){

    $query_chk_Images = "SELECT images.image_name FROM images WHERE ShootId = ? AND directory = ?";

    $chk_Images = $this-&gt;dbh-&gt;prepare ($query_chk_Images);
    $chk_Images-&gt;bindValue(1, $this-&gt;ShootId);
    $chk_Images-&gt;bindValue(2, $this-&gt;directory);
    $chk_Images-&gt;execute();
    return $chk_Images;
    }

    // create function
    function getImages(){

    $query_get_Images = "SELECT * FROM images WHERE ClientID = ? ORDER BY image_name ASC";

    $get_Images = $this-&gt;dbh-&gt;prepare ($query_get_Images);
    $get_Images-&gt;bindValue(1, $this-&gt;ClientID);
    $get_Images-&gt;execute();
    return $get_Images;

    }

     // create function
    function getImageID(){

        $query_rsImageID = "SELECT * FROM images WHERE ShootId = ? ORDER BY image_id ASC";

        $rsImageID = $this-&gt;dbh-&gt;prepare($query_rsImageID);
        $rsImageID-&gt;bindValue(1, $this-&gt;ShootId);
        $rsImageID-&gt;execute();

        return $rsImageID;
    }

     // create function
    function get_image_id(){

        $q = "SELECT image_id FROM images WHERE ShootId = ? ORDER BY image_id ASC";

        $stmt = $this-&gt;dbh-&gt;prepare($q);
        $stmt-&gt;bindValue(1, $this-&gt;ShootId);
        $stmt-&gt;execute();

        return $stmt;
    }

    // create function
    function countOneShoot(){

        $query_newImages = "SELECT * FROM images WHERE ShootId = ?";

        $newImages = $this-&gt;dbh-&gt;prepare($query_newImages);
        $newImages-&gt;bindValue(1, $this-&gt;ShootId);
        $newImages-&gt;execute();

        return $newImages;
    }

    // create function
    function check4Dup(){

        $qry = "SELECT * FROM `images` WHERE image_name = ?";

        $result = $this-&gt;dbh-&gt;prepare($qry);
        $result-&gt;bindValue(1, $this-&gt;image_name);
        $result-&gt;execute();

        return $result;
    }
}
</code></pre>

<p>I've striped out all the extra stuff I've tried, like entering the info one record at a time, binding the Values with colon prefixed field names instead of the ?'s.  I've tried different loops.  I think it comes down to trying to push too much through one query... but then why does it work on XAMPP and why was it working fine with PHP 5.2?</p>

<p>I appreciate any light that can be shed on this.  This is my first ever post with regards to PHP, MySQL or anything site related, I've been learning this stuff as I go and had it 90% completed and debugged and when I put it online to do some real testing with the actual directories and client folders that's when I found out that between PHP 5.4 and 5.2, there have been a number of changes and I found myself rewriting almost every line to move up to either MySQLi or PDO/OOP.  After doing a lot searching around the internet I've opted for the OOP approach and still need to rewrite even more of the code above to clean things up a ton, but right now I'm troubleshooting the INSERT failure which I have not been able to solve on my own or with the help of all the forums, posts and blogs I've read to date.</p>

