# Cannot Access Magento Admin when Site Root not in Domain Root
[Link to question](https://stackoverflow.com/questions/13040131/cannot-access-magento-admin-when-site-root-not-in-domain-root)
**Creation Date:** 1351030251
**Score:** 2
**Tags:** magento, admin
## Question Body
<p>I don't think this question is a duplicate.</p>

<p>There are similar questions, but none addressing this particular cause.</p>

<p>Server is CentOS Apache, PHP 5.3.10</p>

<p>I have 2 copies of the same Magento site. The admin works in one, but not the other.</p>

<p>Where it works, the Magento installation is in the site root:</p>

<p>e.g. <code>www.example.com</code> leads you to the website, and <code>www.example.com/admin</code> brings you to the admin.</p>

<p>But the other copy is in:</p>

<p><code>www.example.com/othersite/</code></p>

<p>So I try to access the admin via <code>www.example.com/othersite/admin</code> but I get a 404 error.</p>

<p>I tried editing app/etc/local.xml so that it reads "othersite/admin" instead of just "admin" but that did not fix the problem. I've restarted apache several times although that should not do anything anyway.</p>

<p>I've seen a solution that involved setting a certain values in the database to '0' in 4 different tables (e.g. in <code>core_store</code>). Those values are already 0 so I didn't run any queries.</p>

<p>Thank you</p>

<p>EDIT:</p>

<p>Also note I tried changing the admin access on the working site to <code>test/admin</code> instead of just <code>admin</code> in <code>local.xml</code>. It didn't work. Changing it to just <code>test</code> did work. Does Magento not allow admin to be located in a subfolder? Is this a url rewrite problem?</p>

