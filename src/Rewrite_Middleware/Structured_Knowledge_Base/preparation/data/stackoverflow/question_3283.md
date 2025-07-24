# Return true or false based on a mysql query
[Link to question](https://stackoverflow.com/questions/75060973/return-true-or-false-based-on-a-mysql-query)
**Creation Date:** 1673285562
**Score:** 0
**Tags:** mysql, node.js
## Question Body
<p>So bare with me, I'm trying to create a function that checks if a user exists in a mysql database, and if it exists it would return true, else return false. However, I've run into a problem due to the fact that I'm using ANOTHER function to get the result of the mysql query to which the return is using that function instead of the main function that I need. So heres a snippet of the function that I am currently using.</p>
<pre><code>let connection = mysql.createConnection(db_config);
connection.connect()
let query = connection.query('SELECT * FROM users WHERE usid = &quot;' + token + '&quot;', function (err, result, fields) {
 if (Object.keys(result).length != 0){
    return true
     } else {
          return false;
     }
})
connection.end();
 
}
</code></pre>
<p>So is there some way that I could get the return value from that inner function and then return that same value to where I am originally calling the function or would I need to completely rewrite how I am currently doing this?</p>
<p>The way I am calling it is just putting it as a variable and determining the values and what to do with each of them.</p>
<p><code>let usercheck = checkClient(userid);</code></p>

