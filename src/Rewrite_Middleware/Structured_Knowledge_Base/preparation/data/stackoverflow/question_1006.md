# Using promises in Mongoose
[Link to question](https://stackoverflow.com/questions/54346045/using-promises-in-mongoose)
**Creation Date:** 1548330774
**Score:** 0
**Tags:** express, mongoose, promise
## Question Body
<p>I am new to the Promise method used to retrieve multiple database records at the same time and I want to rewrite my existing code to use promises</p>

<p>I have this piece of code in Express:</p>

<pre><code>getController.getData = function(req,res, collection, pagerender) {
  var id = req.params.id;
  collection.find({}, function(err, docs){
    if(err) res.json(err);
    else res.render(pagerender, {data:docs, ADusername: req.session.user_id, id: req.params.id});
    console.log(docs);
  });
};
</code></pre>

<p>Now I want to use promises here, so I can do more queries to the database. Anyone know how I can get this done?</p>

## Answers
### Answer ID: 54346821
<p>First, check if <code>collection.find({})</code> returns a promise. If it does, then you can call your code like:</p>

<pre><code>collection.find({}).
    then(function(docs){
        res.render(pagerender, {data:docs, ADusername: req.session.user_id, id: req.params.id});
    })
    .catch( function(err) {
        res.json(err);
    })
</code></pre>

<p>If you want more calls here, just create new DB call and add another <code>.then</code> block.</p>

<p>I suggest you read the documentation on promises, just to get a general feeling about them (<a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/then" rel="nofollow noreferrer">https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise/then</a>). You will also see how you can handle both success and rejection in the same function if you want.</p>

