# Handle multiple accounts and users in one CakePHP app with URL domain.com/account/controller/action
[Link to question](https://stackoverflow.com/questions/2255038/handle-multiple-accounts-and-users-in-one-cakephp-app-with-url-domain-com-accoun)
**Creation Date:** 1266007892
**Score:** 0
**Tags:** php, .htaccess, mod-rewrite, cakephp
## Question Body
<p>What I need to accomplish is a single Application with a single database but multiple accounts (companies), each with multiple users.</p>

<p>The URL convention must be as follows: domain.com/account/controller/action</p>

<p>So ALL controllers are prefixed by the company/account name.</p>

<p>All accounts would share the single database, but each one would need to be able to restrict access to their data.</p>

<p>The question is, how do I implement this? I've thought about implementing some sort of htaccess rewrite where I strip out the first URL parameter (account) and pass as a query string parameter, which would be internally parsed by the app_controller. The challenge, however, is maintaining integrity with all of the links throughout the app. I.e. the cake routing would somehow need to be aware of the account parameter and pass it to all outputted links.</p>

<p>Has anyone accomplished something similar to this before?</p>

## Answers
### Answer ID: 2255183
<p>You can do two things, both with Routes.</p>

<p>First, setting a variable in the routes:</p>

<pre><code>Router::connect('/:user/blog/*', array('controller' =&gt; 'blogs', 'action' =&gt; 'index'));
</code></pre>

<p>And now you can access the user variable with <code>$this-&gt;params['user']</code>. The thing with this is that you will have to manually set each controller and action you want to manage. I think it's no big deal, since most of the times it is better to rewrite the default routes architecture for CakePHP.</p>

<p>Second, you can tell you are waiting for a variable and will be accessible as a parameter in your function.</p>

<pre><code>Router::connect('/(.*)/*', array('controller' =&gt; 'blogs', 'action' =&gt; 'index'));
</code></pre>

<p>In your controller:</p>

<pre><code>function index($a, $b){
    pr($a);
    pr($b);
}
</code></pre>

<p>And now you will be getting both vars.</p>

<p>I don't know if it can be made automatically, perhaps rewriting the htaccess could be a good idea.</p>

<p>Hope it helped.</p>

### Answer ID: 2255173
<p>It's perfectly possible to do this (but I've never done it).</p>

<p>I assume you use the standard CakePHP authentication scheme. If so, information about the currently logged in user can be found in the Auth->User array.</p>

<p>Cake expects you to have a users table in your database. You should alter your models to have a belongsTo relationship with the user table (i.e. all tables have a user_id field).</p>

<p>In your models you could probably utilize the afterFind() hook to check that the user_id field  matches the currently logged in user and return false if thats not the case. In your controller you should then check all model operations for falseness.</p>

<p>The .htaccess idea is probably not very good. You should put the authorization as close as possible to the data source, in cake that would be in your model (you could put the afterFind callback in the AppModel class).</p>

<p>Extending your example:</p>

<p>User requests /someController/someAction.</p>

<pre><code>someAction:

if($this-&gt;someModel-&gt;someOperation(someArgument)) {

   //OK, show view

} else {

   // Something went wrong
   // Your afterFind method provides a clue via the model-&gt;failure attribute

   $this-&gt;flash($this-&gt;someModel-&gt;failure);

}
</code></pre>

