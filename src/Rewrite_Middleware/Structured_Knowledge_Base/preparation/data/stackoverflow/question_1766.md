# Using jquery to displaying query results in a form
[Link to question](https://stackoverflow.com/questions/6990528/using-jquery-to-displaying-query-results-in-a-form)
**Creation Date:** 1312853853
**Score:** 1
**Tags:** jquery
## Question Body
<p>A friend recently introduced me to jquery and now I'd like to use it rewrite and develop a inventory web application.  </p>

<p>My original app consisted of a simple web page that required you to enter an id number and click a button.  The id number is passed to a php file via the post method. The php file queries a database and displays the results in a table.</p>

<p>I created a HTML form that I would like to use update, enter new records, and display query results based on the button pressed.</p>

<p>At this time I want to display query results.  </p>

<p>I have figured out how to use jquery to display the results of a query in a div at the bottom of my form.  what I need help with is how if display the results in given location of the form.</p>

<p>Here is a real simple example of what I want:  </p>

<h2>HTML</h2>

<pre><code>&lt;html&gt;  
&lt; head&gt;  
&lt; title&gt;JQuery test&lt; /title&gt;  
&lt; /head&gt;  
&lt; body&gt;  
&lt; form&gt;  
&lt; table&gt;  
&lt; tr&gt;&lt; th&gt;Equipment ID&lt; /th&gt;  
&lt; td&gt;&lt; input type="text name="eqid" id="eqid" /&gt;&lt; /td&gt;  
&lt; th&gt;Manufacturer&lt; /th&gt;  
&lt; td&gt;&lt; input type="text name="manuf" id="manuf" /&gt;&lt; /td&gt;  
&lt; th&gt;Model&lt; /th&gt;  
&lt; td&gt;&lt; input type="text name="model" id="model" /&gt;&lt; /td&gt;&lt; tr&gt;  
&lt; /table&gt;  
&lt; div id=output&gt; &lt; /div&gt;  
&lt; /form&gt;  
&lt; /body&gt;  
&lt; /html&gt;  
</code></pre>

<h2>JQUERY</h2>

<pre><code>$("#submit_btn").click(function()  
{  
  var data = $('form:first').serialize();  
   $.ajax(  
   {  
    url:"passdata.php",   
    type: "POST",  
    data:data,  
    success:function(data)  
    {  
       $("#output").html(data);  
    } //end success  
   }); // end ajax  
});  // end click  
</code></pre>

<hr>

<p>This what I'm using on my php file</p>

<h2>PHP</h2>

<pre><code>&lt;?php
    $eqid = $_POST['eqid'];  
    $manuf = 'Apple';  
    $model ='IPAD 2';  

    echo "&lt;table border=0&gt;&lt;tr&gt;";
    echo "&lt;th align ='left'&gt;Manufacturer&lt;/th&gt;&lt;td&gt;&lt;input name='manuf' id='manuf' type='text' size='10' value=" . $manuf . "&gt;&lt;/td&gt;&lt;/tr&gt;";  
    echo "&lt;tr&gt;&lt;th align ='left'&gt;Surveyed by&lt;/th&gt;&lt;td&gt;&lt;input name='model' id='model' type='text' value=". $model . "&gt;&lt;/td&gt;&lt;/tr&gt;&lt;/total&gt;";  
?php&gt;
</code></pre>

<hr>

<p>I would like the results of the query (manufacture and model) to be displayed in the appropriate location of the form in the example above.</p>

<p>Any suggestion would be greatly appreciated.</p>

<p>Chris</p>

## Answers
### Answer ID: 6990790
<p>passdata.php needs to do your database querying then return the data. JSON is a nice way of doing this.</p>

<pre><code>&lt;?php
$iteminfo = array('id' =&gt; $id, 'manuf' =&gt; $manuf, 'model' =&gt; $model);

echo json_encode($iteminfo);
?&gt;
</code></pre>

<p>your ajax call then needs to take this data and populate your form.</p>

<pre><code>$("#submit_btn").click(function()  
{  
  var data = $('form:first').serialize();  
   $.ajax(  
   {  
    url:"passdata.php",   
    type: "POST", 
    dataType: 'json', 
    data:data, 
    success:function(data)  
    {  
       $("eqid").val(data.id); 
       $("manuf").val(data.manuf);
       $("model").val(data.model);      
    } //end success  
   }); // end ajax  
});  // end click 
</code></pre>

<p>Of course if you're using the same form for all CRUD operations, your php is going to have to be just as sneaky as your javascript. You sure this is a good idea for you?</p>

