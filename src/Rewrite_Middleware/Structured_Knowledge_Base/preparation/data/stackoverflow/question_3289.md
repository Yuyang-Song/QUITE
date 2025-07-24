# Why does MongoDB advise on upgrading MongoDB incrementally, version-by-version?
[Link to question](https://stackoverflow.com/questions/75206097/why-does-mongodb-advise-on-upgrading-mongodb-incrementally-version-by-version)
**Creation Date:** 1674453786
**Score:** 1
**Tags:** mongodb
## Question Body
<p>Apologies if this question is too open-ended.</p>
<p>I have inherited an aging tech stack and am required to upgrade our 200GB MongoDB Community Edition v3.4 installation (hosted on Ubuntu 20) to MongoDB v5 in order to support some new features.</p>
<p>MongoDB advises that to install v5.0, one must be already on MongoDB v4.4:</p>
<p><a href="https://www.mongodb.com/docs/manual/release-notes/5.0-upgrade-standalone/" rel="nofollow noreferrer">https://www.mongodb.com/docs/manual/release-notes/5.0-upgrade-standalone/</a></p>
<p>They say that if you are on a version older than 4.4, then you need to incrementally upgrade to v4.4 before upgrading to v5.</p>
<p>However, if you follow the links in that official upgrade tutorial, you will find that in order to upgrade to any version of MongoDB, they insist on you upgrading version-by-version, successively.</p>
<p>So for me on v3.4 the upgrade path will look like this:</p>
<pre><code>v3.4 -&gt; v3.6 -&gt; v4.0 -&gt; v4.2 -&gt; v4.4 -&gt; v5.0.13
</code></pre>
<p>Following these tutorials:</p>
<ol>
<li><a href="https://www.mongodb.com/docs/manual/release-notes/3.6-upgrade-standalone/" rel="nofollow noreferrer">https://www.mongodb.com/docs/manual/release-notes/3.6-upgrade-standalone/</a></li>
<li><a href="https://www.mongodb.com/docs/manual/release-notes/4.0-upgrade-standalone/" rel="nofollow noreferrer">https://www.mongodb.com/docs/manual/release-notes/4.0-upgrade-standalone/</a></li>
<li><a href="https://www.mongodb.com/docs/manual/release-notes/4.2-upgrade-standalone/" rel="nofollow noreferrer">https://www.mongodb.com/docs/manual/release-notes/4.2-upgrade-standalone/</a></li>
<li><a href="https://www.mongodb.com/docs/manual/release-notes/4.4-upgrade-standalone/" rel="nofollow noreferrer">https://www.mongodb.com/docs/manual/release-notes/4.4-upgrade-standalone/</a></li>
<li><a href="https://www.mongodb.com/docs/manual/release-notes/5.0-upgrade-standalone/" rel="nofollow noreferrer">https://www.mongodb.com/docs/manual/release-notes/5.0-upgrade-standalone/</a></li>
</ol>
<p>I'm not entirely sure why this is necessary, as the tutorials themselves seem to mostly involve copying over newer binaries and then setting a feature compatibility version in the database config.</p>
<p>To test whether this was necessary I did a <code>mongodump</code> of our entire v3.4 database and then installed a standalone MongoDB v5.0.13 on the same server and then <code>mongorestore</code> to the new v5.0.13 database. Everything seems to work fine, <code>mongorestore</code> spent two hours recreating all the indexes as its last step (something various articles told me would not happen using the mongodump/mongorestore method).</p>
<p>I am able to connect Mongo clients to this new v5.0.13 Community instance without issue. All the data is there and I am able to query it just fine.</p>
<p>So my question is, why does MongoDB strongly advise doing the upgrade incrementally, one version at a time when dumping the database and restoring it to a new version of MongoDB seems to work just fine?</p>
<p>The only issues I have currently is having to rewrite some client code which is using an older Mongo Java driver. This is something I am going to have to do regardless of the upgrade method I used.</p>
<p>Our MongoDB instance is Community Edition and is a single, standalone instance (not a replica set) so I don't know if this matters. Perhaps the upgrade process described by MongoDB is for Mongo Cloud or for Enterprise?</p>
<p>I'm just looking for clarification on whether the simpler method I tried is going to cause me issues. Maybe I've missed something I hadn't considered.</p>

## Answers
### Answer ID: 78809104
<p>One version at a time upgrade path is because of data format changes; the versions need to be able to read/write the format, and if you skip versions and something goes wrong you won't be able to rollback.</p>

