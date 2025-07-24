# Alfresco 5.0 transactional queries
[Link to question](https://stackoverflow.com/questions/33282392/alfresco-5-0-transactional-queries)
**Creation Date:** 1445521089
**Score:** 0
**Tags:** solr, alfresco, transactional
## Question Body
<p>I have some questions about how index in Alfresco One works with transactional queries.</p>

<ol>
<li>We use Alfresco 5.0.2 and in documentation I can read this: "When you are upgrading the database, you can add optional indexes in order to support the metadata query feature."</li>
</ol>

<p>Suppose that in my model.xml I add a custom property like this:</p>

<pre><code> &lt;type name="doc:myDoc"&gt;
 &lt;title&gt;Document&lt;/title&gt;
 &lt;parent&gt;cm:content&lt;/parent&gt;
 &lt;properties&gt;
   &lt;property name="doc:level"&gt;     
     &lt;title&gt;Level&lt;/title&gt;                                                                    
     &lt;type&gt;d:text&lt;/type&gt;
     &lt;mandatory&gt;true&lt;/mandatory&gt;
     &lt;index enabled="true"&gt;
        &lt;atomic&gt;true&lt;/atomic&gt;
        &lt;stored&gt;false&lt;/stored&gt;
        &lt;tokenised&gt;both&lt;/tokenised&gt;
     &lt;/index&gt;
   &lt;/property&gt;
   ...    
  &lt;/properties&gt;
&lt;/type&gt;                
</code></pre>

<p>And I have on my alfresco-global.properties these sets</p>

<pre><code>solr.query.cmis.queryConsistency=TRANSACTIONAL_IF_POSSIBLE
solr.query.fts.queryConsistency=TRANSACTIONAL_IF_POSSIBLE
system.metadata-query-indexes.ignored=false  
</code></pre>

<p>My first question is... How Alfresco knows which properties I want to index on DB? Read my model.xml and index only the indexed properties that I specify there? Index all the custom properties? Or I need to create a script to add these new indexes?</p>

<p>I read the script metadata-query-indexes.sql but I don't understand how rewrite it in order to add a new index for my property. If it's necessary this script, could you give me an example with the doc:myDoc property that I wrote before, please?</p>

<ol start="2">
<li>Another question is about query syntax that isn't supported by DB and goes directly to SOLR. </li>
</ol>

<p>I read that PATH, SITE, ANCESTOR, OR, any d:content, d:boolean or d:any (among others) properties in your query or it will not be executable against the DB. But I don't understand what d:content is exactly.</p>

<p>For example, a query (based on my custom property written before) like TYPE:whatever AND @doc\:level:"value" is considered d:content? This query is supported by BD or goes to SOLR? </p>

<ol start="3">
<li>I read also this: </li>
</ol>

<p>"Any property checks must be expressed in a form that means "identical value check" as querying the DB does not provide the same tokenization / similarity capabilities as the SOLR index. E.g. instead of my:property:"value" you'd have to use =my:property:"value" and "value" must be written in the proper case the value is stored in the DB."   </p>

<p>This means that if I use the =, for example doing =@doc\:level:"value", this query isn't accepted on DB and goes to SOLR? I can't search for an exact value on DB?</p>

## Answers
### Answer ID: 44735190
<p>A nice explanation can be found here.</p>

<p><a href="https://community.alfresco.com/people/andy1/blog/2017/06/19/explaining-eventual-consistency" rel="nofollow noreferrer">https://community.alfresco.com/people/andy1/blog/2017/06/19/explaining-eventual-consistency</a></p>

<blockquote>
  <p>When changes are made to the repository they are picked up by SOLR via
  a polling mechanism. The required updates are made to the Index Engine
  to keep the two in sync. This takes some time. The Index Engine may
  well be in a state that reflects some previous version of the
  repository. It will eventually catch up and be consistent with the
  repository - assuming it is not forever changing.</p>
</blockquote>

### Answer ID: 33870810
<p>I've been researching TMQs recently. I'm assuming that you need transactionality, which is why TMQ queries are interesting. Queries via SOLR are eventually consistent, but TMQs will immediately return the change. There are certain applications where eventual consistency is a huge problem, so I'm assuming this is why you are looking into them.</p>

<p>Alfresco says that they use TMQs by default, and in my limited testing (200k documents), I found no appreciable performance difference between a solr and TMQ query. I can't imagine they are horrible for performance if Alfresco set it up to be the default style, but I need to do further testing with millions of documents to be sure. It will of course depend on your database load. If your database is a bottleneck and you don't need the transactionality, you could consider using @ syntax in metadata searches to avoid them, or you could disable them via properties configuration.</p>

<p>1) How Alfresco knows which properties I want to index on DB? Read my model.xml and index only the indexed properties that I specify there? Index all the custom properties? Or I need to create a script to add these new indexes?</p>

<p>When you execute a query using a syntax that is compatible with a TMQ, Alfresco will do so. The default behavior is "TRANSACTIONAL_IF_POSSIBLE":
<a href="http://docs.alfresco.com/4.2/concepts/intrans-metadata-configure.html" rel="nofollow">http://docs.alfresco.com/4.2/concepts/intrans-metadata-configure.html</a></p>

<p>You do not have to have the field marked as indexable in the model for this to work. This is unclear from the documentation but I've tried disabling indexing for the field in the model and these queries still work. You don't even have to have solr running!</p>

<p>2) Another question is about query syntax that isn't supported by DB and goes directly to SOLR.</p>

<p>Your example of TYPE and an attribute does not go to solr. It's things like PATH that must go to SOLR. </p>

<p>3) "Any property checks must be expressed in a form that means "identical value check" as querying the DB does not provide the same tokenization / similarity capabilities as the SOLR index. E.g. instead of my:property:"value" you'd have to use =my:property:"value" and "value" must be written in the proper case the value is stored in the DB."</p>

<p>What they are saying is that you must use the = operator, not the default or @ operator. The @ operator depends on tokenization, but TMQs go straight to the database. However, you can use * in an attribute if you omit the "", like so:</p>

<p>=cm:\title:Startswith*</p>

<p>Works for me on 5.0.2 vía TMQ. You can absolutely search for an exact value as well however.</p>

<p>I hope this cleared it up for you. I highly recommend putting the solr.query.fts.queryConsistency=TRANSACTIONAL to force TMQs always in a test evironment and testing different queries if you still have questions about what syntax is supported.</p>

<p>Regards</p>

