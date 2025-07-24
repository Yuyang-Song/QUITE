# Authenticate a user using a nodejs web server but no framework
[Link to question](https://stackoverflow.com/questions/19416237/authenticate-a-user-using-a-nodejs-web-server-but-no-framework)
**Creation Date:** 1381969549
**Score:** 2
**Tags:** javascript, mysql, node.js, authentication, restful-authentication
## Question Body
<p>still trying to learn javascript and nodejs. I got to a point where i have a server in node, it routes my requests, answers me, queries the mysql db and i think works quite well!, problem is, im going to need some way to authenticate a user that will be the only one able to edit, delete or create records in the db.</p>

<p>It would be something like this:
User1 - browses the page, all select queries, except some that will increment a visits counter
User2 - the admin, all powerful</p>

<p>I have investigated and found several ways of doing this, i don't understand them very well, but they all seem to require me to rewrite almost all my server! I used what i think is pure nodejs for it, </p>

<pre><code>var http = require("http"); 
var url = require("url");
</code></pre>

<p>I also used sequelize to connect to my db.</p>

<p>Investigating i found this:
- <a href="http://passportjs.org/" rel="nofollow">http://passportjs.org/</a>
The problem with passport is that it works with express, and i would have to rewrite all</p>

<ul>
<li><p>expressjs
Again, rewrite</p></li>
<li><p><a href="http://mcavage.me/node-restify/" rel="nofollow">http://mcavage.me/node-restify/</a>
And i also found restify, which looks awesome, but it would mean a complete rewrite of something that already works.</p></li>
<li><p>nodejs
i cant seem to find something about authentication in the nodejs docs.</p></li>
</ul>

<p>I have never done authentication and i cant understand how they work without involving the db, what i understand as authentication is: a user logs in, and his requests connect to the database using a db user with certain access, i know how to do the db side, but what happens between the client and the server until it reaches the db is beyond me.</p>

<p>I will post all the sources, feel free to skip them, hopefully, they will help someone looking to do the same thing.</p>

<p>basically, the only things left i think are some kind of authentication and the ability to upload an image from the browser to the server, and save it in the server.
I will implement an angularjs client (which im still yet to learn) that will make all the requests.</p>

<p>Any help will be really appreciated!</p>

<p>index.js</p>

<pre><code>var server = require("./server");
var router = require("./router");
var requestHandlers = require("./requestHandlers");

var handle = {};
handle["/insertHood"] = requestHandlers.insertHood;
handle["/selectHood"] = requestHandlers.selectHood;


server.start(router.route, handle);
</code></pre>

<p>server.js</p>

<pre><code>var http = require("http");
var url = require("url"); //This module has utilities for URL resolution and parsing.  http://nodejs.org/api/all.html#all_url

function start(route, handle) {
    //the web service will respond with this
    function onRequest(request, response) {
        var urlValues = {
            params: {},
            pathName: ""
        };
        var postData = "";

        //read the url used to call our web service
        parseUrl(request, urlValues);
        //console.log("path: " + urlValues.pathName);
        //console.log("params: " + JSON.stringify(urlValues.params));

        //set encoding for the recieved request
        request.setEncoding("utf8");

        //if post data is recieved process it here by chunks
        request.addListener("data", function (postDataChunk) {
            postData += postDataChunk;
            console.log("Recieved POST data chunk '" + postDataChunk + "'.");
        }
        );

        //when we are done storing all the post data, go to the pathName
        request.addListener("end", function () {
            route(handle, urlValues, response, postData);
        }
        );
    }
    http.createServer(onRequest).listen(8888);
    console.log("Server has started");
}

function parseUrl(request, urlValues) {
    urlValues.pathName = url.parse(request.url).pathname; //parse the url pathName
    urlValues.params = url.parse(request.url, true).query;
}

exports.start = start;
exports.parseUrl = parseUrl;
</code></pre>

<p>router.js</p>

<pre><code>function route(handle, urlValues, response, postData) {
    console.log("Router.js --&gt; About to route a request for " + urlValues.pathName);
    if (typeof handle[urlValues.pathName] === 'function') {
        handle[urlValues.pathName](response, urlValues, postData);
    } else {
        response.writeHead(404, { "Content-Type": "text/plain" });
        response.write("404, no request handler found for " + urlValues.pathName);
        response.end();
    }
}

exports.route = route;
</code></pre>

<p>requesthandlers.js</p>

<pre><code>var exec = require("child_process").exec;
var db = require("./dataBase");

function insertHood(response, urlValues) {
    urlValues.params["zoom_level"] = parseInt(urlValues.params["zoom_level"]);
    urlValues.params["lat"] = parseFloat(urlValues.params["lat"], 10);
    urlValues.params["lon"] = parseFloat(urlValues.params["lon"], 10);

    console.log("requestHandler.js --&gt; Request handler 'insertHood' was called.");
    var result = db.execute("modify", 'INSERT INTO neighborhood (hood_location, hood_name, zoom_level) values (GeomFromText(\'POINT(:lat :lon)\'), :name, :zoom_level)', response, urlValues.params);
}

function selectHood(response, urlValues) {
    console.log("requestHandler.js --&gt; Request handler 'selectHood' was called.");
    var result = db.execute("select", 'select x(hood_location), y(hood_location), hood_name, zoom_level from neighborhood where hood_name = :name', response, urlValues.params);
}

exports.insertHood = insertHood;
exports.selectHood = selectHood;
</code></pre>

<p>database.js</p>

<pre><code>var Sequelize = require("sequelize");

//this tells sequelize how to connect to the data base
//see http://sequelizejs.com/documentation#usage-basics
var sequelize = new Sequelize('mydb', 'myuser', 'mypass',
    {
        host: "localhost",
        port: 3306,
        dialect: 'mysql'
    }
);

/*
Pre:
type: a string to know if the query is a select and returns rows, or a modify query, and returns nothing
query: an sql query in string format with the parameters :param in place
response: a response object where the results of the query will be written
parameters: from sequelize, an array with the parameter for the sql query in the correct order

Pos:
response: the object will have the results of the query, an error or the rows of the results set
*/
function execute(type, query, response, parameters) {
    console.log("Query: " + query); 
    var options = { raw: true };

    var result = sequelize.query(query, null, options, parameters)
    .success(function (rows) {        
        if (type == 'select') {
            response.writeHead(200, { "Content-Type": "application/json" });
            response.write(JSON.stringify(rows));
            response.end();
        } else if (type == 'modify') {
            response.writeHead(200, { "Content-Type": "text/html" });
            response.write("Query was successful");
            response.end();
        }
    }
    ).error(function (e) {
        console.log("An error occured: ", e);
        response.writeHead(404, { "Content-Type": "text/html" });
        response.write("There was an error man, shits on fire yo ---&gt; " + e);
        response.end();
    }
    );
}

exports.execute = execute;
</code></pre>

## Answers
### Answer ID: 19417742
<p>Basic authentication is not too difficult, even without an external framework. The most difficult part is really just properly maintaining sessions. I would <em>strongly</em> recommend that you use <a href="http://www.senchalabs.org/connect/middleware-session.html" rel="nofollow">session</a> for this, but it is not a necessity. Connect's session is really ideal here, because it manages expired sessions so that you don't have an ever-increasing object.</p>

<p>In order to maintain authentication, once a user has input their credentials and they are sent to the server, crosscheck them with the valid credentials; If they match, then  you will need to store a cookie on the client-side with a unique UUID. On the server side, keep an object containing hashes of all authenticated users. This way, as soon as a user connects, the server can check if they already have a cookie proving their credentials, so that you don't have to log in on every page.</p>

<p>Something like this should work in basic cases:</p>

<p>Routing:</p>

<p><code>var sessions = {}</code></p>

<pre><code>if(req.headers.cookies['sid'] &amp;&amp; sessions[req.headers.cookies['sid']])
    //continue
else
    //return login page
</code></pre>

<p>On user login:</p>

<pre><code>if(req.query.username == someUsername &amp;&amp; req.query.password == somePassword){
      res.writeHead(200, {
          'Set-Cookie': 'sid=UUID', //will need a uuidgen here
          'Content-Type': 'text/plain'
      })
      sessions[UUID] = true //store session on server
      return res.send(200,somePage)
}
</code></pre>

