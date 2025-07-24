# Linq Include helper function for f# style pipelining
[Link to question](https://stackoverflow.com/questions/16595290/linq-include-helper-function-for-f-style-pipelining)
**Creation Date:** 1368730594
**Score:** 2
**Tags:** entity-framework, f#, ef-code-first, pipelining, query-expressions
## Question Body
<p>I want to eagerly load some records from and their relations from the database something like this:</p>

<pre><code>let getEmails() =
    let emails =
        (query { for q in entities.QueueItems do
                    select q.Email
                    take batchSize }
        ).Include(fun (e:Email) -&gt; e.QueueItem)
        |&gt; Seq.toArray

    emails 
    |&gt; Array.iter (fun e -&gt; entities.QueueItems.Remove(e.QueueItem) |&gt; ignore)

    entities.SaveChanges(logger) |&gt; ignore 
    emails
</code></pre>

<p>This works great, although I have to wrap the query expression in brackets to be able to call include on it which looks a bit weird. I wondered if I could write a helper function to call Include in a more idiomatic F# style, and I came up with this.</p>

<pre><code>module Ef =
    let Include (f:'a -&gt; 'b) (source:IQueryable&lt;'a&gt;) = 
        source.Include(f)
</code></pre>

<p>now my query can look like this (type inference works on the queryable type :D)</p>

<pre><code>let emails =
    query { for q in entities.QueueItems do
                select q.Email
                take batchSize }
    |&gt; Ef.Include(fun e -&gt; e.QueueItem)
    |&gt; Seq.toArray
</code></pre>

<p>It compiles! But when I run it, I get an error from the DbExtensions library telling me <code>The Include path expression must refer to a navigation property defined on the type.</code> </p>

<p>Inspecting the lambda function before it's passed to Queryable.Include, it looks like this <code>{&lt;StartupCode$Service&gt;.$Worker.emails@30} Microsoft.FSharp.Core.FSharpFunc&lt;Entities.Email,Entities.QueueItem&gt; {&lt;StartupCode$Service&gt;.$Worker.emails@30}</code>.</p>

<p>I guess problem is to do with how my lambda is being interpreted and conversions between <code>FSharpFunc</code>s and <code>Expression&lt;Func&lt;&gt;&gt;</code>s. I tried to rewrite my helper function so it had an <code>Expression&lt;Func&lt;'a, 'b&gt;&gt;</code> as its first parameter, and even downloaded the FSharp.Core source to look for inspiration in the implementations of the Seq module and QueryBuilder, but I couldn't get anything working. I tried redefining my helper function as so:</p>

<pre><code>module Ef =
    let Include (y:Expression&lt;Func&lt;'a,'b&gt;&gt;) (source:IQueryable&lt;'a&gt;) = 
        source.Include(y)
</code></pre>

<p>But then I get the compiler error <code>This function takes too many arguments, or is used in a context where a function is not expected</code>. </p>

<p>I'm a bit stumped. Can anyone suggest how I can get this working?</p>

## Answers
### Answer ID: 16596903
<p>AFAIR type-directed conversions are applied only to uncurried type members, not to let bindings.
As a fix you can try to change Ef.Include to be a static member</p>

<pre><code>type Ef = 
    static member Include (f : Expression&lt;System.Func&lt;'a, 'b&gt;&gt;) = 
        fun (q : IQueryable&lt;'a&gt;)  -&gt; q.Include f
</code></pre>

