# .htaccess mod_rewrite URL query
[Link to question](https://stackoverflow.com/questions/10059193/htaccess-mod-rewrite-url-query)
**Creation Date:** 1333841181
**Score:** 0
**Tags:** php, .htaccess, mod-rewrite, get
## Question Body
<p>I was hoping someone could help me out. I'm building a CRM application and need help modifying the .htaccess file to clean up the URLs. I've read every post regarding .htaccess and mod_rewrite and I've even tried using <a href="http://www.generateit.net/mod-rewrite/" rel="nofollow">http://www.generateit.net/mod-rewrite/</a> to obtain the results with no success. Here is what I am attempting to do.</p>

<ul>
<li>Let's call the base URL www.domain.com</li>
<li>We are using php with a mysql back-end and some jQuery and javascript</li>
<li>In that "root" folder is my .htaccess file. I'm not sure if I need a .htaccess file in each subdirectory or if one in the root is enough.</li>
<li>We have several actual directories of files including "crm", "sales", "finance", etc.</li>
<li>First off we want to strip off all the ".php" extensions which I am able to do myself thanks to these posts. However, the querying of the company and contact IDs are where I am stuck.</li>
<li>Right now if I load www.domain.com/crm/companies.php it displays all the companies in a list.</li>
<li>If I click on one of the companies it uses javascript to call a "goto_company(x)" jQuery script that writes a form and submit that form based on the ID (x) of the company. This works fine and keeps the links clean as all the end user sees is www.domain.com/crm/company.php. However you can't navigate directly to a company.</li>
<li>So we added a few lines in PHP to see if the POST is null and try a GET instead allowing us to do www.domain.com/crm/company.php?companyID=40 which displays company #40 out of the database.</li>
<li>I need to rewrite this link, and all other associated links to www.domain.com/crm/company/40</li>
<li>I've tried everything and nothing seems to work.  Keep in mind that I need to do this for "contacts" and also on the sales portion of the app will need to do something for "deals".</li>
</ul>

<p>To summarize here's what I am looking to do:</p>

<ol>
<li>Change www.domain.com/crm/dash.php to www.domain.com/crm/dash</li>
<li>Change www.domain.com/crm/company.php?companyID=40 to www.domain.com/crm/company/40</li>
<li>Change www.domain.com/crm/contact.php?contactID=27 to www.domain.com/crm/contact/27</li>
<li>Change www.domain.com/sales/dash.php to www.domain.com/sales/dash</li>
<li>Change www.domain.com/sales/deal.php?dealID=6 to www.domain.com/sales/deal/6</li>
</ol>

<p>(40, 27, and 6 are just arbitrary numbers as examples)</p>

<p>Just for reference, when I used the generateit.net/mod-rewrite site using www.domain.com/crm/company.php?companyID=40 as an example, here is what it told me to put in my .htaccess file:</p>

<pre><code>Options +FollowSymLinks
RewriteEngine On
RewriteRule ^crm/company/([^/]*)$ /crm/company.php?companyID=$1 [L]
</code></pre>

<p>Needless to say that didn't work.</p>

<p><strong>OK here is an updated based on the help received from Gohn67 below</strong></p>

<p>It is working with the exception of a small bug I can't seem to figure out.  I have created the .htaccess file in the "crm" directory. Here is the code:</p>

<pre><code>RewriteEngine On
RewriteRule ^test/([\d]+)$ /crm/company.php?companyID=$1 [L]
</code></pre>

<p>This rewrites www.domain.com/test/40 to www.domain.com/crm/company.php?companyID=40 so it's very close to what I need.</p>

<p>The bug is that I cannot replace "test" with the word "company" in my RewriteRule. I do not know why. I can put anything but the word "company" in there; even the names of other PHP files in the "crm" directory such as "contact" or "add-contact".  As a further test I actually renamed company.php to test.php and changed the RewriteRule to:</p>

<pre><code>RewriteRule ^company/([\d]+)$ /crm/test.php?companyID=$1 [L]
</code></pre>

<p>which worked.</p>

## Answers
### Answer ID: 10059929
<p>Yeah, the generated rewrite looks kind of strange there. I'm not sure what it is trying to match here <code>([^/]*)</code>.</p>

<p>Here is an example that may work for you. I tested these on my system.</p>

<pre><code>RewriteEngine On
RewriteRule ^crm/dash/?$ /crm/dash.php [L]
RewriteRule ^crm/company/([\d]+)/?$ /crm/company.php?companyID=$1 [L]
RewriteRule ^crm/contact/([\d]+)/?$ /crm/contact.php?contactID=$1 [L]
</code></pre>

<p>This is only a few of your routes as an example. I admit that they could be more robust though, because doing this way will lead to a lot of rewrite rules, some of which you could elminate with better regex patterns. But hopefully this gets you started.</p>

<p>Here are some updated rewrite rules taking into consideration a subdirectory. It also fixes a a mistake from above:</p>

<pre><code>RewriteEngine On
RewriteBase /crm
RewriteRule ^dash/?$ dash.php [L]
RewriteRule ^company/([\d]+)/?$ company.php?companyID=$1 [L]
RewriteRule ^contact/([\d]+)/?$ contact.php?contactID=$1 [L]
</code></pre>

