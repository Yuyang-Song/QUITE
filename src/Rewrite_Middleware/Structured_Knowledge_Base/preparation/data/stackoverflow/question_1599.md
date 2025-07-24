# program for optimal performance and scalability from the start?
[Link to question](https://stackoverflow.com/questions/961250/program-for-optimal-performance-and-scalability-from-the-start)
**Creation Date:** 1244352195
**Score:** 1
**Tags:** optimization, scalability
## Question Body
<p>First question on stackoverflow.  I have no previous experience of running a high traffic website and I would consider myself somewhere in between a novice and an intermediate programmer....please be gentle :)<br>
I am trying to make a social website that I ultimately hope will handle a lot of traffic and users.  However, I don't know if the concept will fly and programming for scalability is a lot of additional work compared to slapping some sloppy code together that functionally works the same way.  In addition, since I'm relatively uninformed about programming for high scalability, I find myself doing a lot of research which is further slowing me down (highscalability.com is amazing...I'm currently trying to figure out offline queues)</p>

<p>My question is, should I:<br>
A)<br>
1. put together some code that's suboptimal but functional (somewhat sloppy code, excessive database queries, no caches, etc.)<br>
2. work on gathering traffic<br>
3. rewrite and restructure code</p>

<p>or
B)<br>
1. fully research scalable designs and apply from the beginning so I don't have to restructure much<br>
2. work on gathering traffic  </p>

<p>Any advice is appreciated, thank you.</p>

## Answers
### Answer ID: 961308
<p>Spend a couple weeks studying Cal Henderson's <a href="http://oreilly.com/catalog/9780596102357/" rel="nofollow noreferrer">Building Scalable Web Sites</a>, Theo Schlossnagle's <a href="https://rads.stackoverflow.com/amzn/click/com/067232699X" rel="nofollow noreferrer" rel="nofollow noreferrer">Scalable Internet Architectures</a>, and of course the site you've already found, Todd Hoff's excellent <a href="http://highscalability.com" rel="nofollow noreferrer">highscalability.com</a>.  At a minimum you'll understand the tradeoffs between (A) and (B) and be able to make a better decision. </p>

<p>Also spend time looking at <a href="http://aws.amazon.com/" rel="nofollow noreferrer">Amazon Web Services</a>, especially their EC2 (Elastic Cloud Computing) and S3 (Simple Storage System).  A group at my company just deployed a web application on the Amazon infrastructure and it was dramatically simpler than trying to run it on their own physical hardware.</p>

<p>If you're still at an early ideation stage and just want to work out your ideas and run small experiments, (A) would work well.  But once you decide you want to deploy a small-scale trial leading into a full scale product, you absolutely need to follow (B).  </p>

<p>When you start to shift into (B) mode, I'd suggest you use AWS to save nearly all the effort and capital expenditure in setting up your own infrastructure.  Use some of the time you'll save using AWS to thoroughly learn (B) and apply the lessons.  Then if you succeed, your scalable architecture will allow you to rent as many AWS machine-hours as you need.  If you don't succeed, you'll have learned a lot of very useful things to apply to your next startup idea (or job).</p>

<p>Keep in mind this isn't an either-or choice too.  Once you understand the basic principles behind scaling, you'll be able to start out along path (B) with something simple, while at the same time have the comfort in knowing how you'll progress to the next step.  Danga has some very interesting <a href="http://danga.com/words" rel="nofollow noreferrer">presentations</a> along these lines.  Take a look at <a href="http://danga.com/words/2007_06_usenix/usenix.pdf" rel="nofollow noreferrer">this one</a>, and you'll see how they started off with just one machine, shifted to an app server machine and a database machine, to three app servers and a database machine, and so.</p>

### Answer ID: 961262
<p>You make it sound like A) would result in sloppy, poorly thought-out code that works, but will not scale well and is almost certainly going to require a rewrite <em>once you already have users and need to provide reasonable uptime</em>.  Fixing prevantable problems once you already have traffic sounds like a nightmare.</p>

<p>I would definitely go with B).  Thinking about, researching and planning the architecture of your application, not just for optimisation or performance but also just for sensible overall design, is an absolute must for any non-trivial software application.</p>

<p>There is a common myth that premature optimisation is the root of all evil.  This is absolutely false, though it would be more accurate to say that unnecessary optimisation is the root of all evil.  Do not make the newbie mistake of optimising where it doesn't matter, which is just going to mess up your code, but do spend the time finding out which optimisations DO matter.</p>

<p>Twitter nearly died when they realised they'd made some poor DB design choices once they already had traffic.</p>

### Answer ID: 961270
<p>Web development is a continual process.  We may <em>think</em> we know what we want at the beginning, but it will inevitably change by the time we get there.</p>

<p>I suggest that you start by getting the book by the 37 Signals Crew -- Getting Real:
<a href="http://gettingreal.37signals.com/" rel="nofollow noreferrer">http://gettingreal.37signals.com/</a></p>

<p>Mix A and B.  Try to get a good hosting situation.  Think about <em>ways</em> that you can cache (memcache -- it's easy).  Write clear code, but don't spend too much time...</p>

<p>"Release Early, Release Often".</p>

<p>--</p>

<p>Here is a tale of two projects.</p>

<ol>
<li>Developed on side time -- hacked together -- released early (and often).  It grew to 15,000 users and 6,000,000 views per month (in 5 months).</li>
<li>Developed in a corporate "do-it-all-just-right" mentality.  Took 4 months, 10+ people, tens of thousands of dollars.  It peaked out at ~ 100 users.</li>
</ol>

<p>Let wisdom guide you...</p>

### Answer ID: 961260
<p>I would go for option A. It's much harder to generate traffic to a website than it is to improve performance. If your idea is unique then time to market should be your primary goal. <a href="http://highscalability.com/" rel="nofollow noreferrer">http://highscalability.com/</a> contains tons of good articles on how others have solved scalability problems.</p>

