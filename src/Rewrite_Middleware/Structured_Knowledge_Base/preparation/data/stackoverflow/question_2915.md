# How does querying nested data work? Can I still retrieve data from 1 level down?
[Link to question](https://stackoverflow.com/questions/58365976/how-does-querying-nested-data-work-can-i-still-retrieve-data-from-1-level-down)
**Creation Date:** 1570987173
**Score:** 0
**Tags:** swift, firebase, firebase-realtime-database
## Question Body
<p>I want to query data that is two levels down, however, would I still be able to retrieve data from its original node?</p>

<p>To explain better, my Firebase Database looks like:</p>

<pre><code>posts
  -192u3jdj0j9sj0
     -message: haha this is funny (CAN I STILL GET THIS DATA)
     -genre: comedy (CAN I STILL GET THIS DATA)
        -author
           -user: "jasonj"
        -comment
           -ajiwj2319j0jsf9d0jf
               -comment: "lol"
               -user: "David" (QUERY HERE****)
           -jfaiwjfoj1ijifjojif
               -comment: "so funny"
               -user: "Toddy"
</code></pre>

<p>I essentially want to query by all of the comments David has posted.  However, with how query works, can I still grab the original (message &amp; genre) that was from "level 1"? Or would I have to restructure my data?  Possibly rewriting the level 1 data under comment.</p>

<p>(End goal: something like Yahoo answers, where the user can see the questions he posted, as well as the questions to where he posted comments)</p>

<p>Below code works, but I'm not sure how to pull up level 1 data or if its even possible</p>

<pre><code>   ref = Database.database().reference().child("posts").child(myPost).child("comment")
    var queryRef:DatabaseQuery
    queryRef = ref.queryOrdered(byChild: "user").queryEqual(toValue: "David")
    queryRef.observeSingleEvent(of: .value, with: { (snapshot) in
        if snapshot.childrenCount &gt; 0 {
</code></pre>

## Answers
### Answer ID: 58366516
<p>Your current data structure makes it easy to find the comments for a specific post. It does not however make it easy to find the comments from a specific author. The reason for that is that Firebase Database queries treat your content as a flat list of nodes. The value you want to filter on, must be at a fixed path under each node.</p>

<p>To allow finding the comments from a specific author, you'll want to add an additional node where you keep that information. For example:</p>

<pre><code>"authorComments": {
  "David": {
    "-192u3jdj0j9sj0_-ajiwj2319j0jsf9d0jf": true
  },
  "Toddy": {
    "-192u3jdj0j9sj0_-jfaiwjfoj1ijifjojif": true
  }
}
</code></pre>

<p>This structure is often known as a reverse index, and it allows you to easily find the comment paths (I used a <code>_</code> as the separator of path segments above) for a specific user.</p>

<p>This sort of data duplication is quite common when using NoSQL databases, as you often have to modify/expand your data structure to allow the use-cases that your app needs.</p>

<p>Also see my answers here:</p>

<ul>
<li><p><a href="https://stackoverflow.com/questions/27207059/firebase-query-double-nested">Firebase Query Double Nested</a></p></li>
<li><p><a href="https://stackoverflow.com/questions/40656589/firebase-query-if-child-of-child-contains-a-value">Firebase query if child of child contains a value</a></p></li>
</ul>

