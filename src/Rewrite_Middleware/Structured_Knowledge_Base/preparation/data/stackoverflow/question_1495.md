# Mongoose error: lodash bind no longer accepts a callback function
[Link to question](https://stackoverflow.com/questions/78917166/mongoose-error-lodash-bind-no-longer-accepts-a-callback-function)
**Creation Date:** 1724734481
**Score:** 0
**Tags:** mongodb, mongoose, callback, lodash, bind
## Question Body
<p>The upgrade to MongoDB 7 dropped function callbacks, as has been discussed on other threads. Most times it is fairly easy to replace the callback by .then asyn/await etc, as documented at <a href="https://stackoverflow.com/questions/75649330/mongooseerror-model-findone-no-longer-accepts-a-callback-at-function">MongooseError: Model.findOne() no longer accepts a callback at Function</a>. But this one baffled me:</p>
<pre><code>return _.bind(function(req, res, next) {
  var query = this.getQuery(req);
  async.waterfall([
    _.bind(query.exec, query),
  ], this.sendData(req, res, next));
}, this);
</code></pre>
<p>Wrapping the lodash bind function in async.waterfall has the effect of a promise: this.sendData is only executed after bind function is complete. However, the &quot;_.bind(query.exec, query)&quot; expression raises the &quot;no longer accepts a callback function&quot; exception. So how do I rewrite this to avoid the exception?</p>
<p>Moving on: I can get the data from the database with this call:</p>
<pre><code>query.exec() .then(result =&gt; {
     console.log(result);
 })
</code></pre>
<p>So I could do without the async wrapper and do something like:</p>
<pre><code>return _.bind(function(req, res, next) {
    var query = this.getQuery(req);
    query.exec() .then(result =&gt; {
       this.sendData(req, res, next);  
   });
})
</code></pre>
<p>Currently this does not work as the result of the query needs to be bound to the this object. I can't figure out how to do that.</p>
<p>Update, this is the sendData function which receives the data:</p>
<pre><code>sendData: function(req, res, next) {
   var fields = _parseJSON(req.query.fields, []), optFields;
   if (!_.isArray(fields)) {
      fields = [fields];
   }
  function _sendData(err, data) {
    if (err) {
      res.json({'data':data,'error':err}); 
    } else {
      res.json(data);
    }
  }
  fields = _.intersection(fields, this.model.optionalFields);
  return function(err, data) {
    if (fields.length &gt; 0) {
     var isArray = _.isArray(data);
     async.map(isArray ? data : [data], function(doc, callback) {
      var obj = doc.toObject();
      async.each(fields, function(field, cb) {
        doc['get' + field].call(doc, function(err, value) {
          obj[field] = value;
          cb(err);
        });
      }, function(err) {
        callback(err, obj);
      });
    }, function(err, objs) {
      return _sendData(err, isArray ? objs : objs[0]);
    });
  } else {
    _sendData(err, data);
  }
};
</code></pre>
<p>It isn't clear to me how the data correctly retrieved by query.exec is passed through sendData back to the calling function. The context of this call is that it returns an array of JSON objects, such as [{name:&quot;CTP&quot;}, {name:&quot;TES&quot;}], which is then used in a node web page to populate a menu. So sendData needs to extract this data from the result, manipulate if required, and return it.</p>

## Answers
### Answer ID: 78917778
<p>In your suggested solution using promises, it looks like the issue is caused because you are missing this <code>this</code> in the <code>_.bind</code> function.</p>
<p>The function should look like this:</p>
<pre class="lang-js prettyprint-override"><code>return _.bind(function(req, res, next) {
    var query = this.getQuery(req);
    const callback = this.sendData(req, res, next);
    query.exec().then(result =&gt; {
        callback(null, result);
    }).catch(err =&gt; callback(err));
}, this)
</code></pre>
<p>You could also replace the call to <code>_.bind</code> entirely by using an arrow function for the outer wrapper, but maybe there is a reason you are using this - e.g.</p>
<pre class="lang-js prettyprint-override"><code>return (req, res, next) =&gt; {
  const callback = this.sendData(req, res, next);
  this.getQuery(req).exec().then(result =&gt; {
    callback(null, result);
  }).catch(err =&gt; callback(err));
}
</code></pre>

