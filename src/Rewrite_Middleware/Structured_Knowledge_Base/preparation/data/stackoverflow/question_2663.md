# How to build a desktop app from a web app whilst being able to capture the communication with the server?
[Link to question](https://stackoverflow.com/questions/45616575/how-to-build-a-desktop-app-from-a-web-app-whilst-being-able-to-capture-the-commu)
**Creation Date:** 1502375457
**Score:** 1
**Tags:** qt, web-applications, electron, desktop-application, server-communication
## Question Body
<p>I'm trying to transform a web application to a desktop one without rewriting the code. Two solutions I found that seem promising are Qt with WebEngine (WebView) and Electron. The thing is I would like to be able to capture the communication with server, for example database queries and stuff like that and treat it locally. Is that possible using either of that tools? If so do you have any tips on how to go about the issue?</p>

<p>Thanks in advance.</p>

## Answers
### Answer ID: 46096618
<p>Just for future reference I decided on <code>Electron</code> and used <code>onBeforeRequest</code> function to capture the http requests.</p>

### Answer ID: 45616823
<p>If you don't have enough time to build a desktop app, I recommend to build hybrid app. (Native App + Web). Use <strong><em>Cache</em></strong>, I am not sure about <strong><em>Web Database</em></strong>.</p>

<p>you can read these..</p>

<p><a href="https://en.wikipedia.org/wiki/Web_cache" rel="nofollow noreferrer">Web Cache</a></p>

<p><a href="https://en.wikipedia.org/wiki/Web_SQL_Database" rel="nofollow noreferrer">Web DB</a> (it works on browser like Chrome, Safari, Android Browser...)</p>

