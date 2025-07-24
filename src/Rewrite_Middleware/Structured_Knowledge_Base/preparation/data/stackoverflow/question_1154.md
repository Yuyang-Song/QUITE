# How can I force jQuery Validate to check for duplicate username in database?
[Link to question](https://stackoverflow.com/questions/6117901/how-can-i-force-jquery-validate-to-check-for-duplicate-username-in-database)
**Creation Date:** 1306278380
**Score:** 3
**Tags:** javascript, jquery, validation, jquery-validate
## Question Body
<p>I'm coming into the middle of this project so I'm having to do a bit of re-writing because of sloppy code. I am using jQuery 1.6.1 and Validate 1.8.1.</p>

<p>First, here's the PHP which runs the back-end (<strong>dbquery.php</strong>):</p>

<pre><code>include("../includes/dbconnection.php");
session_start();

$location='';
$action='';
if($_GET['action']=='')
    $action=$_POST['action'];
else
    $action=$_GET['action'];

if($action=='checkusername'){
    $error='';
    $username=$_GET['username'];
    // exclude denied account
    $checkuserquery=mysql_query("Select * from database_users as user LEFT OUTER JOIN  database_approval as approval on user.user_id=approval.approval_user_id  where (approval.approval_status IS NULL or approval.approval_status &lt;&gt; 4) and user_username='".$username."'");
    $checkuserresult=mysql_numrows($checkuserquery);
    if($checkuserresult&gt;0) {
        $error = 'false';
    } else {
        $error = 'true';
    }
    echo $error;
} 
</code></pre>

<p>I'm trying to use jQuery Validate script to query the database for existing usernames on the fly. I either get two extremes: it never works or it always spits back given username as taken.</p>

<p>I believe the problem is that I cannot grab the input value of the username variable. When I create <code>alert (username)</code> within <code>function (output)</code>, it returns nothing. My assumption is that <code>.val()</code> is only working when the page loads thus anything I'm typing into the input isn't working for some reason.</p>

<p>Here's the jQuery I've re-written and copied from sources online:</p>

<pre><code>$(document).ready(function(){

$.validator.addMethod("checkAvailability",function(value,element){
    var username = $("#username").val();
    $.ajax({
          url: "dbquery.php",
          type: "GET",
          async: false,
          data: "action=checkusername&amp;username="+username,
          success: function(output) {
                     return output;
         }
     });
},"Sorry, this user name is not available");

// jQuery Validation script
    $("#signup").validate( {
        rules: {
            username: {
                required: true,
                minlength: 5,
                checkAvailability: true // remote check for duplicate username
            },
        },
        messages: {
            username: {
                required: "Enter a username"
            }
        },
        submitHandler: function(form) {
            form.submit();
        }
    });

});
</code></pre>

<p>I am only a beginner with jQuery but am getting my hands pretty dirty with this code. Am I on the right track or should I use <code>remote:</code> under <code>rules</code> and <code>username</code>? I've been told that the <code>remote</code> method won't work because of the dynamnic nature of the input value I'm trying to validate.</p>

<p>The other major problem I've been running into is making the remote error message ONLY show up when a username already exists in the database. Unfortunately, it shows up whether dbquery.php comes back as <code>true</code> or <code>false</code>. If I try an existing username, it returns <code>false</code>, then I rewrite a new username that returns <code>true</code>, the message doesn't go away. Similarly, when I write a username and it returns <code>true</code>, I still get the remote error message.</p>

<p>The original coder was referencing <code>getXMLHTTP</code> and using <code>ActiveXObject</code>. The method he programmed seemed a little outdated so I'm trying to make the code a little more contemporary and clean it up.</p>

<p>5/25 - <strong>I am editing this to include the OLD original JavaScript code which works but is using the outdated method which I'd like to get away from (<em>I have since removed the following code and replaced with jQuery above</em>)</strong>:</p>

<pre><code>function getXMLHTTP() { //function to return the xml http object
    var xmlhttp=false;    
    try{
        xmlhttp=new XMLHttpRequest();
    }
    catch(e)    {        
        try{            
            xmlhttp= new ActiveXObject("Microsoft.XMLHTTP");
        }
        catch(e){
            try{
            xmlhttp = new ActiveXObject("Msxml2.XMLHTTP");
            }
            catch(e1){
                xmlhttp=false;
            }
        }
    }

    return xmlhttp;
}
//validate username
function validateUsername(username){
    var strURL="dbquery.php?action=checkusername&amp;username="+username;
    var req = getXMLHTTP();        
    if (req) {            
        req.onreadystatechange = function() {
            if (req.readyState == 4) {
                // only if "OK"
                if (req.status == 200) {          
                    if(req.responseText=='notavailable'){
                        document.getElementById("errorusername").style.display="block";
                        document.getElementById("errorusername").innerHTML="&lt;div id=\"errors\"&gt;&lt;strong&gt;"+username+"&lt;/strong&gt; is already taken by another user.&lt;/div&gt;";
                        error = true;
                    }
                    else{
                        error = false;
                        document.getElementById("errorusername").style.display="none";   
                    }

                } else {
                    alert("There was a problem while using XMLHTTP:\n" + req.statusText);
                }
            }                
        }            
        req.open("GET", strURL, true);
        req.send(null);
    }     
}
</code></pre>

## Answers
### Answer ID: 16809130
<p>My code:</p>

<pre><code>$( "#myform" ).validate({
  rules: {
    EMAIL: {
      remote: {
        type: "post",  
        url: "checkMail.php",           
        data:{checkUsername:function(){return $("#EMAIL").val()}            
        }
      }
    }
  },messages:{EMAIL:{remote: "Already taken!"}}
});
</code></pre>

### Answer ID: 13921504
<p>I faced the same problem, But I find the easiest solution just return true or false after encoding into json through php.</p>

<pre><code>if ($users-&gt;username_exists())
{
    echo json_encode(FALSE);
}else{
    echo json_encode(TRUE);
}
</code></pre>

### Answer ID: 6164753
<p>Check when the validation function is getting called, what the value of <code>username</code> is and what the value of <code>output</code> is: is it <code>true</code> or <code>"true"</code>?</p>

<p>I'm guessing latter: a string, so you could just do:</p>

<pre><code>return output === "true" ? true : false; // I sincerely recommend using === here
</code></pre>

<p>Since if you <code>return "false";</code> will evaluate to <code>true</code> because it's a non-empty string - yay dynamic langauges! :/</p>

<p>Example with <code>remote</code>:</p>

<pre><code>$("#signup").validate( {
    rules: {
        username: {
            required: true,
            minlength: 5,
            remote: {
                url: "dbquery.php",
                type: "get",
                data: {
                    action: function () {
                        return "checkusername";
                    },
                    username: function() {
                        var username = $("#username").val();
                        return username;
                    }
                }
            }
        }
    },
    messages: {
        username: {
            required: "Enter a username"
        }
    },
    submitHandler: function(form) {
        form.submit();
    }
});
</code></pre>

<p>To set a custom error message your PHP file must return the message instead of false, so echo <code>"Sorry, this user name is not available"</code> in your PHP file.</p>

### Answer ID: 6134439
<p>While you adding <strong>addMethod</strong> you should return <strong>true</strong> or <strong>false</strong> from server side.</p>

<p>and also that value have to be returned from addMethod.</p>

<p>ie something like this</p>

<pre><code>$.validator.addMethod("checkAvailability",function(value,element){
    var parameter="action=checkusername&amp;username="+username;
    $.ajax({
          url: "dbquery.php",
          type: "POST",
          async: false,
          data: parameter
          success:function(output)
                 {
                    return output
                 }
     });
},"Sorry, this user name is not available");
</code></pre>

### Answer ID: 6118080
<p>On your server side script, try returning <code>true</code> or <code>false</code> instead of <code>available</code> and <code>notavailable</code>, as both of those strings are equivalent to <code>true</code>.</p>

