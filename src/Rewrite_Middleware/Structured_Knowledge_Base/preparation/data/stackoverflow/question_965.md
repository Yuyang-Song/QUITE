# Dump series back into InfluxDB after querying with replaced field value
[Link to question](https://stackoverflow.com/questions/52188429/dump-series-back-into-influxdb-after-querying-with-replaced-field-value)
**Creation Date:** 1536160221
**Score:** 4
**Tags:** python-3.x, influxdb, influxdb-python
## Question Body
<h2>Scenario</h2>
<p>I want to send data to an MQTT Broker (Cloud) by querying measurements from InfluxDB.</p>
<p>I have a <strong>field</strong> in the schema which is called <code>status</code>. It can either be <code>1</code> or <code>0</code>. <code>status=0</code> indicated that series has not been sent to the cloud. If I get an acknowlegdment from the MQTT Broker then I wish to rewrite the query back into the database with <code>status=1</code>.</p>
<p>As mentioned in <a href="https://docs.influxdata.com/influxdb/v1.6/troubleshooting/frequently-asked-questions/#how-does-influxdb-handle-duplicate-points" rel="nofollow noreferrer">FAQs for InfluxDB regarding Duplicate data</a> If the information has the same timestamp as the previous query but with a different field value =&gt; then the update field will be shown.</p>
<p>In order to test this I created the following:</p>
<pre><code>CREATE DATABASE dummy
USE dummy
INSERT meas_1, type=t1, status=0,value=123 1536157064275338300
</code></pre>
<p>query:</p>
<pre><code>SELECT * FROM meas_1
</code></pre>
<p>provides</p>
<pre><code>time                status type value         
1536157064275338300 0      t1   234      
</code></pre>
<p>now if I want to <strong>overwrite</strong> the series I do the following:</p>
<pre><code>INSERT meas_1, type=t1, status=1,value=123 1536157064275338300                                                                       
</code></pre>
<p>which will overwrite the series</p>
<pre><code> time                status type value         
 1536157064275338300 1      t1   234     
</code></pre>
<p>(Note: this is not possible via <strong>Tags</strong> currently in InfluxDB)</p>
<h3>Usage</h3>
<ol>
<li>Query some information using the client with <code>&quot;status&quot;=0</code>.</li>
<li>Restructure JSON to be sent to the cloud</li>
<li>Send the information to cloud</li>
<li>If successful then write the output from Step 1. back into the DB but with <code>status=1</code>.</li>
</ol>
<p>I am using the <a href="https://influxdb-python.readthedocs.io/en/latest/api-documentation.html" rel="nofollow noreferrer"><code>InfluxDBClient Python3</code></a> to create the Application (MQTT + InfluxDB)</p>
<p>Within the <a href="https://influxdb-python.readthedocs.io/en/latest/api-documentation.html#influxdb.InfluxDBClient.write_points" rel="nofollow noreferrer"><code>write_points</code> API</a> there is a parameter which mentions <code>batch_size</code> which require <code>int</code> as input.</p>
<p>I am not sure how can I use this with the Application that I want. Can someone guide me with this or with the Schema of the DB so that I can upload actual and non-redundant information to the cloud ?</p>

## Answers
### Answer ID: 52328818
<p>The <code>batch_size</code> is actually the length of the list of the measurements that needs to passed to <code>write_points</code>.</p>

<h2>Steps</h2>

<ol>
<li><p>Create client and query from measurement (here, we query gps information)</p>

<pre><code>client = InfluxDBClient(database='dummy')

op = client.query('SELECT * FROM gps WHERE "status"=0', epoch='ns')
</code></pre></li>
<li><p>Make the <code>ResultSet</code> into a list:</p>

<pre><code> batch = list(op.get_points('gps'))
</code></pre></li>
<li><p>create an empty list for update</p>

<pre><code> updated_batch = []
</code></pre></li>
<li><p>parse through each measurement and change the <code>status</code> flag to <code>1</code>. Note, default values in InfluxDB are float</p>

<pre><code>   for each in batch:
new_mes = {
'measurement': 'gps',
'tags': {
'type': 'gps'
},
'time': each['time'],
'fields': {
  'lat': float(each['lat']),
  'lon': float(each['lon']),
  'alt': float(each['alt']),
  'status': float(1)
}
}
updated_batch.append(new_mes)
</code></pre></li>
<li><p>Finally dump the points back via the client with <code>batch_size</code> as the length of the <code>updated_batch</code></p>

<pre><code>client.write_points(updated_batch, batch_size=len(updated_batch))
</code></pre></li>
</ol>

<p>This overwrites the series because it contains the same timestamps with <code>status</code> field set to <code>1</code></p>

