# Avoiding race conditions in TypeORM
[Link to question](https://stackoverflow.com/questions/67384331/avoiding-race-conditions-in-typeorm)
**Creation Date:** 1620129488
**Score:** 3
**Tags:** typescript, typeorm
## Question Body
<p>I'm working on a code base that uses TypeORM and we have a table where we keep a user's balance information.</p>
<p>Here's what our code kind of looks like:</p>
<pre class="lang-js prettyprint-override"><code>async updateAccountInfo(account: Account, tx: Transaction) {
  if (tx.type == 'credit') {
    account.balance = account.balance + amount
  }
  else if (tx.type == 'debit') {
    account.balance = account.balance - amount
  }

  await this.accountRepo.save(account)
}
</code></pre>
<p>The problem is we're starting to get race conditions when transactions come in at the same time and we end up getting the wrong balance (there is a lot more that the code does like updating the ledger, etc but I can't post it here and don't think it's pertinent to the question).</p>
<p>Is it possible to rewrite this so that I can leverage the database (mysql) instead to make the calculation so I can hopefully avoid the race condition but also without having to use the query builder.</p>
<p>ie. on sequelize, you may be able to do something like</p>
<pre class="lang-js prettyprint-override"><code>account.udpate({ 
  balance: Sequelize.literal(`balance + ${amount}`), 
  where: { id: account.id } 
})
</code></pre>
<p>On typeORM, however, I'm not sure how to do this and I couldn't find anything about it in the documentation. Any help would be great.</p>

