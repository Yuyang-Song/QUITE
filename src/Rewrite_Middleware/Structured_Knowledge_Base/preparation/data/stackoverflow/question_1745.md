# Does CakePHP finderQuery work with SQL Server? Where would I debug that?
[Link to question](https://stackoverflow.com/questions/6128630/does-cakephp-finderquery-work-with-sql-server-where-would-i-debug-that)
**Creation Date:** 1306345730
**Score:** 6
**Tags:** sql-server, cakephp
## Question Body
<p>I'm new to cakePHP, so I may be missing the obvious.</p>

<p>The system is running the latest download using Microsoft SQL Server 2005 as database.  I appreciate that is slightly unusual, but having fixed the URL rewrite I have seen no other issues.</p>

<p>I'd like use a custom finderQuery, but I cannot even seem to replace the default.  Specifically if I use</p>

<pre><code>    var $hasMany = array(
        'RecyclateTypeConversion' =&gt; array(
        'className' =&gt; 'RecyclateTypeConversion',
        'foreignKey' =&gt; 'recyclate_type_id',
        'dependent' =&gt; false,
        'conditions' =&gt; '',
        'fields' =&gt; '',
        'order' =&gt; '',
        'limit' =&gt; '',
        'offset' =&gt; '',
        'exclusive' =&gt; '',
        'finderQuery' =&gt; 'select RecyclateTypeConversion.* from recyclate_type_conversions AS RecyclateTypeConversion WHERE RecyclateTypeConversion.recyclate_type_id IN ({$__cakeID__$});',
        'counterQuery' =&gt; ''
    ),
     };
</code></pre>

<p>I see this error</p>

<blockquote>
  <p>Notice (8): Undefined index: 
  RecyclateTypeConversion
  [CORE\cake\libs\model\datasources\dbo_source.php,
  line 1099]</p>
</blockquote>

<p>However the SQL debug output confirms that the query itself runs fine and returns 4 records, and the view runs perfectly when the finderQuery is not specified.  I've tried for other hasMany tables too - with exactly the same issue.</p>

<p>I've attempted to replace the select all with specific field selects but I still see the same result.  Certainly the query looks correct according to the manual - so what is the issue (and could it be related to using MSSQL?)</p>

<p>EDIT: Also, as this hasn't picked up any answers yet, what would be the best approach to debugging this?  I've started hunting through the cake debugging class, but so far with no results that have enlightened me.  Of course if there is a problem I'll be submitting the fix back to the project.</p>

## Answers
### Answer ID: 6199124
<p>did you go through it step by step?</p>
<ol>
<li>try to get everything (all data)</li>
<li>try conditions</li>
<li>try &quot;containable&quot; behavior to create your query, which makes things a lot easier in my opinion</li>
</ol>

### Answer ID: 6209838
<p>Try removing the alias from the select - the casting in in the "AS RecyclateTypeConversion" part should handle that for you. I also like to wrap custom queries in double quotes. I might just be paranoid but string parsing errors have bit me in the ass before.</p>

<pre><code>var $hasMany = array(
    'RecyclateTypeConversion' =&gt; array(
    'className' =&gt; 'RecyclateTypeConversion',
    'foreignKey' =&gt; 'recyclate_type_id',
    'dependent' =&gt; false,
    'finderQuery' =&gt; "select * from recyclate_type_conversions AS RecyclateTypeConversion WHERE RecyclateTypeConversion.recyclate_type_id IN ({$__cakeID__$});",
);
</code></pre>

<p>Also, I highly suggest you use the DebugKit plugin and post back to us the query log and a debug output of the find results that cause the errors.</p>

### Answer ID: 6174581
<p>Have you checked that there is actually a model called <code>RecyclateTypeConversion</code> and that it exists with a filename according to the CakePHP conventions? I.e. is there a <code>models/recyclate_type_conversion.php</code> and in that file, is the name of the model defined as <code>RecyclateTypeConversion</code>.</p>

<p>The error that you're getting seems to hint that there's something wrong with that model name, as it cannot find the associated index.</p>

### Answer ID: 6171958
<p>Have you tried <a href="http://cakephp.lighthouseapp.com/projects/42880-debug-kit" rel="nofollow">CakePHP Debug Kit</a></p>

