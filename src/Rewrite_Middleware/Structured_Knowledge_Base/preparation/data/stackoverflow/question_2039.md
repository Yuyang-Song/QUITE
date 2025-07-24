# How to explicitly unsubscribe from a collection?
[Link to question](https://stackoverflow.com/questions/16776055/how-to-explicitly-unsubscribe-from-a-collection)
**Creation Date:** 1369667639
**Score:** 8
**Tags:** meteor
## Question Body
<p>I have a MongoDB with a large "messages" collection; all messages belonging to a specific <code>groupId</code>. So have started with a publication like this:</p>

<pre><code>Meteor.publish("messages", function(groupId) {
  return Messages.find({
    groupId: groupId
  });
});
</code></pre>

<p>and a subscription like this:</p>

<pre><code>Deps.autorun(function() {
   return Meteor.subscribe("messages", Session.get("currentGroupId"));
});
</code></pre>

<p>This got me into trouble because initially <code>currentGroupId</code> is undefined but sill mongod would use up the CPU to find messages with <code>groupId == null</code> (although I know there are none).</p>

<p>Now, I tried to rewrite the publication as follows:</p>

<pre><code>Meteor.publish("messages", function(groupId) {
  if (groupId) {
    return Messages.find({
      groupId: groupId
    });
  } else {
    return {}; // is this the way to return an empty publication!?
  }
});
</code></pre>

<p>and/or to rewrite the subscription to:</p>

<pre><code>Deps.autorun(function() {
   if (Session.get("currentGroupId")) {
     return Meteor.subscribe("messages", Session.get("currentGroupId"));
   } else {
     // can I put a Meteor.unsubscribe("messages") here!?
   }
});
</code></pre>

<p>which both helps initially. But as soon as <code>currentGroupId</code> becomes undefined again (because the user navigates to a different page), mongod is still busy requerying the database for the last subscribed <code>groupId</code>. So how can I unsubscribe from a publication such that the mongod is stopped being queried?</p>

## Answers
### Answer ID: 35973191
<p>I found it more simple and straight-forward to call the <code>.stop()</code> function on the handler which is returned from the <code>.subscribe()</code> call:</p>

<pre><code>let handler = Meteor.subscribe('items');
...
handler.stop();
</code></pre>

### Answer ID: 16778366
<p>According to the documentation it must be <a href="http://docs.meteor.com/#publish_stop" rel="noreferrer">http://docs.meteor.com/#publish_stop</a> </p>

<blockquote>
  <p>this.stop()
  Call inside the publish function. Stops this client's subscription;
  the onError callback is not invoked on the client.</p>
</blockquote>

<p>So something like </p>

<pre><code>Meteor.publish("messages", function(groupId) {
  if (groupId) {
    return Messages.find({
      groupId: groupId
    });
  } else {
    return this.stop();
  }
});
</code></pre>

<p>And I guess on the client side you can just remove your if/else like in your first example</p>

<pre><code>Deps.autorun(function() {
   return Meteor.subscribe("messages", Session.get("currentGroupId"));
});
</code></pre>

### Answer ID: 16792879
<p>Simply adding a condition to the publication:</p>

<pre><code>Meteor.publish("messages", function(groupId) {
  if (groupId) {
    return Messages.find({
      groupId: groupId
    });
});
</code></pre>

<p>and keeping the subscription:</p>

<pre><code>Deps.autorun(function() {
  return Meteor.subscribe("messages", Session.get("currentGroupId"));
});
</code></pre>

<p>does the job.</p>

<p>There is no need to stop the publication explicitly. Eventually, the MongoDB is not queried anymore after finishing the currently running query and issuing yet another one (which seems to be queued somewhere in the system).</p>

### Answer ID: 16779138
<p>in your case, you should stop the <code>autorun</code> </p>

<p>there is an example in the <a href="http://docs.meteor.com/#deps_autorun" rel="nofollow">documentation</a> </p>

<p>Your autorun is actually called with a parameter that allows you to stop it:</p>

<pre><code>Deps.autorun(function (c) {
  if (! Session.equals("shouldAlert", true))
    return;

  c.stop();
  alert("Oh no!");
});
</code></pre>

