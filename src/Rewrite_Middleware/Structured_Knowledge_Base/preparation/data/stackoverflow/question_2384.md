# SequenceType / GeneratorType That Can Also Throw?
[Link to question](https://stackoverflow.com/questions/32228285/sequencetype-generatortype-that-can-also-throw)
**Creation Date:** 1440596408
**Score:** 1
**Tags:** swift, sqlite, swift2
## Question Body
<p>I'm in the process of learning Swift and as an exercise, I'm writing a wrapper around SQLite. As I was experimenting, I realized that for queries that return rows (like SELECT), I could implement the SequenceType / GeneratorType protocols so that I can return a set of data for each sqlite3_step that I perform.</p>

<p>In practice, sqlite3_step either returns a row or is done, but in theory, it could error out. I'm not doing anything crazy with SQLite. It's just a simple data store for me, so I'm not rewriting schemas on the fly or potentially ripping the database out from under itself, but the fact remains that IN THEORY sqlite3_step could fail.</p>

<p>The question then is, is there a proper way to handle errors in the SequenceType / GeneratorType pattern? GeneratorType's next method doesn't support a throws parameter and returning nil just dictates the end of a sequence. Would there be a good way to handle the error and propagate it up the chain?</p>

## Answers
### Answer ID: 32229678
<p>You have a few options, depending on what you're looking for.</p>

<p>If you need the Sequence to be lazy, you could use a ResultType kind of thing:</p>

<pre><code>enum SQLiteRow&lt;T&gt; {
  case Success(T), FailureTypeOne, FailureTypeTwo
}
</code></pre>

<p>Then, your <code>next()</code> method would return a <code>SQLiteRow&lt;T&gt;?</code>, where <code>T</code> is the type of your row.</p>

<p>This fits in nicely with for-loops, as you can use it like this:</p>

<pre><code>for case let .Success(row) in queries {...
</code></pre>

<p>so the successful queries are bound to the <code>row</code> variable. This is only if you want to filter out the failed queries. If you wanted to stop everything, you could switch within the for loop, or have a function like this:</p>

<pre><code>func sanitize&lt;
  S : SequenceType, T where
  S.Generator.Element == SQLiteRow&lt;T&gt;
  &gt;(queries: S) -&gt; SQLiteRow&lt;[T]&gt; {
  var result: [T] = []
  result.reserveCapacity(queries.underestimateCount())
  for query in queries {
    switch query {
    case let .Success(x): result.append(x)
    case .FailureTypeOne: return .FailureTypeOne
    case .FailureTypeTwo: return .FailureTypeTwo
    }
  }
  return SQLiteRow.Success(result)
}
</code></pre>

<p>That will take a sequence of possibly-failed queries, and give back either a sequence of successful queries (if none failed), or a failure type representing the first failure it came across.</p>

<p>However, the second option there <em>isn't</em> lazy. Another eager way to do it would be to use <code>map</code>, which (as of the latest beta) can take a closure which throws:</p>

<pre><code>func makeQuery(x: String) throws -&gt; String {
  return x
}

let queries = ["a", "b", "c"]

do {
  let successful = try queries.map(makeQuery)
} catch {
  // handle
}
</code></pre>

<p>Unfortunately the lazy version of <code>map</code> <em>doesn't</em> throw, so you have to evaluate the whole sequence if you want to throw like this.</p>

