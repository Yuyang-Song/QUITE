# Which of the following data structures is scalable in elasticsearch?
[Link to question](https://stackoverflow.com/questions/32087468/which-of-the-following-data-structures-is-scalable-in-elasticsearch)
**Creation Date:** 1439963513
**Score:** 0
**Tags:** elasticsearch
## Question Body
<p>I want to build an event analytics system, where I can record and query events that a user has done, for example on a website.</p>

<p>My naive idea of the data model was simply a collection of event documents, each event including the userid, event type, and so on. So I thought something like this:</p>

<pre><code>{ userid: Joe, event: homepage }
{ userid: Mike, event: homepage }
{ userid: Joe, event: productsPage }
{ userId: Joe, event: accountSettings }
{ userId: Joe, event: checkout }
etc
</code></pre>

<p>But now I'm struggling to figure out how to do some of the queries I'm most likely to be able to want to do.</p>

<p>For example, I want to say "Give me a list of all users who have visited the homepage AND the products page AND the checkout page"</p>

<p>Seems to me I would need to use my application code to do this, rather than elasticsearch? And I would need to do something like:</p>

<pre><code>Step 1: select all users who have done 'homepage'
Step 2: select all users who have done 'products page'
Step 3: select all users who have done 'checkout page'
Step 4: build a list of only those users who appear in all 3 lists.
</code></pre>

<p>If I have a userbase of 20 million users, I risk bringing huge lists of data into my application?</p>

<p>An alternative would be to have one document per user, so that Joe looks like</p>

<p>{ userid: Joe, event: [ homepage, productsPage, accountSettings, checkout ] }</p>

<p>and so on.</p>

<p>But then that would involve updating this document every time the user did something. Since elasticsearch writes a new record rather than updating in place, that would involve a horrendous amount of rewriting, given that each user might do say 5000 events in a year, and spread across different days. Not to mention rewriting of the index?</p>

<p>Is there an idiomatic way I'm missing of accomplishing a database by user that can handle regular updates to each user, and buid indexes that allow for fast querying of that data by multiple criteria - eg users who have done eventA AND eventB AND eventC?</p>

<p>Many thanks for all your help!</p>

## Answers
### Answer ID: 32088638
<p>You can use Kibana for Visualizing Data stored in Elasticsearch.</p>

<blockquote>
  <p>You can use this type of events itself:-</p>
</blockquote>

<pre><code>{ userid: Joe, event: homepage }
{ userid: Mike, event: homepage }
{ userid: Joe, event: productsPage }
{ userId: Joe, event: accountSettings }
{ userId: Joe, event: checkout }
etc
</code></pre>

<p>After storing your data in Elasticsearch, You can use Kibana and create visualizations specifying AND Filters over the event field.</p>

