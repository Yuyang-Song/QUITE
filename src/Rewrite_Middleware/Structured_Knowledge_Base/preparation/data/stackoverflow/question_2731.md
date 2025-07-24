# html5 appcache stoped working on IOS 11.3
[Link to question](https://stackoverflow.com/questions/49694395/html5-appcache-stoped-working-on-ios-11-3)
**Creation Date:** 1523022727
**Score:** 3
**Tags:** ios, google-chrome, safari, html5-appcache
## Question Body
<p>We now know this is an issue with IOS 11.3, and seems to target only Ipad. </p>

<p>When requesting ressources through appcache, the cookies are discarded. If your ressources are behind some authentication. They will be redirected to your authentication page.</p>

<p>As mentioned by Apple, we tried experimentation feature on/off. </p>

<p>Removing authentication for ressources is not a valid permanent option.</p>

<p>We are looking for solutions while the next version of IOS hopefully fix this problem which seem the case with 11.4 beta 2. Changes are to be as minimal as possible to reduce risks.</p>

<p>Following informations are the process we when through when trying to solve our problem. To this day, no valid solutions have been attempted. Service Workers being the most plausible path.</p>

<p><strong>Day 1</strong><br>
We have an application which was running fine in production for a while (almost a year since last deployment).</p>

<p>Our application use app cache to enable offline mode when wifi is not available.
Our application is mostly used on ipad with safari and some surface pro with chrome. Currently most cases are reported with ipad.</p>

<p>In the last few day, more and more users start to have problem loading the cache. We have been able to reproduce the probleme on an ipad after updating to 11.3 (could not reproduce on iphone 11.3) and using google chrome desktop incognito mode on dev machine. Application work on an older iPad we have which is at version 10.3.3.</p>

<blockquote>
  <p>--Application Cache Error event: Resource fetch failed (2) <a href="http://localhost:63330/client/vendor/kendo-ui/kendo.all.js--" rel="nofollow noreferrer">http://localhost:63330/client/vendor/kendo-ui/kendo.all.js--</a></p>
</blockquote>

<p><strong>Fact</strong><br>
 - It always block on the same files, after some testings it seems to be all files bigger than 1.2Mb, in this case kendo is 4.7Mb and the minified one is 1.7Mb.<br>
 - Fiddler does not report any error, all files status response is 200</p>

<p><strong>Guess</strong><br>
 1. An update to safari and chrome might have changed<br>
 2. An ipad setting might have been changed by admins<br>
 3. An update to windows or ios, might have changes something  </p>

<p>Since safari and ios follow the same release (29 Mar 2018), they are probably linked and the most likely guess, does anyone have an idea why this might happen?</p>

<p>Could not find much on apple support page of changes for 11.3<br>
<a href="https://support.apple.com/en-ca/HT208067" rel="nofollow noreferrer">https://support.apple.com/en-ca/HT208067</a><br>
<a href="https://support.apple.com/en-ca/HT201222" rel="nofollow noreferrer">https://support.apple.com/en-ca/HT201222</a>  </p>

<p><strong>Update Monday 9 april 2018</strong><br>
We have been able to reproduce the issue both by debugging an Ipad and on the mac mini we have. However, the problem is different and for this reason we currently discarded what we found on Chrome on our desktop in incognito.</p>

<p>Here are the new facts:</p>

<ul>
<li>Cookies were not provided while downloading file with appcache. The first file request is rejected and redirected to login page.</li>
</ul>

<blockquote>
  <p>[Warning] ApplicationCache is deprecated. Please use ServiceWorkers
  instead. (192.168.0.152, line 2)<br>
  [Error] Failed to load resource: the
  server responded with a status of 401 (Unauthorized) (cache.manifest,
  line 0)<br>
  [Error] Application Cache manifest could not be fetched,
  because the manifest had a 401 response.<br>
  [Error] 2018-04-09 12:01:51 :
  APPLICATION CACHE error<br>
      logMsg (logDecorator.js:111)<br>
      error (logDecorator.js:128)<br>
      (fonction anonyme) (applicationCacheUpdateSrv.js:121)<br>
      dispatch (jquery-1.10.2.js:5109)<br>
      handle (jquery-1.10.2.js:4780)  </p>
</blockquote>

<p><strike>
 - After effect of solving authentication, we have problems with IDBDatabase, might be related to Authorization we removed (currently under investigation)</p>

<blockquote>
  <p>IndexedDB request error (get all rapports) -> NotFoundError: Failed to
  execute 'transaction' on 'IDBDatabase': One of the specified object
  stores was not found.
  </strike></p>
</blockquote>

<p>We found this by using Charles Proxy for Mac. For this reason, we removed authentication to our statics files and Home page. This seems to work, but our files would be public which is not really an option.</p>

<p>Similar questions:
<a href="https://stackoverflow.com/questions/10437605/cache-manifest-how-to-handle-authentication-cookies">Cache-Manifest How to handle authentication cookies?</a>  </p>

<p><strong>Update Monday 10 april 2018</strong><br>
<strike>
IndexDB error are not related. Databases were not initialized properly due to authorization missing.<br>
</strike></p>

<p>We currently added an alternative home page where authorization is not required instead of removing authorization from the default home page. It would be called by the manifest cache and downloaded properly.</p>

<p><strong>Update Monday 12 april 2018</strong><br>
We tried to secure the static files, we ended up with adding a token in the query url. While it work and we can authenticate the request (note that since we do not have cookies to authenticate the user, the authentication is far from flawless), the Url is now different than what was requested in the cached Home page and make the custom authentication worthless by itself.</p>

<p>We would need to also rewrite all the url for the cached page base the token genereted by the user. In our cases, it involve throwing out the ASP.Net MVC Bundle feature to maybe make a custom one? At this point, we think it might just be easier to try ServiceWorker since appcache is deprecated. This does not guarantee cookie will be passed on with ServiceWorker...</p>

<p><strong>Update Monday 19 april 2018</strong><br>
We had some return from Apple yesterday. They asked be try <em>Prevent Cross-Site Tracking</em> property (both on and off) in Settings > Safari and also try Experimental feature in Settings > Safari > Advanced > Experimental (mentionning ServiceWorkers, but tried them all)</p>

<p>Unfortunately it didn't change anything for me at the moment.</p>

<p>Note: strikethrough some part that were not related directly to the issue</p>

<p><strong>Update Friday 25 may 2018</strong><br>
Added a section to the top to resume the situation and make the question more to the point.</p>

## Answers
### Answer ID: 50026394
<p>As of 25 april 2018, we tried iOS 11.4 beta and it seem to resolve the issue. According the the deployement timeline, it should be available in about a month according to <a href="https://www.macworld.com/article/3267786/iphone-ipad/ios-11-4-features-release-date-and-how-to-install.html" rel="nofollow noreferrer">this</a>.</p>

<p>However until then moving to service workers might be a good idea. </p>

<p><a href="https://developers.google.com/web/ilt/pwa/caching-files-with-service-worker" rel="nofollow noreferrer">Here</a> is an example from google.<br>
<a href="https://youtu.be/MiLAE6HMr10?list=WL&amp;t=676" rel="nofollow noreferrer">Here</a> is a video which gives an introduction to the subject</p>

<p>I will add an example if we get to move to Service workers</p>

