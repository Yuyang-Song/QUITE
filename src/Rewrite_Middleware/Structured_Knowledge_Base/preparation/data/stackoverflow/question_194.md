# Ajax Messaging system Questions
[Link to question](https://stackoverflow.com/questions/16507328/ajax-messaging-system-questions)
**Creation Date:** 1368361595
**Score:** 0
**Tags:** javascript, ajax
## Question Body
<p>I'm working on a messaging system like Facebook. I do have on left a list of conversation, and on right a box where i load the messages, just like facebook does.</p>

<p>The basic system is complete (PHP/MySQL), and here some information on how it is structured:</p>

<blockquote>
  <ul>
  <li><p><strong>messages.php</strong> - Main page, based on url parameters. Rewrited    with.htaccess:</p>
  
  <p>Examples: </p>
  
  <ol>
  <li>URL = <a href="http://www.domain.com/messages/" rel="nofollow">http://www.domain.com/messages/</a> - Right Box: Display form to send new message.</li>
  <li>URL = <a href="http://www.domain.com/messages/Username" rel="nofollow">http://www.domain.com/messages/Username</a> - Ajax call to <code>getUserMessages.php</code> to load Messages between Logged in user and
  <code>Username</code> and show them on the Right Box.</li>
  </ol></li>
  </ul>
  
  <hr>
  
  <ul>
  <li><strong>getUserMessages.php</strong> - Get from database messages between Logged in user and user selected. It does Output HTML ready to be displayed.</li>
  </ul>
  
  <hr>
</blockquote>

<p>Now the system is partially Ajaxified, and i want it to be, just like Facebook does.</p>

<p>At the moment the Ajaxified part is:</p>

<p>When a user is vieweing a conversation, it display automatically new messages, and also update the conversation list with the last message.</p>

<p>If the user is not viewing a conversation, it does get new messages received and update the conversation list.</p>

<p>This is done with a PUSH service, to give Real Time experience to users.</p>

<p>I want to improve this, and make it to act like that:</p>

<p>The user click on the Conversation List, and it load the messages on the right Box, and also change the URL on the Address Bar, withut reload the entire page.</p>

<p>I can easily do the part to load messages when user click a conversation, but before i start i have two question: </p>

<p><s><strong>1.</strong> How i do change the Address URL while displaying a User Conversation WITHOUT reload the page?</s><br>
<strong>I found the answer.</strong></p>

<p><strong>2.</strong> How i do cache the conversations ? So if a user switch between two conversation, it does not call again the php file and query the database for all the messages, but appending only new messages (Maybe via another php File to fetch only Unread Messages)</p>

<blockquote>
  <p><strong>EDIT</strong></p>
</blockquote>

<p>I comed up with a solution: </p>

<p>When a user open a conversation, i cache the entire Ajax response (that is HTML) in a variable, like <code>messages-n</code>, Where <code>n</code> is the <code>user_id</code> of the conversation selected, then if the user click again on that conversation, i check if <code>messages-n</code> is set, if it is, i print it and run an ajax request to get only unread message and append them.
That's only in my mind i didn't made it to actual code.</p>

<p><strong>Could work well?</strong></p>

## Answers
### Answer ID: 16546653
<p><strong>Solved 1/2 :</strong></p>

<p><strong>1.</strong> To change Address URL i'm using the HTML5 <code>.pushState()</code> event.</p>

<p>Since HTML5 Browsers implement the <code>pushState</code> method in different way, to have a Cross-Browser solution, and have support for HTML4 browsers with hash Fallback, i used <a href="http://github.com/browserstate/history.js/%E2%80%8E" rel="nofollow">Hystory.js</a>.</p>

<p><strong>2.</strong> To cache messages, i haven't found a solution yet, nor i tried to do it for now.
But as @Christopher suggested, i changed the Ajax response from HTML to Json.
If i find it i will update my answer.</p>

