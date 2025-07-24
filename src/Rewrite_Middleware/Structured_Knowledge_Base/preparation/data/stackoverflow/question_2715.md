# FMDB usage with swift - returning a boolean
[Link to question](https://stackoverflow.com/questions/48664888/fmdb-usage-with-swift-returning-a-boolean)
**Creation Date:** 1518009570
**Score:** 0
**Tags:** objective-c, swift, fmdb
## Question Body
<p>I am currently building an app in swift that uses FMDB to interact with a database that is stored on the device. I chose to use FMDB since I have experience using it with Objective C, and it says it supports swift.</p>

<p>I am having problems with returning booleans in swift when executing a statement. Here is an image of the update functions available to me when using FMDB in an Objective C class, notice how the overwhelming majority return bools</p>

<p><a href="https://i.sstatic.net/NnAjZ.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/NnAjZ.png" alt="FMDB update objc"></a></p>

<p>And here are the funcs available in swift:
<a href="https://i.sstatic.net/9f2mz.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/9f2mz.png" alt="FMDB update swift"></a></p>

<p>Doesn't give me much to work with!</p>

<p>Here is an existing query I am currently using in an app (with names changed).</p>

<pre><code>sql = @"INSERT INTO Table (IdValue, AnotherIDValue) VALUES (?, ?);";
BOOL success =  [db executeUpdate:sql,
                 [NSNumber numberWithLong:preference.idvalue1],
                 [NSNumber numberWithLong:preference.idvalue2],
                 nil];
</code></pre>

<p>Once this statement runs I close off the database &amp; return the boolean. This essentially gives me a completion block and lets me hold the UI up until the sql has successfully completed.</p>

<p>Unfortunately with swift I have alot less to work with, and I don't really understand the function inputs that return bools. So far in my swift database class I run updates like so:</p>

<pre><code>try! db.executeUpdate(sqlStatement, values: dataArray)
</code></pre>

<p>Giving me safety, if it fails, but no way to return a success boolean. I am wondering if anyone has any suggestions for implementing the database class like I showed in objective c. </p>

<p>The only alternative I can see is rewriting the class in objective c, however I would prefer to keep this app 100% swift.</p>

## Answers
### Answer ID: 48665913
<p>From <a href="https://developer.apple.com/library/content/documentation/Swift/Conceptual/BuildingCocoaApps/AdoptingCocoaDesignPatterns.html" rel="nofollow noreferrer">Adopting Cocoa Design Patterns</a> in the
"Using Swift with Cocoa and Objective-C" reference:</p>

<blockquote>
  <p>Swift automatically translates Objective-C methods that produce errors into methods that throw an error according to Swift’s native error handling functionality.</p>
</blockquote>

<p>Therefore the Objective-C method</p>

<pre><code>- (BOOL)executeUpdate:(NSString *)sql values:(NSArray *_Nullable)values error:(NSError *_Nullable __autoreleasing *)error
</code></pre>

<p>is mapped as</p>

<pre><code>func executeUpdate(sql: String, values: [Any]?) throws 
</code></pre>

<p>into Swift, and must be called with (a variant of) <code>try</code>.</p>

<p>If you are only interested in the success/failure status, but not
in the actual error message (as in your Objective code), then
you can use <code>try?</code>, which evaluates to <code>nil</code> if the evaluation failed:</p>

<pre><code>let success = (try? db.executeUpdate(sqlStatement, values: dataArray)) != nil
</code></pre>

