# Is there a better way to run this mysql update?
[Link to question](https://stackoverflow.com/questions/10163258/is-there-a-better-way-to-run-this-mysql-update)
**Creation Date:** 1334502807
**Score:** 1
**Tags:** mysql, insert
## Question Body
<p>I have the following code, which firstly retrieves each unique style from a database and then searches through the products table to find the terms associated with each style and updates the stylerefs table with the styleid and the productid:</p>

<pre><code>$query = "Select id,style,terms from su_styles";

if ($results = $sudb-&gt;query($query)) {

while($result = $results-&gt;fetch_array(MYSQLI_ASSOC)) {

      $id=$result['id'];
      $style=$result['style'];
      $terms=$result['terms'];      

$query= "INSERT IGNORE INTO su_stylerefs (mykey,id) 
    SELECT mykey,$id FROM su_pref where (match(name) against ('$terms' in Boolean Mode)) 
    ON DUPLICATE KEY UPDATE id=$id, mykey = su_pref.mykey";     

$sudb-&gt;query($query);
</code></pre>

<p>Is there anyway I can rewrite this query into one, rather than looping through the results of the first query?  I have 10 other similar queries that need to run every day and some of the tables in the first query could have 100s of records, which mean hundreds of connections to the database, which takes a while.</p>

<p>Thank you in advance</p>

## Answers
### Answer ID: 10163337
<p>I would fetch all these rows first along with the match() case, and then do an update:</p>

<pre><code>INSERT INTO su_stylerefs (mykey, id)
VALUES ($mykey[0], $id[0]), ($mykey[1] $id[1]), ...
ON DUPLICATE KEY UPDATE id=$id, mykey = su_pref.mykey
</code></pre>

<p><strong>2nd solution:</strong></p>

<pre><code>INSERT IGNORE INTO su_stylerefs (mykey,id) 
SELECT sp.mykey, ss.id
FROM su_styles AS ss
INNER JOIN su_pref AS sp
ON match(sp.name) against (ss.terms in Boolean Mode)
ON DUPLICATE KEY UPDATE id = VALUES(id), mykey = VALUES(mykey)
</code></pre>

<p>This may be a better solution.</p>

