# Same URL iFrames but using different session data
[Link to question](https://stackoverflow.com/questions/74183018/same-url-iframes-but-using-different-session-data)
**Creation Date:** 1666623207
**Score:** 0
**Tags:** php, session, iframe
## Question Body
<p>I have 2x iframes that includes the same website (from same origin).</p>
<p>I'm using sessions to switch between 2x different database tables, depending on which iframe they use. One is for Employees, the other is for Customers. I do this by differentiating with a URL parameter</p>
<pre><code>&lt;iframe src=&quot;website/index.php?customer=1&quot; frameborder=&quot;0&quot; style=&quot;width:100%; height:100%;&quot; name=&quot;product_frame&quot; id=&quot;product_frame&quot;&gt;&lt;/iframe&gt;
</code></pre>
<p>It then registers which iframe is being used and in turn uses the correct DB table in my queries.</p>
<p>This works fine unless the user goes to the other iframe and navigates, it detects the URL parameter isn't there and rewrites the session information, so if you go back to the other iframe, the incorrect data is shown.</p>
<p>How can I know that the user is in a specific iframe even if they switch between both?</p>
<p>I know one solution would be to have 2x completely different directories and clone the website but this seems excessive.</p>

