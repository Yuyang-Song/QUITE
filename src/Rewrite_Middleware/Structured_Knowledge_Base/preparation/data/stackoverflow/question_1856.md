# How to prevent PostgreSQL full text search parser rewriting symbols to spaces?
[Link to question](https://stackoverflow.com/questions/10258508/how-to-prevent-postgresql-full-text-search-parser-rewriting-symbols-to-spaces)
**Creation Date:** 1335007780
**Score:** 0
**Tags:** ruby-on-rails, postgresql, full-text-search
## Question Body
<p>My problem is that the <a href="http://en.wikipedia.org/wiki/PL/pgSQL" rel="nofollow">PL/pgSQL</a> parser treats symbols like '#' or '+' as space symbols (which is OK) hence the queries like 'C++' or 'C#' or 'PL/SQL' are parsed like so:</p>

<pre><code> asciiword | Word, all ASCII | C     | {english_stem}        | english_stem | {c}
 blank     | Space symbols   | #     | {thesaurus_en,simple} | simple       | {#}
</code></pre>

<p>I'm trying to find a best way to handle this kind of queries. I've been trying to accomplish that by using the thesaurus dictionary, but it doesn't look like it could possibly work.</p>

<p>What I'm thinking of is something that rewrites "C#" to "CSHARP" while writing to the database (since I guess "C#" would be indexed as "C") and something that would do the same while searching.</p>

<p>I could possibly do it on my web application side, but it just doesn't seem right.</p>

<p>How would I handle that or what PL/pgSQL triggers could I possibly use for the approach I'm thinking of?</p>

## Answers
### Answer ID: 30874556
<p><em>(Posted on behalf of the OP.)</em></p>

<p>For future reference, there's a great guide on creating tsearch parser here: <a href="http://www.sai.msu.su/~megera/postgres/gist/tsearch/V2/docs/HOWTO-parser-tsearch2.html" rel="nofollow">http://www.sai.msu.su/~megera/postgres/gist/tsearch/V2/docs/HOWTO-parser-tsearch2.html</a></p>

<p>Anyway, the solution suggested by Richard works just fine and required much less effort.</p>

### Answer ID: 10260335
<p>Well, you could write your own parser (in C) but that's probably more effort than you wanted to go to.</p>

<p>You could do something like:</p>

<pre><code>to_tsvector('english', my_transformer(document_text)) 
...
to_tsquery('english', my_transformer(query_text))
</code></pre>

<p>You don't need to transform the actual literal document text, just the tsvector index and the query. You can do this in the index-definition too (but my_transformer needs to be an immutable function).</p>

<p>The question then becomes what the simplest/most efficient way to transform the incoming text is. If you're already using plperl/pltcl then you could probably do some clever regex replacement. If not, try several simpler regex replacements in plpgsql or even plsql. There are always fiddly corner-cases with this sort of thing though, so make sure you test your replacements thoroughly.</p>

