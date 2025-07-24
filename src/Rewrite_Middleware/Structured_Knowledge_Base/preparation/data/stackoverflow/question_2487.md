# Why does google UTM code disappear after initial landing page?
[Link to question](https://stackoverflow.com/questions/36826688/why-does-google-utm-code-disappear-after-initial-landing-page)
**Creation Date:** 1461519717
**Score:** 1
**Tags:** php, wordpress, google-analytics, utm
## Question Body
<p>Im running a self-hosted wordpress site and I am trying to tailor what secondary content a user sees based off of parameters in the utm code. All I was doing was <code>&lt;?php if (isset($_GET['utm_source'])) {dynamic_sidebar( 'sidebar-1' );}else {dynamic_sidebar( 'sidebar-2' );} ?&gt;</code></p>

<p>For either testing for a UTM pram or a string variable to display one widget vs the other. After I did this and was testing I realized that the UTM code disappears after a user clicks to the next page or to any other page. i.e the utm query disappears from the end of the URL in the bar (but google is still tracking the session of course, just no visible utm). So after the initial landing page the condition is no longer true </p>

<p>I was wondering if anyone knows why it does this? Because I have been on sites where the UTM stays appended to the URL and when it disappears, like it does for me. Im assuming the tag is saved by wordpress in the database table, but can't find an answer. I am trying to figure out what is going on. and if I should solve my problem by declaring a new variable to check or if I should tell wordpress to continue appending the UTM using a rewrite rule.</p>

## Answers
### Answer ID: 36827058
<p>It is normal that UTM parameters (like any other parameters) are only used on the landing page.</p>

<p>Google Analytics requires them only on the landing page; these are session based values, so it is enough to see them on the first page call. Google Analytics will automatically attribute all subsequent pageviews in that session to the same visitor (identified by the client id which is stored in a cookie).  You can see how this works exactly <a href="https://support.google.com/analytics/answer/6205762?hl=en#flowchart" rel="nofollow">in the documentation</a>. When the campaign parameter changes Google will start a new session.</p>

<p>Since attribution happens on the Google servers the GA code will do nothing to persist the utm parameters on the client side. It is quite normal that parameters from a link are not passed around  though the site - if you want that you have to do some programming and add them yourself. Actually it would be better to set a cookie with the utm values, that way they would not be visible in the URL (which looks odd). </p>

<p>But it is normal that they show only in the incoming link. If you want the parameters to stay appended you have to append them yourself.</p>

