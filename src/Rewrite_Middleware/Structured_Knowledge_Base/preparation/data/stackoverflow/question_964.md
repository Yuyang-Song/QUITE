# How do I properly use sessions with passport_ldapauth?
[Link to question](https://stackoverflow.com/questions/52172391/how-do-i-properly-use-sessions-with-passport-ldapauth)
**Creation Date:** 1536087120
**Score:** 0
**Tags:** node.js, express, passport.js, ldapauth
## Question Body
<p>I've gone through the documentation and have an expressjs app working with login and logout endpoints using passport_ldapauth and sessions. The session is stored to a database using sequelize and a cookie containing just the sessionID, expiration, path, &amp; domain are stored to the browser.</p>

<p>I'm now trying to secure my other endpoints. In the console, I can see that the deserializer is hit first, and the proper query is sent to the database's session table, looking up my user by the proper session ID and finding it.</p>

<p>But then - passport_ldapauth is called and since there is no password, I get a flash message of "Missing credentials" and a 400 return.</p>

<p>I think that is what kav was referring to in his second comment here (<a href="https://github.com/vesse/passport-ldapauth/issues/53" rel="nofollow noreferrer">https://github.com/vesse/passport-ldapauth/issues/53</a>) which didn't get an answer.</p>

<p>Perhaps I'm complicating this? Should I simply switch to a 'session' strategy (if one exists) instead of 'ldapauth' once I have the user logged in for my other routes? Or is this supposed to work and isn't? Or am I just doing something wrong?</p>

<p>Here is the route in question:</p>

<p><div class="snippet" data-lang="js" data-hide="false" data-console="true" data-babel="false">
<div class="snippet-code">
<pre class="snippet-code-js lang-js prettyprint-override"><code>api.post('/role/add', passport.authenticate(
    'ldapauth', {session: true, failureFlash: true}
  ), (req, res, next) =&gt; {
    Roles.create(req.body).then(
      role =&gt; res.json(role)
    ).catch(err =&gt; {
      if (err) {
        console.log(err);
        next(err);
      }
    });
  });</code></pre>
</div>
</div>
</p>

<p>What else might one need me to provide in order to assist me?</p>

<p>Perhaps my serializer or deserializer are bad? They seem to work for the login/logout endpoints. See below: </p>

<p><div class="snippet" data-lang="js" data-hide="false" data-console="true" data-babel="false">
<div class="snippet-code">
<pre class="snippet-code-js lang-js prettyprint-override"><code>passport.serializeUser(function(user, done) {
    let sessionUser = {
      username: user.sAMAccountName,
      sessionID: user.sessionID
    };
    done(null, sessionUser);
  });
  
passport.deserializeUser(function(user, done) {
    Session.findOne({where: {sid: user.sessionID}}).then(user =&gt; {
      return done(null, user);
    });
  });</code></pre>
</div>
</div>
</p>

<p>Note that the user object returned from Active Directory is ENORMOUS, which is why I'm rewriting the whole thing as a minimum of username and sessionID. I am not sure, but I think the user as returned by the findOne may or may not be the 'passport' object contained in the 'data' column of the database. Hmm. Do I need to ensure that it is? It's possible the user is the whole row from the DB.</p>

## Answers
### Answer ID: 52191206
<p>Well that was ridiculously easy, but nowhere in the official docs could I find this. So for those who are having difficulty groking passport, here is what I found.</p>

<p>req.isAuthenticated()</p>

<p>Simply write your own middleware function, either above your routes or in a separate file, like this:</p>

<p><div class="snippet" data-lang="js" data-hide="false" data-console="true" data-babel="false">
<div class="snippet-code">
<pre class="snippet-code-js lang-js prettyprint-override"><code>const unAuthMsg = 'You are not authorized for this endpoint.';

export const ensureAuthenticated = (req, res, next) =&gt; {
  if (req.isAuthenticated()) {
    next();
  } else {
    res.status(401).json({"message": unAuthMsg});
  }
};</code></pre>
</div>
</div>
</p>

<p>Then use it in your routes like this: </p>

<p><div class="snippet" data-lang="js" data-hide="false" data-console="true" data-babel="false">
<div class="snippet-code">
<pre class="snippet-code-js lang-js prettyprint-override"><code>api.post('/role/add', ensureAuthenticated, (req, res, next) =&gt; {
Roles.create(req.body).then(role =&gt; {
  return res.json(role)
}).catch(err =&gt; {
  if (err) {
    console.log(err);
    next(err);
  }
});
  });</code></pre>
</div>
</div>
</p>

<p>And that's it.</p>

