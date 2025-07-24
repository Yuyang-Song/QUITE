# Can I get a boto3 DynamoDB table object from a client object?
[Link to question](https://stackoverflow.com/questions/74320720/can-i-get-a-boto3-dynamodb-table-object-from-a-client-object)
**Creation Date:** 1667581988
**Score:** 3
**Tags:** amazon-web-services, amazon-dynamodb, boto3
## Question Body
<p>I have some existing code that uses boto3 (python) DynamoDB Table objects to query the database:</p>
<pre class="lang-py prettyprint-override"><code>import boto3
resource = boto3.resource(&quot;dynamodb&quot;)
table = resource.table(&quot;my_table&quot;)
# Do stuff here
</code></pre>
<p>We now want to run the tests for this code using DynamoDB Local instead of connecting to DynamoDB proper, to try and get them running faster and save on resources. To do that, I gather that I need to use a client object, not a table object:</p>
<pre class="lang-py prettyprint-override"><code>import boto3
session = boto3.session.Session()
db_client = session.client(service_name=&quot;dynamodb&quot;, endpoint_url=&quot;http://localhost:8000&quot;)
# Do slightly different stuff here, 'cos clients and tables work differently
</code></pre>
<p>However, there's really rather a lot of the existing code, to the point that the cost of rewriting everything to work with clients rather than tables is likely to be prohibitive.</p>
<p>Is there any way to either get a table object while specifying the endpoint_url so I can point it at DynamoDB Local on creation, or else obtain a boto3 dynamodb table object from a boto3 dynamodb client object?</p>
<p>PS: I know I could also mock out the boto3 calls and not access the database at all. But that's also prohibitively costly, because for all of the existing tests we'd have to work out where they touch the database and what the appropriate mock setup and use is. For a couple of tests that's perfectly fine, but it's a lot of work if you've got a lot of tests.</p>

## Answers
### Answer ID: 74334280
<p>‎The other answers correctly told you that if you liked the &quot;resource&quot; API, you can still use it even with DynamoDB local (by the way, shameless plug: if you're looking for self-installable version of DynamoDB, you can also consider the open-source ScyllaDB project which has a DynamoDB API).</p>
<p>I just wanted to add that if you do want to switch to the &quot;client&quot; API - which I recommend (it's easier to use) - it's still possible to get a table object from a client. Just do:</p>
<pre class="lang-py prettyprint-override"><code>table = db_client.Table(name)
</code></pre>

### Answer ID: 74320872
<p>Yes, you can use the resource-level classes such as <a href="https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#table" rel="nofollow noreferrer">Table</a> with both the real DynamoDB service and DynamoDB Local via the <a href="https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#service-resource" rel="nofollow noreferrer">DynamoDB service resource</a>, as follows:</p>
<pre><code>resource = boto3.resource('dynamodb', endpoint_url='http://localhost:8000')
table = resource.Table(name)
</code></pre>

