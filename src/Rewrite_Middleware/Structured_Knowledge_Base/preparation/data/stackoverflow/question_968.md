# Edit Database entry with AJAX and return edited data
[Link to question](https://stackoverflow.com/questions/52307888/edit-database-entry-with-ajax-and-return-edited-data)
**Creation Date:** 1536820552
**Score:** 0
**Tags:** php, jquery, mysql, ajax
## Question Body
<p>I have the following form: </p>

<pre><code> &lt;?php 
        echo "&lt;strong&gt;".$Event_data_fetched['event_subject']."&lt;/strong&gt;&lt;br /&gt;";

        echo   '&lt;form id="Event_Editing" action="#" method="post"&gt;
                    Event-Type:&lt;br /&gt;
                    &lt;select name="edited_event_type"&gt;
                        &lt;option&gt;'.$Event_type.'&lt;/option&gt;
                        &lt;option&gt;'.$Unselected_1.'&lt;/option&gt;
                        &lt;option&gt;'.$Unselected_2.'&lt;/option&gt;
                    &lt;/select&gt;&lt;br /&gt;&lt;br /&gt;

                    Event-Subject:&lt;br /&gt;
                    &lt;input type="text" name="edited_event_subject" value="'.$Event_data_fetched['event_subject'].'"/&gt;&lt;br /&gt;&lt;br /&gt;

                    &lt;input id="Edit_Event" type="submit" name="Edit_Event" value="Speichern"&gt;
                &lt;/form&gt;';               
    ?&gt;
</code></pre>

<p>The form is meant to display data, from a row in the database and offer the user the option to edit said data. And I already have a query that handles the data and rewrites the edited data in the Database, when the form is submitted: </p>

<pre><code>if(isset($_POST['Edit_Event'])){
        $New_Type_Value = $_POST['edited_event_type'];
        $New_Subject_Value = $_POST['edited_event_subject'];

        if($New_Type_Value == "Meet"){
            $New_Type_Value = 1;
        }
        else if($New_Type_Value == "Clubday"){
            $New_Type_Value = 2;
        }
        else if($New_Type_Value == "Surprise-Event"){
            $New_Type_Value = 3;
        }

        $edit_data_query = "UPDATE b6vjp_event
                            SET event_type_id = $New_Type_Value,
                                event_subject = '$New_Subject_Value'
                            WHERE id = $Event_id";

        mysqli_query($GLOBALS['connect'], $edit_data_query);
    }
</code></pre>

<p>Now I want to put this block of code into a separate .php File. </p>

<p>My ultimate goal is to post the form to an AJAX script, that then sends the data to a separate file, where it edits the DB with the new data. After it has been inserted the newly edited data should be given back and written back into the form. I also need to post a variable with the ID of the row. Otherwise, the query won't know where to insert the edited data.</p>

<p>I googled a bunch and tried a lot of things, but don't seem to find anything specifically working for me. I did stumble across a code that looks like a good start but not what I want to do: </p>

<pre><code> &lt;script type='text/javascript'&gt;
    /* attach a submit handler to the form */
    $("#Event_Editing").submit(function(event) {

    /* stop form from submitting normally */
    event.preventDefault();

    /* get the action attribute from the &lt;form action=""&gt; element */
    var $form = $( this ),
        url = $form.attr( 'action' );

    /* Send the data using post with element id name and name2*/
    var posting = $.post( url, { name: $('#name').val(), name2: $('#name2').val() } );

    /* Alerts the results */
    posting.done(function( data ) {
        alert('success');
    });
    });
&lt;/script&gt;
</code></pre>

<p>My biggest Problem is that I'm not that good at AJAX. Does anybody know how I would go about doing this? </p>

## Answers
### Answer ID: 52308101
<p>You can set up the AJAX call like so:</p>

<pre><code>&lt;?php 
echo "&lt;strong&gt;".$Event_data_fetched['event_subject']."&lt;/strong&gt;&lt;br /&gt;";

echo   '&lt;form id="Event_Editing" action="#" method="post"&gt;
            Event-Type:&lt;br /&gt;
            &lt;select name="edited_event_type"&gt;
                &lt;option&gt;'.$Event_type.'&lt;/option&gt;
                &lt;option&gt;'.$Unselected_1.'&lt;/option&gt;
                &lt;option&gt;'.$Unselected_2.'&lt;/option&gt;
            &lt;/select&gt;&lt;br /&gt;&lt;br /&gt;

            Event-Subject:&lt;br /&gt;
            &lt;input type="text" name="edited_event_subject" value="'.$Event_data_fetched['event_subject'].'"/&gt;&lt;br /&gt;&lt;br /&gt;

            &lt;input id="Edit_Event" type="submit" name="Edit_Event" value="Speichern" onclick='editData();'&gt;
        &lt;/form&gt;';        

?&gt;


&lt;script&gt;

    function editData(){
        var value = document.getElementById('Event_Editing').value;

        $.ajax({
            url : 'your-backend-file-with-DB-Query.php',
            method : 'POST',// OR GET
            data: {value:value},
            dataType: 'json',
            success:function(data) {

            },
            error: function (xhr, ajaxOptions, thrownError) {
                alert("readyState: "+xhr.readyState+"\nstatus: "+xhr.status);
                alert("responseText: "+xhr.responseText);
            }

        }); 

    }

&lt;/script&gt;
</code></pre>

<p>Then in your backend file you can receive the values like so:</p>

<pre><code>&lt;?php

/*CONNECTION TO DB*/

$value = $_POST['value'];

/*Now you can use this value in your Query and update the database*/

?&gt;
</code></pre>

### Answer ID: 52308019
<p>If your current code works fine without any issue then,</p>

<p>you can just use
<code>echo json_encode($_POST);</code> at the end of your code in PHP file to return data that you have updated in your DB.</p>

<p>In your javascript code try,</p>

<pre><code>posting.done(function( data ) {
       //Prits data you returned on console.
        console.log(data);
    });
</code></pre>

