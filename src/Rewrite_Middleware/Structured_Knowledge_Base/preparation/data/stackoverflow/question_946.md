# Deploying rails app to heroku which uses raw sql code
[Link to question](https://stackoverflow.com/questions/51568497/deploying-rails-app-to-heroku-which-uses-raw-sql-code)
**Creation Date:** 1532757133
**Score:** 0
**Tags:** ruby-on-rails, heroku
## Question Body
<p>Rails has a emphasis on using Active record which abstract's queries sent to the database. Thus Heroku can use postgresql without us having to rewrite queries. </p>

<p>What if rails app uses raw sql and we now want to deploy the app to heroku, how do we do that.</p>

<p>The model contains code like this </p>

<pre><code>sql = "Select * from ... your sql query here"
records_array = ActiveRecord::Base.connection.execute(sql)
</code></pre>

## Answers
### Answer ID: 51569077
<p>You can use Active Record Migrations mechanism which allows you to use raw SQL queries as described in sections 3.7, 3.9.</p>

<p><a href="https://guides.rubyonrails.org/active_record_migrations.html#when-helpers-aren-t-enough" rel="nofollow noreferrer">https://guides.rubyonrails.org/active_record_migrations.html#when-helpers-aren-t-enough</a></p>

