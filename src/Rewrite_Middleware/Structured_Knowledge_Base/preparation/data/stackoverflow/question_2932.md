# How to wait for coroutine Dispatch.IO database query to finish to populate RecyclerView
[Link to question](https://stackoverflow.com/questions/59130408/how-to-wait-for-coroutine-dispatch-io-database-query-to-finish-to-populate-recyc)
**Creation Date:** 1575237851
**Score:** 1
**Tags:** android, kotlin, android-recyclerview, kotlin-coroutines
## Question Body
<p>I'm rewriting my Java note taking app in Kotlin. I'm trying to populate a RecyclerView with TextViews built from my SQLite database query, but I can't figure out how to make it wait for the query to be done, or take an action when it is done. </p>

<p>In my Java version I accomplished this by using AsyncTask for the query and then calling PostExecute.</p>

<p>Now in my Kotlin version I'm using launch(Dispatchers.IO), but I'm not sure how to do the rest. How do I accomplish the same functionality?</p>

## Answers
### Answer ID: 59133527
<p>In coroutines you can make a queue of non-identical coroutine codes. For example one block from coroutine1 and another one from coroutine2 and make them run sequentially. It is possible using <code>withContext(CoroutineContext)</code></p>

<p>Assume this code:</p>

<pre><code>fun uiCode() {
  // doing things specially on mainThread
}

fun uiCode2() {
  // More work on mainThread
}

fun ioCode() {
  // Doing something not related to mainThread.
}

fun main() {

  launch(Dispatchers.Main) { // 1- run a coroutine
     uiCode() // will run on MainThread
     withContext(Dispachers.IO) { // 2- Coroutine will wait for ioCode
         ioCode() // Will run on ioThread
     }
     uiCode2() // 3- And then it will run this part
  }
}
</code></pre>

<p>If you wanted to do it asyncronously, use <code>launch()</code>, instead of <code>withContext()</code>.</p>

