# How to relay PHP functions/variables inside a socketio return
[Link to question](https://stackoverflow.com/questions/59475523/how-to-relay-php-functions-variables-inside-a-socketio-return)
**Creation Date:** 1577252336
**Score:** 1
**Tags:** javascript, php, node.js, json, socket.io
## Question Body
<p>I feel like this may have already been asked, and have tried scouring this site for an exact replica of what I'm trying to do, however every question which seems to be suggested to me as similar asks questions about post-load JS utilizing PHP variables/functions, which is not a close match to what I'm trying to do.</p>

<p>I'll start with why I'm asking this question instead of just writing the full code in Node which would make this much simpler, the answer to which is simply due to scale of the task. This project is well over half a year in development, and has been written almost in bulk in PHP and therefore translating over to Node for most of the functionality is simply out of the question at this point in time. We have put it on the timeline to eventually transfer all PHP to NodeJS but at the moment it has to be a mix of both, which, while not ideal, is our only option with our resources ATM.</p>

<p>Now onto the question and code; we have a chat system which uses a NodeJS server with socket.io, I already have established a message template for the returns from the socket.io emits, however, they utilize PHP variables. Upon page load (of any page which includes the chat function) a PHP MySQL query is ran which queries by id for that user in the users database, and returns several values of that user which dictate how the message displays and what options the user has with others messages. I will post this li template to show you the obvious issues I will encounter.</p>

<pre><code>&lt;li class="exampleMessageDELETE"&gt;&lt;img src="&lt;?=$userPicture?&gt;" class="chatMessageUserPicture"&gt;&lt;h2 class="chatUserName"&gt;&lt;?php if($userRank == 7) { echo "[Owner]";} elseif ($userRank == 3) { echo "[Mod]";} elseif ($userRank == 5) { echo "[Admin]";} else {}?&gt; &lt;?=$_SESSION['userName']?&gt;&lt;/h2&gt;&lt;?php if($userRank &gt; 0) { ?&gt;&lt;a id="chatMessageAdminOptions" href=""&gt;Mod&lt;/a&gt; &lt;?php } ?&gt;&lt;a id="chatMessageOptions" href=""&gt;Options&lt;/a&gt;&lt;p class="chatMessageContentText"&gt;This is an example message to set up the CSS class for chat messages... Stay tuned for updates...&lt;/p&gt;
</code></pre>

<p>As you can see, several displayed functions which are crucial to making the chat system what it should be rely on PHP code. With several functions being restricted to users with higher privileges and usernames and tags being displayed based on other PHP variables and the SQL returns.</p>

<p>At the moment, the socketio capture is just as the following:</p>

<pre><code>            socket.on('chatMessage', function(msg){
                $('.chatMessageList').append($('&lt;li&gt;').text(msg));
            });
</code></pre>

<p>Now what I hope would be the solution would simply to post all of that previously posted LI inside the append function with concatenation for each PHP variable, but as I believe I have a beginners knowledge of website loading I do not believe it is possible to generate these variables to output post-load, and especially not inside of a JS function. What I was thinking of doing was to JSON encode all of the variables before sending the message, and send those along with the message, which would allow the output to use the JSON variables to convert into actual text which would output, however, this seems perhaps very complex and might overlook a simpler solution that might exist, which is where I present this question. This, again, I do not believe relates directly to any other questions as I'm not looking to reference a PHP function through front-end javascript, just simply a variable it outputs, which may or may not exist post-load in some sort of PHP variable cache behind the scenes. I'm sure that line sounded stupid, and it probably is, but it was only for the lack of a better phrase. I hope there is any solution which exists which doesn't involve complete rewriting of my code. Any help is greatly appreciated</p>

## Answers
### Answer ID: 60843630
<p>Store required values in js variables and inside the socket listener use them as required.</p>

<p>Ex:</p>

<pre><code>var userPicture = "&lt;?php echo $userPicture;?&gt;";
socket.on('chatMessage', function(msg){
   $('.chatMessageList').append('&lt;li&gt;&lt;img src="' + userPicture + '" /&gt;" + msg + '&lt;/li&gt;');
});
</code></pre>

