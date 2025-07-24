# shared hosting website optimization (US server)
[Link to question](https://stackoverflow.com/questions/9242756/shared-hosting-website-optimization-us-server)
**Creation Date:** 1328984373
**Score:** 4
**Tags:** php, mysql, apache, .htaccess, optimization
## Question Body
<p>i have a hosting server on godaddy. i have the economic plan which is a shared one for my current project (i have a tight budget until i get traffic and mnoey)</p>

<p>i am using linux and i have data in my databases (pages, user etc...). when i display <code>/folder/pagex/</code> i rewrite it internally to <code>rewriterule ^([^/]+)/([^/]+)/? index.php?f=$1&amp;p=$2</code> then after is query the database, get the data and generate the webpage.</p>

<p>everything works great but obviously it has to go to a process</p>

<ol>
<li>get the page from the .htaccess -> query the database -> generate -> display</li>
</ol>

<p>i would like to know if there's a faster way to execute this? like skipping the database query some how but still displaying the page</p>

## Answers
### Answer ID: 9243187
<p>Yes, there is an awful lot you can do.  I run my blog on a LAMP/suPHP-based shared hosting service, Webfusion rather than GoDaddy, but their overall implementation architectures are pretty similar: a load-balancing IP switch fronting onto a LAMP server farm which then has switched 1Gb interconnect back to NAS infrastructure for the user directory space and a D/B farm to operate the databases.  (And yes, I also have an Amazon EC2 micro instance.)</p>

<p>This type of service offering is low cost, scalable and does not involve the account holder in known how to configure and administer a cloud VM.  I also hold all of my content and configuration in a backend D/B.  My blog has an average page load time (measured by Chome Pagespeed) of 200-500mSec and <a href="http://code.google.com/speed/page-speed/">PageSpeed</a> score of 99/100. </p>

<p>So yes in an suPHP configuration, each script involves a PHP image activation which normally adds ~100mSec to request times (<a href="http://blog.ellisons.org.uk/article-44">this article</a> explains how to benchmark this for your own service), but when you do Pagespeed timing of transactions from the end-user perspective, it is usually poor caching and lack of compression that dogs performance.  Once you've sorted out that, then there's the image start-up which you can't avoid for dynamic content -- unless as Zeus suggests, you move to a dedicated VM + mod_php5 + Xcache/APC.  </p>

<p>The next big hit is the I/O overhead of marshalling and reading in all of the script files, and this can add a few seconds on the first request when these are not in a VFAT cache, but again I discuss mitigation in my blog articles. </p>

<p>The PHP compilation time itself and the script execution time are in the noise -- unless you've done something <em>really</em> dumb, like doing full table scans or joins on the same for large tables that aren't properly indexed.  </p>

<p>Anyway, I've written a bunch of articles that address this sort of topic for developers just like you.  Read them, and I hope that you find them useful.  Please come back here with any more Qs, but remember to keep them focused; also make sure that you provide the supporting info and don't use this as a substitute for reasonable levels of research.  :-)</p>

### Answer ID: 9242774
<p>I'm afraid you can't, because it's getting the data from a database, maybe using Cloudflare and CDN can improve your page load time (I think that is what you mean). </p>

<p>Good luck</p>

