# Ionic Storage is it possible to use SQL anymore?
[Link to question](https://stackoverflow.com/questions/42011581/ionic-storage-is-it-possible-to-use-sql-anymore)
**Creation Date:** 1486066799
**Score:** 2
**Tags:** mysql, json, sqlite, ionic-framework, ionic2
## Question Body
<p>The newest Ionic now uses "Storage" which relies on a key value pair based storage. Now I'm a webdeveloper and I use MySQL almsot everyday, and I'd love to use it in Ionic too. Now there are numerous SQLite and WebSQL tutorials available but I read everywhere that in the future this will drop so be prepared to use key pair value databases.</p>

<p>Now I'm confused, because how can you do cross related queries in databases for relational data? I always presumed relational databases are way more efficient and keeps the data organized. Is this even possible with key value?</p>

<p>I thought about using JSON, but that would mean every time you want to add or delete a row, you need to rewrite the whole JSON database... And how would you update one row with the Storage functionality of Ionic?</p>

## Answers
### Answer ID: 42053889
<p>There are options other than WebSQL for a relational database in web apps. <a href="https://github.com/kripken/sql.js/" rel="nofollow noreferrer">SQL.js</a> is SQLite cross-compiled to Javascript and <a href="https://github.com/google/lovefield" rel="nofollow noreferrer">lovefield</a> is a relational database built on top of indexeddb. The fact that it's possible to build a relational database on top of indexeddb was one of the arguments for dropping WebSQL. Neither of these options are as performant as WebSQL, so there are proposals such as <a href="https://arthurhsu.github.io/rdb/" rel="nofollow noreferrer">rdb</a> for adding a relational database API to the web.</p>

<p>Since you are building a hybrid Ionic app, you have access to native functionality as well. There is a <a href="http://ngcordova.com/docs/plugins/sqlite/" rel="nofollow noreferrer">plugin</a> that gives you a similar API to WebSQL and will work even if browsers drop WebSQL. If you need a relational database in your app, I think this is your best option.</p>

