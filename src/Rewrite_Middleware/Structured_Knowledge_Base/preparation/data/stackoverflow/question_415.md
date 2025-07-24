# Hidden condition to all possible queries
[Link to question](https://stackoverflow.com/questions/25361843/hidden-condition-to-all-possible-queries)
**Creation Date:** 1408359950
**Score:** 1
**Tags:** sql, postgresql
## Question Body
<p>I'd like to hide selecting objects not by rewriting all SQL queries but by more simple way.</p>

<p>So, I'd like to add a rule (or something else) to a database for a particular table. E.g. if we delete a user from a website we execute something like the next:</p>

<pre><code>UPDATE user_common SET is_deleted='t' WHERE user_id=1234
</code></pre>

<p>And there are no need to rewrite all existing queries about users, the condition is hidden:</p>

<pre><code>SELECT first_name, second_name FROM user_common WHERE coins&gt;200
</code></pre>

<p>The SELECT above will be executed with a hidden condition, e.g.:</p>

<pre><code>SELECT first_name, second_name FROM user_common WHERE coins&gt;200 AND is_deleted!='t'
</code></pre>

<p>How to make it working?</p>

## Answers
### Answer ID: 25365560
<p>As <a href="https://stackoverflow.com/a/25361960/1104979">@Gordon</a> pointed out in his answer, you can use a view to hide the deleted rows, and (as of Postgres 9.3, at least) changes to this view will be automatically applied to the underlying table.</p>

<p>But you can take this a step further, transforming <code>DELETE</code>s on the view into <code>UPDATE</code>s of the base table's <code>is_deleted</code> flag, using Postgres' <a href="http://www.postgresql.org/docs/9.3/static/sql-createrule.html" rel="nofollow noreferrer">rule system</a>. If you exclude <code>is_deleted</code> itself from the view, it should be pretty much indistinguishable from a "normal" table.</p>

<pre><code>CREATE TABLE user_common_base
(
  user_id SERIAL PRIMARY KEY,
  first_name TEXT,
  second_name TEXT,
  coins INTEGER,
  is_deleted BOOLEAN DEFAULT false
);

CREATE VIEW user_common AS
  SELECT
    user_id,
    first_name,
    second_name,
    coins
  FROM user_common_base
  WHERE NOT is_deleted;

CREATE RULE user_common_delete AS
ON DELETE TO user_common
DO INSTEAD
  UPDATE user_common_base
  SET is_deleted = true
  WHERE id = OLD.id;
</code></pre>

### Answer ID: 25361960
<p>You can accomplish what you want with a view.</p>

<pre><code>create view v_table
    select uc.*
    from user_common uc
    where is_deleted &lt;&gt; 't';
</code></pre>

<p>The key is that references to the table really need to change to the view.  One way to do this is by renaming the table and then creating a view with the same name:</p>

<pre><code>alter table user_common to base_user_common;

create view user_common as
    select uc.*
    from user_common uc
    where is_deleted &lt;&gt; 't';
</code></pre>

