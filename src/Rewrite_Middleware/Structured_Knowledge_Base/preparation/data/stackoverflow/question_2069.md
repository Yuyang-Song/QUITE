# Android detecting when all threads idle -- unit testing
[Link to question](https://stackoverflow.com/questions/17838984/android-detecting-when-all-threads-idle-unit-testing)
**Creation Date:** 1374681025
**Score:** 0
**Tags:** android, multithreading, testing, android-listview, android-espresso
## Question Body
<p>How do I know when all threads have completed execution and are idle?</p>

<p>I am trying to write unit tests for a Java based Android application.
The tests require that a content provider is queried, and that contents are added to a ListView prior to the actual test.</p>

<p>What I cannot figure out is how to know when all my operations are completed; specifically that the list view has completed its update when the database changed, and that all database operations have completed.</p>

<p>I can throw sleeps into my test cases, but as expected they make things unreliable if the system gets under heavy load; and slow down execution.  </p>

<p>After watching the <a href="https://www.youtube.com/watch?v=T7ugmCuNxDU&amp;t=580" rel="nofollow noreferrer">GTAC 2013: Espresso: Fresh Start to Android UI Testing - YouTube video</a> (See video at 9:40-11:31)
 I am thinking there has to be a way of detecting when all threads are idle, and executing my
next code step.</p>

<p>I am hoping to be able to implement a poor mans version of Espresso, since I would like to have stable tests now.  And then rewrite them if Espresso ever becomes available.</p>

## Answers
### Answer ID: 19440522
<p>Espresso's been <a href="https://code.google.com/p/android-test-kit/" rel="nofollow">released</a> - So give it a shot.</p>

### Answer ID: 17839802
<p>When the are signaled and so start doing things, have them first inc an atomic int.  When they are done and about to stop doing things, have them dec the int.  Any thread that decs the int to 0 calls an 'onCompletion' method/function/whatever.</p>

