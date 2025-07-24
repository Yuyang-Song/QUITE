# Synchronous mongoose request
[Link to question](https://stackoverflow.com/questions/41676992/synchronous-mongoose-request)
**Creation Date:** 1484571574
**Score:** 3
**Tags:** node.js, mongodb, asynchronous, mongoose, ecmascript-2016
## Question Body
<p>Is it possible to process a <code>db.model.find()</code> query inside of function context and retrieve a result <strong>without</strong> using <strong>callbacks and promises</strong> with mongoose library?</p>

<p>I need to get assured, if some user exists in process of running controller, so, I can't minimize current scope to callback due to large amount of same operations (for example, communication with database). Also I'm trying to realize MVC model in my project, so, I want to keep the helper libs (modules) in separated files. That's why I don't want to use any callbacks or promises - they will much times complicate everything even more then things already do. 
<hr>
For example, how should I rewrite the following code to be executed successfully (if it's actually possible) (you can ignore <em>login model and controller</em> - they are written to represent complicacy if to rewrite that code using callbacks):</p>

<p><strong>user.js lib</strong></p>

<pre><code>var db = require('./lib/db');

class User{
    constructor(id){ //get user by id
        var result = db.models.user.findOne({_id: id}); //unsupported syntax in real :(
        if(!result || result._id != _id)
            return false;
        else{
            this.userInfo = result;

            return result;
        }

    }
}

module.exports = User;
</code></pre>

<p><strong>login model</strong></p>

<pre><code>var user = require('./lib/user')
var model = {};

model.checkUserLogged(function(req){
    if(!req.user.id || req.user.id == undefined)
        return false;

    if(!(this.user = new user(req.user.id)))
        return false;
    else
        return true;
});

module.exports = model;
</code></pre>

<p><strong>login controller</strong></p>

<pre><code>var proxy = require('express').router();

proxy.all('/login', function(req, res){

    var model = require('./models/login');

    if(!model.checkUserLogged()){
        console.log('User is not logged in!');
        res.render('unlogged', model);
    }else{
        console.log('User exists in database!');
        res.render('logged_in', model);
    }

});
</code></pre>

<p>Generator functions/yields, async/await (<em>es2017</em>), and everything et cetera can be used just to solve the problem without nesting.</p>

<p>Thx in advance.</p>

## Answers
### Answer ID: 60248759
<p>Old question, but I want to share a method for handling this that I didn't see in my first couple searches.</p>

<p>I want to get data from a model, run some logic and return the results from that logic. I need a promise wrapper around my call to the model.</p>

<p>Below is a slightly abstracted function that takes a model to run a mongoose/mongo query on, and a couple params to help it do some logic. It then returns the value that is expected in the promise or rejects.</p>

<pre><code>export function promiseFunction(aField: string, aValue, model: Model&lt;ADocument, {}&gt;): Promise&lt;aType&gt; {
    return new Promise&lt;string&gt;((resolve, reject) =&gt; {
      model.findOne({[aField]: aValue}, (err, theDocument) =&gt; {
        if(err){
          reject(err.toString());
        } else {
          if(theDocument.someCheck === true){
            return(theDocument.matchingTypeField)
          } else {
            reject("there was an error of some type")
          }
        }
      });
    })    
}

</code></pre>

### Answer ID: 41677155
<p>There are two points wrong:</p>

<ul>
<li>Mongoose methods can't be called synchronously (Anyway a call to a DB done synchronously is not a good idea at all).</li>
<li>Nor async/await nor generators can be used in the constructor of an ES6 Class. It is explained in this <a href="https://stackoverflow.com/a/37556473/6254875">answer</a>.</li>
</ul>

<p>If you don't want nested code an easy option could be to use async/await (currently available in Node.js using a flag, not recommended for production). Since Mongoose methods return promises they can be used with async/await.</p>

<p>But as I said you can not do that in the constructor, so it has to be somewhere else.</p>

<p>As an example you could do something like this:</p>

<pre><code>var proxy = require('express').router();
var db = require('./lib/db');

proxy.all('/login', async function(req, res){
    const result = await db.models.user.findOne({_id: req.user.id}).exec();
    if (!result) {
        console.log('User is not logged in!');
        return res.render('unlogged');
    }
    res.render('logged_in');
});
</code></pre>

