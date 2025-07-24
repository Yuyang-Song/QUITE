# Real time chat, message handling - Socket.io, PHP, MySQL, Apache
[Link to question](https://stackoverflow.com/questions/45348866/real-time-chat-message-handling-socket-io-php-mysql-apache)
**Creation Date:** 1501153193
**Score:** 6
**Tags:** php, mysql, node.js, socket.io
## Question Body
<p>I am a beginner when it comes to web development. Recently i have been working on a real time chat website based completely on PHP and JS/jQuery (i'm not using any frameworks). Currently, my setup is just simple AJAX polling, which obviously isn't as good as i'd like it to be. My database is a MYSQL database.</p>

<p>I have read about websockets and my new initial plan was to create a NodeJS server with Socket.io which will handle messages (<a href="https://stackoverflow.com/questions/17209717/how-to-integrate-nodejs-socket-io-and-php">How to integrate nodeJS + Socket.IO and PHP?</a>), and i thought about storing those messages in a MySQL database (<a href="https://stackoverflow.com/questions/5818312/mysql-with-node-js">MySQL with Node.js</a>).</p>

<p>Here is what i have currently (not much, i'd like to clarify how to progress before i actually do progress). This is my test setup, the HTML used in actual chat is a bit different obviously. </p>

<p>Node.js Server: </p>

<pre><code>// NODE
var socket = require( 'socket.io' );
var express = require( 'express' );
var https = require( 'https' );
var http = require( 'http'); //Old
var fs = require( 'fs' );

var app = express();

//Working HTTPS server 
var server = https.createServer({ 
               key: fs.readFileSync('/etc/letsencrypt/live/%site%/privkey.pem'),
               cert: fs.readFileSync('/etc/letsencrypt/live/%site%/fullchain.pem')
             },app);

// var server = https.createServer( app ); Won't work cause no cert. 

var io = socket.listen( server );
console.log("Server Started"); 
io.sockets.on( 'connection', function( client ) {
    console.log( "New client !" );

    client.on( 'message', function( data ) {
        console.log( 'Message received ' + data); //Logs recieved data
        io.sockets.emit( 'message', data); //Emits recieved data to client.
    });
});
server.listen(8080, function() {
    console.log('Listening');
});
</code></pre>

<p>JS Client script: </p>

<pre><code>var socket = io.connect('https://%site%:8080');



document.getElementById("sbmt").onclick = function () {

socket.emit('message', "My Name is: " + document.getElementById('nameInput').value + " i say: " + document.getElementById('messageInput').value); 

};

socket.on( 'message', function( data ) {
    alert(data); 
    });
</code></pre>

<p>My super-simple test HTML: </p>

<pre><code>&lt;form id="messageForm"&gt;
&lt;input type="text" id="nameInput"&gt;&lt;/input&gt;
&lt;input type="text" id="messageInput"&gt;&lt;/input&gt;
&lt;button type="button" id="sbmt"&gt;Submits&lt;/button&gt;
&lt;/form&gt;
</code></pre>

<p>PHP requires a bit explanation - At the moment when someone connects to my website i run <code>session_start()</code>. This is because i want to have something like anonymous sessions. I distinguish between logged in and anonymous users through <code>$_SESSION</code> variables. An anon user will have <code>$_SESSION['anon']</code> set to true, as well as will NOT have <code>$_SESSION['username']</code> set. Logged in user will obviously have it inverted. </p>

<p>When it comes to the chat - it's available to both logged in users as well as anonymous users. When user is anonymous, a random username is generated from a database or random names. When user is logged in, his own username is chosen. Right now my system with Ajax polling works like this: </p>

<p>User inputs the message (in the current chat solution, not the testing HTML i sent above) and presses enter and an AJAX call is made to following function: </p>

<pre><code>  function sendMessage($msg, $col) {
    GLOBAL $db;
      $un = "";


    if (!isset($_SESSION['username'])) {

        $un = self::generateRandomUsername();

    } else {
    $un = $_SESSION['username'];
    }

    try {
      $stmt = $db-&gt;prepare('INSERT INTO chat (id, username, timestamp, message, color) VALUES (null, :un, NOW(), :msg, :col)');
      $stmt-&gt;bindParam(':un', $un, PDO::PARAM_STR);
      $stmt-&gt;bindValue(':msg', strip_tags(stripslashes($msg)), PDO::PARAM_STR); //Stripslashes cuz it saved \\\ to the DB before quotes, strip_tags to prevent malicious scripts. TODO: Whitelist some tags. 
      $stmt-&gt;bindParam(':col', $col, PDO::PARAM_STR);
        } catch (Exception $e) {
            var_dump($e-&gt;getMessage());
    }
      $stmt-&gt;execute();
  }
</code></pre>

<p>(Please don't hate my bad code and crappy exception handling, this is not any official project). This function inputs users message to the database. </p>

<p>To recieve new messages, i use <code>setTimeout()</code> function of JS, to run an AJAX check every 1s after new messages. I save the ID of last message that is displayed in JS, and send that ID as a parameter to this PHP function (and it's ran every 1s): </p>

<pre><code>  /* Recieve new messages, ran every 1s by Ajax call */
  function recieveMessage($msgid) {
    //msgid is latest msg id in this case
    GLOBAL $db;
    $stmt = $db-&gt;prepare('SELECT * FROM chat WHERE id &gt; :id');
    $stmt-&gt;bindParam(':id', $msgid, PDO::PARAM_INT);
    $stmt-&gt;execute(); 
    $result = $stmt-&gt;fetchAll(PDO::FETCH_ASSOC);
    return json_encode($result);

  }
</code></pre>

<p>The question is: How to implement something similar, but with my earlier mentioned setup of node.js server and websockets? I need to distinguish between logged in and anonymous users somehow. My first idea was to just run an ajax call from node.js server to PHP and pass message data, and PHP will insert it into DB exactly as it does right now. But the problem in this case is how to send the message out to the clients again? Usernames are applied while the message is being input into database, that means i'd have to call AJAX to save to the DB, and then call another AJAX to extract the newly input message and emit it to the clients, or make a function that inserts and extracts and returns extracted message. However, won't that cause problems when 2 messages are input at the exactly same time? </p>

<p>Is it somehow possible to access PHP session variables in Node.js? Then i could rewrite all DB querying to work in the Node.js server instead of PHP. </p>

<p>I apologize once more if my code or explanation is messy.</p>

## Answers
### Answer ID: 45501088
<p>SO, for everyone that is wondering and will find this thread in the future: <strong>I DID NOT FIND AN ANSWER WITH THE SOLUTION I WANTED TO USE, HOWEVER I CAME UP WITH SOMETHING ELSE, AND HERE IS A DESCRIPTION:</strong></p>

<p>Instead of making Node.js server send the AJAX request, i left it as i had before, the jQuery $.post() request from the client, to a PHP function. </p>

<p>What i did next was to implement a MySQL listener, that checked the MySQL binlog for changes. I used <a href="https://www.npmjs.com/package/mysql-events" rel="noreferrer"><code>mysql-events</code></a>module. It retrieves the newly added row with all data and then uses socket.io emit function to send it to connected clients. I also had to drop SSL because it apparently hates me. It's a small hobby project, so i don't really have to bother that much with SSL. </p>

<p>Best solution would be obviously to program the whole webserver in Node.js and just drop Apache completely. Node.js is awesome for real time applications, and it's a very easy language to learn and use. </p>

<p>My setup of <strong>Node.js + Socket.io + mysql-events:</strong> (ignore the unused requires)</p>

<pre><code>// NODE
var socket = require( 'socket.io' );
var express = require( 'express' );
var https = require( 'https' );
var http = require( 'http');
var fs = require( 'fs' );
var request = require( 'request' );
var qs = require( 'qs' );
var MySQLEvents = require('mysql-events');

var app = express();


/*Correct way of supplying certificates.
var server = https.createServer({
               key: fs.readFileSync('/etc/letsencrypt/live/x/privkey.pem'),
               cert: fs.readFileSync('/etc/letsencrypt/live/x/cert.pem'),
               ca: fs.readFileSync('/etc/letsencrypt/live/x/chain.pem')
       },app); */

var server = http.createServer( app ); // Won't work without cert.

var io = socket.listen( server );
console.log("Server Started");

//DB credentials
var dsn = {
  host:     'x',
  user:     'x',
  password: 'x',
};
var mysqlEventWatcher = MySQLEvents(dsn);

//Watcher magic, waits for mysql events.
var watcher = mysqlEventWatcher.add(
  'newage_db.chat',
  function (oldRow, newRow, event) {

     //row inserted
    if (oldRow === null) {
      //insert code goes here
      var res = JSON.stringify(newRow.fields); //Gets only the newly inserted row data
    res.charset = 'utf-8'; //Not sure if needed but i had some charset trouble so i'm leaving this. 
      console.log("Row has updated " + res);
      io.sockets.emit('message', "[" + res + "]"); //Emits to all clients. Square brackets because it's not a complete JSON array w/o them, and that's what i need. 
    }

     //row deleted
    if (newRow === null) {
      //delete code goes here
    }

     //row updated
    if (oldRow !== null &amp;&amp; newRow !== null) {
      //update code goes here
    }

    //detailed event information
    //console.log(event)
  });

io.sockets.on( 'connection', function( client ) {
    console.log( "New client !" );



    client.on( 'message', function( data ) {
        //PHP Handles DB insertion with POST requests as it used to.
    });
});
server.listen(8080, function() {
    console.log('Listening');
});
</code></pre>

<p><strong>Client JavaScript SEND MESSAGE:</strong></p>

<pre><code>$('#txtArea').keypress(function (e) {

  if (e.which == 13 &amp;&amp; ! e.shiftKey) {

      var emptyValue = $('#txtArea').val();
      if (!emptyValue.replace(/\s/g, '').length) { /*Do nothing, only spaces*/ }
      else {
            $.post("/shana/?p=execPOST", $("#msgTextarea").serialize(), function(data) {

            });


  }

  $('#txtArea').val('');
  e.preventDefault();
}


});
</code></pre>

<p><strong>Cliend JavaScript RECIEVE MESSAGE:</strong></p>

<pre><code>socket.on( 'message', function( data ) {
          var obj = JSON.parse(data);

          obj.forEach(function(ob) {
          //Execute appends

          var timestamp = ob.timestamp.replace('T', ' ').replace('.000Z', '');
          $('#messages').append("&lt;div class='msgdiv'&gt;&lt;span class='spn1'&gt;"+ob.username+"&lt;/span&gt;&lt;span class='spn2'style='float: right;'&gt;"+timestamp+"&lt;/span&gt;&lt;div class='txtmsg'&gt;"+ob.message+"&lt;/div&gt;");
          $('#messages').append("&lt;div class='dashed-line'&gt;- - - - - - - - - - - - - - - - - - - - - - - - - - -&lt;/div&gt;"); //ADD SCROLL TO BOTTOM
          $("#messages").animate({ scrollTop: $('#messages').prop("scrollHeight")}, 1000);
        });
    });
</code></pre>

<p>Somehow, the binlog magic destroys the timestamp string, so to clean it up i had to replace a bit of the string itself. </p>

<p><strong>PHP DB INSERT FUNCTION:</strong></p>

<pre><code>  function sendMessage($msg, $col) {
    GLOBAL $db;
      $un = "";


    if (!isset($_SESSION['username'])) {

        $un = self::generateRandomUsername();

    } else {
    $un = $_SESSION['username'];
    }
    try {
      $stmt = $db-&gt;prepare('INSERT INTO chat (id, username, timestamp, message, color) VALUES (null, :un, NOW(), :msg, :col)');
      $stmt-&gt;bindParam(':un', $un, PDO::PARAM_STR);
      $stmt-&gt;bindValue(':msg', strip_tags(stripslashes($msg)), PDO::PARAM_LOB); //Stripslashes cuz it saved \\\ to the DB before quotes, strip_tags to prevent malicious scripts. TODO: Whitelist some tags.
      $stmt-&gt;bindParam(':col', $col, PDO::PARAM_STR);
        } catch (Exception $e) {
            var_dump($e-&gt;getMessage());
    }
      $stmt-&gt;execute();
  }
</code></pre>

<p>I hope this helps someone at least a bit. Feel free to use this code, as i probably copied most of it from the internet already anyway :) I will be checking this thread from time to time, so if you have any questions leave a comment. </p>

