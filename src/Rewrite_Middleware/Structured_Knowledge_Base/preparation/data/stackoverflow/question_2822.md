# How to validate file size to upload php mysql
[Link to question](https://stackoverflow.com/questions/53927078/how-to-validate-file-size-to-upload-php-mysql)
**Creation Date:** 1545794050
**Score:** 0
**Tags:** php, mysql, file-upload
## Question Body
<p>I'm newby with php + mysql and i have this script to upload a file to a server and insert the data to a database. All works fine except that I don't know how to limit the file size to 3MB. Here is the code:</p>

<pre><code>// limit file types
$valid_extensions = array('jpeg', 'jpg', 'png', 'gif', 'bmp' , 'pdf' , 'doc' , 'ppt'); // valid extensions
$path = 'uploads/'; // upload directory

if(!empty($_POST['name']) || !empty($_POST['email']) || $_FILES['image'])
{
$img = $_FILES['image']['name'];
$tmp = $_FILES['image']['tmp_name'];

// get uploaded file extension
$ext = strtolower(pathinfo($img, PATHINFO_EXTENSION));

// rename file to prevent rewrite existing files
$final_image = rand(1000,1000000).$img;

// check's valid format
if(in_array($ext, $valid_extensions)) 
{ 
$path = $path.strtolower($final_image); 

if(move_uploaded_file($tmp,$path)) 
{
echo "File uploaded succesfully";
$name = $_POST['name'];
$email = $_POST['email'];

//include database configuration file
include_once 'db.php';

//insert form data in the database
$insert = $db-&gt;query("INSERT uploading (name,email,file_name) VALUES ('".$name."','".$email."','".$path."')");

}
} 
else 
{
echo 'File not uploaded, try again';
}
}
</code></pre>

<p>I'll appreciatte any help.</p>

## Answers
### Answer ID: 53928353
<p>The $_FILES is a global variable in PHP and an array element and contains the key named </p>

<p><code>size</code>,
this is the size of the file which you are trying to upload, you can add any validations on this key element.</p>

<p>Ref: <a href="http://php.net/manual/en/reserved.variables.files.php" rel="nofollow noreferrer">http://php.net/manual/en/reserved.variables.files.php</a></p>

### Answer ID: 53927128
<p>you can modify the php.ini file to set a maximum file size that you will allow to upload. </p>

<p>upload_max_filesize = 40M</p>

<p>or you can set it in your script a</p>

<pre><code>$fileSize = $_FILES['image']['size'];
</code></pre>

<p>than use a if statement </p>

<pre><code>if ($fileSize &lt; 3000000) {
            echo "this image cannot be uploaded";
        }
</code></pre>

<p>Inserted in your script. </p>

<pre><code>   &lt;?php


    $valid_extensions = array('jpeg', 'jpg', 'png', 'gif', 'bmp' , 'pdf' , 'doc' , 'ppt'); // valid extensions
    $path = 'uploads/'; // upload directory

    if(!empty($_POST['name']) || !empty($_POST['email']) || $_FILES['image'] )
    {


    $img = $_FILES['image']['name'];
    $tmp = $_FILES['image']['tmp_name'];
    $fileSize = $_FILES['image']['size']

    // get uploaded file extension
    $ext = strtolower(pathinfo($img, PATHINFO_EXTENSION));

    // rename file to prevent rewrite existing files
    $final_image = rand(1000,1000000).$img;



    // check's valid format
    if(in_array($ext, $valid_extensions))
    {
    $path = $path.strtolower($final_image);

// if condition to make sure filesize is less than 3000000 bytes, 3MB
    if($fileSize &lt; 3000000){ //php uses bytes so 3000000 is 3MB 


    if(move_uploaded_file($tmp,$path))
    {
    echo "File uploaded succesfully";
    $name = $_POST['name'];
    $email = $_POST['email'];

    //include database configuration file
    include_once 'db.php';

    //insert form data in the database
    $insert = $db-&gt;query("INSERT uploading (name,email,file_name) VALUES ('".$name."','".$email."','".$path."')");
    }
    } else {

    echo 'Cannot upload file too large' ;
    }
    }

    else
    {
    echo 'File not uploaded, try again';
    }
    }

    ?&gt;
</code></pre>

### Answer ID: 53927121
<p>First, fetch file size in KB as:</p>

<pre><code>$fileSize = $_FILES['image']['size'];
</code></pre>

<p>Then you can convert bytes into MBs as:</p>

<p><code>$fileSizeInMB = ($fileSize)/(1024*1024)</code>;</p>

<p>Then you can have a check if this $fileSizeInMB is greater than 3 or not.</p>

