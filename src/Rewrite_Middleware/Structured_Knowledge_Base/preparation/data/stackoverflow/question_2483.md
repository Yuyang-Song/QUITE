# Best approach to store page routing and navigation for different userlevels
[Link to question](https://stackoverflow.com/questions/36617578/best-approach-to-store-page-routing-and-navigation-for-different-userlevels)
**Creation Date:** 1460622436
**Score:** -1
**Tags:** php
## Question Body
<p>I'm rewriting an old php-framework. Currently the navigation, routing and authorization is done based on configuration files which are loaded on each page request.</p>

<p>I've changed the configuration files towards a database. The number of pages that are loaded differs per user, based on userlevel and authorization.
But still with each page request multiple database queries are executed, all entries are loaded and navigation, routing and authorization are processed. 
I guess this can be 'cached' because most of the time the outcome of these functions are the same for the specific user.</p>

<p>What is the best approach? </p>

<p>Cache the outcome of the functions in objects and store them in a session? 
Generate temp files with objects for each user? Store those in memory with memcached? 
Or do keep it this way and do the processing on each page request?</p>

<p>edit:
The framework is OOP oriented and already caches things like username/userlevel in session objects. </p>

## Answers
### Answer ID: 36618086
<p>No idea how your framework works, whether it's bunch of functions or a bit OOP-oriented so it's not easy to point you in the exact direction, but here's one approach that you can take in order to avoid executing repeated queries that always return the same data during a single request.</p>

<p>Let's say you have several places in your app where you need logged user's information, and for the sake of simplicity, I'll assume that your users are objects and that auth is also performed using a class :)</p>

<pre><code>class Auth
{

  private static $logged_user = false;

  static function getLoggedUser()
  {
    if (self::$logged_user === false) {
      self::$logged_user = do_some_magic_();
    }

    return self::$logged_user;
  }

}
</code></pre>

<p>In the example above, calling <code>Auth::getLoggedUser()</code> will check if private property <code>$logged_user</code> is default <code>false</code>, and if it is then it will perform the authenication (e.g. using data in session or whatever), store it in that private class property, and every consecutive call to <code>Auth::getLoggedUser()</code> will simply return the already fetched user's object. You can can also set the <code>logged_user</code> upon login.</p>

<p>In a similar way, you can 'cache' various other results of complex operations and save time/memory/queries. However, note that this may have undesirable results if the resulting object actually does change during app's request, so take care :)</p>

