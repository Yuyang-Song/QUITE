# App Engine (Flask) memory limit: how should I cache &quot;large&quot; (3 MB) database calls? How can I monitor memory usage on a local server or during testing?
[Link to question](https://stackoverflow.com/questions/76726139/app-engine-flask-memory-limit-how-should-i-cache-large-3-mb-database-call)
**Creation Date:** 1689816710
**Score:** 1
**Tags:** python, flask, google-app-engine, out-of-memory, memcached
## Question Body
<p>For some time now, I've been running into this error on my current project, <a href="https://golfcourse.wiki/" rel="nofollow noreferrer">golfcourse.wiki</a> (App Engine F1, Python 3.9, Flask 2.0.2):</p>
<p><code>Exceeded hard memory limit of 384 MiB with 395 MiB after servicing 39 requests total. Consider setting a larger instance class in app.yaml.</code></p>
<p>This has been an issue more and more as my database has been growing. I thought it might be an issue of database calls (which I clearly understand is wrong now), so I added the builtin memcache to the system. This has been a huge pain, as adding a wsgi wrapper has make all my tests break, and I'm going to need to rewrite the __init__.py code using the <a href="https://flask.palletsprojects.com/en/2.3.x/patterns/appfactories/" rel="nofollow noreferrer">app factory pattern</a> and then go through the entire code rewriting app calls as current_app calls (haven't gotten around to that yet).</p>
<p>Unfortunately, the process of this has actually increased the number of times the app crashes:</p>
<p><code>Exceeded hard memory limit of 384 MiB with 424 MiB after servicing 539 requests total. Consider setting a larger instance class in app.yaml.</code></p>
<p>While doing this, I realized some of my larger database calls (3 MB) were over the memcache limit, and so I wrote the common serialization workaround to deal with it and my memory exploded:</p>
<p><code>Exceeded hard memory limit of 384 MiB with 904 MiB after servicing 0 requests total. Consider setting a larger instance class in app.yaml.</code></p>
<p>I figured I'd bite the bullet and upgrade to F2... I couldn't believe it when it caused the memory usage <em>to go up by 20%</em>:</p>
<p><code>Exceeded hard memory limit of 768 MiB with 1105 MiB after servicing 0 requests total. Consider setting a larger instance class in app.yaml.</code></p>
<p>I'm deeply confused. I cannot find anything related to this in the App Engine docs (I've really looked). I'm admittedly an amateur at this stuff, even as I've been working with python for over a decade.</p>
<p>Can someone explain to me:</p>
<ol>
<li>What is <em>actually</em> happening here? I understand that without sharing my entire code base, that nobody can point out the inefficiencies, but I'm assuming now that I'm running up against the <a href="https://en.wikipedia.org/wiki/Resident_set_size" rel="nofollow noreferrer">RSS</a> limit? Because when I run the process locally, I'm not coming anywhere close to that! As far as I can tell the program, while running locally, is <em>maybe</em> reaching 150MiB.</li>
<li>How can I monitor this with testing?</li>
<li>Should I even worry about the number of database calls I'm making? I'm operating on a shoestring (obviously, being on F1), but I'm paying for MongoDB, and I don't think I'm anywhere near the quotas yet. It looks like I can cache most of the queries just fine, but the larger ones happen on the home page.</li>
</ol>
<p>I've been trying to figure this out for months, any help would be really appreciated.</p>

## Answers
### Answer ID: 76726487
<p>I understand that error to mean that your instance ran out of RAM, so adding a cache wouldn't necessarily help. A cache will save you the round-trip to the db, not how much you're loading into memory before return a result to your website.</p>
<blockquote>
<p>This has been an issue more and more as my database has been growing.</p>
</blockquote>
<p>I visited your website. It looks like the problem is you are fetching your entire DB's list of golf courses to return the home page. You need to either:</p>
<ol>
<li>only fetch the golf courses you need for that particular page load (i.e. only the golf courses within 100 miles of the user's location). Then when you user moves on the map, you query your backend for the golf courses at the new location</li>
<li>produce like a published list of all the golf courses, store it in a GCS bucket and have your website read that file from that bucket.</li>
</ol>
<p>There are other solutions to this problem too, but those are the simplest. Pulling your entire DB table into RAM everytime the home page is just not a good idea.</p>

