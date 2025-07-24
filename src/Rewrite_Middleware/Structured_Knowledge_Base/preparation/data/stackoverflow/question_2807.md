# Fixing code using Promises / Async-Await (Node.JS)
[Link to question](https://stackoverflow.com/questions/53416454/fixing-code-using-promises-async-await-node-js)
**Creation Date:** 1542817546
**Score:** 0
**Tags:** javascript, node.js
## Question Body
<p>So, I am currently developing some functionality on one of my projects at work. The project is using JavaScript mainly - Node.JS for backend and React.JS for frontend, and I have to admit I am not experienced with either of them. I believe that the code I am writing could look much better and work more efficient if I utilised promises or async/await functionality (prior to asking the question here I read few articles about them, and I am still not sure how to use them in the project the way it actually makes sense, hence I decided to ask community here). I also had a glance at this article, but again I am not sure whether my implementation actually does anything <a href="https://stackoverflow.com/questions/14220321/how-do-i-return-the-response-from-an-asynchronous-call/14220323#14220323">StackOverflow</a>.
At the end of this post I am going to paste some code from both front and backend and hopefully someone will be able to point me into a right direction. To make things clear - I am not asking for anybody to rewrite the code for me, but to explain what it is I'm doing wrong (or not doing at all).</p>

<p><strong>Use case:</strong></p>

<p>User writes a company name in the search bar on the website. Typed string is then sent to the backend via http-request and the database is checked for the entry (to get the company's logo) - here I am running an algorithm to check for spelling mistakes and propose similar names to the one typed, as a result the database may be queried more than 2 times before the result is sent back, but it's always working fine.
Once the response is received by the frontend few things should happen - to start with another request should be sent to the web in order to receive other results. If correct results are received, that should be the end of the function, otherwise it should send another request, to google this time, to get the results from there.</p>

<p>Backend Code:</p>

<pre><code>.post('/logo', (req, res) =&gt; {
        res.header("Access-Control-Allow-Origin", "*");
        res.header("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept");

        if (req.body.key !== "" &amp;&amp; req.body.key.trim().length &gt; 0) {
            let results = {};
            let proposedNames = [];

            var promise1 = new Promise((resolve, reject) =&gt; {
                let getLogo = "SELECT title, img_dir FROM logo_approved WHERE LOWER(title) LIKE LOWER($1)";
                let searchedCompanyName = ["%"+req.body.key+"%"];

                db.queryDB(getLogo, searchedCompanyName, (data) =&gt; {
                    if (data.rows.length &gt; 0){
                        results.databaseResults = data.rows;
                    }
                    resolve(data.rows);
                });
            });

            // Returns the list of all companies' names from the database
            var promise2 = new Promise((resolve, reject) =&gt; {
                let returnAllNames = "SELECT title, img_dir as img FROM logo_approved";
                db.queryDB(returnAllNames, [], (data) =&gt;{
                    // Compare searched company's name with all names from the database
                    data.rows.forEach(function(element) {
                        // If name from the database is similar to the one searched for
                        // It's saved in propsedNames array and will be used later on for database query
                        if (jw.distance(req.body.key, element.title) &gt; 0.7){
                            element.probability = parseFloat(jw.distance(req.body.key, element.title).toFixed(2));
                            proposedNames.push(element);
                        }
                    })
                    resolve(proposedNames);
                });
                    proposedNames.sort(function(a,b){return a.distance-b.distance});
                    results.proposedNames = proposedNames;
            });

            var promiseAll = Promise.all([promise1, promise2]);
            promiseAll.then(() =&gt; {
                res.send(results);
            });
    }   
        else {
            res.status(400);
            res.send("Can't search for an empty name");
        }
    })
</code></pre>

<p>Frontend code:</p>

<pre><code>  engraveLogoInputHandler() {
    let results = {};
    let loadedFromWeb = false, loadedFromClearbit = false, loadedFromDatabase = false;

    this.setState({
      engraveLogo: this.engravingLogo.value.length
    });
    // charsElthis.engravingInput.value
    if (inputLogoTimer) {
      clearTimeout(inputLogoTimer);
      // inputLogoTimer = null;
    }

    if (this.engravingLogo.value !== ''){
    // Wait to see if there is any new input coming soon, only render once finished to prevent lag
    inputLogoTimer = setTimeout(() =&gt; {

    request.post({url: NODEENDPOINT+'/logo', form: {key: this.engravingLogo.value}}, (err, res, body) =&gt; {
      if (err){
        console.log(err);
      }
      else {
        if (res.body &amp;&amp; res.statusCode !== 400){
          results.database = JSON.parse(res.body);
          loadedFromDatabase = true;
        }
    }
  });

    request(link+(this.engravingLogo.value), (err, res, body) =&gt; {
      if (err) {
        console.log(err);
      }
      else {
        let jsonBody = JSON.parse(body);
        if (jsonBody &amp;&amp; !jsonBody.error){
          let sources = [];
          let data = JSON.parse(body);
          for (let item of data) {
            sources.push({
              domain: item.domain,
              image: item.logo+'?size=512&amp;grayscale=true',
              title: item.name
            });
          }
          loadedFromClearbit = true;
          results.clearbit = sources;
        }
      }
    });

    if (!loadedFromClearbit &amp;&amp; !loadedFromDatabase){
    request('https://www.googleapis.com/customsearch/v1?prettyPrint=false&amp;fields=items(title,displayLink)&amp;key='+GOOGLE_CSE_API_KEY+'&amp;cx='+GOOGLE_CSE_ID+'&amp;q='+encodeURIComponent(this.engravingLogo.value), { json: true }, (err, res, body) =&gt; {
      if (err) {
        console.error(err);
      }
      else {
        if (body &amp;&amp; body.items) {
          let sources = [];
          for (let s of body.items) {
            sources.push({
              domain: s.displayLink,
              image: 'https://logo.clearbit.com/'+s.displayLink+'?size=512&amp;greyscale=true',
              title: s.title
            });
          }
          loadedFromWeb = true;
          results.googleSearches = sources;
        } else {
          console.error(body);
        }
      }
    });
  }

    console.log("Results: ", results);

    if (loadedFromClearbit || loadedFromWeb){
      console.log("Propose the logo to be saved in a local database");
    }
    }, 500);}
  }
</code></pre>

<p>So, in regarding to the backend code, is my implementation of promises actually correct there, and is it usefull? Could I use something similar for the front end and put the first two requests in Promise, and run the third request only if those two fail? (and failing means that they return empty results). 
I thought I could use logic like this (see below) to catch if the promise failed, but that didn't work and I got an error saying I didn't catch the rejection:</p>

<pre><code>var promise1 = new Promise((resolve, reject) =&gt; {
  // ... some logic there

  else {
    reject();
  }
});

var promise2 = promise1.catch(() =&gt; {
  new Promise((resolve, reject) =&gt; {
    // some logic for 2nd promise
  });
});
</code></pre>

<p>Any answer is appreciated. As mentioned, I'm not very familiar with JavaScript, and this is the first asynchronous project I am working on, so I want to make sure I utilise and adapt the correct behaviour and methods.
Thanks</p>

