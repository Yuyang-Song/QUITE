# How can I select and block row for each thread in oracle?(There is a working example for PostgreSQL)
[Link to question](https://stackoverflow.com/questions/54125380/how-can-i-select-and-block-row-for-each-thread-in-oraclethere-is-a-working-exa)
**Creation Date:** 1547111970
**Score:** 0
**Tags:** sql, multithreading, oracle-database, select
## Question Body
<p>I have table <code>products</code>:</p>

<pre><code>id  name count description          status  expiration_date
1   Hz    1    Test1537208034036    NEW     2018-09-17
2   Pz    3    Test1537209516789    NEW     2018-10-17
3   Uz    7    Test1537210999618    NEW     2018-08-17
4   Mz    12   Test1537212483215    NEW     2018-11-17
</code></pre>

<p>I need select row with the biggest <strong><em>count</em></strong> and status = <strong><em>NEW</em></strong>. For this I can write on postgreSQL:</p>

<pre><code>Select * 
from products 
where status = 'NEW' 
order by count desc 
LIMIT 1
</code></pre>

<p>But if 4 threads will start doing this select - each thread get equal row(with count = 12). I can rewrite this query and it work fine:</p>

<pre><code>Select * 
from products 
where status = 'NEW' 
order by count desc 
LIMIT 1 
for update of products skip locked 
</code></pre>

<p>But I can not repeat this in <strong>Oracle</strong>. </p>

<pre><code>SELECT p.* 
from (
  Select * 
  from products 
  where status = 'NEW' 
  order by count desc
) p 
WHERE p.ROWNUM = 1 
FOR UPDATE OF products SKIP LOCKED
</code></pre>

<p>Oracle has not <code>LIMIT 1</code> and <code>rownum</code> works differently. I need get first row from <em>ordered</em> table(<code>order by desc</code>) <code>but this row not locked</code>.</p>

<p>How can I repeat logic like PostgreSQL. Maybe my select is wrong. </p>

<p>If you look easier, that's what I want to get - I have table and many threads. I need each thread to receive the oldest row from the database (or the largest count) and only it is one. other threads should not receive it. The next thread should receive the oldest (or largest) row following it.</p>

## Answers
### Answer ID: 54126200
<p>I suggest to use dynamic sql. The lock is acquired at a fetch time. You fetch one record and it is get locked at the same time. Keep in mind that record is unlocked once you finish the transaction - commit or rollback.</p>

<p>Here is the short example of function which returns the next <code>products.id</code> for your thread. </p>

<pre><code>create or replace function get_next_unlocked_id
return number
is
  cRefCursor sys_refcursor;
  rRecord    products%rowtype;
begin
  -- open cursor. No locks so far
  open cRefCursor for 
    'select * from products '||
    'where status = ''NEW'' '||
    'order by count desc '||
    'for update skip locked';

  -- we fetch and lock at the same time one record
  fetch cRefCursor into rRecord;

  -- close cursor
  close cRefCursor;

  -- return ID or any other attribute(s)
  return rRecord.id; 

end;
</code></pre>

