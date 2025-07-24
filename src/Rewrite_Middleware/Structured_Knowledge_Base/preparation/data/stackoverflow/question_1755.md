# Can NoSql be used for reporting in this situation?
[Link to question](https://stackoverflow.com/questions/6420970/can-nosql-be-used-for-reporting-in-this-situation)
**Creation Date:** 1308635972
**Score:** 4
**Tags:** sql, architecture, nosql, design-consideration
## Question Body
<h2>The Situation</h2>

<p>I am considering building a NoSQL-based application as an alternative to an existing Excel based financial risk management reporting tool. In short, my question revolves around the suitability of using NoSQL considering the following</p>

<ol>
<li>The main source data(csv files) comes from another application and are actually reports of current transactions and associated valuation calculations based on market movements. This is a fixed source and will not change. Reports row counts can range from a meagre 1,5k rows to over 65k rows. Not really massive amounts of data but this is on a fairly linear rate of increase. There are several other supporting data sources.</li>
<li>The report formats are fairly consistent, however the report content can be dynamic. i.e. most reports allows for business to decide what additional columnar data they would like see based on the business requirement. </li>
<li>Reporting as it occurs at the moment involves splicing and dicing the above reports; in this case think pivots, graphs, aggregations, additional calculations etc. There some complex stuff here which I don't know much about. </li>
<li>This is not a transactional system but rather a risk management system, so there is an assumed and expected time delay with the source data being used. It will primarily be read-heavy.</li>
<li>Reporting typically is only relevant for the current day (most important) and a history of previous runs needs to be maintained for every change in the source data (listed in #1) for further analysis.</li>
<li>This is no simple application, but my feeling is that Excel is not scaling well enough and fast enough (six months ago this was the dream come true and it was). There are too many hidden business rules that are known to a few and going through this exercise/rewrite will force all of this surface. We have too many <a href="http://en.wikipedia.org/wiki/Bus_factor" rel="nofollow">bus-factors</a> from a business and development perspective.</li>
<li>The solution overall needs to cater for dynamic reporting or rather dynamic presentation of the data. When compared to Excel, I think that speed is not really an issue (I'm assuming my solution will be faster) - however if truly dynamic queries were to be used, they need to complete in a reasonable time (&lt;1 minute).</li>
</ol>

<h2>Why I considered using NoSQL?</h2>

<p>Firstly, I'm a complete noob when it comes to NoSQL so my current understanding may be under-developed.I have tinkered and played around with NoSQL a bit but nothing to the scale of what I'm currently considering. </p>

<p>The main reason I considered NoSQL was due the source data. While the actual format(csv files) is irrelevant, the dynamic nature of the data in terms of dynamic columns may me think the a SQL-base approach would be severely restricted and inflexible since table structures are pretty static. NoSQL documents however would be able handle this. </p>

<p>The second reason, is that changes to data formats need to catered for on the fly, on a day-to-day basis. Using a SQL based solution, forces us to conform to enterprise level change management processes (for changes to a SQL database) which are laborious and painstakingly cumbersome. So I guess, my objective here is to have enough flexilbilty in my application and solution to bypass the bureaucracy of it all. (<em>If you intend commenting about the wonders and benefits of enterprise change management, don't!</em>)</p>

<p>The last reason, and somewhat selfish, I want to try something different.</p>

<p>I fully concede that I have not thought about this in full detail, thus the reason for my question since I know I am missing some very relevant aspects for consideration. If a SQL based solution is more appropriate, can you elaborate based on the 6 listed points.</p>

<p>Right now, this is still in a very exploratory phase - I need to get all my ducks in a row before I even considered proposing this type of solution.</p>

## Answers
### Answer ID: 6433877
<p>The key question is how the reports will be defined. </p>

<p>If reports are all custom code and you can reasonably set up a new custom index or map reduce query to get a simple table of data for the report then it may make sense to use NoSQL. </p>

<p>If you need reports to be defined or configured by end users you really have no reasonable option other than excel or a SQL based reporting tool.</p>

<p>You also need to consider how the dynamic columns will be used - schemaless stores work well for columns that only need to be displayed after you find a record, but not so well for queries. With SQL, all columns are queryable. A lot of NoSQL systems get their performance improvements by knowing that most columns will never be included in a query.</p>

