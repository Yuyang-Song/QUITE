# PHP dealing with concurrency
[Link to question](https://stackoverflow.com/questions/16815466/php-dealing-with-concurrency)
**Creation Date:** 1369834685
**Score:** 6
**Tags:** php, concurrency, enterprise
## Question Body
<p>I'm running an enterprise level PHP application. It's a browser game with thousands of users online on an infrastructure that my boss refuses to upgrade and the machinery is running on 2-3 system load (yep linux) at all times. Anyhow that's not the real issue. The real issue is that some users wait until the server gets loaded (prime time) and they bring their mouse clickers and they click the same submit button like 10 - 20 times, sending 10-20 requests at the same time while the server is still producing the initial request, thus not updated the cache and the database. </p>

<p>Currently I have an output variable on each request, which is valid for 2 minutes and I have "mutex" lock which is basically a flag inside memcache which if found blocks the execution of the script further, but the mouse clicker makes so many requests at the same time that they run almost simultaneously which is a big issue for me. </p>

<p>How are you, the majority of StackOverflow folks dealing with this issue. I was thinking of flagging the cookie/session but I think I will get in the same issue if the server gets overloaded. Optimization is impossible, the source is 7 years old and is quite optimized, with no queries on most pages (running off of cache) and only querying the database on certain user input, like the one I'm trying to prevent. </p>

<p>Yep it's procedural code with no real objects. Machines run PHP 5 but the code itself is more of a PHP 4. I know, I know it's old and stuff but we can't spare the resource of rewriting this whole mess since most of the original developers left that know how stuff is intertwined and yeah, I'm basically patching old holes. But as far as I know this is a general issue on loaded PHP websites. </p>

<p>P.S: Disabling the button with javascript on submit is not an option. The real cheaters are advanced users. One of them had written a bot clicker and packed it as a Google Chrome extension. Don't ask how I dealt with that. </p>

## Answers
### Answer ID: 35957306
<p>I don't know if there's an implementation already out there, but I'm looking into writing a cache server which has responsibility for populating itself on cache misses. That approach could work well in this scenario.</p>

<p>Basically you need a mechanism to mark a cache slot as pending on a miss; a read of a pending value should cause the client to sleep a small but random amount of time and retry; population of pending data in a traditional model would be done by the client encountering a miss instead of pending.</p>

<p>In this context, the script is the client, not the browser.</p>

### Answer ID: 21319877
<p>I'm getting the feeling this is touching more on how to update a legacy code base than anything else. While implementing some type of concurrency would be nice, the old code base is your real problem.</p>

<p>I highly recommend <a href="http://www.dev-metal.com/interesting-talk-on-modernizing-a-legacy-php-codebase/" rel="nofollow">this video</a> which discusses Technical Debt. </p>

<p>Watch it, then if you haven't already, explain to your boss in business terms what <strong>technical debt</strong> is. He will likely understand this. Explain that because the code hasn't been managed well (debt paid down) there is a very high level of technical debt. Suggest to him/her how to address this by using small incremental iterations to improve things. </p>

### Answer ID: 18784465
<p>limiting the IP connections will only make your players angry.
I fixed and rewrote a lot of stuff in some famous opensource game clones with old style code:
well, i must say that cheating can be always avoid executing the right queries and logic.
for example look at here <a href="http://www.xgproyect.net/2-9-x-fixes/9407-2-9-9-cheat-buildings-page.html" rel="nofollow">http://www.xgproyect.net/2-9-x-fixes/9407-2-9-9-cheat-buildings-page.html</a></p>

<p>Anyway, about performace, keep in mind that code inside sessions will block all others thread untill current one is closed. So be carefull to inglobe all your code inside sessions.Also, sessions should never contain heavy data.</p>

<p>About scripts: in my games i have a php module that automatically rewrite links adding an random id saved in database, a sort of CSRFprotection. Human user will click on the changed link, so they will not see the changes but scripts will try to ask for the old link and after some try there are banned!
others scripts use the DOM , so its easy to avoid them inserting some useless DIV around the page.</p>

<p>edit: you can boost your app with <a href="https://github.com/facebook/hiphop-php/wiki" rel="nofollow">https://github.com/facebook/hiphop-php/wiki</a></p>

### Answer ID: 16815810
<p>I would look for a solution outside your code.</p>

<p>Don't know which server you use but apache has some modules like mod_evasive for example.</p>

<p>You can also limit connections per second from an IP in your firewall</p>

