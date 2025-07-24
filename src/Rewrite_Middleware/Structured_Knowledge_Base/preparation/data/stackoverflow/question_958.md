# Delete data in two tables with one SQL statement
[Link to question](https://stackoverflow.com/questions/51933133/delete-data-in-two-tables-with-one-sql-statement)
**Creation Date:** 1534775842
**Score:** 0
**Tags:** php, mysql, sql
## Question Body
<p>Hi Stackoverflow users,</p>

<p>I have a problem with deleting data in two tables with their foreign keys.</p>

<p><strong>Intro:</strong> I created a blogging website hosted locally with xampp and written in PHP and MySQL. Basically I have the functionality of it done, but that's not why I'm here. I have a problem with deleting data from two tables at once.</p>

<p><strong>Scenario:</strong> </p>

<p>The structure of part of my database is shown in the picture below</p>

<p><a href="https://i.sstatic.net/Nel1V.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/Nel1V.png" alt="enter image description here"></a></p>

<p>Let's say a user created a post for his website, the post is stored in table blog_entries, <em>username</em> is referenced from <strong>user_table</strong> and a unique entry_id is generated for that post. </p>

<p>I created a separate table for storing comments added to a particular post called <strong>entry_comments</strong>. 
With entry comments, i also reference <em>username</em> from <strong>user_table</strong> so that people can tell who made the comment and referenced <em>entry_id</em> from <strong>blog_entries</strong> for that post. </p>

<p>The problem is when the user goes to their profile in order to delete a post, I want the database to delete all the comments associated with that post before deleting the post itself.</p>

<p><strong>My Code</strong> </p>

<p>I achieved this by deleting the comments for a post first before deleting the post itself, but I want to know if there is a way to delete data from both tables by using a single query as shown below.</p>

<pre><code>$entry_id = mysqli_real_escape_string($DBConn, $_GET['entry_id']);

        $query1 = "DELETE FROM $entry_comments WHERE entry_id='$entry_id'";
        $result1 = mysqli_query($DBConn, $query1);
        if(!$result1){
            //display error message if query failed
        }
        else{
         $_GLOBAL['message'] = "Comments with id $entry_id has been deleted!!!";
         }
        $query2 = "DELETE FROM $blog_entries WHERE entry_id='$entry_id'";
        $result = mysqli_query($DBConn, $query2);
        if(!$result){
            //display error message if query failed
        }
        else{ $_GLOBAL['message'] .= "Entry with id $entry_id has been deleted!!!";
        include 'profile.php'; //redirect
        }
</code></pre>

<p>So i tried shortening the query to use a Join query in order to delete data from two rows with this query but it didn't work.</p>

<pre><code>DELETE FROM $blog_entries, $entry_comments 
        WHERE $blog_entries.username =  $entry_comments.username
        AND entry_id='$entry_id'
</code></pre>

<p>or I used</p>

<pre><code>DELETE be, ec
  FROM $blog_entries be
  JOIN $entry_comments ec ON be.username = ec.username
 WHERE be.entry_id = '$entry_id'
</code></pre>

<p>I researched the problem and the closest answer I found to my problem was this: <a href="https://stackoverflow.com/questions/3331992/how-to-delete-from-multiple-tables-in-mysql">How to delete from multiple tables in MySQL?</a> and I tried to rewrite my sql code to match it but would still get an error saying it has problems deleting due to foreign keys, and I can't figure out what I'm doing wrong.</p>

<pre><code>451 - Cannot delete or update a parent row: a foreign key constraint fails (`thenefariousblog`.`entry_comments`, CONSTRAINT `entry_comments_ibfk_2` FOREIGN KEY (`entry_id`) REFERENCES `blog_entries` (`entry_id`))
</code></pre>

<p>Sorry if this post feels a little bit long-winded, but i'm trying to explain the problem I have as much as possible in order to get the best feedback</p>

## Answers
### Answer ID: 51933296
<p>You can create the procedure to delete data in a proper order as you did in your 2-step approach. The input parameter for procedure would be the post ID. In this way you could simply run: <code>call removeEntry(ID);</code></p>

<p>You can also use ON DELETE CASCADE clause.</p>

<p>You can also try to temporarily disable the foreign key check like here: <a href="https://stackoverflow.com/q/15501673/3266991">How to temporarily disable a foreign key constraint in MySQL?</a></p>

