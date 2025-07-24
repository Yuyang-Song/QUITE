# Is It Possible To Perform A SQL Database Query As Part Of A WebConfig URL Rewrite Rule?
[Link to question](https://stackoverflow.com/questions/43015860/is-it-possible-to-perform-a-sql-database-query-as-part-of-a-webconfig-url-rewrit)
**Creation Date:** 1490441784
**Score:** 0
**Tags:** .htaccess, azure, url-rewriting, web-config, azure-web-app-service
## Question Body
<p>I'm currently in the process of migrating a PHP website from LAMP Hosting to Microsoft Azure Web Apps Hosting.</p>

<p>The site being migrated uses HTAccess for URL Rewriting purposes; however from what I can tell, Azure does not support the use of HTAccess files (please correct me if I am wrong in this) - instead, it appears that I must use IIS WebConfig for this purposes (a technology that I am not overly familiar with).</p>

<p>Assuming that I have to rewrite the file from HTAccess to WebConfig, the HTAccess file to be rewritten uses Mod_Rewrite and external Rewrite Maps as part of the URL rewriting process. The HTAccess Rewrite Map performs a Database Query as part of this process whereby a URL such as <em>www.example.com/category/music</em> is inputted and then re-written to <em>www.example.com/category.php?catID=1</em>, i.e. <em>the ID associated with each category name is identified via a Database query</em>.</p>

<p>I've familiarised myself with the basics of Web Config and IIS Rewrite Maps thus far; however I have only encountered tutorials outlining <a href="https://www.iis.net/learn/extensions/url-rewrite-module/using-rewrite-maps-in-url-rewrite-module" rel="nofollow noreferrer">static rewrite rules</a>.</p>

<p>Is it possible to perform database queries using IIS Config - similar to the HT Access scenario outlined above?</p>

<p>If so, can someone please point me in the direction of some tutorials dealing with the topic or provide some sample code.</p>

<p>Any help is much appreciated.</p>

## Answers
### Answer ID: 43075783
<p>Not sure if that article answers your question but the right way would be using IIS manager on a windows machine to convert from mod rewite rules to urlrewrite config as detailed in <a href="https://www.iis.net/learn/extensions/url-rewrite-module/importing-apache-modrewrite-rules" rel="nofollow noreferrer">https://www.iis.net/learn/extensions/url-rewrite-module/importing-apache-modrewrite-rules</a></p>

### Answer ID: 43029612
<p>Found a tutorial that deals this topic <a href="https://www.iis.net/learn/extensions/url-rewrite-module/using-custom-rewrite-providers-with-url-rewrite-module" rel="nofollow noreferrer">here</a>.</p>

