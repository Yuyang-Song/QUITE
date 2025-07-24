# Mongoose / Mongodb migration to MySQL
[Link to question](https://stackoverflow.com/questions/42276591/mongoose-mongodb-migration-to-mysql)
**Creation Date:** 1487254948
**Score:** 3
**Tags:** mysql, node.js, mongodb, mongoose, database-migration
## Question Body
<p>I have a NodeJS project running with mongodb database (using mongoose). </p>

<p>For a technological constraint reason I need to migrate the app from using mongodb to mysql - is there a way to migrate to mysql without having to rewrite the whole mongoose model files?</p>

<p>PS. although I'm using mongodb all the query is mainly still not on the nested document (I'm querying only by ID or by some first-level attribute) so actually putting nested document into a field in mysql table should still be fine</p>

## Answers
### Answer ID: 42277193
<p>I would suggest letting your application run with Mongo for now. Meanwhile write a wrapper for MySQL that would translate your Mongo queries to mysql. Switch to that wrapper once done. Then write another wrapper for Mongo, just in case you need to switch back.</p>

<p>Try and keep all your Database specific function calls in the wrapper. So, that you won't need to do this again and again. Just write a new wrapper for whatever Database you will use and just switch.</p>

<p>And you'll probably need to run some sort of job to migrate your data from Mongo to MySQL.</p>

