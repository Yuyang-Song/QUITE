# Node.js: Asynchronous callback confusion
[Link to question](https://stackoverflow.com/questions/28449869/node-js-asynchronous-callback-confusion)
**Creation Date:** 1423644069
**Score:** 0
**Tags:** javascript, node.js, asynchronous, callback
## Question Body
<p>I am trying to figure out how to create asynchronous functions for a web app. I am doing a database query, manipulating the data to a format that is more convenient, and then trying to set my router to pass back that file.</p>

<pre><code>//Module 1
//Module 1 has 2 functions, both are necessary to properly format
function fnA(param1){
    db.cypherQuery(query, function(err, result){
        if(err){
            return err;
        }
        var reformattedData = {};
        //code that begins storing re-formatted data in reformattedData

        //the function that handles the rest of the formatting
        fnB(param1, param2);
    });
});

function fnB(param1, reformattedData){
    db.cypherQuery(query, function(err, result){
        if(err){
            return err;
        }
        //the rest of the reformatting that uses bits from the second query 
        return reformattedData;
    });
});

exports.fnA = fnA;
</code></pre>

<p>Then in my router file:</p>

<pre><code>var db = require('module1');

router.get('/url', function(req,res,next){
    db.fnA(param1, function(err, result){
        if (err){
            return next(err);
        }
        res.send(result);
    });
});
</code></pre>

<p>When I tried to test this out by hitting the URL indicated by the router, it just loads indefinitely.</p>

<p>I know what I have above is wrong, since I never wrote my function to require a callback. When I tried figuring out how to rewrite it though, I got really confused - How do I write my function to have a callback when the asynchronous stuff happens inside it? </p>

<p>Can someone help me rewrite my functions to use callbacks correctly, so that when I actually use the function, I can still work with the asynchronous response?</p>

## Answers
### Answer ID: 28449976
<p>You use db.fa from your router file, and pass the second parameter as a callback function. but the function signature don't have the cb param and doesnt use it.</p>

<p>The main idea - you try to initiate an async operation and cannot know when it ends, so you send it a callback function to get triggered when all operations are done.</p>

<p>Fixed code should be like that:</p>

<pre><code>//Module 1
//Module 1 has 2 functions, both are necessary to properly format
function fnA(param1, cb1){
    db.cypherQuery(query, function(err, result){
        if(err){
            cb1(err); &lt;-- return error to original call
        }
        var reformattedData = {};
        //code that begins storing re-formatted data in reformattedData

        //the function that handles the rest of the formatting
        fnB(param1, param2, cb1);
    });
});

function fnB(param1, reformattedData, cb1){
    db.cypherQuery(query, function(err, result){
        if(err){
            cb1(err); &lt;-- return error to original call
        }
        //the rest of the reformatting that uses bits from the second query 
        cb1(false, dataObjectToSendBack); &lt;--- This will call the anonymouse function in your router call
    });
});

exports.fnA = fnA;
</code></pre>

<p>Router file:</p>

<pre><code>var db = require('module1');

router.get('/url', function(req,res,next){
    db.fnA(param1, function(err, result){ &lt;-- This anonymous function get triggered last 
        if (err){
            return next(err);
        }
        res.send(result);
    });
});
</code></pre>

