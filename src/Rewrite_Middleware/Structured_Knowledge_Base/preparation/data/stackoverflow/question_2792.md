# Authorization, tokens and nodejs
[Link to question](https://stackoverflow.com/questions/52459694/authorization-tokens-and-nodejs)
**Creation Date:** 1537641162
**Score:** 0
**Tags:** node.js, api, security, jwt
## Question Body
<p>I’m thinking about authorization for my app. Beyond JWT authentication against a mongo database, i'd like to secure certain routes for different roles. I’m not interested in OAuth or 3rd party services </p>

<p>What I’m having difficulty with is where to store role. If I query database for authentication and return a token, should I also return the role in the payload? Then check with middleware once authenticated if the user is further authorized? Can’t someone rewrite the token with admin privileges ?</p>

<p><strong>What’s the standard way for doing this?</strong></p>

<p>This is ultimately and api serving an angular app on the front end </p>

<p>Thanks </p>

## Answers
### Answer ID: 52459919
<p>Standard way to do this using a <code>JWT signed token</code>  which is signed by a private key from the server generated on it and a public key is sent over to all the consuming clients.If, anyone changes the body within the token the <strong>authenticating authority</strong> which is the server will try to digitally verify the signature through its private key . Since, this token is different to the one sent over by signing from the server , the signatures will never match.</p>

<p>Also, to protect your <code>JWT token</code> to be sniffed out as a part of alive session you put up <a href="https://github.com/aspnet/Home/issues/3312" rel="nofollow noreferrer">CSRF/XSRF</a> mitigation strategy in place</p>

