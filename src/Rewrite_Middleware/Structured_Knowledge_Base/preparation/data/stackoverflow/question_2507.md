# expressJS promise and error handling
[Link to question](https://stackoverflow.com/questions/37750248/expressjs-promise-and-error-handling)
**Creation Date:** 1465567377
**Score:** 2
**Tags:** javascript, express, error-handling, promise, catch-block
## Question Body
<p>I have a route that first need to query the database, then with the results, query another web service, then with that result render the page.
I have that flow worked out and am trying to figure out the error handling. Given that i talk to multiple service, I'm trying to massage the error before returning them to express.</p>

<p>Here is the structure of the code for the route:</p>

<pre><code>Models.Episode.findById(request.params.episodeID)
    .catch(function (error) {
        throw (throwjs.notFound());
    })
    .then(function (episode) {
        if (episode.getUser().id !== request.user.href) {
            return next(throwjs.unauthorized("You do not have access to this podcast"));
        }
        return doSomeOtherAsyncStuff();
    })
    .then(function (queryResponse) {
        renderPage();
    })
    .catch(function (error) {
        next(error);
    });
</code></pre>

<p>My problem is with the first catch. My goal in this catch is to repackage the error and stop the execution and send the error to express middleware.</p>

<p>With the way it is written above, the execution stops, but my express error handler are not called.</p>

<p>I tried rewriting the first catch as </p>

<pre><code>.catch(function(error){
     return next(error);
})
</code></pre>

<p>But that does not solve the issue. The only solution i found is to move the catch to the end. But then i lose context of the failure location.</p>

<p>Any clue as to what i'm doing wrong?
Thanks, olivier</p>

## Answers
### Answer ID: 37841950
<p>I'd recommend taking a different approach so you don't have to rely on long running promise chains. With the following approach, you've decoupled your authorization and and validation to separate middleware, since they're not necessarily a concern of the actual episode handler itself. Plus this approach is more idiomatic to express.</p>

<p>An added bonus is that you're free to pass errors down to an error handler so you further decouple your errors from your route handlers.</p>

<pre><code>function validateEpisode(req, res, next) {
  Models.Episode
    .findById(req.params.episodeID)
    .then(function(episode) {
      req.yourApp.episode = episode;
      next() // everything's good
    })
    .catch(function(error) {
      // would be better to pass error in next
      // so you can have a general error handler
      // do something with the actual error
      next(throwjs.notFound());
    });
}

function authUserByEpisode(req, res, next) {
  if (req.yourApp.episode.getUser().id !== req.user.href) {
    next(throwjs.unauthorized("You do not have access to this podcast"));
  }

  next(); // authorized
}

function episodeController(req, res) {
  // do something with req.yourApp.episode
}

app.get('/episode/:id', validateEpisode, authUserByEpisode, episodeController)
</code></pre>

### Answer ID: 37750481
<p>Well after all, this is related to the throwjs framework I'm using and the fact that I'm using incorrectly</p>

<pre><code>    throw (throwjs.notFound());
</code></pre>

<p>should be </p>

<pre><code>    throw (new throwjs.notFound());
</code></pre>

<p>...</p>

