# Twisted server-client interconnecting XML-RPC and REST services
[Link to question](https://stackoverflow.com/questions/11129978/twisted-server-client-interconnecting-xml-rpc-and-rest-services)
**Creation Date:** 1340238071
**Score:** 1
**Tags:** python, twisted, xml-rpc, python-requests
## Question Body
<p>I have a service provided by a REST API, with a Python library wrapping it using python-requests.</p>

<p>I have a 'dumb' user interface designed by a third party (not Python) to connect to a local XML-RPC.</p>

<p>Now I have to connect both ends and forward the XML-RPC calls to the REST API and return the results. It's mostly asynchronous and doesn't depend on results returning to the user in real-time. Most of the XML-RPC calls are supposed to return immediately, queue a task, and some other call will query the results later. Data is stored in an sqlite database until needed.</p>

<p>So, I decided to use twisted.web.xmlrpc for this middle layer and use the requests based lib for the remote calls and it works fine. I guess I'm blocking twisted's mainloop for a few seconds once in a while, but that's not a big deal.</p>

<p>The problem is that I also have to make some big file uploads from this middle layer to the  HTTP server providing the REST API. I can't make those uploads using the requests based lib because it will block the twisted loop until the upload is finished.</p>

<p>I'd rather not use multithreading, and I really don't want to rewrite the python-requests based lib I have as a twisted client. Is there any way I can integrate requests into twisted's mainloop, or any other reasonable solution?</p>

## Answers
### Answer ID: 13553689
<p>If you like requests' style of API, but want something that would work with Twisted, consider using <a href="https://github.com/dreid/treq" rel="nofollow">treq</a>.  There are <a href="https://launchpad.net/synchronous-deferred" rel="nofollow">support libraries</a> for writing interfaces which can be either synchronous or asynchronous depending on their caller's needs.</p>

<p>If you really want to use requests, but you don't want to block the main loop, you can invoke it with <a href="http://twistedmatrix.com/documents/current/api/twisted.internet.threads.deferToThread.html" rel="nofollow"><code>twisted.internet.threads.deferToThread</code></a>.  This is mostly transparent, and if your requests don't share any state you can almost ignore the fact that you're using multithreading.</p>

<p>But, ultimately, Jean-Paul's comment is correct; you are going to need to make some changes to the way this code works, if you want to change the way it works.</p>

