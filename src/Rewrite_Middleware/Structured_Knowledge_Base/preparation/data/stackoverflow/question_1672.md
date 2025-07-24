# MySQL Multiple Left Outer Join Query Question involving 3 tables
[Link to question](https://stackoverflow.com/questions/3469643/mysql-multiple-left-outer-join-query-question-involving-3-tables)
**Creation Date:** 1281629069
**Score:** 10
**Tags:** mysql
## Question Body
<p>Due to 0 responses, I'm guessing that my LEFT JOIN question got into too much detail about a database that was too esoteric.  I've already programmed around the issue, but I'd still like to know how to join in a similar scenario:</p>

<p>Assume a basic surrogate key strategy (each table has an id field that just auto-increments), as well as a foreign key to its obvious parent. Words in all caps can be considered tables.</p>

<p>Say you have a Database containing DOGS. Example: Wolfie, Winston, Butch, and Benny</p>

<p>Each DOG has FLEAs. (for simplicity lets make it so that one flea lives on only one dog and leave this a 1 to many relationship).  The fleas have id's as names or whatever, along with what <em>color</em> they are.</p>

<p>Each FLEA will BITE it's DOG host several times, and that is stored in this database, and recorded daily.<br>
Fields id(PK), flea id(FK), date, times_bitten.</p>

<p>Say you want to get the total number of times each dog was bitten (this is easy)</p>

<pre><code>SELECT Dog.Name, sum(Bite.times_bitten)
FROM Dog, Flea, Bite
WHERE Dog.id = Flea.Dog_id and Bite.id = Flea.Bite_id
GROUP BY Dog.Name
</code></pre>

<p>Let's say that you were to add criteria to the "WHERE" clause limiting it to "Brown" fleas, and no "Brown" Fleas ever bit Benny.  </p>

<pre><code>SELECT Dog.Name, sum(Bite.times_bitten)
FROM Dog, Flea, Bite
WHERE Dog.id = Flea.Dog_id and Bite.id = Flea.Bite_id and Flea.color = "Brown"
GROUP BY Dog.Name
</code></pre>

<p><strong>Benny is not in the result</strong></p>

<p>How would you rewrite the query so that Benny's name would still show up, with either a 0(preferably) or NULL in the sum filed, rather than just having Benny eliminated altogether from the result?</p>

<p>This seems like its about multiple left outer joins..  but with multiple tables like this, the documentation that's readily findable doesn't seem to answer a question involving 3 tables with a value filter in the middle of the 3 tables.</p>

<p>Does anyone have advice on how to rewrite this to allow for multiple left outer joins, or have some other <strong>method of keeping all of the dog's names in the query even if the sum = 0?</strong></p>

## Answers
### Answer ID: 3559401
<p>This should work:</p>

<pre><code>SELECT Dog.Name, COALESCE(SUM(Bite.times_bitten), 0) AS times_bitten
FROM Dog
LEFT JOIN Flea
  ON Flea.Dog_id = Dog.id
    AND Flea.color = "Brown"
LEFT JOIN Bite
  ON Bite.id = Flea.Bite_id
GROUP BY Dog.Name
</code></pre>

<p>By using <code>LEFT JOIN</code>s, you will pull all the Dog records, even those without corresponding Fleas (for which the columns from the join will be NULL). You can use <a href="http://dev.mysql.com/doc/refman/5.6/en/comparison-operators.html#function_coalesce" rel="noreferrer"><code>COALESCE</code></a> to set <code>times_bitten</code> to 0 if no records are found (otherwise it would be NULL).</p>

<p>You probably also want to group by <code>Dog.id</code> instead of <code>Dog.Name</code> (unless it is impossible for there to be multiple dogs with the same name?)</p>

