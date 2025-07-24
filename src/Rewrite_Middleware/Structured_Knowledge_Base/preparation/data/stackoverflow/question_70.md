# Flask/MySQL app seems to be blocking concurrent requests when query is complicated
[Link to question](https://stackoverflow.com/questions/11860385/flask-mysql-app-seems-to-be-blocking-concurrent-requests-when-query-is-complicat)
**Creation Date:** 1344413718
**Score:** 1
**Tags:** mysql, nginx, flask, blocking, tornado
## Question Body
<p>I have a simple, single page Flask (v0.8) application that queries a MySQL database and displays results for each request based on different request params. The application is served using Tornado over Nginx.</p>

<p>Recently I've noticed that the application seems to blocking concurrent requests from different clients when a DB query is still running. E.g - </p>

<ol>
<li>A client makes a request with a complicated DB query that takes a while to complete (> 20 sec).</li>
<li>A different client makes a request to the server and is blocked until the first query returns.</li>
</ol>

<p>So basically the application behaves like a single process that serves everyone. I was thinking the problem was with a shared DB connection on the server, so I started using the <code>dbutils</code> module for connection pooling. That didn't help. I think I'm probably missing something big in the architecture or the configuration of the server, so I'd appreciate any feedback on this.</p>

<p>This is the code for the Flask that performs the db querying (simplified):</p>

<pre><code>#... flask imports and such

import MySQLdb
from DBUtils.PooledDB import PooledDB

POOL_SIZE = 5

class DBConnection:

    def __init__(self):
        self.pool = PooledDB(MySQLdb, 
                             POOL_SIZE, 
                             user='admin', 
                             passwd='sikrit', 
                             host='localhost', 
                             db='data',
                             blocking=False,
                             maxcached=10,
                             maxconnections=10)

    def query(self, sql):
        "execute SQL and return results"

        # obtain a connection from the pool and
        # query the database
        conn   = self.pool.dedicated_connection()
        cursor = conn.cursor()
        cursor.execute(sql)

        # get results and terminate connection
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        return results


global db
db = DBConnection()

@app.route('/query/')
def query():
    if request.method == 'GET':
        # perform some DB querying based query params
        sql     = process_request_params(request)
        results = db.query(sql)
        # parse, render, etc...
</code></pre>

<p>Here's the tornado wrapper (<code>run.py</code>):</p>

<pre><code>#!/usr/bin/env python
import tornado
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop
from myapplication import app
from tornado.options import define, options

define("port", default=8888, help="run on the given port", type=int)

def main():
    tornado.options.parse_command_line()
    http_server = HTTPServer(WSGIContainer(app), xheaders=True)
    http_server.listen(options.port)
    IOLoop.instance().start()

if __name__ == '__main__': main()
</code></pre>

<p>Starting the app via startup script:</p>

<pre><code>#!/bin/sh
APP_ROOT=/srv/www/site
cd $APP_ROOT
python run.py --port=8000 --log_file_prefix=$APP_ROOT/logs/app.8000.log 2&gt;&amp;1 /dev/null
python run.py --port=8001 --log_file_prefix=$APP_ROOT/logs/app.8001.log 2&gt;&amp;1 /dev/null
</code></pre>

<p>And this is the nginx configuration:</p>

<pre><code>user nginx;
worker_processes 1;

error_log /var/log/nginx/error.log;
pid /var/run/nginx.pid;

events {
  worker_connections 1024;
  use epoll;
}

http {
  upstream frontends {
    server 127.0.0.1:8000;
    server 127.0.0.1:8001;
  }

  include /usr/local/nginx/conf/mime.types;
  default_type application/octet-stream;

  # ..

  keepalive_timeout 65;
  proxy_read_timeout 200;
  sendfile on;

  tcp_nopush on;
  tcp_nodelay on;

  gzip on;
  gzip_min_length 1000;
  gzip_proxied any;
  gzip_types text/plain text/html text/css text/xml application/x-javascript
             application/xml application/atom+xml text/javascript;

  proxy_next_upstream error;

  server {
    listen 80;
    root /srv/www/site;

    location ^~ /static/ {
      if ($query_string) {
        expires max;
      }
    }

    location / {
      proxy_pass_header Server;
      proxy_set_header Host $http_host;
      proxy_redirect off;
      proxy_set_header X-Real-IP $remote_addr;
      proxy_set_header X-Scheme $scheme;
      proxy_pass http://frontends;
    }

  }
}
</code></pre>

<p>This is a small application that serves a very small client base, and most of it is legacy code I inherited and never got around to fix or rewrite. I've only noticed the problem after adding more complex query types that took longer to complete. If anything jumps out, I'd appreciate your feedback. thanks.</p>

## Answers
### Answer ID: 11870160
<p>So, as we know - standard mysql drivers are blocking, so server will block while query executing. Here is <a href="https://blog.chartio.com/blog/making-mysql-queries-asynchronous-in-tornado" rel="nofollow noreferrer">good article</a>, about how you can achieve non-blocking mysql queires in tornado. </p>

<p>By the way, as Mike Johnston mentioned - if your query executes >20s - it is very long. My suggestion is find way to move this query in background. Tornado does not have asynchronous mysql driver in it's package - because guys at FriendFeed done their best, to make their queries executing really fast. </p>

<p>Also instead of using pool of 20 synchronous database connections - you can start 20 server instances with 1 connection each, and use nginx as reverse proxy for them. They will be more bulletproof, than pool. </p>

### Answer ID: 11870353
<p>The connection pool doesn't make MySQLdb asyncronous. The <code>results = cursor.fetchall()</code> blocks Tornado, until the query is complete.</p>

<p>That's what happens when using non-asynchronous libraries with Tornado. Tornado is an IO loop; it's one thread. If you have a 20 second query, the server will be unresponsive while it waits for MySQLdb to return. Unfortunately, I'm not aware of a good async python MySQL library. There are <a href="https://groups.google.com/forum/?fromgroups#!topic/python-tornado/qkn71J3zYqc%5B1-25%5D" rel="nofollow">some Twisted ones</a> but they introduce additional requirements and complexity into a Tornado app.</p>

<p>The Tornado guys recommend abstracting slow queries into an HTTP service, which you can then access using <code>tornado.httpclient</code>. You could also look at tuning your query (>20 seconds!), or running more Tornado processes. Or you could switch to a datastore with an async python library (MongoDB, Postgres, etc).</p>

### Answer ID: 11865244
<p>What kind of 'complicated db queries' are you running? Are they just reads or are you updating the tables. Under certain circumstances, MySQL must lock the tables - even on what might seem likely read-only queries. This could explain the blocking behavior.</p>

<p>Additionally, I'd say any query that takes 20 seconds or more to run and that is run frequently is a candidate for optimization. </p>

