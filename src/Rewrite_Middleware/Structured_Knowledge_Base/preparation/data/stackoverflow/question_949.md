# Why does Haskell have bottom (infinite recursions)?
[Link to question](https://stackoverflow.com/questions/51800389/why-does-haskell-have-bottom-infinite-recursions)
**Creation Date:** 1533996025
**Score:** 7
**Tags:** haskell, recursion
## Question Body
<p>There are languages other than Haskell, such as <a href="https://coq.inria.fr/" rel="nofollow noreferrer">Coq</a>, which banned bottom, or <code>undefined</code>, or infinite recursive definitions like</p>

<pre><code>bot :: forall a. a
bot = bot
</code></pre>

<p>The benefit of not having bottom is simple : all programs terminate. The compiler guarantees that there are no infinite loops, no infinite recursions.</p>

<p>There is also a less obvious benefit : the logic of the language (given by the <a href="https://en.wikipedia.org/wiki/Curry%E2%80%93Howard_correspondence" rel="nofollow noreferrer">Curry-Howard correspondence</a>) is consistent, it cannot prove a contradiction. So the same language can write both programs and proofs that the programs are correct. But that's maybe off-topic here.</p>

<p>The protection against infinite recursions is also simple : force each recursive definition to have arguments (here <code>bot</code> has none) and force recursive calls to be decreasing on one of those arguments. Here decreasing is in the sense of algebraic data types, seen as finite trees of contructors and values. Coq's compiler checks that the decreasing argument is an ADT (<code>data</code> in Haskell) and that the recursive calls are done on subtrees of the argument, typically via a <code>case of</code>, not on other trees coming from somewhere else.</p>

<p>Now the cost of this language constraint : we lose Turing-completeness (because we cannot solve the <a href="https://en.wikipedia.org/wiki/Halting_problem" rel="nofollow noreferrer">halting problem</a>). That means there are terminating functions, possible to code in Haskell using general recursions, that would become refused by the compiler. In practice however, the magnitude of Coq's library shows that those exotic functions are rarely needed. Does someone even know one of them ?</p>

<p>There are cases where infinite loops make sense :</p>

<ul>
<li>Interactive programs, where the user issues commands by clicking or typing on the keyboard, usually run forever. They wait for a command, process it and then wait for the next command. Until the end of time, or more seriously until the user issues the quit command.</li>
<li>Likewise, instead of processing an infinite stream of user commands, process an infinite stream of data. Such as continuous queries on a database.</li>
</ul>

<p>Those cases are rather specific and might be treated by new language primitives. Haskell introduced <code>IO</code> to trace unsafe interactions. Why not declare the possibility of infinite loops in the signature of functions ? Or split a complex program into a <a href="https://en.wikipedia.org/wiki/Data_stream_management_system" rel="nofollow noreferrer">DSMS</a> that calls Haskell functions for pure computations ?</p>

<p><strong>EDIT</strong></p>

<p>Here is an algorithm example, that might clarify what changes if we switch to total programming. Euclid's algorithm for computing the GCD of 2 numbers, first in plain recursive Haskell</p>

<pre><code>euclid_gcd :: Int -&gt; Int -&gt; Int
euclid_gcd m n = if n &lt;= 0 then m else euclid_gcd n (m `mod` n)
</code></pre>

<p>Two things can be proven concerning this function : that it terminates, and that it does compute the GCD of m and n. In a language accepting proof scripts, we would give the compiler a proof that <code>(m mod n) &lt; n</code>, so that it concludes the recursion is decreasing on its second argument, and therefore terminates.</p>

<p>In Haskell I doubt we can do that, so we can try to rewrite this algorithm in a structural recursive form, that the compiler can easily check. That means a recursive call must be done on the predecessor of some argument. Here <code>m mod n</code> won't do, so it looks like we are stuck. But as with tail recursion, we can add new arguments. If we find a bound on the number of recursive calls, we are done. The bound does not have to be precise, it just needs to be above the actual number of recursive calls. Such a bound argument is usually called <code>variant</code> in the literature, I personally call it <code>fuel</code>. We force the recursion to stop with an error value when it runs out of fuel. Here we can take the successor of any of the 2 numbers :</p>

<pre><code>euclid_gcd_term :: Int -&gt; Int -&gt; Int
euclid_gcd_term m n = euclid_gcd_rec m n (n+1)
  where
    euclid_gcd_rec :: Int -&gt; Int -&gt; Int -&gt; Int
    euclid_gcd_rec m n fuel =
      if fuel &lt;= 0 then 0
      else if n &lt;= 0 then m else euclid_gcd_rec n (m `mod` n) (fuel-1)
</code></pre>

<p>Here the termination proof somewhat leaks into the implementation, making it slightly harder too read. And the implementation makes useless computations on the fuel argument, which could slow down a bit, though in this case I hope Haskell's compiler will make it negligible. Coq has an extraction mechanism, that erases the proof part of such mixes of proofs and program, to produce OCaml or Haskell code.</p>

<p>As for <code>euclid_gcd</code> we would then need to prove that <code>euclid_gcd_term</code> does compute the GCD of n and m. That includes proving Euclid's algorithm terminates in less than n+1 steps.</p>

<p><code>euclid_gcd_term</code> is obviously more work than <code>euclid_gcd</code> and arguably less fun. On the other hand, once the habit is taken, I find it rewarding intellectually to know bounds for my algorithms. And when I cannot find such bounds, it usually means I don't understand my algorithms. Which also usually means they are bugged. We cannot force all developers to use total programming for all programs, but wouldn't a compiling option in Haskell to do it on demand be nice?</p>

## Answers
### Answer ID: 51807451
<p>I can't give you a comprehensive answer, but I've spent some time working in Agda over the past year, and here are some drawbacks of totality that I've seen.</p>

<p>Basically, when writing a program in Haskell, there are some bits of information that I have, but that I do not explicitly share with the compiler.  If this information is necessary for the program to terminate without errors, then Agda forces me to make this information explicit.</p>

<p>Consider Haskell's <code>Data.Map.!</code> operator that lets you lookup an element in a map by its key.  If you pass a key that is not in the map, it will throw an exception.  The Agda counterpart of this operator would need to take not only the key, but also a proof that the key is in the map.  This has some drawbacks:</p>

<ol>
<li>Someone would have to come up with a type that lets us express "map <code>m</code> contains key <code>k</code>", and prove lemmas about how this type interacts with insertion and deletion.</li>
<li>Any changes to the definitions of <code>insert</code> and <code>delete</code> will likely invalidate the proofs of these lemmas.</li>
<li>When I use this map, I have to keep track of all the membership proofs explicitly, passing them around and keeping them up to date.  This is both a syntactic and a mental burden.</li>
<li>If I care about performance, I need to make sure that all these proofs are erased at runtime.</li>
</ol>

<p>Alternatively, I could use <code>Maybe</code> or <code>Either</code> to explicitly pass these errors around.  Often this is the right thing to do, but it makes it less clear when I anticipate an error happening, and when I've simply not gone through the trouble of showing that an error is impossible.  This approach also doesn't work as well with interactive debuggers: I can easily break on an exception, but not so easily on the construction of a <code>Nothing</code>.</p>

<p>I've been focusing on errors in the above, but the same things hold for non-termination.</p>

<p>This isn't to say that total languages are useless—as you say, they have many benefits.  So far, I just wouldn't say that those benefits obviously outweigh these drawbacks for all applications.</p>

