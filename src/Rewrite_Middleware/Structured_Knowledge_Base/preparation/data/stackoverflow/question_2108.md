# PHP CLI with NodeJs
[Link to question](https://stackoverflow.com/questions/19248528/php-cli-with-nodejs)
**Creation Date:** 1381237587
**Score:** 0
**Tags:** php, node.js, apache
## Question Body
<p>I have a php application [mostly REST] which runs on top of Apache in a Linux Virtual Machine. This application does a lot of Data queries and i have started having performance issues. </p>

<p>To me one way to address this is using NodeJs Async Patterns. I also plan to implement websockets. But the problem is code size in php is very large. It will take months to rewrite in Node. </p>

<p>Is there a middle ground to complete rewrite. Where i can handle interaction with browser in Node and interaction with database in php cli. and Node can call php cli with approximating Apache environment? </p>

<p>I am using Slim PHP Framework for the REST API, Both HTTP Basic Auth and PHP Sessions, $_GET and variables for extra filters on GET requests. I dont know much about internal workings of Slim. But i think it depends on Apache-PHP implementation of HTTP requests and responses. </p>

<p>How to send the message body [post, put] to the php cli which is in 99% cases JSON (I have file uploads too but which can be ignored as of now). i can have php cli put the json output in STDOUT and parse from there.</p>

<p>The real problem is how to remove dependency on php apache SAPI without changing much of the codebase and how to integrate it with Node. is there any tools, lib which can help in this case.</p>

<p>One more side question, can NGinx help me here somehow?</p>

<p>**Note - My knowledge of node is limited to few fun scripts and custom linting, template compiling, testing scripts for browser side code.</p>

## Answers
### Answer ID: 19389240
<p>First you could put nginx in front of Apache. This will allow you to slowly transition your actions to node by routing selectively to one or the other.</p>

<p>Alternatively you could put node in front and use <a href="https://github.com/nodejitsu/node-http-proxy" rel="nofollow">node-http-proxy</a> with express (for exemple) to proxy selectively to Apache. I haven't tried it myself but I guess it should work.</p>

<p>You could also/or use <a href="https://github.com/substack/dnode" rel="nofollow">dnode</a> to call php functions from node. <a href="http://zeromq.org/" rel="nofollow">zeromq</a> is an option, too.</p>

