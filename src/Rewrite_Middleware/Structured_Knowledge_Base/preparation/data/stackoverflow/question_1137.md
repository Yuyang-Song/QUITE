# Getting result from MySQL
[Link to question](https://stackoverflow.com/questions/60603462/getting-result-from-mysql)
**Creation Date:** 1583766804
**Score:** 1
**Tags:** javascript, mysql, node.js, backend
## Question Body
<p>My backend is consist of Api and DB. When I want to get response from DB I have had delayed output by 1 query.
<br>
<strong>API</strong> <em>(I think api is ok. Start read DB first)</em></p>

<pre><code>app.post('/api/query', (req, res) =&gt; {
  console.log(`\n  Query input : ${JSON.stringify(req.body)}`);
  let queryInput = (Object.values(req.body).join(' '));


    if(!dbApi.checkArray(queryInput)){ //If array is not made from clear strings
      res.json(dbApi.queryFromUser(queryInput));
    }
    else{
      res.json(dbApi.queryOutput);
    }
});
app.listen(dbConfig.server.port, () =&gt;
    console.log(`Server running on port ${dbConfig.server.port}`));
</code></pre>

<p><strong>DB</strong></p>

<pre><code>queryOutput = [];
    const receivingQuery =(queryInput) =&gt; {

        db.query(queryInput, (err, result) =&gt;{
            if(err) throw err+' : '+queryInput;
            queryOutput = result;
            console.log("\nQuery output "+ JSON.stringify(queryOutput)); //Output (result) is ok
        });
        return queryOutput //Here is Output from previous query (sends to API)

    }

module.exports = {
    queryOutput: queryOutput,
    queryFromUser: receivingQuery,
}
</code></pre>

<p>I tryied callback method and I rewrite it couple of times. But I dont have enough skill to solve it.</p>

## Answers
### Answer ID: 60604171
<p>If You want to return result of query so simply do following things:</p>
<ol>
<li>add <code>query</code> method to db module:</li>
</ol>
<pre><code>function query(sql, args = []) {
  return new Promise(function(resolve, reject) {
    db.query(sql, args, (err, result) =&gt; {
      if (err) return reject(err);
      resolve(result);
    });
  });
}

// extra feature, getting user by id
async function getUserById(id) {
  const result = await query('SELECT * FROM users WHER id = ? LIMIT 1', [id]);
  if (Array.isArray(result) &amp;&amp; result[0]) return result[0];
  return null;
}

module.exports = {
    query,
    getUserById, // export user by id

    queryOutput,
    queryFromUser: receivingQuery,
}
</code></pre>
<ol start="2">
<li>use it (with async and await):</li>
</ol>
<pre><code>app.post('/api/query', async (req, res) =&gt; {
  try {
    console.log('Query input:', req.body);
    const queryInput = Object.values(req.body).join(' ');
  
    const result = await dbApi.query(queryInput);
    res.json(result);
  }
  catch (error) {
    console.error(error);
    res.status(500).json({message: 'Please try again soon'});
  }
});

app.get('/api/users/:id', async (req, res) =&gt; {
  try {
    const user = await dbApi.getUserById(req.params.id);
    if (!user) return res.status(404).json({message: 'User not found'});
    res.status(200).json(user);
  }
  catch (error) {
    console.error(error);
    res.status(500).json({message: 'Please try again soon'});
  }
});

app.listen(dbConfig.server.port, () =&gt;
    console.log('Server running on port', dbConfig.server.port));
</code></pre>

