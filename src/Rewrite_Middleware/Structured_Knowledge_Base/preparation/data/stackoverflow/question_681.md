# OrientDB: slow query, need help creating index to speed it up
[Link to question](https://stackoverflow.com/questions/36941717/orientdb-slow-query-need-help-creating-index-to-speed-it-up)
**Creation Date:** 1461942199
**Score:** 1
**Tags:** sql, indexing, orientdb
## Question Body
<p>I'm using an SQL query to retrieve money transactions from my OrientDB database (v2.1.16)</p>

<p>The query is running slowly and I'd like to know how to create the index that will speed it up.</p>

<p>The query is:</p>

<pre><code>SELECT timestamp, txId 
FROM MoneyTransaction
WHERE (
    out("MoneyTransactionAccount").in("AccountMoneyProfile")[accountId] = :accountId
    AND moneyType = :moneyType
    AND :registerType IN registerQuantities.keys()    
)    
ORDER BY timestamp DESC, @rid DESC
</code></pre>

<p>I also have another variant that resumes the list from a specific point in time:</p>

<pre><code>SELECT timestamp, txId 
FROM MoneyTransaction
WHERE (
    out("MoneyTransactionAccount").in("AccountMoneyProfile")[accountId] = :accountId
    AND moneyType = :moneyType
    AND :registerType IN registerQuantities.keys()    
)
AND timestamp &lt;= :cutoffTimestamp
AND txId NOT IN :cutoffTxIds

ORDER BY timestamp DESC, @rid DESC
</code></pre>

<p>The difficulty I have is trying to figure out how to create an index with the more complex fields, namely the accountId field which doesn't reside within the same vertex, and the registerType field which is to be found within an EMBEDDEDMAP field.</p>

<p>Which index would you create to speed up this query? Or how would you rewrite this query?</p>

<p>My structure is as follows:</p>

<pre><code>[Account] --&gt; (1 to 1) AccountMoneyProfile --&gt; [MoneyProfile]
[MoneyTransaction] --&gt; (n to 1) MoneyTransactionAccount --&gt; [MoneyProfile]
</code></pre>

<p>Important fields:</p>

<pre><code>Account.accountId STRING
MoneyTransaction.registerQuantities EMBEDDEDMAP
MoneyTransaction.timestamp DATETIME
</code></pre>

<p>The account I'm fetching right now has about 500 MoneyTransaction vertices attached to it.</p>

## Answers
### Answer ID: 37199443
<p>about the index choice, it depends by the amounts of your dataset:</p>

<ul>
<li>If the dataset isn't very large, you could use an <strong><code>SB-TREE</code></strong> index because they maintain sorting and allow range operations;</li>
<li>If the dataset instead is very large, you could use an <strong><code>HASH INDEX</code></strong> which is more functional on large numbers and consumes less resources than other indexes, but it doesn't support range operations.</li>
</ul>

<p>In your case you could create, for example, an <strong><code>SB-TREE UNIQUE INDEX</code></strong> on the <strong><code>accountId</code></strong> (e.g. <strong><code>Account.accountId</code></strong>) and rewrite your query in a way that the target query directly matches the index and so that it reads fewer records as possible. Example:</p>

<pre><code>SELECT timestamp, txId
FROM (
     SELECT expand(out("AccountMoneyProfile").in("MoneyTransactionAccount"))
     FROM Account
     WHERE accountId = :accountId
     )
WHERE moneyType = :moneyType AND :registerType IN registerQuantities.keys()
ORDER BY timestamp DESC, @rid DESC
</code></pre>

<p>In this way you directly select the <strong><code>Account</code></strong> records you're looking for (by using the index previously created) and then you can retrieve only the connected <strong><code>MoneyTransaction</code></strong> records.</p>

<p>You can find more detailed information about indexes in the <a href="http://orientdb.com/docs/2.1/Indexes.html" rel="nofollow noreferrer">OrientDB official documentation</a>.</p>

<p>Another way, based on the fact that you specified that <strong><code>MoneyProfile</code></strong> class doesn't contains important data (if I've understood well), could be to change the structure to make the search more direct. E.g.:</p>

<p><strong>Before:</strong></p>

<p><a href="https://i.sstatic.net/zk32s.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/zk32s.png" alt="enter image description here"></a></p>

<p><strong>After</strong> (I've previously created a new <strong><code>AccountMoneyTransaction</code></strong> edge class):</p>

<p><a href="https://i.sstatic.net/RgugU.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/RgugU.png" alt="enter image description here"></a></p>

<p>Hope to have been helpful</p>

