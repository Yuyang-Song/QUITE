# MySQL 2 queries combine into 1 query - self referencing
[Link to question](https://stackoverflow.com/questions/67854297/mysql-2-queries-combine-into-1-query-self-referencing)
**Creation Date:** 1622931027
**Score:** 0
**Tags:** mysql, select, count
## Question Body
<p>We have build a very simple referral system that tracks userID's without cookies and referrals for social media. I am trying to create something like a 'leader board' so I can show the UserID of the top leaders in the database.</p>
<p>I'm trying to combine these 2 queries into 1 query.</p>
<pre><code>SELECT
Count(users.AffiliateID) AS affiliate,
users.AffiliateID
FROM
users 
group by affiliateID
order by affiliate desc
</code></pre>
<p>This generates an output where the variable 'affiliate' contains the USERID of the top referring affiliate.  In this case the #1 person is affiliateID = 5297dc41331235</p>
<p>What I then do is look up the name of the person with this query.</p>
<pre><code>Select name from users where UserIDHash = &quot;5297dc41331235&quot;;
</code></pre>
<p>How can I rewrite the query above so that it looks up the value of the name field as a column that references the value of the AffiliateID i.e.  where AffiliateID=UserIDHash on each record?</p>
<p>Your help is greatly appreciated.
Thanks!</p>

