# how to make regexp query faster
[Link to question](https://stackoverflow.com/questions/21450525/how-to-make-regexp-query-faster)
**Creation Date:** 1391067864
**Score:** 0
**Tags:** php, mysql
## Question Body
<p>i have username in my database like abc,abc1,abc2,abc3.
i want to retireve name abc3.
my query is :
select username from users where REGEXP '^abc[0-9]*$' order by userid limit 0,1.</p>

<p>in detail:-
i have to fetch user whose name starts with abc and after that there must be only digits. and the one who have largest digit after abc i have to find that. i know largest userid will have largest digit after abc. so i have to find out all users with username strats with abc and after that contains digiits.</p>

<p>i have to apply this logic to make custom user names.for example if user firstname is ab and lastname is cat. then username will be abc. if abc exists in database then username will be abc1. if abc1 exists in database then username will be abc2.so on...</p>

<p>how to i rewrite my query to make it faster.</p>

## Answers
### Answer ID: 21467097
<p>If you can be sure the first characters are only letters, and afterwards are only numbers, then you might try:</p>

<pre><code> select max(cast(substr(username, length('abc')) as int)) as 'number' from user where username like 'abc%'
</code></pre>

<p>But this woudn't work if there might be an user like <code>abc1def0</code>, because this would return the number 10 in the query above (when mysql converts strings to integers it drops anything that is not a digit and then converts the result).</p>

<p>You should also create an index for the username column, if you don't have one already.</p>

<p><em><strong>Update</em></strong> </p>

<p>This wouldn't work if you have a bigger textual part, like <code>abcd11</code> -- for that you need an extra check, like <code>where username like 'abc%' and length(username)=length( cast(substr(username, length('abc')) as int))</code>.</p>

<p>But that might not be faster than a regex...</p>

### Answer ID: 21450664
<p>You can use the LIKE query. <code>LIKE 'abc%'</code>.</p>

