# wildcard searches on specific elements only
[Link to question](https://stackoverflow.com/questions/37451242/wildcard-searches-on-specific-elements-only)
**Creation Date:** 1464234560
**Score:** 3
**Tags:** search, wildcard, marklogic, marklogic-8
## Question Body
<p>I am looking for a way to do wildcard search only on specific elements when executing a <code>search:search</code>.  Specifically, I might have documents that look like the following:</p>

<pre><code>&lt;pdbe:person-envelope xmlns:pdbe="http://schemas.abbvienet.com/people-db/envelope"&gt;
  &lt;person xmlns="http://schemas.abbvienet.com/people-db/model"&gt;
    &lt;costcenter&gt;
      &lt;code&gt;0000601775&lt;/code&gt;
      &lt;name&gt;DISC-PLAT INFORM&lt;/name&gt;
   &lt;/costcenter&gt;
    &lt;displayName&gt;Tj Tang&lt;/displayName&gt;
    &lt;upi&gt;10025613&lt;/upi&gt;
    &lt;firstName&gt;
      &lt;preferred&gt;TJ&lt;/preferred&gt;
      &lt;given&gt;Tze-John&lt;/given&gt;
   &lt;/firstName&gt;
    &lt;lastName&gt;
      &lt;preferred&gt;Tang&lt;/preferred&gt;
      &lt;given&gt;Tang&lt;/given&gt;
   &lt;/lastName&gt;
    &lt;title&gt;Principal Research Scientist&lt;/title&gt;
  &lt;/person&gt;
  &lt;pdbe:raw/&gt;
&lt;/pdbe:person-envelope&gt;
</code></pre>

<p>When searches happen, I want the search text to be automatically wildcarded, but only for certain elements like displayName, firstName, lastName, but NOT for upi or code.  As I understand it, I would have certain wildcard related indexes enabled in the database, but then I would need to have a custom query parser that rewrite the query into multiple <code>cts:element-query</code> and <code>cts:element-value-query</code> statements for each element that I want to wildcard search on, OR'd with the originally parsed search query.  Or I can create field constraints, and rewrite the query to use field contraints.</p>

<p>Is there another way to conditionally search using wildcard on some elements but not others, when the user is entering as simple search query?, i.e. partial first and last name, "TJ Tan", but no partial hits when I search "100256".</p>

## Answers
### Answer ID: 37452975
<p>You are on the right track.  Lets take an element (or maybe field) query on "TS Tan"</p>

<p>With <a href="https://docs.marklogic.com/cts:tokenize">cts:tokenize</a>, you can break this up (read about cs:tokenize - it is not just a normal tokenizer).</p>

<p>Then I have "TS" and "Tan"</p>

<p>You can the do things like apply business rules on which word should be wild-carded and which not and build the appropriate cts query (probably individual word queries in an and statement - or a near query - tuning depends on your need).</p>

<p>Now with search phrase tokenized, you can also consider that you may find building your results relies not on a wildcard index, but on a an element word lexicon - where you do your term-expansion with <a href="https://docs.marklogic.com/cts:element-word-match">word-matches</a> and those terms are then sent to the query.</p>

<p>We sometimes take that further and combine the query building with xdmp:estimate and make the query less restrictive if we don't get enough results early on.</p>

<p>Where to put this logic?
You mention search:search, so in this case, I would suggest you package this into a custom constraint.</p>

