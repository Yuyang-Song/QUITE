# How to share the server code to electron app?
[Link to question](https://stackoverflow.com/questions/64100132/how-to-share-the-server-code-to-electron-app)
**Creation Date:** 1601287806
**Score:** 4
**Tags:** node.js, mongodb, typescript, mongoose, electron
## Question Body
<p>I am developing a postman like application with some added features. For the frontend, I am using Angular 10, and for the backend, I am using node with fastify.js and for the database, I am using MongoDB via Atlassian MongoDB hosting.</p>
<p>Right now, I have set-up the electron app and using the same frontend code. It's working fine if I use the API(I have hosted my node server on ec2). I want to run this app without an internet connection. for that, I set up the node server in electron. The node server is working fine if I run it in the main electron process.</p>
<p>My electron application setup:
I am running a node server in the electron app on port 5000.
when electron app starts it will start the server.</p>
<p>To make sure everything is working fine I used a postman to access the node server running from the electron process.
In postman, if I am hitting on http://localhost:5000/ while the electron app is running I am getting a response from the node server running in the electron.
If I use localhost:5000 as the base URL and hit the API from frontend in electron it's working and I am getting a response. I checked the electron console network tab, Request is going to the  http://localhost:5000/.</p>
<p>Now I want this app to run without the Internet. neDB is the most suggested DB for electron and it provides the same query syntax as MongoDB. Also, I found out library mongoose-nedb. Using that library I can use mongoose with neDB. So, If I use that library I don't need to change my node code and can use mongoose with neDB instead of MongoDB. So, I set-up my app with neDB and mongoose-neDB. for testing, I again use the postman as well as electron frontend. But now I am not getting any response.</p>
<p>I tried LinvoDB as well. same result.</p>
<p>Is this happening because I am using neDB outside the electron browser context?
Can you suggest some solution so that I don't need to rewrite the node server in the electron app?
Is this approach proper? any suggestion?</p>
<p>Ref:</p>
<p>I am using this boilerplate for the electron app: <a href="https://github.com/maximegris/angular-electron" rel="nofollow noreferrer">https://github.com/maximegris/angular-electron</a> (I am putting my node code in root and importing it in main.ts)</p>
<p>mongoose-neDB: <a href="https://github.com/aerys/mongoose-nedb" rel="nofollow noreferrer">https://github.com/aerys/mongoose-nedb</a></p>
<p>neDB: <a href="https://github.com/louischatriot/nedb" rel="nofollow noreferrer">https://github.com/louischatriot/nedb</a></p>
<p>LinvoDB: <a href="https://github.com/aerys/linvodb3" rel="nofollow noreferrer">https://github.com/aerys/linvodb3</a></p>
<p>mongoose-LinvoDB: <a href="https://github.com/aerys/mongoose-linvodb3" rel="nofollow noreferrer">https://github.com/aerys/mongoose-linvodb3</a></p>

