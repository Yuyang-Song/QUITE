# Maximizing apache server instances with large mod_wsgi application
[Link to question](https://stackoverflow.com/questions/10017645/maximizing-apache-server-instances-with-large-mod-wsgi-application)
**Creation Date:** 1333566404
**Score:** 2
**Tags:** python, database, django, apache, mod-wsgi
## Question Body
<p>I'm writing a Oracle of Bacon type website that involves a breadth first search on a very large directed graph (>5 million nodes with an average of perhaps 30 outbound edges each). This is also essentially all the site will do, aside from display a few mostly text pages (how it works, contact info, etc.). I currently have a test implementation running in Python, but even using Python arrays to efficiently represent the data, it takes >1.5gb of RAM to hold the whole thing. Clearly Python is the wrong language for a low-level algorithmic problem like this, so I plan to rewrite most of it in C using the Python/C bindings. I estimate that this'll take about 300 mb of RAM.</p>

<p>Based on my current configuration, this will run through mod_wsgi in apache 2.2.14, which is set to use mpm_worker_module. Each child apache server will then load up the whole python setup (which loads the C extension) thus using 300 mb, and I only have 4gb of RAM. This'll take time to load and it seems like it'd potentially keep the number of server instances lower than it could otherwise be. If I understand correctly, data-heavy (and not client-interaction-heavy) tasks like this would typically get divorced from the server by setting up an SQL database or something of the sort that all the server processes could then query. But I don't know of a database framework that'd fit my needs.</p>

<p>So, how to proceed? Is it worth trying to set up a database divorced from the webserver, or in some other way move the application a step farther out than mod_wsgi, in order to maybe get a few more server instances running? If so, how could this be done?    </p>

<p>My first impression is that the database, and not the server, is always going to be the limiting factor. It looks like the typical Apache mpm_worker_module configuration has ServerLimit 16 anyways, so I'd probably only get a few more servers. And if I did divorce the database from the server I'd have to have some way to run multiple instances of the database as well (I already know that just one probably won't cut it for the traffic levels I want to support) and make them play nice with the server. So I've perhaps mostly answered my own question, but this is a kind of odd situation so I figured it'd be worth seeing if anyone's got a firmer handle on it. Anything I'm missing? Does this implementation make sense? Thanks in advance!</p>

<p>Technical details: it's a Django website that I'm going to serve using Apache 2.2.14 on Ubuntu 10.4. </p>

## Answers
### Answer ID: 10020054
<p>First up, look at daemon mode of mod_wsgi and don't use embedded mode as then you can control separate to Apache child processes the number of Python WSGI application processes. Secondly, you would be better off putting the memory hungry bits in a separate backend process. You might use XML-RPC or other message queueing system to communicate with the backend processes, or even perhaps see if you can use Celery in some way.</p>

