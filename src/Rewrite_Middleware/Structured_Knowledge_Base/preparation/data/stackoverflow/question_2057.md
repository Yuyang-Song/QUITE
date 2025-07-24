# Ajax reload not working
[Link to question](https://stackoverflow.com/questions/17159542/ajax-reload-not-working)
**Creation Date:** 1371521227
**Score:** 1
**Tags:** php, javascript, ajax, .htaccess, mod-rewrite
## Question Body
<p>I'll start this out by saying this: I'm very new to all of this. I'm really just crashing through everything I can find out. I'm an artist and a writer, I've only really gotten into developing this stuff in the last year.</p>

<p>I'm developing a project that combines a cms, a project manager, and a database front-end (and anything else that my group might want to add). I'm building this out of php, mysql, and javascript. But I'm having trouble getting past setting up the foundation.</p>

<p>I'm trying to test some things out, first and foremost, a mysql query using AJAX to call a php script for the data back-end.</p>

<p>This project has two folders, a private and a public. And everything goes through an index.php bootstrap file. I have a .htaccess mod_rewrite that looks like this:</p>

<pre><code>&lt;IfModule mod_rewrite.c&gt;
RewriteEngine On

RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d

# Rewrite all other URLs to index.php/URL
RewriteRule ^(.*)$ index.php/$1 [PT,L]

&lt;/IfModule&gt;
&lt;IfModule !mod_rewrite.c&gt;
    ErrorDocument 404 /index.php
&lt;/IfModule&gt;
  php_value include_path "../private/libs/classes/:../private/config/:../private/config/inc/:../private/libs/smarty/:../private/libs/scripts/:../private/libs/smarty/libs/:../private/libs/smarty/libs/sysplugins/:../private/libs/smarty/libs/plugins/"
</code></pre>

<p>I have a bit of javascript here, which is supposed to call the php script showCode.php:</p>

<pre><code>&lt;script&gt;
    function showCode(str)
    {
        if (str=="")
          {
              document.getElementById("code").innerHTML="";
              return;
          }
        if (window.XMLHttpRequest)
              {// code for IE7+, Firefox, Chrome, Opera, Safari
              xmlhttp=new XMLHttpRequest();
          }
        else
          {// code for IE6, IE5
            xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
          }
        xmlhttp.onreadystatechange=function()
          {
              if (xmlhttp.readyState==4 &amp;&amp; xmlhttp.status==200)
                {
                    document.getElementById("code").innerHTML=xmlhttp.responseText;
                }
          }
        xmlhttp.open("POST","showCode.php",false);
        xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");
        xmlhttp.send("id="+str);
    }
&lt;/script&gt;
</code></pre>

<p>I'm not concerned with my php. I've tested all of the scripts separately and they work fine, my bootstrap file has never given me any trouble either. I have a relatively complex loading system that has always worked perfectly.</p>

<p>I have a serious hunch that it's the .htaccess that's causing me the trouble. the mod_rewrite is probably causing the ajax to not reach the showCode.php file, but for the life of me I cannot find the answer to this.</p>

<p>Any suggestions?</p>

<p>I would love any help, but I am not one to work with jquery... I am really intent on learning the ins and outs of base javascript. Once I'm to a proficient enough point with that, I'll move on to a library.</p>

<p>--EDIT-------------------</p>

<p>Ok, thanks to some of the helpful advice I've gotten here, I've discovered that .htaccess is not my problem. I was figuring that whatever code I brought in through the AJAX function would use my previous PHP setup (the required files I bring in through my bootstrap)... which, upon simply thinking about it, is ridiculous because php runs on the server and the AJAX calls just reload the div on the client. SO... now I have to fix my code accordingly... </p>

<p>--FINAL------------------</p>

<p>Yeah... I needed to include the baseConfig script in my showCode script. Everything works now, with the .htaccess rewrites in place. Thanks for pointing me in the right direction.</p>

## Answers
### Answer ID: 17179921
<p>If you think you're having trouble with some kind of script or file, find a way to try the whole setup without that script or file... in my case, it was the .htacces which I thought was the culprit. Turned out to not have anything to do with that file, which I was only able to discover after I had commented out my rewrites.</p>

<p>So, the real answer to this was... when you're doing an AJAX call to another script that requires logic or other files that are loaded through a bootstrap... don't assume the bootstrap is going to load it. PHP is, of course, a server-side language. When you call an AJAX function, you're doing it from the client, the original bootstrap is already done executing... Require whatever you need in the called php, or create some kind of ajax bootstrap file that you can load any script through via a javascript function. Here's an example of a simple one... or maybe a not-so-simple one... either way, it's my example:</p>

<p><strong>Javascript:</strong></p>

<pre><code>    function ajaxLoader(post,script,div){

    if (post==""){
        document.getElementById(div).innerHTML="";
        return;
    }

    if (window.XMLHttpRequest){
        // code for IE7+, Firefox, Chrome, Opera, Safari
        xmlhttp=new XMLHttpRequest();
    }else{
        // code for IE6, IE5
        xmlhttp=new ActiveXObject("Microsoft.XMLHTTP");
    }

    xmlhttp.onreadystatechange=function(){
        if (xmlhttp.readyState==4 &amp;&amp; xmlhttp.status==200){
            document.getElementById(div).innerHTML=xmlhttp.responseText;
        }
    }

    xmlhttp.open("POST","/includes/scripts/ajaxBootstrap.php",true);
    xmlhttp.setRequestHeader("Content-type","application/x-www-form-urlencoded");

    /* This is a very simple one, with only 'id' being sent to the script 
       by the sender below. With more effort, I'm sure you could make it send 
       multiple data by taking out "&amp;id=" and only working with the post variable*/ 

    xmlhttp.send("script="+script+"&amp;id="+post);
    }
</code></pre>

<p><strong>PHP ajax bootstrap:</strong></p>

<p><em>To load all necessary scripts/functions/includes/etc, without having to include with every new script</em></p>

<pre><code>&lt;?php
    // require configuration
    require_once('config.php');

    // test whether the $_POST array has a key called 'script', which should be set in the javascript function.
    IF(array_key_exists('script',$_POST)){
        foreach($_POST as $key=&gt;$data){
        // set variable variables from the $_POST data
            $$key = $data;
        }
        // include the called script
        include($script.".php");
    }ELSE{
    // place any error messages you'd like to show.
    }
?&gt;
</code></pre>

<p>Also, I'm not sure if this is necessary (one could circumvent this with ini_set in the config file, probably), but I found I had to put an .htaccess file with compensated php include_paths due to the bootstrap being placed in a different folder than my index.php file.</p>

<p><strong>PHP script:</strong></p>

<p><em>This is what actually executes the code we want</em></p>

<pre><code>&lt;?php
    $form = new forms;
    $id = $form-&gt;getPOST('id');
    $connection = new dbPortal;
    eval($connection-&gt;showSingle('pages', 'page_content', $id));
 ?&gt;
</code></pre>

<p>I've tested this and it works perfectly for me, of course, including my classes and other things which I have not shown here.</p>

