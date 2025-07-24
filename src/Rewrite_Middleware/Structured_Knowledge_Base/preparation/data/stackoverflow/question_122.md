# web.config MS Access query
[Link to question](https://stackoverflow.com/questions/13692641/web-config-ms-access-query)
**Creation Date:** 1354572510
**Score:** 1
**Tags:** coldfusion, web-config
## Question Body
<p>I want to do automated rewrites for my product pages in web.config. 
So something like this "itemdetail.cfm?ProductID=4399" becomes "products/Ipad_3". I got this to work</p>

<pre><code>&lt;?xml version="1.0"?&gt;
  &lt;configuration&gt; 
    &lt;system.webServer&gt;     
      &lt;rewrite&gt; 
        &lt;rules&gt; 
          &lt;rule name="Rewrite for Products" stopProcessing="true"&gt; 
            &lt;match url="products/(.+)" /&gt; 
            &lt;action type="Rewrite" url="itemdetail.cfm?ProductID={Products:{R:1}}" /&gt; 
          &lt;/rule&gt; 
        &lt;/rules&gt; 
        &lt;rewriteMaps&gt; 
          &lt;rewriteMap name="Products"&gt; 
            &lt;add key="Ipad_3" value="4399" /&gt; 
          &lt;/rewriteMap&gt; 
        &lt;/rewriteMaps&gt; 
      &lt;/rewrite&gt;
    &lt;/system.webServer&gt; 
  &lt;/configuration&gt; 
</code></pre>

<p>How can I modify code in web.config to have it get "title" from MS Access database using "ProductID"? If it was coldfusion the query would be something like this</p>

<pre><code>&lt;cfquery name="GetData" datasource="myaccessdns"&gt;
  SELECT Title 
  FROM   Products  
  WHERE  ProductID = #ProductID#
&lt;/cfquery&gt;
</code></pre>

## Answers
### Answer ID: 13715026
<p>Yup so as I mentioned you've got the right idea, you just need ColdFusion to generate the rewriteMap in the web.config periodically (or tie it to re-generate everytime the product title is changed or a new product is added/deleted)</p>

<p>generateRewriteMap.cfm</p>

<pre><code>&lt;cfquery name="AllProducts" datasource="#request.dsn#"&gt;
     select ProductID, URLTitle
     from Products
&lt;/cfquery&gt;

&lt;cfsavecontent variable="WebConfigFileData"&gt;&lt;?xml version="1.0"?&gt;
  &lt;configuration&gt; 
    &lt;system.webServer&gt;     
      &lt;rewrite&gt; 
        &lt;rules&gt; 
          &lt;rule name="Rewrite for Products" stopProcessing="true"&gt; 
            &lt;match url="products/(.+)" /&gt; 
            &lt;action type="Rewrite" url="itemdetail.cfm?ProductID={Products:{R:1}}" /&gt; 
          &lt;/rule&gt; 
        &lt;/rules&gt; 
        &lt;rewriteMaps&gt; 
          &lt;rewriteMap name="Products"&gt;
            &lt;cfoutput query="allProducts"&gt;&lt;add key="#URLTitle#" value="#ProductID#" /&gt;
            &lt;/cfoutput&gt;
          &lt;/rewriteMap&gt; 
        &lt;/rewriteMaps&gt; 
      &lt;/rewrite&gt;
    &lt;/system.webServer&gt; 
  &lt;/configuration&gt;&lt;/cfsavecontent&gt;

&lt;!--- Backup the Original Web.Config ---&gt;
&lt;cffile
  action = "copy"
  source = "c:/inetpub/wwwroot/mysite/web.config"
  destination = "c:/inetpub/wwwroot/mysite/web.config.#getTickCount()#"&gt;

&lt;cffile
  action = "write"
  file = "c:/inetpub/wwwroot/mysite/web.config"
  output = "#WebConfigFileData#"&gt;
</code></pre>

<p>The other way I do it is convert /products.index.cfm to search for title after /products/This_Products_Title parse out everything past /products/ and then do a database search for the title of the product and pull up the appropriate page.  Anything not found, returns the user to the homepage. This does require that you change all your links in your application to use the FriendlyURLTitle.</p>

### Answer ID: 13697129
<p>I think you want to use <a href="http://msdn.microsoft.com/en-us/library/ms228302%28v=vs.100%29.aspx" rel="nofollow">urlMappings</a>. </p>

<p>You can use it to map a request for <code>/products/Ipad_3</code> to <code>/itemdetail.cfm?ProductID=4399</code> (which could even originate from a rewritten request using the code that you posted). </p>

<p>This is a decent guide to urlMappings: <a href="https://web.archive.org/web/20201205222807/https://www.4guysfromrolla.com/articles/011007-1.aspx" rel="nofollow">A Look at ASP.NET 2.0's URL Mapping</a></p>

<p>(Note: you can't use web.config to directly query a database)</p>

