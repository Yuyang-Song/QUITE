# How to optimize the Lemoon content from ContentService?
[Link to question](https://stackoverflow.com/questions/25936778/how-to-optimize-the-lemoon-content-from-contentservice)
**Creation Date:** 1411138444
**Score:** 0
**Tags:** optimization, lemoon
## Question Body
<p>I am doing maintenance work for a company which uses Lemoon for its pages and content. The customer noticed that their website is running very slowly and I suspect that their data is being retrieved inefficiently from the database. Looking at their code in Visual Studio, it seems like the site is grabbing data from ContentService many times through "Get" methods while loading each page.</p>

<p>I'm wondering what would be the correct way to make their site load faster. Does the ContentService object query the database each time a Get method is used? Or does it retrieve the data once and store it in memory? I am considering rewriting the code so that fewer "Get" methods are used, but I don't know what effect this will have on page load time. I've looked for documentation regarding ContentService on Lemoon's website but did not find any answers there.</p>

## Answers
### Answer ID: 25959175
<p>In general Lemoon is highly optimized and almost always returns data from the in-memory cache instead of querying the database. This is true for ContentService, UserService, SiteService, SettingService etc. The exception to the rule is all Search methods that go directly to the database. But as long as you only use Get methods you can count on the result coming from the cache. </p>

<p>If you still suspect that database access in an issue, I would recommend you set up a profiling session against the database to find slow and/or frequent queries. </p>

