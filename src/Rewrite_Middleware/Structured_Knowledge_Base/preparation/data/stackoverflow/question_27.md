# Need a mod_rewrite .htaccess solution to replace %20 spaces with -&#39;s in the finished URL
[Link to question](https://stackoverflow.com/questions/10407594/need-a-mod-rewrite-htaccess-solution-to-replace-20-spaces-with-s-in-the-fini)
**Creation Date:** 1335931880
**Score:** 1
**Tags:** .htaccess, mod-rewrite, cgi-bin
## Question Body
<p>I need an .htaccess mod_rewrite solution that will take a .cgi search query like this:</p>

<p>www.mydomain.com/cgi-bin/finda/therapist.cgi?Therapy_Type=Pilates Training&amp;City=Los Angeles&amp;State=CA</p>

<p>and return matching results in the browser's address bar to look like this:</p>

<ul>
<li><code>www.mydomain.com/therapists/Pilates-Training-Los-Angeles-CA.html</code></li>
</ul>

<p>or better yet:</p>

<ul>
<li><code>www.mydomain.com/therapists/pilates-training-los-angeles-ca.html</code></li>
</ul>

<p>Notice the database includes values with one, two or three words + spaces...</p>

<p>For example:</p>

<pre><code>Therapy_Type=Pilates Training &lt;- includes a space

City=Los Angeles &lt;- includes a space

State=CA &lt;- no space
</code></pre>

<p>I used the tool at: <a href="http://www.generateit.net/mod-rewrite/" rel="nofollow">http://www.generateit.net/mod-rewrite/</a> to generate the following RewriteRule:</p>

<pre><code>RewriteEngine On
RewriteRule ^([^-]*)-([^-]*)-([^-]*)\.html$ /cgi-bin/finda/therapist.cgi?Therapy_Types=$1&amp;City=$2&amp;State=$3 [L]
</code></pre>

<p>This does work (finds the search matches) and generates the results page, but because the parameter values have spaces in them, we end up with a URL that looks like this:</p>

<p>www.mydomain.com/therapists/Pilates%20Training-Los%20Angeles-CA.html</p>

<p>I've spent days in this forum and others trying to find a solution to get rid of these %20 (encoded spaces) so the final returned URL will look like 1) or 2) above.</p>

<p>I know someone on here must know how to do this... Help ;-)</p>

## Answers
### Answer ID: 10409591
<p>If you replace the %20 with -, then how would you know where the therapy type ends and the city starts?</p>

<pre><code>pilates-training-los-angeles-ca
</code></pre>

<p>would be</p>

<pre><code>type=pilates
city=training
state=los
</code></pre>

<p>So I don't think you like to replace the %20 by -. You could however replace it with another character, like _:</p>

<pre><code>pilates_training-los_angeles-ca
</code></pre>

<p>You then would have to translate every _ to a space within your PHP script (or whatever language you are using server side).</p>

