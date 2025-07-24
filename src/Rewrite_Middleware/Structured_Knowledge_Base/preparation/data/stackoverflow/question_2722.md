# How do I retrieve an image sent in JSON to my server in PHP?
[Link to question](https://stackoverflow.com/questions/49126233/how-do-i-retrieve-an-image-sent-in-json-to-my-server-in-php)
**Creation Date:** 1520324457
**Score:** 0
**Tags:** javascript, php, json
## Question Body
<p>I want to retrieve a temporary image file sent from an app to my <em>PHP</em> script on my server. The problem is I want to take the image as declared in the path variable within the <code>JSON</code> and use it as a PHP file such as <code>$_FILES['picture']['name'];</code> just as if it was sent from a traditional web form file input.</p>

<p>The <em>PHP</em> code and <em>JSON</em> is below and any help is appreciated as I've been stuck on this!</p>

<p><strong>JSON:</strong></p>

<pre><code>{"_origin":-112,"_subscribers":[{"version":2,"active":true}],"_isProxy":false,"_values":[{"path":"/private/var/mobile/Containers/Data/Application/3EF19C87-AA05-4990-883B-7F569E118105/tmp/images/IMG_4980428D-A13F-4647-98F4-D9C75232D752.jpg","name":"IMG_4980428D-A13F-4647-98F4-D9C75232D752.jpg","width":901,"height":1200,"info":{}}],"_beganSubscriptions":true}
</code></pre>

<p>PHP:</p>

<pre><code>&lt;?php

//Grab variables
$pass = $_GET['pass'];
$title = $_POST['name'];
$email = $_POST['email'];
$market = $_POST['market'];
$account = "414890";
$date = date("Y-m-d");

//Decode JSON
$picture = json_decode($_POST['picture'], true);
$name = $picture-&gt;{'path'};

if($pass == "MY_KEY") { 

        $name = $_FILES['picture']['name'];
        $size = $_FILES['picture']['size'];
        $type = $_FILES['picture']['type'];

        $tmp_name = $_FILES['picture']['tmp_name'];

        $extension = substr($name, strpos($name, '.') + 1);

        $max_size = 8000000;

        //iOS Image Rotation Fix
        function correctImageOrientation($filename) {
          if (function_exists('exif_read_data')) {
            $exif = exif_read_data($filename);
            if($exif &amp;&amp; isset($exif['Orientation'])) {
              $orientation = $exif['Orientation'];
              if($orientation != 1){
                $img = imagecreatefromjpeg($filename);
                $deg = 0;
                switch ($orientation) {
                  case 3:
                    $deg = 180;
                    break;
                  case 6:
                    $deg = 270;
                    break;
                  case 8:
                    $deg = 90;
                    break;
                }
                if ($deg) {
                  $img = imagerotate($img, $deg, 0);       
                }
                // then rewrite the rotated image back to the disk as $filename
                imagejpeg($img, $filename, 95);
              } // if there is some rotation necessary
            } // if have the exif orientation info
          } // if function exists     
        }

        //Unique Image Filename
        $newfilename = round(microtime(true)) . '.' . end($tmp_name);


        //Validate and Post
        if(isset($name) &amp;&amp; !empty($name)){
            if(($extension == "jpg" || $extension == "jpeg" || $extension == "png" || $extension == "JPG" || $extension == "PNG" || $extension == "JPEG") &amp;&amp; $extension == $size&lt;=$max_size){
                $location = "../member-images/";
                correctImageOrientation($tmp_name);
                if(move_uploaded_file($tmp_name, $location.$newfilename)){



                    // Insert Info into Database
                    $mysqli-&gt;query("INSERT INTO voting (account, date, title, market, image) VALUES ('$account', '$date', '$title', '$market', $newfilename')");

                    /* Insert Info into Database
            $mysqli-&gt;query("INSERT INTO voting (account, date, title, phone, carrier, note, market, image) VALUES ('$account', '$date', '$title', '$cleaned_phone', '$carrier', '$note', '$market', '$newfilename')"); */


                }else{
                    echo 'Failed to Upload Photo. Please click back and try again.';
                }
            }else{
                echo 'File size should be no more than 100 KiloBytes &amp; Only JPEG, JPG or PNG File. Please click back and try again.';
            }
        }else{
            echo 'Please click back and be sure to select a photo file.';
        }

        // close connection 
        $mysqli-&gt;close();


} else {

    die();

}


?&gt;
</code></pre>

