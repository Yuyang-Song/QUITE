# Result of database query won&#39;t load into flask template
[Link to question](https://stackoverflow.com/questions/56094630/result-of-database-query-wont-load-into-flask-template)
**Creation Date:** 1557612392
**Score:** 0
**Tags:** python, database, postgresql, flask, flask-sqlalchemy
## Question Body
<p>I changed the way I'm querying the database and although the result loads fine I cant get the information to show up in the template.</p>

<p>I tried rewriting the code in a simpler way to try and catch errors but found nothing. I am not sure what else to do.</p>

<pre><code>from flask import render_template
from app import app, db


@app.route("/page")
def page():
    '''
    this is the old way that is useable in the template
    result = Test.query.filter_by(id=12))
    '''


    # test variables
    d = 65465
    s = 'rebrb'


    result = db.engine.execute('SELECT * FROM test WHERE id IN (183, 184, 180, 181, 182, 185, 95, 179)')
    # new way works here but not in the template
    print(result)
    for row in result:
        print(row.content)
    return render_template('page.html', s=s, d=d, result=result, title='Video')





'''
The d and s load but the for loop doesn't do anything 
'''
{{ d }}
{{ s }}
    {% for row in result %}
        {{ row }}
        {{ d }}
    {% endfor %}
</code></pre>

<p>The d and s variables show up but nothing past the for loop works.</p>

<p><strong>edit 1:</strong> I made some progress by converting the result to a list before sending it to the template, but I feel like I shouldn't have to do that and I'm still looking for a better option.</p>

<p><strong>edit 2:</strong> I found out I can also do the query this way.</p>

<pre><code>result = Test.query.filter(Test.id.in_(183, 184, 180, 181, 182, 185, 95, 179))
</code></pre>

<p>Which works better but I need the result to be in the same order as the list</p>

## Answers
### Answer ID: 56097638
<p>The query I was trying to change to can be accomplished by using</p>

<pre><code>result = Test.query.filter(Test.id.in_(95, 179, 180, 181, 182, 183, 184, 185))
</code></pre>

<p>without any extra problems.</p>

