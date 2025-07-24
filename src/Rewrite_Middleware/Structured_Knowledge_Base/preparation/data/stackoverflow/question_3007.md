# REGEX alternative
[Link to question](https://stackoverflow.com/questions/61999866/regex-alternative)
**Creation Date:** 1590400106
**Score:** 0
**Tags:** mysql, regex
## Question Body
<p>Any guy can find the alternative way to rewrite the 2 REGEXs below without the question mark (?).</p>

<pre><code>^(?:2131|1800|35\d{3})\d{11}$
^4[0-9]{12}(?:[0-9]{3})?$
</code></pre>

<p>Or, can you suggest how to make a query for search VISA and JCB card pattern with SQL language.</p>

<p>I just want to make a query to search card pattern inside my database. I try to use the regular expression to done this. Unfortunately, POSIX regexes don't support using the question mark <code>?</code> as a non-greedy (lazy) modifier to the star and plus quantifiers like PCRE (Perl Compatible Regular Expressions). This means you can't use <code>+?</code> and <code>*?</code>.</p>

## Answers
### Answer ID: 62000074
<p>In MySQL versions before v.8, you need to use POSIX ERE like regex syntax, that is:</p>

<ul>
<li>You can't use non-capturing groups</li>
<li>You can't use <code>\d</code> shorthand character class for digits, you need to use <code>[[:digit:]]</code> or <code>[0-9]</code></li>
<li>You won't be able to use lazy quantifiers, but your patterns do not contain them. In some cases, they can be replaced with negated bracket expressions (e.g. <code>a.*?b</code> is better written as <code>a[^ab]*b</code>).</li>
</ul>

<p>In your case, you need to replace <code>(?:</code> with <code>(</code> and replace <code>\d</code> with <code>[0-9]</code></p>

<pre><code>^(2131|1800|35[0-9]{3})[0-9]{11}$
^4[0-9]{12}([0-9]{3})?$
</code></pre>

### Answer ID: 61999913
<p>You drop the question mark in <code>(?:</code> that makes it a normal group.</p>

<p>instead of the <code>)?</code> use <code>){0,1}</code></p>

