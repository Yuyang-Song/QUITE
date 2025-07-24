# Using Flask SQLAlchemy from worker threads
[Link to question](https://stackoverflow.com/questions/41580029/using-flask-sqlalchemy-from-worker-threads)
**Creation Date:** 1484089569
**Score:** 4
**Tags:** python, database, multithreading, flask-sqlalchemy, flask-restful
## Question Body
<p>I have a python app that uses <a href="http://flask-restful-cn.readthedocs.io/en/0.3.5" rel="nofollow noreferrer">Flask RESTful</a> as well as <a href="http://flask-sqlalchemy.pocoo.org/2.1" rel="nofollow noreferrer">Flask SQLAlchemy</a>. Part of the API I'm writing has the side effect of spinning off <a href="https://docs.python.org/2/library/threading.html#timer-objects" rel="nofollow noreferrer">Timer</a> objects. When a <code>Timer</code> expires, it executes some database queries. I'm seeing an issue in which code that is supposed to update rows in the database (a sqlite backend) is actually not issuing any <code>UPDATE</code> statements. I have verified this by turning the <code>SQLALCHEMY_ECHO</code> flag on to log the SQL statements. Whether or not the code works seems to be random. About half the time it fails to issue the <code>UPDATE</code> statement. See full example below.</p>
<p>My guess here is that SQLAlchemy Flask does not work properly when called from a worker thread. I think part of the point of Flask SQLAlchemy is to manage the SQLAlchemy sessions for you per API request. Obviously since there are no API requests going on when the <code>Timer</code> expires, I could see where things may not work properly.</p>
<p>Just to test this, I went ahead and wrote a simple data access layer using python's <a href="https://docs.python.org/2/library/sqlite3.html" rel="nofollow noreferrer">sqlite3 interface</a> and it seems to solve the problem.</p>
<p>I'd really rather not have to rewrite a bunch of data access code though. Is there a way to get Flask SQLAlchemy to work properly in this case?</p>
<h2>Sample code</h2>
<p>Here's where I set up the flask app and save off the SQLAlchemy <code>db</code> object:</p>
<pre><code>from flask import Flask
from flask_restful import Api
from flask.ext.sqlalchemy import SQLAlchemy
from flask_cors import CORS
import db_conn

flask_app = Flask(__name__)
flask_app.config.from_object('config')
CORS(flask_app)
api = Api(flask_app)
db_conn.db = SQLAlchemy(flask_app)

api.add_resource(SomeClass, '/abc/&lt;some_id&gt;/def')
</code></pre>
<p>Here's how I create the ORM models:</p>
<pre><code>import db_conn

db = db_conn.db

class MyTable(db.Model):
    __tablename__ = 'my_table'
    id = db.Column(db.Integer, primary_key=True)
    phase = db.Column(db.Integer, nullable=False, default=0)

    def set_phase(self, phase):
        self.phase = phase
        db.session.commit()
</code></pre>
<p>Here's the API handler with timer and the database call that is failing:</p>
<pre><code>from flask_restful import Resource
from threading import Timer
from models import MyTable
import db_conn
import global_store

class SomeClass(Resource):    
    def put(self, some_id):
        global_store.saved_id = some_id
        self.timer = Timer(60, self.callback)
        return '', 204

    def callback(self):
        row = MyTable.query.filter_by(id=global_store.saved_id).one()
        
        # sometimes this works, sometimes it doesn't
        row.set_phase(1)
        db_conn.db.session.commit()
</code></pre>

## Answers
### Answer ID: 41600912
<p>I'm guessing in your callback you aren't actually changing the value of the object.  SQLAlchemey won't issue DB UPDATE calls if the session state is not dirty.  So if the phase is already 1 for some reason there is nothing to do.</p>

