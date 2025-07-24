# Monad troubles porting from Lift to Yesod&#39;s Persistent
[Link to question](https://stackoverflow.com/questions/12628314/monad-troubles-porting-from-lift-to-yesods-persistent)
**Creation Date:** 1348772271
**Score:** 2
**Tags:** haskell, monads, persistent, yesod
## Question Body
<p>I have a Lift app I'm porting to Yesod as a way to learn the framework and Haskell. Part of the app resides only on the TCP and database layers: parsing incoming bytes from a socket connection and turning them into Updates for the model to handle. I did this in Scala with regexes and pattern-matching, and failed to reproduce it in Haskell.</p>

<p>A highly simplified example:</p>

<pre><code>share [mkPersist sqlSettings, mkMigrate "migrateAll"] [persist|
Person
    name String
    deriving Show

UnknownMessage
    text String
    deriving Show
|]

parseMsg m = runDB $ do
    case ms of
        ["add",name]       -&gt; insert Person{personName = name}
        ["delete",name]    -&gt; deleteWhere [PersonName ==. name]
        ["change",from,to] -&gt; updateWhere [PersonName ==. from] [PersonName =.to]
        _                  -&gt; insert UnknownMessage{unknownMessageText = m}
where
    ms = splitRegex (mkRegex ",") m
</code></pre>

<p>The above code will only compile with three of the four pattern matches commented out. "insert Person" does not play with "deleteWhere", or even "insert UnknownMessage". The results tend to be type-matching error messages which I often can't make heads or tails of.</p>

<p>How might I rewrite the above code? Is there a Persistent guide for the monadically challenged anywhere? The book chapter doesn't go into much detail on how to chain queries and the like.</p>

<p>Edit: hammar's suggestion of adding (>>) to the Inserts fixed the issue. If I remove "runDB $ do", the function's type becomes "parseMsg :: PersistQuery backend m => String -> backend m ()". Would this allow me to execute the returned query later within a monad, as I was doing with my Updates in Scala?</p>

## Answers
### Answer ID: 12628497
<p>I'm no Yesod expert, but from a quick look at the docs it looks like the problem is that the <code>insert</code> action returns a key for the new record, while <code>updateWhere</code> and <code>deleteWhere</code> both return <code>()</code>.</p>

<pre><code>insert      :: (...) =&gt; val -&gt; backend m (Key backend val)
updateWhere :: (...) =&gt; [Filter val] -&gt; [Update val] -&gt; backend m ()
deleteWhere :: (...) =&gt; [Filter val] -&gt; backend m ()
</code></pre>

<p>Presumably, you don't care about the key here, so you can discard it by doing</p>

<pre><code>insert Person{personName = name} &gt;&gt; return ()
</code></pre>

<p>which should make it type check.</p>

