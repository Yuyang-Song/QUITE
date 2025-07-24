# deleting mysql records with ajax
[Link to question](https://stackoverflow.com/questions/530307/deleting-mysql-records-with-ajax)
**Creation Date:** 1234218140
**Score:** 2
**Tags:** php, javascript, ajax
## Question Body
<p>I would like to know the best way to delete records from a live database and refresh the page instantly. At the moment I am using ajax, with the following javascript method:</p>

<pre><code>function deleterec(layer, pk) {
   url = "get_records.php?cmd=deleterec&amp;pk="+pk+"&amp;sid="+Math.random();
   update('Layer2', url);
}
</code></pre>

<p>if cmd=deleterec on the php page, a delete is done where the primary key = pk. This works fine as in the record is deleted, however the page is not updated.</p>

<p>My update method is pretty simple:</p>

<pre><code>function update(layer, url) {
    var xmlHttp=GetXmlHttpObject(); //you have this defined elsewhere

    if(xmlHttp==null) {
        alert("Your browser is not supported?");
    }

    xmlHttp.onreadystatechange = function() {
        if(xmlHttp.readyState==4 || xmlHttp.readyState=="complete") {
            document.getElementById(layer).innerHTML=xmlHttp.responseText;
        } else if (xmlHttp.readyState==1 || xmlHttp.readyState=="loading") {
            document.getElementById(layer).innerHTML="loading";
        }

       //etc
    }

    xmlHttp.open("GET",url,true);
    xmlHttp.send(null);
}
</code></pre>

<p>how to delete or alter record, and upate the page.</p>

<p>At the moment my ajax framework works by passing data to a javascript update method, which works fine for selecting different queries to display in different layers. </p>

<p>I want to add the functionality to delete, or alter the records in a certain way.</p>

<p>I am wondering if it is possible when clicking a link to execute a query and then call my update method and refesh tge page. Is there any easy way to do this given my update methods?</p>

<p>I would like to avoid rewriting my update method if possible. </p>

<p>WOuld the simplest method be to have the php page(only in the layer) reload itself after executing a mysql query?</p>

<p>Or to make a new "alterstatus" method, which would pass delete or watch as a paramter, and have the php execute a query accordingly and then update the page?</p>

<p>edit: The links are generated like so. deleterec would be called from an additional link generated.</p>

<p>{</p>

<pre><code>$pk = $row['ARTICLE_NO'];

echo '&lt;tr&gt;' . "\n"; 

    echo '&lt;td&gt;&lt;a href="#" onclick="updateByPk(\'Layer2\', \'' . $pk . '\')"&gt;'.$row['USERNAME'].'&lt;/a&gt;&lt;/td&gt;' . "\n"; 

echo '&lt;td&gt;&lt;a href="#" onclick="updateByPk(\'Layer2\', \'' . $pk . '\')"&gt;'.$row['shortDate'].'&lt;/a&gt;&lt;/td&gt;' . "\n"; 

echo '&lt;td&gt;&lt;a href="#" onclick="updateByPk(\'Layer2\', \'' . $pk . '\')"&gt;'.$row['ARTICLE_NAME'].'&lt;/a&gt;&lt;/td&gt;' . "\n"; 


echo '&lt;td&gt;&lt;a href="#" onclick="deleteRec(\'Layer2\', \'' . $pk . '\')"&gt;'.$row['ARTICLE_NAME'].'&lt;/a&gt;&lt;/td&gt;' . "\n"; 

echo '&lt;/tr&gt;' . "\n"; 
</code></pre>

<p>}</p>

<p>edit: the update method can not be modified, as it is used by the updateByPk and updateBypg methods which need a layer.</p>

## Answers
### Answer ID: 600805
<p>I have found that there are three basic operations that one performs with an Ajax based administration page, update, delete and append. Each of these actions changes the DOM in inherently different ways. </p>

<p>You've written a function that can <b>update</b> an existing div in the DOM, but this function won't work well if you want to <b>remove</b> a div from the DOM like you do in this question nor will it work well when you decide that you want to add new records using Ajax. </p>

<p>In order to handle this correctly, you first need to assign an unique id to each row that you output:</p>

<pre><code>$pk = $row['ARTICLE_NO'];

echo '&lt;tr id=\"article_' . $pk . '\"&gt;' . "\n"; 

        echo '&lt;td&gt;&lt;a href="#" onclick="updateByPk(\'Layer2\', \'' . $pk . '\')"&gt;'.$row['USERNAME'].'&lt;/a&gt;&lt;/td&gt;' . "\n"; 

echo '&lt;td&gt;&lt;a href="#" onclick="updateByPk(\'Layer2\', \'' . $pk . '\')"&gt;'.$row['shortDate'].'&lt;/a&gt;&lt;/td&gt;' . "\n"; 

echo '&lt;td&gt;&lt;a href="#" onclick="updateByPk(\'Layer2\', \'' . $pk . '\')"&gt;'.$row['ARTICLE_NAME'].'&lt;/a&gt;&lt;/td&gt;' . "\n"; 


echo '&lt;td&gt;&lt;a href="#" onclick="deleteRec(\'article_' . $pk .'\', )"&gt;'.$row['ARTICLE_NAME'].'&lt;/a&gt;&lt;/td&gt;' . "\n"; 

echo '&lt;/tr&gt;' . "\n";
</code></pre>

<p>And then you need to create a delete function that can remove the table row:</p>

<pre><code>function delete(layer, url) {
    var xmlHttp=GetXmlHttpObject(); //you have this defined elsewhere

    if(xmlHttp==null) {
        alert("Your browser is not supported?");
    }

    xmlHttp.onreadystatechange = function() {
        if(xmlHttp.readyState==4 || xmlHttp.readyState=="complete") {
            if(xmlHttp.responseText == 'result=true') {
                // Here you remove the appropriate element from the DOM rather than trying to update something within the DOM
                var row = document.getElementById(layer);
                row.parentNode.removeChild(row);
            }
        } else if (xmlHttp.readyState==1 || xmlHttp.readyState=="loading") {
            document.getElementById(layer).innerHTML="loading";
        }

       //etc
    }

    xmlHttp.open("GET",url,true);
    xmlHttp.send(null);
}
</code></pre>

<p>And then lastly adjust your deleterec function:</p>

<pre><code>function deleteRec(layer, pk) {
   url = "get_records.php?cmd=deleterec&amp;pk="+pk+"&amp;sid="+Math.random();
   delete(layer, url);
}
</code></pre>

<p>As a final note I have to echo the sentiments of others that have suggested the usage of a framework. The usage of any framework be it jQuery, Prototype, Dojo or other, is going to have both short term and long term benefits. Additionally, I would NEVER actually use GET to perform an operation of this nature. All that one has to do to force the deletion of an element is hit the appropriate URL and pass in the relevant article number. </p>

### Answer ID: 601026
<p>I would have voted up one of the other answers that recommended jQuery, but I don't have enough points yet.</p>

<p>I think the easiest way to achieve the "update" you're looking for is to either have your AJAX delete return the relevant post-delete HTML, or you could use jQuery to fire off the delete and then delete the tr, div, etc. from the page.</p>

<pre><code>jQuery.post("get_records.php ", { cmd: "delete", pk: 123 }, function() {
    jQuery("tr.row123").remove(); 
})
</code></pre>

### Answer ID: 598151
<p>To Delete and update DOM:</p>

<pre><code>echo '&lt;td&gt;&lt;a href="#" onclick="deleteRec(this, \'' . $pk . '\')"&gt;'.$row['ARTICLE_NAME'].'&lt;/a&gt;&lt;/td&gt;' . "\n"; 

function deleterec(row, pk) {
    var rowId = row.parentNode.parentNode.rowIndex;
    url = "get_records.php?cmd=deleterec&amp;pk="+pk+"&amp;sid="+Math.random();
    update(rowId, url);
}

function update(rowId, url) {
    var xmlHttp=GetXmlHttpObject(); //you have this defined elsewhere

    if(xmlHttp==null) {
        alert("Your browser is not supported?");
    }

    xmlHttp.onreadystatechange = function() {
        if(xmlHttp.readyState==4 || xmlHttp.readyState=="complete") {
            document.getElementById(layer).innerHTML=xmlHttp.responseText;
            deleteRow(rowId); //You may wish to check the response here
        } else if (xmlHttp.readyState==1 || xmlHttp.readyState=="loading") {
            document.getElementById(layer).innerHTML="loading";
        }
    }
    xmlHttp.open("GET",url,true);
    xmlHttp.send(null);
}


function deleteRow(i){
    document.getElementById('myTable').deleteRow(i)
}
</code></pre>

### Answer ID: 597815
<p>I would not use a HTTP GET method to delete records from the database, I would use POST. And I would not use Ajax since the interaction you are looking for is clearly <strong>synchronous</strong> : delete then update. I would use a regular submit (either JS or HTML).</p>

<p>That said, the only remaining solution if you are really committed to use XHR is a callback based on response from the server like suggested by Renzo Kooi.</p>

### Answer ID: 579829
<p>When you say "update instantly" I presume you mean update the Document via Javascript. Ajax and page refreshes don't go together. </p>

<p>How are you displaying your existing rows of data? Say for example you were listing them like this:</p>

<pre><code>&lt;div id="row1"&gt;row 1&lt;/div&gt;
&lt;div id="row2"&gt;row 2&lt;/div&gt;
</code></pre>

<p>Where row1 and row2 are rows in your database with primary keys 1 &amp; 2 respectively. Use a simple javascript function to remove the associated div from the DOM:</p>

<pre><code>function deleterec(pk) {
    url = "get_records.php?cmd=deleterec&amp;pk="+pk+"&amp;sid="+Math.random();
    update(pk, url);
}

function update(pk, url) {
    var xmlHttp=GetXmlHttpObject(); //you have this defined elsewhere

    if(xmlHttp==null) {
        alert("Your browser is not supported?");
    }

    xmlHttp.onreadystatechange = function() {
        if(xmlHttp.readyState==4 || xmlHttp.readyState=="complete") {
            document.getElementById(layer).innerHTML=xmlHttp.responseText;
            removeDomRow(pk); //You may wish to check the response here
        } else if (xmlHttp.readyState==1 || xmlHttp.readyState=="loading") {
            document.getElementById(layer).innerHTML="loading";
        }
    }
    xmlHttp.open("GET",url,true);
    xmlHttp.send(null);
}
</code></pre>

<p>And the following function to manipulate the DOM:</p>

<pre><code>function removeDomRow(pk){
        var row = document.getElementById('row' + pk);
        row.parentNode.removeChild(row);
}
</code></pre>

<p>If you're using tables:</p>

<pre><code>&lt;tr id="row1"&gt;
    &lt;td&gt;row 1&lt;/td&gt;
&lt;/tr&gt;
&lt;tr id="row2"&gt;
    &lt;td&gt;row 2&lt;/td&gt;
&lt;/tr&gt;
</code></pre>

<p>You could use:</p>

<pre><code> function removeDomRow( id ) { // delete table row
    var tr = document.getElementById( 'row' + id );
    if ( tr ) {
      if ( tr.nodeName == 'TR' ) {
        var tbl = tr; // Look up the hierarchy for TABLE
        while ( tbl != document &amp;&amp; tbl.nodeName != 'TABLE' ) {
          tbl = tbl.parentNode;
        }
        if ( tbl &amp;&amp; tbl.nodeName == 'TABLE' ) {
          while ( tr.hasChildNodes() ) {
            tr.removeChild( tr.lastChild );
          }
          tr.parentNode.removeChild( tr );
        }
      }
    }
</code></pre>

<p>In respect to theraccoonbear's point, if you were to make use of a framework such as Qjuery things would be far easier:</p>

<pre><code>$('#row'+id).remove();
</code></pre>

### Answer ID: 577759
<blockquote>
  <p>I am wondering if it is possible when clicking a link to execute a query and then call my update method and refesh tge page. Is there any easy way to do this given my update methods?</p>
</blockquote>

<p>So, why don't you just submit a form?</p>

### Answer ID: 577744
<p>You have two choice:</p>

<ul>
<li><p>Do a complete round trip, ie don't update the UI until you know the item has been successfully deleted, OR</p></li>
<li><p>Lie to your users</p></li>
</ul>

<p>If the results of the operation are questionable and important, the use the first option. If you're confident of the result, and people don't need to know the details, use the second.</p>

<p>Really, nothing keeps people happy so much as being successfully lied to.</p>

### Answer ID: 577265
<p>You could create a callback that at the client side takes care of updating the screen. You can do that within your XHR function.</p>

<pre><code>    function update(layer, url) {
        var xmlHttp=GetXmlHttpObject(),
             callbackFn = function(){ 
                  /* ... do thinks to reflect the update on the user screen,
                         e.g. remove a row from a table ...*/
                 };

        if(xmlHttp==null) {
            alert("Your browser is not supported?");
        }

        xmlHttp.onreadystatechange = function() {
            if(xmlHttp.readyState==4 || xmlHttp.readyState=="complete") {
                /* if the server returns no errors run callback 
                   (so server should send something like 'ok' on successfull
                   deletion 
                */
                if (xmlHttp.responseText === 'ok') {
                      callback();
                }
        //=&gt;[...rest of code omitted]
</code></pre>

### Answer ID: 530370
<p>Without digging too much into your code specifics, I don't know of any way to update/delete from the server side DB without doing a round trip (either AJAX or a page navigation).  I would however recommend using a JavaScript framework (like <a href="http://jquery.com/" rel="nofollow noreferrer">jQuery</a>, or something else) to handle the AJAX and DOM manipulations.  That should, in theory, alleviate any cross-browser troubleshooting on the client side of thinbs.</p>

