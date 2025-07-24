# Call serverless functions in offline mode of MongoDB Realm Sync
[Link to question](https://stackoverflow.com/questions/72046027/call-serverless-functions-in-offline-mode-of-mongodb-realm-sync)
**Creation Date:** 1651158189
**Score:** 1
**Tags:** react-native, mongodb-atlas, mongodb-realm
## Question Body
<p>MongoDB Realm allows the creation of <a href="https://www.mongodb.com/docs/realm/functions/" rel="nofollow noreferrer">serverless functions</a> on the cloud which can be called from the client SDK.</p>
<p>My query is when working with Realm sync, are these functions also synced to the local database and can they be called on the locally synced database in <strong>offline mode</strong>. If yes what would be the correct way of doing it with react-native assuming that the basic configurations have been done for connection? If not then do I need to rewrite the complex function logic(which does more than just querying and filtering) on the client-side?</p>
<p>I did some basic investigation but could not find any concrete answers except <a href="https://www.mongodb.com/community/forums/t/mongodb-realm-offline-with-graphql-and-functions/117765" rel="nofollow noreferrer">this</a>. This answer assumes that the functions are called using <a href="https://www.mongodb.com/docs/realm/endpoints/" rel="nofollow noreferrer">HTTPS endpoints</a> but my intention is to call these functions directly on the client without endpoints.</p>

