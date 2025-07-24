# Retrieving data in recycler view not working -query correction
[Link to question](https://stackoverflow.com/questions/67872861/retrieving-data-in-recycler-view-not-working-query-correction)
**Creation Date:** 1623073608
**Score:** 2
**Tags:** android, firebase, android-studio, firebase-realtime-database, android-recyclerview
## Question Body
<p>I have a problem retrieving data from Firebase. I am attaching the structure of my database in the figure.<a href="https://i.sstatic.net/e4Bfr.png" rel="nofollow noreferrer">enter image description here</a>
Here I have the parent node as &quot;Reply&quot;, inside that I have replykey, inside push key parent for each node have its children. I like to fetch data based on particular &quot;teacherID&quot; that matches the current teacher. The query I wrote is shown below</p>
<pre><code>RootRef = FirebaseDatabase.getInstance().getReference(); 
  query=RootRef.child(&quot;Reply&quot;).orderByChild(&quot;teacherID&quot;).equalTo(CurrentTeacherrId);
       FirebaseRecyclerOptions&lt;StudentModelClass&gt; options =
               new FirebaseRecyclerOptions.Builder&lt;StudentModelClass&gt;()
                       .setQuery(InstRef,StudentModelClass.class)
                       .build();
</code></pre>
<p>Using this code recycleView is not fetching the data. How I can rewrite the query to fetch data correctly</p>

