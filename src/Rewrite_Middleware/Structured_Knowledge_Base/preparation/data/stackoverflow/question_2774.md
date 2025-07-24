# Searching trough JSON data stored in MySql
[Link to question](https://stackoverflow.com/questions/51931021/searching-trough-json-data-stored-in-mysql)
**Creation Date:** 1534768985
**Score:** 0
**Tags:** mysql, json
## Question Body
<p>I've a big set of json data inside a database, the data wasn't supposed to be queryed, so the was stored in a very messy way... this is the structure</p>

<pre><code>{
"0": {"key": "Developer(s)", "values": ["Capcom"]}, 
"1": {"key": "Publisher(s)", "values": ["Capcom"]}, 
"2": {"key": "Producer(s)", "values": ["Tokuro Fujiwara"]}, 
"3": {"key": "Composer(s)", "values": ["Setsuo Yamamoto"]}, 
"4": {"key": "Series", "values": ["X-Men"]}, 
"6": {"key": "Release", "values": ["EU:", " 1995"]}, 
"7": {"key": "Mode(s)", "values": ["Single-player"]}
}
</code></pre>

<p>I should query inside the db  to verify which records has which property (i.e. all records with a "Release" key inside, all that contains the value "Capcom" inside the Developoer key, etc.)</p>

<p>Can someone point me to the right way? I found only examples with simple structures (i.e. { "key": "value" }), here the key is the index number, and the value is an array with two different keys...</p>

<p>Should I find a way to rewrite all the data or there is something easy?</p>

<p>p.s. I'm building a laravel application over this data, so I can also use an eloquent approach.</p>

<p>Thanks in advance</p>

## Answers
### Answer ID: 51945276
<p>Thanks everyone, at the end i've decided to fetch all the data and storing them again properly.</p>

### Answer ID: 51932477
<p>as @Guy L mentioned in his answer, you can use LIKE or REGEX. But, It will be expensive.</p>

<p>example: </p>

<pre><code> SELECT * FROM table WHERE json_column LIKE '%"Release"%';
</code></pre>

<p>answering:</p>

<blockquote>
  <p>Should I find a way to rewrite all the data or there is something easy?</p>
</blockquote>

<p>Consider, how often do you have to access this data?</p>

<p>a NoSQL database like MongoDB is a really good usecase for data like this, I have been using Mongo and I am happy with it.</p>

<p>You can easily migrate your data to MongoDB and use a ORM similar to Eloquent model like : <a href="https://github.com/jenssegers/laravel-mongodb" rel="nofollow noreferrer">https://github.com/jenssegers/laravel-mongodb</a> to communicate with mongo from your laravel project.</p>

<p>Hope it helps you arrive at a solution.</p>

### Answer ID: 51932035
<p>Thanks for the suggestions about using mysql json specific functions, the column is already in JSON type, so i can definitively use thm, but unfortunally even after reading the mysql documentation i can't figure out how to solve my problem, honestly i'm not a data specialist, i'm kind of confused when dealing with database, so any examples will be appreciated.</p>

<p>So far i've tried to mess up with queries, but i wasn't able to find a correct "selector" for the keys of my dataset, using '$[0]' will return only the first column, i'd need some hints for creating the right syntax using json_extract, json_contains, etc.</p>

### Answer ID: 51931243
<p>Query JSON as a string can be done using the LIKE or REGEXP operators
But in general, since the strings are long an complex it's really not recommended</p>

<p>The best way is reloading the info into proper tables, storing in an SQL way</p>

<p>If your MySQL version is 5.7 or above, you can try some options will its JSON support:</p>

<p><a href="https://dev.mysql.com/doc/refman/8.0/en/json.html#json-paths" rel="nofollow noreferrer">https://dev.mysql.com/doc/refman/8.0/en/json.html#json-paths</a></p>

### Answer ID: 51931180
<p>Please refer to 
<a href="https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html" rel="nofollow noreferrer">https://dev.mysql.com/doc/refman/8.0/en/json-search-functions.html</a></p>

<p>which allows you to search for specific value at specific place of the JSON structure.</p>

<p>However, I would suggest - if the data is NOW supposed to be searchable - redesign/convert the data.</p>

