# use functions inside of defaultscope in sequelize
[Link to question](https://stackoverflow.com/questions/47151411/use-functions-inside-of-defaultscope-in-sequelize)
**Creation Date:** 1510036443
**Score:** 1
**Tags:** node.js, orm, sequelize.js
## Question Body
<p>I'm using Sequelize for a project with a single db for multiple applications. I need to query MSSQL database for each request based on the application_id I receive in the request. (on Nodejs)</p>

<p>Calling a function inside of scope in Sequelize model definition requires specifying the name of the scope for each query which is not desired.</p>

<p>I think if I could use functions inside of defaultscope to make it work (without manually overriding it again and again) . Or if there's any other way to accomplish this (better without rewriting Sequelize functions). Thank you!</p>

