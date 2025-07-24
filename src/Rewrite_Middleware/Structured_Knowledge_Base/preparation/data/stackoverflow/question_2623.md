# Caching select query data on server side
[Link to question](https://stackoverflow.com/questions/43158217/caching-select-query-data-on-server-side)
**Creation Date:** 1491057629
**Score:** 0
**Tags:** javascript, node.js, database, express, memcached
## Question Body
<p>I am writing an express app, where I'm pushing data from my views to a database. But most of the data is mapped to some other data in database tables.</p>

<p>For example, is a choose student name drop down-  once you choose the student by his name , a drop down below - will show all roles that he is allowed for.</p>

<p>So I'm following this pattern of</p>

<pre><code>app.post('\action1', function(req,res){
  function querySomething(){
    var defered = Q.defer();
      connection.query(some_select_query,defered.makeNodeResolver());
      return defered.promise;
    }

  function querySomethingElse(){
    var defered = Q.defer();
      connection.query(some_other_select_query,defered.makeNodeResolver());
      return defered.promise;
    }

   Q.all([querySomething(), querySomethingElse()]).then((results,err) =&gt; {
       connection.release()
       if(results){
          res.render('some_view.ejs', {
             result1:results[0][0],
             result2:results[1][0]
          });
       }
       else{
         res.render('error.ejs',{});
       }
   })
})
</code></pre>

<p>Now the problem is that I have to follow this pattern of selecting something from multiple tables, pass all these function to a promise- and when the results is passed back, goto my view with all those result objects - so that I can use them in my view - as a means of doing drop downs dependent on one another.</p>

<p>Sometimes I have to re-write this multiple times.  </p>

<p>Doing a select query like this would be performance intensive especially if all views are using the result of the same query.</p>

<p>Is there any way I can build a cached data store on my express server side code and query that instead of the actual database??</p>

<p>If there is an insert or an update - i will refresh this store and just do a new select * that one time.</p>

<p>What libraries are there on top of express which will help me do this??</p>

<p>Does mysql-cache does the same thing?? I'm also using connection pooling with createPool.</p>

<p>How do I achieve this - or do I just restore to using big mvc's like sails to rewrite my app?</p>

## Answers
### Answer ID: 43158650
<p>You can try <a href="https://github.com/kwhitley/apicache" rel="nofollow noreferrer">apiCache</a> npm module.</p>

<p>"<strong>Sometimes I have to re-write this multiple times.</strong>"</p>

<p>Based on the business need, you may want to handle each use case separately and this scenario doesn't deal with caching.</p>

<p><strong>Doing a select query like this would be performance intensive especially if all views are using the result of the same query.</strong></p>

<p>This is a classic example for the need of <a href="https://goenning.net/2016/02/10/simple-server-side-cache-for-expressjs/" rel="nofollow noreferrer">server-side</a> caching. </p>

