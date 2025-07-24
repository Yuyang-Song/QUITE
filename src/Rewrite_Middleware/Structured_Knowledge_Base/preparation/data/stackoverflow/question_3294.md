# How to decompose a monolith into microservices by business capability?
[Link to question](https://stackoverflow.com/questions/75277066/how-to-decompose-a-monolith-into-microservices-by-business-capability)
**Creation Date:** 1675014475
**Score:** 0
**Tags:** microservices, system-design
## Question Body
<p>I have a monolith application that uses one database, and in my company, we decide to rewrite the application and use microservices in the backend.</p>
<p>At this time, we decided NOT to split the database because other applications and processes are using it, and it takes two years to change.</p>
<p>The difficulty in the process is to decompose and identify the right microservices.</p>
<p>I'll try to explain our system by start describing the UI. Please read carefully because I am trying to explain it in detail.</p>
<p>The system displays the stock market data. <strong>The Company or Fund or Fund manager</strong> in the market is posting everyday reports about the company's activities like status, information for investors, and more.</p>
<p><strong>&quot;breaking announcement&quot; page</strong>
displays a list of today's priority reports. Each row contains the subject from the pdf document (the report) that the company is publishing and the company that belongs to the report:</p>
<p><a href="https://i.sstatic.net/p8sUM.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/p8sUM.png" alt="enter image description here" /></a></p>
<p>When the user clicks on the row, we redirect to &quot;report page&quot; and which contains the report details:</p>
<p><a href="https://i.sstatic.net/fSOzy.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/fSOzy.png" alt="enter image description here" /></a></p>
<p>In the database, we have entities such <code>report</code>, <code>company</code>, <code>company_report</code>, <code>event</code>, <code>public_offers</code>, <code>upcoming_offering</code>, and more.</p>
<p>So to get the list, we run an inner join query like this:</p>
<pre><code>Select ... From report r inner join
company_report cr on r.reportid=cr.reportid
inner join company c on cr.company_cd=c.company_cd
Where ....
</code></pre>
<p>Most of our server endpoints are not changing anything but are only used to retrieve the data.</p>
<p>So I'll create this endpoint <code>/reports/breaking-announcement</code> to get the list, and it returns an object like that:</p>
<pre><code>[{ reportId, subject, createAt, updateAt, pdfUrl, company: { id, name } }]
</code></pre>
<p><strong>today's companies report page</strong> acts like &quot;breaking announcement&quot; page. but the page displays all the reports from today (not necessarily with priority).</p>
<p><em>disclosures are reports</em></p>
<p><a href="https://i.sstatic.net/iKB0H.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/iKB0H.png" alt="enter image description here" /></a></p>
<p>On this page, we also have a search to get all reports by cretiria for example to get reports by company name. to do that we have autocomplete so the user types the company name or id.</p>
<p>In other to do that we think it should be API endpoint <code>/companies/by-autocomplete</code> and the response will <code>[{ companyId, companyName, isCompany }]</code>.</p>
<p><strong>eft page</strong> same as before, but this time we display the Funds report's (not a companys reports).
The list contained the fund name and the subject of the report. each click on the row leads to the report detail page (same page).</p>
<p>On this page we have a search by criteria such date-from date-to, name or id of the funds by autocomplete. and endpoint (<code>/funds/by-autocomplete</code> returns <code>[{ fundId, fundName, ...}]</code>).</p>
<p><strong>foreign etf page</strong> same as before, list of items. each item is like before:</p>
<pre><code>&lt;fund name&gt;
&lt;subject of the report&gt;
</code></pre>
<p>The query is different.</p>
<hr />
<p>Okay, this was a very long description. thank you for reading.</p>
<p>Now I want to detect what are the microservices for this application.</p>
<p>I endup with:</p>
<ul>
<li><p>Report microservice - responsible for getting and handling all the reports in the system.
which have a endpoints like getall, getbyid, get like getbreakingannouncement, getcompanytodayreports, getfunds, getforeignfunds. the report microservice will make a request to company or funds microservice to join the data from the company and build to the response.</p>
</li>
<li><p>company microservice:
handle all companies data. I mean endpoints such <code>getall</code>, <code>getByIds</code> (for report service), <code>getByAutocomplete</code>.</p>
</li>
<li><p>funds microservice:
handle all funds data. I mean endpoints such <code>getall</code>, <code>getByIds</code> (for report service), <code>getByAutocomplete</code>.</p>
</li>
</ul>
<p>There are other services, such as a notification service or email service. but those are not business services. I want to split up my business logic into microservices in order to deploy and maintain them easily.</p>
<hr />
<p>I'm not sure I decomposing right. maybe I do. but is fit the microservice ideas? it's fit the <a href="https://microservices.io/patterns/decomposition/decompose-by-business-capability.html" rel="nofollow noreferrer">Pattern: Decompose by business capability
</a>? if not what are the business capability in my system?</p>

## Answers
### Answer ID: 75282504
<blockquote>
<p>At this time, we decided NOT to split the database because other applications and processes are using it, and it takes two years to change.</p>
</blockquote>
<p>I'll try to stop you right here. In general case shared database is a huge antipattern in microservices architecture and should be avoided as much as possible. There are multiple problems here - less transparent dependencies between services which can cause high coupling with all the consequences in development and deployment, increasing chance to eventually end up with distributed monolith instead of microservices, etc.</p>
<p>Other applications and processes using it should not stop you from moving away from it - there are things which allow to mitigate that - you just sync data between services and &quot;legacy&quot; database (asynchronously using basically the same approaches like you will use in your microservices - for example <a href="https://microservices.io/patterns/data/transaction-log-tailing.html" rel="nofollow noreferrer">transaction log tailing</a> for example using something like <a href="https://debezium.io/" rel="nofollow noreferrer">debezium</a>). It have it's own costs but I would argue that it is usually better to pay them upfront then have to pay bigger percentages on the tech debt.</p>
<blockquote>
<p>I endup with: ....</p>
</blockquote>
<p>I would argue that this split looks more like <a href="https://microservices.io/patterns/decomposition/decompose-by-subdomain.html" rel="nofollow noreferrer">decomposition by subdomain</a> then by business capability. Which is actually can be quite fine and suits microservices architecture also.</p>
<p>Based on your description I see at least the following business capabilities in your system that can be defined:</p>
<ul>
<li>View (manage?) breaking announcements</li>
<li>View (manage?) reports</li>
<li>Search (reports?)</li>
</ul>
<p>Potentially &quot;today's reports&quot; and &quot;Funds reports&quot; can be considered as separate business capabilities.</p>
<blockquote>
<p>I want to split up my business logic into microservices in order to deploy and maintain them easily.</p>
</blockquote>
<p>Then again - I highly recommend to reconsider not moving away from shared database.</p>
<blockquote>
<p>I'm not sure I decomposing right</p>
</blockquote>
<p>Without whole overview of the system including amount of data, data flows, resources available for development and competences in the teams, amount of incoming new business requirements, potential vectors of change, etc. it is hard to actually tell.</p>
<p>P.S.</p>
<p>Note that despite the microservices architecture having a lot of popularity it is not always a right solution for a concrete project to go full-blown microservices. If you have quite small team and/or do not handle high loads/large amount of data with various access patterns then potentially you do not need microservices. You still can leverage a lot of approaches used in the microservices architecture though.</p>

### Answer ID: 75283174
<p>I don't think a query-oriented decomposition of your current application monolith will lead to a good microservice (MS) design. Two of your proposed microserivces have the same end-point query API which suggests to me that you are viewing your first-generation microservices as just entity-servers.</p>
<p>Your idea to perform joins on cross MS query operations indicates these first gen &quot;microservices&quot; are closely coupled and hence fall short of a genuine MS architecture.</p>
<p>One technique to verify an MS design is to ask yourself, &quot;how would the whole system cope if one MS is unavailable for 3 minutes?&quot;. Solving that design challenge leads down a path towards decoupled message-base interactions between  the microservices. And this in turn leads to interactions between Microservices being expressed as business operations where one MS raises messages that trigger a mutation in the state of another MS.</p>
<p>Maybe you should reduce the scope of your MS ambitions and instead look at Schema Stitching in GraphQL. Reading between the lines of your question I think a more realistic first step towards a distributed system would be to create specialised query services with a GraphQL endpoint.</p>

