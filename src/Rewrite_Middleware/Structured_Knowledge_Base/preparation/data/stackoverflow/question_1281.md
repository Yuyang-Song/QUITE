# Understanding result of fetching CKRecords with new async/await API
[Link to question](https://stackoverflow.com/questions/68019427/understanding-result-of-fetching-ckrecords-with-new-async-await-api)
**Creation Date:** 1623933107
**Score:** 6
**Tags:** ios, swift, cloudkit, ios15
## Question Body
<p>I am a bit confused on how to deal with complex Swift data types, their assignment to variables and accessing the values within. Hopefully someone can clarify the following:</p>
<p>when trying to get data from SwiftUI and CloudKit, and while trying to rewrite a CK function to conform to async/await, I have the following line of code:</p>
<p><code>let result  = try await container.privateCloudDatabase.records(matching: query)</code></p>
<p>now this line is <em><strong>supposed</strong></em> to get all of the records matching the specified query from the cloud private database and return some CKRecords</p>
<p>The old function did this as follows:</p>
<pre><code>container.privateCloudDatabase.perform(query, inZoneWith: nil) { (rec, err) in 
    for record in rec {
        print(&quot;Found this record: \(record)&quot;)
    }
}
</code></pre>
<p>and this worked great because <code>perform(_:inZoneWith:)</code> would return a CKRecord and an Error, those were &quot;picked apart&quot; in the <code>(rec, err) in</code> statement and passed into the loop to be iterated.</p>
<p>With the new async/await method, I am trying to simply await and assign a variable to all of the records that are found and then iterate the data returned, pick out the CKRecords and perform whatever task I want.</p>
<p>What I am confused with is, when I attempt to pick out the data from the returned result, in several ways, I just get errors. I am not fully understanding how to describe the data structure of the returned values and I think this is the root cause of the issue.</p>
<p>I have tried a few things and have gotten the following error messages:</p>
<p>if I try:</p>
<pre><code>let (result, err)  = try await container.privateCloudDatabase.records(matching: query)
</code></pre>
<p>When I use (trying to append the CKRecords to an array of CKRecords I created earlier):</p>
<pre><code>for record in result {
   self.myCKRecordArray.append(record)
}
</code></pre>
<p>the error message states specifically:</p>
<p><code>Cannot convert value of type 'Dictionary&lt;CKRecord.ID, Result&lt;CKRecord, Error&gt;&gt;.Element' (aka '(key: CKRecord.ID, value: Result&lt;CKRecord, Error&gt;)') to expected argument type 'CKRecord'</code></p>
<p>Which definitely gives me some clues. I believe that my <code>result</code> variable contains a Dictionary&lt;CKRecord.ID, Result&lt;CKRecord, Error&gt;&gt;.Element, or a list of key/value pairs wherein the CKRecord.ID is the key for the Result&lt;CKRecord, Error&gt; value.</p>
<p>This is pretty confusing.. So If I understand that correctly, then:</p>
<pre><code>        for thisDict in result {
            let (realResult, err) = result[thisDict.key]
            print(&quot;Found this record: \(realResult)&quot;)
        }
</code></pre>
<p>should theoretically result in the output of each CKRecord assigned to realResult, right? I just get the error: <code>Type of expression is ambiguous without more context</code></p>
<p>I tried to change it to <code>valueForKey</code> and also give it more context, but no change from the error message:</p>
<pre><code>let (realResult, err) = result(valueForKey:thisDict.key) as Result&lt;CKRecord, Error&gt;
</code></pre>
<p>I just believe that I do not fully understand <em><strong>how</strong></em> to properly access the CKRecord from something that is represented by a: <code>Dictionary&lt;CKRecord.ID, Result&lt;CKRecord, Error&gt;&gt;.Element</code> data structure.</p>
<p>Any insight into understanding is greatly appreciated.</p>
<p>Thank you</p>
<p><em><strong>Update</strong></em></p>
<p>Ok, based on the answer from @Shadowrun, if I understand correctly:</p>
<p>The result from:</p>
<pre><code>let result  = try await container.privateCloudDatabase.records(matching: query)
</code></pre>
<p>is a tuple type. Which means that it has two elements, the first being the Dictionary of data and the second being the queryCursor.</p>
<p>If I want to iterate over the Dictionary portion of the tuple and get the CKRecord out:</p>
<pre><code>        for rec in result.0 {
            self.myCKRecordArray.append(try rec.value.get())
        }
</code></pre>
<p>This does not give me any errors.. Am I understanding this correctly?</p>
<p><em><strong>2nd update</strong></em>
it does work as expected this way.</p>

## Answers
### Answer ID: 68025758
<p>At the risk of being pedantic, may I suggest reading the docs?</p>
<p><a href="https://developer.apple.com/documentation/cloudkit/ckdatabase/3856524-records" rel="nofollow noreferrer">https://developer.apple.com/documentation/cloudkit/ckdatabase/3856524-records</a></p>
<pre><code>func records(matching query: CKQuery, 
    inZoneWith zoneID: CKRecordZone.ID? = nil, 
    desiredKeys: [CKRecord.FieldKey]? = nil, 
    resultsLimit: Int = CKQueryOperation.maximumResults) async throws -&gt; 
        (matchResults: [CKRecord.ID : Result&lt;CKRecord, Error&gt;],     
          queryCursor: CKQueryOperation.Cursor?)
</code></pre>
<p>So your result is tuple. Call your result <code>tuple</code>. Then <code>tuple.matchResults</code> is a dictionary keyed by ID whose values are Result objects.</p>
<p>The best way to extract value from a Result object, in my opinion, is to use <code>get</code>. This has the advantage that it either returns a value or throws, and you can cope nicely with that.</p>

### Answer ID: 68019607
<p>There’s an equivalence between functions that return a <code>Result&lt;T, E&gt;</code> and functions that either return <code>T</code> or throw an <code>E</code>. And similar equivalence for functions returning tuple of <code>(T?, E?)</code></p>
<p>When mapping functions with completion handlers to async functions, they become throwing functions, so should just be:</p>
<pre><code>let result = try await container….
</code></pre>
<p>The error, if any, is thrown</p>

