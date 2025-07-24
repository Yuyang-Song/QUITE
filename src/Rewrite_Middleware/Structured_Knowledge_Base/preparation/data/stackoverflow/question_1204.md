# MongoDB convert Select from UNION with Group By with sum
[Link to question](https://stackoverflow.com/questions/63265636/mongodb-convert-select-from-union-with-group-by-with-sum)
**Creation Date:** 1596631885
**Score:** 0
**Tags:** mysql, node.js, mongodb
## Question Body
<p>I'm building a COVID API in NodeJS which have very in-depth detail about my country.</p>
<p>Due huge bill I decided to rewrite my whole database from MySQL to NoSQL which is more affordable for me.</p>
<p>Basically what I have to do is, if date_onset is empty then I will use date_specimen as proxy.</p>
<p>I have the following MySQL query which I need to convert to NoSQL.</p>
<pre class="lang-sql prettyprint-override"><code>SELECT count(a.cases) as cases, a.date FROM 
(SELECT date_specimen AS cases, date_specimen AS date from case_informations WHERE (date_specimen &lt;&gt; '' AND date_onset = '') 
UNION ALL
SELECT date_onset AS cases, date_onset AS date FROM case_informations WHERE date_onset &lt;&gt; '') AS a
GROUP BY a.date ORDER BY a.date ASC
</code></pre>
<p>The Document:</p>
<pre class="lang-js prettyprint-override"><code>{
    &quot;_id&quot;: {
        &quot;$oid&quot;: &quot;5f29a6dcc4ce73be6be928ff&quot;
    },
    &quot;case_code&quot;: &quot;C611583&quot;,
    &quot;age&quot;: 20,
    &quot;age_group&quot;: &quot;20-24&quot;,
    &quot;sex&quot;: &quot;female&quot;,
    &quot;date_specimen&quot;: &quot;&quot;,
    &quot;date_result_release&quot;: &quot;2020-04-22&quot;,
    &quot;date_rep_conf&quot;: &quot;2020-04-24&quot;,
    &quot;date_died&quot;: &quot;&quot;,
    &quot;date_recover&quot;: &quot;&quot;,
    &quot;removal_type&quot;: &quot;recovered&quot;,
    &quot;admitted&quot;: &quot;no&quot;,
    &quot;region_res&quot;: &quot;NCR&quot;,
    &quot;prov_res&quot;: &quot;&quot;,
    &quot;city_mun_res&quot;: &quot;&quot;,
    &quot;city_muni_psgc&quot;: &quot;&quot;,
    &quot;health_status&quot;: &quot;recovered&quot;,
    &quot;quarantined&quot;: &quot;no&quot;,
    &quot;date_onset&quot;: &quot;&quot;,
    &quot;pregnant_tab&quot;: &quot;no&quot;,
    &quot;validation_status&quot;: &quot;Removal Type is \&quot;Recovered\&quot;, but no Recovered Date is recorded\nRemoval Type is \&quot;Recovered\&quot;, but no Recovered Date is recorded\nHealth Status is \&quot;Recovered\&quot;, but no Date Recovered is recorded\nHealth Status is \&quot;Recovered\&quot;, but no Date Recovered is recorded&quot;
}
</code></pre>
<p>This is the closest I can get:</p>
<pre class="lang-js prettyprint-override"><code>collection.aggregate([
            {$project: {date_specimen: 1, date_onset: 1}},
            {$lookup:
                {
                  from: 'case_informations',
                  pipeline: [
                    {$match: {date_specimen: {$exists: true}, date_onset: ''}},
                    {$group: {_id: '$date_specimen', cases: {$sum: 1}}},
                    {$sort: {_id: 1}},
                  ],
                  as: 'a',
                },
            },
            {$lookup:
                {
                  from: 'case_informations',
                  pipeline: [
                    {$match: {date_onset: {$exists: true}}},
                    {$group: {_id: '$date_onset', cases: {$sum: 1}}},
                    {$sort: {_id: 1}},
                  ],
                  as: 'b',
                },
            },
            {$project: {'a': 1, 'b': 1}},
          ]).limit(1);
</code></pre>
<p>result:</p>
<pre class="lang-js prettyprint-override"><code>{
  _id: 5f29a6dcc4ce73be6be928fc,
a: [
    { _id: '2020-03-04', cases: 1 },
    { _id: '2020-03-06', cases: 8 },
    { _id: '2020-03-07', cases: 48 },
    {...}
   ],
b: [
    { _id: '2020-03-03', cases: 45 },
    { _id: '2020-03-04', cases: 32 },
    { _id: '2020-03-05', cases: 55 },
    {...}
]
}
</code></pre>
<p>expected:</p>
<pre class="lang-js prettyprint-override"><code>{
  _id: 5f29a6dcc4ce73be6be928fc,
UnionOfAandC: [
    { _id: '2020-03-03', cases: 45 },
    { _id: '2020-03-04', cases: 33 }, // merge object with same date
    { _id: '2020-03-05', cases: 55 },
    { _id: '2020-03-06', cases: 8 },
    { _id: '2020-03-07', cases: 48 },
    {...},
   ],
}
</code></pre>

## Answers
### Answer ID: 63266284
<p>After some trial and error I finally solved it</p>
<pre class="lang-js prettyprint-override"><code>await collection.aggregate([
            {$match: {$or: [{'date_onset': {'$ne': ''}}, {'date_specimen': {'$ne': ''}}]}},
            {
              $group: {
                _id: {
                  'date': {
                    $cond: {
                      if: {$eq: ['$date_onset', '']}, then: '$date_specimen', else: '$date_onset',
                    },
                  },
                },
                cases: {$sum: 1},
              },
            },
            {$sort: {'_id.date': 1}},
            {$project: {'_id': 0, 'date': '$_id.date', 'cases': 1}},
          ]);
</code></pre>

