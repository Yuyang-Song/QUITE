# SQLite query, &#39;LIKE&#39;
[Link to question](https://stackoverflow.com/questions/12613926/sqlite-query-like)
**Creation Date:** 1348718772
**Score:** 18
**Tags:** sql, sqlite, sql-like
## Question Body
<p>I am trying to retrieve information from my database.<br>
I have words like <code>Lim Won Mong</code> and <code>Limited</code>.</p>

<p>If I do my query, <code>SELECT name FROM memberdb WHERE name LIKE '%LIM%'</code>, it displays both <code>Lim Won Mong</code> and <code>Limited</code> and I only want data from <code>Lim Won Mong</code>.</p>

<p>How should I rewrite my query?</p>

## Answers
### Answer ID: 12613969
<p>Try this one:</p>

<pre><code>SELECT name 
FROM MEMBERDB 
WHERE name LIKE 'LIM %' OR name LIKE '% LIM'
OR name LIKE '% LIM %' OR name LIKE 'LIM';
</code></pre>

<p>Suppose you have data something like this:</p>

<pre><code>'LIMITED'
'Lim Won Mong'
'Wang Tat Lim'
'ELIM TED'
'lim'
'Wang LIM tim'
</code></pre>

<p>This query will return you only following data:</p>

<pre><code>'Lim Won Mong'
'Wang Tat Lim'
'lim'
'Wang LIM tim'
</code></pre>

<h1><a href="http://sqlfiddle.com/#!7/96f9c/2" rel="noreferrer">See this SQLFiddle</a></h1>

### Answer ID: 12613973
<p>If you want to match the word "lim" (so it matches "a lim", "lim a", "a lim a", and "lim", but not "limit" or "alim"), you can use the SQL <code>REGEXP</code> keyword, and use word boundaries (<code>[[:&lt;:]]</code> and <code>[[:&gt;:]]</code>). These match whitespace (spaces, tabs, newlines), string start/end, and some punctuation, as well.</p>

<p>Something like this:</p>

<pre><code>SELECT name FROM memberdb WHERE name REGEXP '[[:&lt;:]]LIM[[:&gt;:]]'
</code></pre>

<p>Note that <code>REGEXP</code> is NOT case-sensitive (unless using binary strings).</p>

<p>If you want it to match ONLY spaces, you can still use <code>REGEXP</code>; this will match either the start of the string or a space, then "lim", then a space or the end of the string:</p>

<pre><code>SELECT name FROM memberdb WHERE name REGEXP '(^| )LIM( |$)'
</code></pre>

<p>Both solutions have been tested on SQL versions which support <code>REGEXP</code> (SQLite 3+; all of Android uses 3.5.9 or higher).</p>

### Answer ID: 12613978
<p>Execute following Query:</p>

<pre><code>select name from memberdb where name like '% LIM %' OR name like "LIM %" OR name like "% LIM" OR name like "LIM"
</code></pre>

