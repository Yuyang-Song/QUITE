# Sphinxsearch ignore_chars and exceptions work around
[Link to question](https://stackoverflow.com/questions/21944847/sphinxsearch-ignore-chars-and-exceptions-work-around)
**Creation Date:** 1393015713
**Score:** 0
**Tags:** mysql, sphinx
## Question Body
<p>I have an exceptions file which breaks the functionality of the ignore_chars directive.</p>

<p>The example keyword I am working with is <code>t-shirt</code>. </p>

<p><code>t-shirt</code> appears in the database. I need the ignore_chars directive to ignore the <code>-</code> so users can search like <code>tshirt</code> or <code>t-shirt</code> and get the same results.</p>

<p>The result of <code>CALL KEYWORDS('tshirt t-shirt', 'catalog')</code> here is </p>

<pre><code>+-----------+------------+
| tokenized | normalized |
+-----------+------------+
| tshirt    | TXRT       |
| tshirt    | TXRT       |
+-----------+------------+
</code></pre>

<p>To get <code>t shirt</code> to map to the above results, I have created an exceptions file which looks like this:</p>

<pre><code>t shirt &gt; tshirt
</code></pre>

<p>When I do the query <code>CALL KEYWORDS('t shirt tshirt t-shirt', 'catalog')</code> this is what I get:</p>

<pre><code>+-----------+------------+
| tokenized | normalized |
+-----------+------------+
| tshirt    | TXRT       |
| tshirt    | TXRT       |
| shirt     | XRT        |
+-----------+------------+
</code></pre>

<p>What I expected to happen was the exceptions file would rewrite the 'words' <code>t shirt</code> to the individual keyword <code>tshirt</code> and all 3 tokens would have the same normalized value.</p>

<p>Except now the <code>-</code> in the <code>t-shirt</code> keyword isn't ignored and it just maps to <code>shirt</code>, which results in a completely different normalized version than <code>tshirt</code>. On top of this, searching with any of the related keywords above returns 0 results.</p>

<p>When I take out the exceptions file, the ignore_chars work fine and search works again for the keywords.</p>

## Answers
### Answer ID: 21946444
<p>The reason I went down this path was because I couldn't get the wordform <code>t shirt &gt; tshirt</code> to work.</p>

<p>Wordforms are applied after being tokenized and I thought this was the reason it did not work.</p>

<p>It turns out that my <code>min_word_len</code> was set to <code>3</code>, so the <code>t</code> in <code>t shirt</code> was not getting read properly. I reduced the <code>min_word_len</code> to <code>1</code> and now the wordform works properly.</p>

<p>This still does not solve the issue with <code>ignore_chars</code> and <code>exceptions</code>, but the search term works now, so I suppose this was the work around I needed.</p>

