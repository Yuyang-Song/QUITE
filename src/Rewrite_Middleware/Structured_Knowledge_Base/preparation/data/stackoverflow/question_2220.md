# MySQL queries, selecting field from one of many databases
[Link to question](https://stackoverflow.com/questions/24452711/mysql-queries-selecting-field-from-one-of-many-databases)
**Creation Date:** 1403874681
**Score:** 0
**Tags:** mysql, database, left-join
## Question Body
<p>I have a <code>remarks</code> table which can be linked to any number of other items in a system, in the case of this example we'll use <code>bookings</code>, <code>enquiries</code> and <code>referrals</code>.</p>

<p>Thus in the <code>remarks</code> table we have columns</p>

<pre><code>remark_id | datetime    | text | booking_id | enquiry_id | referral_id
1         | 2014-06-28  | abc  | 0          | 8          | 0
2         | 2014-06-27  | def  | 3          | 0          | 0
2         | 2014-05-31  | ghi  | 0          | 0          | 10
</code></pre>

<p>Etc...</p>

<p>Each of the <em>item</em> tables will have a field called <code>name</code>. Thus when I want to select a remark the likelihood is I'll need this name.</p>

<p>I'd like to achieve this with a single query, getting a 2d array as follows:</p>

<pre><code>['remark_id'=&gt;1, 'datetime'=&gt;'2014-06-28', 'text'=&gt;'abc', 'name'=&gt;'Harold']
</code></pre>

<p>However the query I'd expect to use would be</p>

<pre><code> SELECT r.remark_id,r.datetime,r.text
 ,b.name AS book,rr.name AS referral,e.name AS enquiry
 FROM remarks AS r
 LEFT JOIN bookings AS b ON b.book_id=r.book_id
 LEFT JOIN referrals AS rr ON rr.referral_id=r.referral_id
 LEFT JOIN enquiries AS e ON e.enquiry_id=r.enquiry_id
</code></pre>

<p>Leaving me with the output</p>

<pre><code>['remark_id'=&gt;1, 'datetime'=&gt;'2014-06-28', 'text'=&gt;'abc', 'book'=&gt;'Harold', 'referral'=&gt;'', 'enquiry'=&gt;'']
</code></pre>

<p>And more processing to do before or during rendering it to a view.</p>

<p>Is there a way to write a query such that it would fill a field from the first <code>NOT NULL</code> string it encountered in one of the joined tables?</p>

<p><em>Please only suggest using a different database system if you <strong>know</strong> that <code>MySQL</code> doesn't provide any way to do what I'm asking. If it's the case it can't be done there's no business sense in rewriting the system anyway, but I'd like to ask!</em></p>

## Answers
### Answer ID: 24453714
<p>Two ways I can think of:</p>

<ol>
<li><p>use UNION:</p>

<pre><code>SELECT remark_id, datetime, text, name
FROM remarks
JOIN bookings ON (remarks.book_id = bookings.book_id)
UNION 
SELECT remark_id, datetime, text, name
FROM remarks
JOIN referrals ON (remarks.referral_id = referrals.referral_id)
UNION
SELECT remark_id, datetime, text, name
FROM remarks
JOIN enquiries ON (remarks.enquiry_id = enquiries.enquiry_id)&lt;/code&gt;
</code></pre></li>
<li><p>use IFNULL (probably much slower):</p>

<pre><code>SELECT r.remark_id,r.datetime,r.text,
IFNULL(b.name,IFNULL(rr.name,e.name)) AS name
FROM remarks AS r
LEFT JOIN bookings AS b ON b.book_id=r.book_id
LEFT JOIN referrals AS rr ON rr.referral_id=r.referral_id
LEFT JOIN enquiries AS e ON e.enquiry_id=r.enquiry_id&lt;/code&gt;
</code></pre></li>
</ol>

<p>Variant 2 is really much slower because of the <code>LEFT JOIN</code>s.</p>

<p>Also, generally I would not recommend using <code>0</code> as value for non-existent links, rather use <code>NULL</code>. This will allow MySQL to speed up the join.</p>

### Answer ID: 24453486
<p>Seems quite messy that you have multiple unused columns for each entry, unless I'm not understanding correctly. If you add more tables, you'd have to adjust each of the views so that it would filter out the new table. </p>

<p>I'd be tempted to redesign your structure so that each of the tables has a remarkgroup_id column, then add the following remark table</p>

<p>remark_id, remarkgroup_id, date, message</p>

<p>This would clean up the extra unused columns and allow you to use simple joining logic.</p>

### Answer ID: 24452862
<p>one way to achieve this is with nested if statements:</p>

<pre><code>if(b.name is not null, b.name, if(rr.name is not null, rr.name, e.name)) as name
</code></pre>

<p>one drawback is that this gives an implicit priority to books? not sure if that would be an issue.</p>

<p>perhaps the main drawback, though, is that this is kind of "magical" and has goofy syntax so it might be more clear to just handle those cases in the controller after all.</p>

