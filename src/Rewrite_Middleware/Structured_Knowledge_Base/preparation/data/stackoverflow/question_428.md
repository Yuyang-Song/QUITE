# Ajax passing php variable to javascript function as an argument
[Link to question](https://stackoverflow.com/questions/25649493/ajax-passing-php-variable-to-javascript-function-as-an-argument)
**Creation Date:** 1409762223
**Score:** 0
**Tags:** javascript, php, jquery, ajax
## Question Body
<p>I have three tables in my database: <code>Person (id, name, last_name), System (id, name), PersonInSystem(id, person_id, system_id)</code>. The last one is used to link a person with a system. </p>

<p>I use <code>&lt;select&gt;</code> to display every person from my DB like this</p>

<pre><code>echo '&lt;option value="'.$queryResult["id"].'"&gt;'.$queryResult["name"].' '.$queryResult["last_name].'&lt;/option&gt;';
</code></pre>

<p>I use Ajax to get the id and to send a query <code>SELECT * FROM Person WHERE id = ID_FROM_SELECT</code>. Then, I display the data like this (I can't copy the code, so I have to rewrite it from head, I will use pseudo PHP + HTML), and the main purpose of it is to edit a chosen person:</p>

<pre><code>&lt;form&gt;
Name: &lt;input type="text" value="'.$nameFromDB.'" name="name"&gt;
Last name: &lt;input type="text" value="'.$lastNameFromDB.'" name="lastname"&gt;
System: while () { // if one person is assigned to many systems, I will display them all in separate selects
            &lt;select&gt;&lt;option value="'.$systemAssignedToPerson.'"&gt;'.$systemAssignedToPerson.'&lt;/option&gt;
            while () {
            // display every system except for the one listed above
            }
            &lt;/select&gt;&lt;img src="drop.gif" onclick="deleteSystem(document.getElementById(\"system\").value)"&gt;&lt;input type="hidden" id="system" value="'.$systemAssignedToPerson.'"&gt; 
        }

&lt;input type-"submit" value="Edit" name="editPerson"&gt;
&lt;/form&gt;
</code></pre>

<p>Now if I want to unassign a person from given system, I would like to click the drop.gif image and trigger <code>deleteSystem(value)</code> function, which will send query <code>DELETE FROM PersonInSystem WHERE system_id = SYSTEM_ID_SENT and person_id = PERSON_ID_SENT</code>, but I can't pass the value and I don't have really idea how to do it (I'm new with Ajax). </p>

<p>I can store person's id in a session variable, but I don't know how to send system id, and also I don't want to sent the data to another page. </p>

<p>Also I would like to refresh the page with changed system assignment (the same person should be displayed).</p>

## Answers
### Answer ID: 25649837
<p>I think you need native javascript function call to the server</p>

<pre><code>function deleteSystem(value){  
    var deleteflag=confirm("Are you sure to delete?!!");
      if(deleteflag){
        //setup your request to the server
         window.location='delete.php?SYSTEM_ID_SENT='+value

       }

    } 
</code></pre>

<p>In your delete.php file you can get the SYSTEM_ID_SENT in this way</p>

<pre><code> $id=$_GET['SYSTEM_ID_SENT'];
 $personid=$_SESSION['your session variable name'];
// run your delete query
 $delqry=mysql_query("");
 if($delqry){
      //redirect to the page you want
      header('location:yourpage.php');
  }
</code></pre>

### Answer ID: 25649760
<p>Your deleteSystem JavaScript function needs to send the following kind of request to the server:</p>

<p>(Example: Handler file for unassign)</p>

<pre><code>"unassign.php?systemId=459&amp;personId=300"
</code></pre>

<p>(Example: Generic handler file)</p>

<pre><code>"handler.php?systemId=459&amp;personId=300&amp;action=unassign"
</code></pre>

<p>In unassign.php:</p>

<pre><code>$systemId = $_GET["systemID"];
$personId = $_GET["personID"];
/* Your SQL stuff here - 
statement something like 
DELETE FROM PersonInSystem WHERE person_id = "$personId" AND system_id = "$systemId" */
</code></pre>

<p>Improvements:
* Use a javascript library like Prototype (oldschool, lightweight) or jQuery (more heavy) for handling the Ajax stuff
* Use $_POST and post variables instead of $_GET
* Use a library for properly quoting your SQL
* Care about html special characters and proper input validation/filtering</p>

### Answer ID: 25649726
<p>Change the code as below.
It should work</p>

<pre><code>&lt;img src="drop.gif" onclick="deleteSystem('&lt;?php echo $systemAssignedToPerson;?&gt;')"&gt;
</code></pre>

