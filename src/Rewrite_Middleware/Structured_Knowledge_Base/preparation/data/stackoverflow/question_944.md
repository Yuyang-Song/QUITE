# Python Redis on Heroku reached max clients
[Link to question](https://stackoverflow.com/questions/51519333/python-redis-on-heroku-reached-max-clients)
**Creation Date:** 1532523007
**Score:** 1
**Tags:** python, heroku, redis, gunicorn
## Question Body
<p>I am writing a server with multiple gunicorn workers and want to let them all have access to a specific variable. I'm using Redis to do this(it's in RAM, so it's fast, right?) but every GET or SET request adds another client.  I'm performing maybe ~150 requests per second, so it quickly reaches the 25 connection limit that Heroku has. To access the database, I'm using <code>db = redis.from_url(os.environ.get("REDIS_URL"))</code> and then <code>db.set()</code> and <code>db.get()</code>.  <strong>Is there a way to lower that number? For instance, by using the same connection over and over again for each worker?  But how would I do that?</strong> The 3 gunicorn workers I have are performing around 50 queries each per second.</p>

<p>If using redis is a bad idea(which it probably is), it would be great if you could suggest alternatives, but also please include a way to fix my current problem as most of my code is based off of it and <strong>I don't have enough time to rewrite the whole thing yet</strong>.</p>

<p>Note: The three pieces of code are the only times <code>redis</code> and <code>db</code> are called.  I didn't do any configuration or anything.  Maybe that info will help.</p>

## Answers
### Answer ID: 51519644
<p>Most likely, your script creates a new connection for each request.<br>
But each worker should create it once and use forever.</p>

<p>Which framework are you using?<br>
It should have some documentation about how to configure Redis for your webapp.</p>

<p>P.S. Redis is a good choice to handle that :)</p>

