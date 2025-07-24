# Trigger to cancel transaction
[Link to question](https://stackoverflow.com/questions/30058824/trigger-to-cancel-transaction)
**Creation Date:** 1430844563
**Score:** 1
**Tags:** sql, oracle-database, triggers, oracle11g, transactions
## Question Body
<p>I have to enforce a rule based on a relatively complex query involving four tables. If any of the tables updates/inserts/deletes, I need to run the same query to check if the operation should be denied (by throwing an exception).</p>

<p>I think there must be four separate triggers because it seems that CREATE TRIGGER only accepts a single "on" clause; but I don't want to repeat the query, rather keeping it in a separate stored procedure.</p>

<p>I wonder if there is a way for the verification query to be given a representation of the database state as it would be after the event firing the trigger; and have the query be able to cancel that transaction if needed, rolling back to the state before the trigger was fired. This isn't what "before/for each row" does, I think; because that uses <code>:new</code> and <code>:old</code> - if I were to use the new row, I would have to rewrite the query four times substituting new in place of each respective table.</p>

<hr>

<p>Adapted answer:</p>

<p>Even if I try my best to be horrible and set autocommit to be on, the 'after statement' trigger does the right thing; i.e. no rows are selected at the bottom of this block.</p>

<pre><code>create or replace trigger test_after_tr
  after insert or update or delete on footable
begin
  raise_application_error(-20000, 'violated');
end;
/

set autocommit on;
begin
  execute immediate 'set autocommit on';
  insert into footable(name) values('fail');
exception when others then null;
end;
/

select * from footable where name = 'fail';
</code></pre>

## Answers
### Answer ID: 30059033
<p>You can see the database state after the statement using an "after statement" trigger (i.e. leaving out the <code>for each row</code> clause).  However you do not have access to <code>old</code> and <code>new</code> in a statement-level trigger.  You can either check that no data in the 4 tables breaks your rules (probably slow), or you can use row-level triggers on each table to record the keys of the affected records in a PL/SQL collection that you can then use to perform more selective queries in the "after statement" trigger.</p>

