# How to Expose SQL Server Hosted on Intranet to Connect Remotely
[Link to question](https://stackoverflow.com/questions/47962583/how-to-expose-sql-server-hosted-on-intranet-to-connect-remotely)
**Creation Date:** 1514135808
**Score:** 1
**Tags:** sql-server, iis, url-rewriting, tedious
## Question Body
<p>I am trying to remote connect to a SQL Server that is hosted on a company intranet.  Ultimately, I would like to connect in with something like tedious and get the data into a web application via a REST API.</p>

<p>I followed this tutorial: <a href="https://blogs.msdn.microsoft.com/friis/2016/08/25/setup-iis-with-url-rewrite-as-a-reverse-proxy-for-real-world-apps/" rel="nofollow noreferrer">https://blogs.msdn.microsoft.com/friis/2016/08/25/setup-iis-with-url-rewrite-as-a-reverse-proxy-for-real-world-apps/</a></p>

<ol>
<li>Entered the <code>client_net_address:1433</code> for the inbound rule.</li>
<li>Disabled SSL Offloading</li>
<li>Entered the public facing IP of the server in the outbound <code>To:</code> field but changed the last digits. e.g. xxx.xxx.xxx.100</li>
</ol>

<p>When I try logging in with tedious I get a connection timeout error using the following config:</p>

<pre><code>let config = {
  userName: "**",
  password: "**",
  server: "xxx.xxx.xxx.100",
  options:{
    port: 1433,
    database: "db_name",
    encrypt: true
  }
}
</code></pre>

<p>What steps must I take to connect remotely to a SQL database hosted on an intranet?</p>

<p>Currently I VPN in and can query from SQL Server 2014 Management Studio.</p>

## Answers
### Answer ID: 48035339
<p>This feature is working for node module mssql version 3.3.0 and SQL Server 2008.</p>

<p>Use <code>npm install mssql@3.3.0</code> and connectivity should work properly.</p>

<p>Version 4 of the mssql module has breaking changes.</p>

