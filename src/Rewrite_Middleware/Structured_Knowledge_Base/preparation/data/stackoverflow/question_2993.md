# Two flask apps (models) using same table
[Link to question](https://stackoverflow.com/questions/61507124/two-flask-apps-models-using-same-table)
**Creation Date:** 1588178956
**Score:** 0
**Tags:** flask, orm, mongoengine, flask-restful
## Question Body
<p>I build 2 flask Apps App1 and App2(Two different services). Both Apps are referring to the same DB. Am using MongoDB as database and MongoEngine to create connections and to support ORM Queries.</p>

<p>I have created a user table in App1 and I defined the structure of the table in models.py file. Now I have to use the same user table in the App2. How would I use the existing table itself without rewriting the same code in APP2?</p>

<p>I can do it in one way that I can write a Mongo wrapper which will connect and serve the data. But I don't want to write RAW queries. Can someone help me how to do this? Thanks!</p>

## Answers
### Answer ID: 61510280
<p>You can put all your database-related code into a separate <a href="https://realpython.com/python-modules-packages/" rel="nofollow noreferrer">Python package</a> which both your applications can then import.</p>

<p>OR</p>

<p>You could also consider building a separate application around your database code that exposes information through an API. Your other applications could then make requests to this API.</p>

