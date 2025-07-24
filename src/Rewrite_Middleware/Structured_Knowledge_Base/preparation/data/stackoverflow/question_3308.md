# Reflection about syncing firebase data to local sqlite on flutter app for &quot;complex&quot; aggregations queries
[Link to question](https://stackoverflow.com/questions/75703690/reflection-about-syncing-firebase-data-to-local-sqlite-on-flutter-app-for-compl)
**Creation Date:** 1678523462
**Score:** 1
**Tags:** flutter, firebase, sqlite
## Question Body
<p>Hi everybody (sorry for my pseudo english in advance)</p>
<p>Today, my flutter app is able to querying sqlite data to perform &quot;complex&quot; queries (count, sum, avg, on grouped data, specifically on date field).</p>
<p>Im working on a cloud option for my users : I have choose Firebase.</p>
<p>And here the issues and questions coming...</p>
<p>My queries are not intendeed to be performed on a no-sql database at the beginning, so should I :</p>
<ul>
<li>write almost same queries for Firebase (and, in majors cases, get all data then group them)</li>
<li>always querying sqlite but sync Firebase to Sqlite at app start, and send create/update/delete to both of them</li>
<li>querying firebase cache (possible ?)</li>
<li>something else that I don't have any idea at the moment...</li>
</ul>
<p>Here is the app (in french), if you want to know what it likes : <a href="https://play.google.com/store/apps/details?id=com.gigout.rudy.mes_releves" rel="nofollow noreferrer">https://play.google.com/store/apps/details?id=com.gigout.rudy.mes_releves</a></p>
<p>I don't want to remove Sqlite part, because first some users have already lot of data, and some don't likes Cloud things.
Firebase solution is only for sharing data with other people, and keep sync between device.</p>
<p>Thanks in advance for your brains !</p>
<p>My Sqlite entities have an id integer auto-increment, firebase by default use random string. So sync firebase to sqlite makes me rewrite part of code to adapt id.</p>
<p>I have an abstract DAO system, for example AbstractCollectionDao =&gt; SqliteCollectionDao and FirebaseCollectionDao. Implements function with data aggregation in Firebase_Dao are not efficient, and complex to maintain.</p>
<p>I have try to sync some part from Firebase to Sqlite for querying sqlite, but it's really slow (copy data every time is not the idea of the century).</p>

