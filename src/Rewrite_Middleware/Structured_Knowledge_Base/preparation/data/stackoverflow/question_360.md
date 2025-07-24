# phonegap ajax user authentication with nodejs-expresss-mongo-passportjs
[Link to question](https://stackoverflow.com/questions/22604270/phonegap-ajax-user-authentication-with-nodejs-expresss-mongo-passportjs)
**Creation Date:** 1395649566
**Score:** 3
**Tags:** cordova, express, passport.js
## Question Body
<p>I have already built a basic node.js user authentication system based on node.js, express.js, passport-local.</p>

<p>I store my username and passwords in a mysql database and I use mongo for persistent storage for the sessions. I now want to move the user registration and login to phonegap.</p>

<p>From the tutorials I have found online, the only way that seems work is is AJAX user authentication. However I have two questions:</p>

<ol>
<li><p>How do I rewrite the express routes to respond JSON since passport.js relies on redirects?</p>

<p><pre>// process the signup form
app.post('/register', passport.authenticate('local-signup', {
        successRedirect : '/home', 
        failureRedirect : '/register', 
        failureFlash : true // allow flash messages
    }));</p>

<pre><code>// process the login form
app.post('/login', passport.authenticate('local', {
    successRedirect : '/home', 
    failureRedirect : '/login', 
    failureFlash : true // allow flash messages
}));
</code></pre>

<p>and in my strategies I have : <br>
passport.use('local-signup', new LocalStrategy({
        usernameField : 'email',
        passwordField : 'password',
        passReqToCallback : true 
    },
    function(req, email, password, done) {
...
rest of the code that queries the db</p>

<p>also for login<br>
//Configure passport Local Strategy for login
passport.use(new LocalStrategy(
  function(username, password, done) {
  var query = 'select * from users where email = '+  connection.escape(username);
    connection.query(query, function (err, user) {
      if (err) { return done(err); 
... rest of code
}</pre></p></li>
<li><p>Will the AJAX authentication in PhoneGap work by sending a post to <code>/login</code> and therefore creating a new active session in the express server?</p></li>
<li><p>How do I handle state in the client. In a normal webapp you use redirects for ie. failed login attempts, logout, etc. In an AJAX authentication how do you handle that? Do you return a status code, return new markup, update part of the view?</p></li>
</ol>

## Answers
### Answer ID: 22641978
<p>I will close this question as I did some research and my original problem was from my lack of understanding of how phonegap apps are architected. I wasn't aware that I need to follow the single page app architecture vs the traditional web page model.</p>

