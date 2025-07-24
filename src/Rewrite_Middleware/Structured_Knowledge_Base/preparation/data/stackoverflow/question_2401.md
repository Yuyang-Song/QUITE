# mongodb GEO2D Index - kilometers?
[Link to question](https://stackoverflow.com/questions/32850079/mongodb-geo2d-index-kilometers)
**Creation Date:** 1443547272
**Score:** 0
**Tags:** mongodb, pymongo, nosql
## Question Body
<p>I have a geospatial index in my database.  <a href="http://docs.mongodb.org/manual/reference/operator/query/near/" rel="nofollow noreferrer">MongoDB's documentation</a> says that the $near operator takes an argument in meters to find matches.  For example:</p>
<pre><code>db.data.find({'coordinates': SON([('$near', [20.450550042732765, 80.52327036857605]), ('$maxDistance', 100)])}).count()
</code></pre>
<p>should return matches within 100 meters of that location.  But too many are returned, about 3,000.  When I rewrite the query as</p>
<pre><code>db.data.find({'coordinates': SON([('$near', [20.450550042732765, 80.52327036857605]), ('$maxDistance', 1)])}).count()  
</code></pre>
<p>I receive 364 results.  I do not think my database has 364 matches within a 1 meter radius of the point I query.  Finally, if I query</p>
<pre><code>db.data.find({'coordinates': SON([('$near', [20.450550042732765, 80.52327036857605]), ('$maxDistance', .1)])}).count()
</code></pre>
<p>I receive 330 matches.  There are definitely not 330 results within 10 centimeters of that point.</p>
<p>I think mongodb interprets distance as kilometers, not meters.  Can anyone confirm or explain what is going on?</p>

## Answers
### Answer ID: 32852123
<p>If you are using the legacy <code>2d</code> index, and it looks like that's what you're doing, then <code>$maxDistance</code> is in radians, as per the documentation you linked to.</p>

