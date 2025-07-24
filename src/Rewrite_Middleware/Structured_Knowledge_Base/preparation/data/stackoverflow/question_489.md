# Sugar CRM - MYSQL show contacts with same email address
[Link to question](https://stackoverflow.com/questions/28277739/sugar-crm-mysql-show-contacts-with-same-email-address)
**Creation Date:** 1422879935
**Score:** 1
**Tags:** mysql, sugarcrm
## Question Body
<p>If I search in Sugar CRM I can find some email addresses which have been assigned to multiple contacts - I do not want this. I wish to have a SQL query which will list any email addresses which have been associated to multiple contacts. So in otherwords, list all Sugar Contacts which have the same email addresses. </p>

<p>I have tried various queries but am getting stuck. The following query will allow me to find a bunch of contacts where the </p>

<pre><code>SELECT ea.email_address, eabr.* FROM email_addr_bean_rel eabr
INNER JOIN email_addresses ea ON eabr.email_address_id = ea.id
WHERE ea.email_address = 'joe.bloggs@gmail.com'
AND eabr.deleted = 0;
</code></pre>

<p>This is ok, but I have to specify which email account I want to check. </p>

<p>Can anyone help me to rewrite this so that the email address is not specified but the whole database is searched for any email addresses where more than one contact exists?</p>

<p>I'm not sure how to write the above query.</p>

<p>Any pointers would be appreciated.</p>

<p>Thanks</p>

<p>James</p>

## Answers
### Answer ID: 28278290
<p>You may try somethin like this, if you want any duplicate email address:</p>

<pre><code>SELECT ea.email_address, eabr.* FROM email_addr_bean_rel eabr
INNER JOIN email_addresses ea ON eabr.email_address_id = ea.id
WHERE ea.email_address IN
(SELECT ea.email_address FROM email_addr_bean_rel eabr
INNER JOIN email_addresses ea ON eabr.email_address_id = ea.id
WHERE  eabr.deleted = 0
GROUP BY email_address
HAVING count(*) &gt; 1)
AND eabr.deleted = 0;
</code></pre>

### Answer ID: 28278187
<p>First, you <code>join</code> the tables. Next, you filter out elements which are removed. Then, you group by <code>ea.email_address</code>. In consequence, you check whether their number if bigger than 1. Finally, you select the grouped <code>ea.email_address</code> and merge the <code>contact_id</code> values using a separator (<code>':'</code> in this case) using <code>group_contact</code>.</p>

<pre><code>SELECT ea.email_address, GROUP_CONCAT(eabr.contact_id SEPARATOR ':') FROM email_addr_bean_rel eabr
INNER JOIN email_addresses ea ON eabr.email_address_id = ea.id
where eabr.deleted = 0
group by ea.email_address
having count(*) &gt; 1
</code></pre>

<p>Code is not tested.</p>

