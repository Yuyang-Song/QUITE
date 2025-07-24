# MVC3 site running fast locally, very slow on live host
[Link to question](https://stackoverflow.com/questions/9551542/mvc3-site-running-fast-locally-very-slow-on-live-host)
**Creation Date:** 1330824956
**Score:** 2
**Tags:** asp.net-mvc, asp.net-mvc-3, performance
## Question Body
<p>So I've been running into some speed issues with my site which has been online for a few weeks now. It's an MVC3 site using MySQL on discountasp.net. </p>

<p>I cleaned up the structure of the site and got it working pretty fast on my local machine, around 800-1100ms to load with no caching. The strange thing is when I try and visit the live site I get times of around 15-16 seconds, sometimes freezing up as long as 30 seconds. I switched off the viewstate in web.config and now the local loads in 1.3 seconds (yes, oddly a little longer) and the live site is down to 8-9 seconds most of the time, but that's still pretty poor.</p>

<p>Without making this problem to specific to my case (since there can be a million reasons sites go slow), I am curious if there are any reasons why the load times between the local Visual Studio sever or IIS Express would run so fast while the live site would run so slow. Wouldn't anything code wise or dependency wise effect both equally? I just can't think of a reason that would affect the live site but not the local.</p>

<p>Any thoughts?</p>

<p><strong>Further thoughts:</strong> I have the site setup as a sub-folder which I'm using IIS URL Rewriting to map to a subdomain. I've not heard of this causing issues before, but could this be a problem?</p>

<p><img src="https://i.sstatic.net/4PyCK.jpg" alt="Screenshot of the local and live sites running"></p>

<p><strong>Further Further  Updates:</strong> So I uploaded a simple page that does nothing but query all the records in the largest table I have with no caching. On my local machine it's averages around 110ms (which still seems slow...), and on the live site it's usually over double the time. If I'm hitting the database several times to load the page, it makes sense that this would heavily affect the page load time. I'm still not sure if the issue is with LINQ or MySQL or MVC in general (maybe even discountasp.net).
<img src="https://i.sstatic.net/f1A9q.jpg" alt="Database query time"></p>

## Answers
### Answer ID: 9587449
<p>So as I mentioned above, I had caching turned off for development, but only on my local machine. What I didn't realise was there was a problem <em>WITH</em> the caching which was turned on for the <em>LIVE</em> server, which I never turned off because I thought it was helping fix the slow speeds! It all makes sense now :)</p>

<p>Fixing my cache issue (IQueryable&lt;> at the top of a dataset that was supposed to cache the entire table.. >_>) my speeds have increased 10 fold.</p>

<p>Thanks to everyone who assisted!</p>

### Answer ID: 9551596
<p>I had a similar problem once and the culprit was the initialization of the user session. Turns out a lot of objects were being read/write to the session state on each request, but for some reason this wasn't affecting my local machine (I probably had <code>InProc</code> mode enabled locally).</p>

<p>So try adding an attribute to some of your controllers and see if that speeds things up:</p>

<pre><code>[SessionState(SessionStateBehaviour.Disabled)]
public class MyController : Controller
{
</code></pre>

<p>On another note, I ran some tests, and surprisingly, it was faster to read some of those objects from the DB <strong><em>on each request</em></strong> than to read them once, then put them in the session state. That kinda makes sense, since session state mode in production was <code>SqlServer</code>, and serialization/deserialization was apparently slower than just assigning values to properties from a <code>DataReader</code>. Plus, changing that had the nice side-effect of avoiding deserialization errors when deploying a new version of the assembly...</p>

<p>By the way, even 992ms is too much, IMHO. Can you use output caching to shave that off a bit?</p>

