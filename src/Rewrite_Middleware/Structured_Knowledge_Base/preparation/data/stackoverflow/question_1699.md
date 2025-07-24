# Handling transactions in the real world
[Link to question](https://stackoverflow.com/questions/4394697/handling-transactions-in-the-real-world)
**Creation Date:** 1291867180
**Score:** 3
**Tags:** php, mysql, transactions
## Question Body
<p>I'm rewriting this question because it got no responses.</p>

<p>I'm trying to figure out the correct way to work with db transactions. Everything I see about how to do transactions is very basic, along the lines of:</p>

<ol>
<li>query "begin" to start transaction</li>
<li>run your queries.</li>
<li>if everything ran fine, commit transaction.</li>
</ol>

<p>I get that, but it's error (deadlock) handling I don't get. I've heard of two options:</p>

<ol>
<li>Show the user an error and say "try again"</li>
<li>Try again on the spot until it succeeds.</li>
</ol>

<p>To me, telling the user to try again because of a technical issue like this seems bad - do real applications do this regularly? Is that the "oops, something went wrong" one-off errors I sometimes see? This is for a website, so users shouldn't even be aware of the database.</p>

<p>So I have a few questions:</p>

<ol>
<li>Which failure handling approach should I take with data involving multiple users at once?</li>
<li>If I do the "instant retry" option, what does that entail for a complex PHP script? Restart the whole request from the top? I'm worried this will cause more problems than it solves.</li>
<li>Is there a third option I haven't seen?</li>
</ol>

## Answers
### Answer ID: 4832670
<p>There's a couple things listed here that you didn't mention:</p>

<p><a href="http://dev.mysql.com/doc/refman/5.0/en/innodb-deadlocks.html" rel="nofollow">http://dev.mysql.com/doc/refman/5.0/en/innodb-deadlocks.html</a></p>

### Answer ID: 4832506
<p>The solution I use is having a retry loop, let's say 3 (I don't think I get more than 1 retry in real life of most apps). In this loop all the request of the transaction must be done, i.e. write request but as well read requests.</p>

<p>One very important point is to do theread requests <strong>inside</strong> the transaction as this set the locks and it is the only way to have the data at th ereal isolation level.</p>

<p>Then all these requests are in a begin/commit block, with a try/catch. In the catch section I run the rollback and I rethrow the exception.</p>

<p>By re-throwing the exception you can catch it in higher level, which is the level where you can decide to re-run (the 3 times loop) or send it to the user.</p>

<p>Depending on the way your application is coded there are several solutions to handle this in a nice way:</p>

<ul>
<li>using a transactionManager object responsible for begin/commit/rollack, all queries in the transaction</li>
<li>get rules, like 'all transaction are handled by controllers, no DAO or DB-level object knows if there is a transaction running</li>
<li>you can even use a dedicated database connection (with write privileges) that only the transactionManager use, and keep the original read-only database connexion for the other things. </li>
</ul>

### Answer ID: 4832437
<p>A deadlock during a transaction would usually indicate that you were trying to update something that someone else also updated at the same time as you.  Exactly how you handle that would be specific to the operation that the user was performing.</p>

<p>In some cases it wouldn't be a problem and you would retry the operation, but I would think that in most cases you would generate an error to the user since you have know way of knowing which update was the "correct" one.</p>

