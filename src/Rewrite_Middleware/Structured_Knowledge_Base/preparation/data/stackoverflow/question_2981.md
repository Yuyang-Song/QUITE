# SSE vs WebSockets vs none of them
[Link to question](https://stackoverflow.com/questions/61047053/sse-vs-websockets-vs-none-of-them)
**Creation Date:** 1586109579
**Score:** 0
**Tags:** php, websocket, server-sent-events
## Question Body
<p>I was hired by a customer to refactor a webapp written in php (for which I have very few documentation) and then add some features .
Consulting the code I found out that this webapp use SSE for random notification and websockets for internal chat (using Ratchet php library). </p>

<p>Reading the code I discover that SSE was implemented in early stage then, they decide to use websockets when chat feature was required from the customer.
Is seems everything runs well enough but customer ask if it is possible to tweak for better performance (unfortunately rewriting everything from scratch is not an option).</p>

<p>I saw a lot of php processes running (apache and mpm_event) so I dive into SSE e websocket implementation and I discover that the VPS that host the webapp is behind a firewall who locked connection time to 120 secs max. So SSE php scripts will be killed soon after client request and then reactivated by reply 5000 stream command (acting like a standard pooling...).
In websockets side I saw that js clients needs to check and re-establish connections frequently for the same reasons. </p>

<p>I think that it is not useful using both SSE and webSockets so I must decide which one is the best to accomplish the various tasks. Websockets is my preferring choice because even reconneting every 120 sec they must be lighter than SSE (implemented like ajax pooling).
I know, there's a lot of things to look at before this (database query, assets loading...), but I know how to handle them.
Any advice?
Thank you in advance</p>

