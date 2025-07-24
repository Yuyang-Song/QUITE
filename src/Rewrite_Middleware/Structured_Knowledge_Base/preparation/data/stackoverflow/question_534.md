# Why does my template not reactive?
[Link to question](https://stackoverflow.com/questions/30389051/why-does-my-template-not-reactive)
**Creation Date:** 1432272996
**Score:** 0
**Tags:** meteor, meteor-blaze, meteor-helper
## Question Body
<p>If I first open <a href="http://localhost:3000/" rel="nofollow">http://localhost:3000/</a>, then click the test link, the <code>roles</code> labels will be displayed.</p>

<p>But if I directly open <a href="http://localhost:3000/test(Input" rel="nofollow">http://localhost:3000/test(Input</a> the url in Chrome's address bar and hit enter),  the <code>roles</code> labels will not be displayed.</p>

<p>Here is my code:</p>

<p>In client startup I subscribe to something:</p>

<pre><code> Meteor.publish("Roles", function(){
   return Roles.find();
 });

 Meteor.startup(function() {
   if(Meteor.isClient) {
     Meteor.subscribe('Roles');
   }
 });
</code></pre>

<p>And roles template:</p>

<pre><code> Template.roles.helper( {
   allRoles: function() {
     return Roles.find();
   }
 })
</code></pre>

<p>html</p>

<pre><code>      &lt;template name="roles"&gt;
      &lt;div&gt;
        {{#each allRoles}}
          &lt;label&gt;test label&lt;/label&gt;
       {{/each}}
      &lt;/div&gt;
    &lt;/template&gt;
</code></pre>

<p>The problem is sometime <code>roles</code> template is rendered before the <code>Roles</code> is ready.
So these is no role labels displayed.</p>

<p>But according to Meteor document, helpers is a reactive computation, and Database queries on Collections is  reactive data source. So after <code>Roles</code> is ready, the <code>{{#with allRoles}}</code> is reactive and should be displayed.</p>

<p>Why does roles not be displayed?</p>

<p>And then I rewrite my code to:</p>

<pre><code> Meteor.startup(function() {
       if(Meteor.isClient) {
        roles_sub = Meteor.subscribe('Roles');
       }
     });

Template.roles.helper( {
       allRoles: function() {
         console.log(2);
         return Roles.find();
       },
       isReady: function() {
         console.log(1);
         console.log(roles_sub.ready());
         return roles_sub.ready();
       }
     })
</code></pre>

<p>html</p>

<pre><code>&lt;template name="roles"&gt;
  &lt;div&gt;
    {{#if isReady}}
    {{#each allRoles}}
      &lt;label&gt;test label&lt;/label&gt;
    {{/each}}
    {{/if}}
  &lt;/div&gt;
&lt;/template&gt;
</code></pre>

<p>And still role labels cannot be displayed.
And console gives me:</p>

<pre><code>1
false
1
false
1
true
2
</code></pre>

<p>Which means <code>isReady()</code> is reactive? but why my roles labels remains blank?</p>

<p>Can somebody explain this?</p>

## Answers
### Answer ID: 30390535
<p>use <strong><a href="https://github.com/meteor/meteor/blob/devel/History.md#blaze-3" rel="nofollow">Template.subscriptionsReady</a></strong> </p>

<p>server/publish.js</p>

<pre><code> Meteor.publish("Roles", function(){
   return Roles.find();
 });
</code></pre>

<p>client/client.js</p>

<pre><code>Meteor.startup(function() {
  Meteor.subscribe('Roles');
});

 Template.roles.helpers({ // --&gt; .helper change to .helpers
   allRoles: function() {
     return Roles.find();
   }
 })
</code></pre>

<p>client/templates.html</p>

<pre><code>&lt;template name="roles"&gt;
  &lt;div&gt;
    {{# if Template.subscriptionsReady }}
      {{#with allRoles}}
        &lt;label&gt;{{&gt; role }}&lt;/label&gt;
      {{/with}}
    {{ else }}
      loading....
    {{/if}}
  &lt;/div&gt;
&lt;/template&gt;

&lt;template name="role"&gt;
  &lt;div&gt;{{ _id }}&lt;/div&gt;
&lt;/template&gt;
</code></pre>

<p>A reactive function that returns true when all of the subscriptions</p>

<p><a href="https://github.com/meteor/meteor/blob/9fe2f4b442ec84eac5352b476d014c977c5ae4a2/packages/blaze/template.js#L424" rel="nofollow">https://github.com/meteor/meteor/blob/9fe2f4b442ec84eac5352b476d014c977c5ae4a2/packages/blaze/template.js#L424</a></p>

