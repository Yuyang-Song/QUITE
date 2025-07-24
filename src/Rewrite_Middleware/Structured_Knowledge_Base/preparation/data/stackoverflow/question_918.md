# Do I need to make one sql query for each keyword in a text?
[Link to question](https://stackoverflow.com/questions/4982112/do-i-need-to-make-one-sql-query-for-each-keyword-in-a-text)
**Creation Date:** 1297565142
**Score:** 3
**Tags:** php, sql, mysql
## Question Body
<p>I am working on a content rewriter, basically it will replace words with their synonyms.</p>

<p>I have the synonms in a mySQL database, the table contains 3 columns </p>

<pre><code>id        int(11)
keyword      varchar(50)
synonyms    varchar(255)
</code></pre>

<p>Entries looks like this:</p>

<pre><code>50  slake       abate,slack,decrease,lessen,minify
51  abate       slake,slack,decrease,lessen,minify
52  slack       slake,abate,decrease,lessen,minify
53  decrease    slake,abate,slack,lessen,minify
54  lessen      slake,abate,slack,decrease,minify
55  minify      slake,abate,slack,decrease,lessen
</code></pre>

<p>So my first idea was to first get every word in the text to rewrite (ignoring some keywords in a blacklist), and then making a sql query to see if a synonym for that word exists in the database. But if I have a text with 1000 words, would 1000 sql queries be too much? Also some of the synonyms have 2 words (like "throw away"), so I could end up having to do a lot more queries than word in the text.</p>

<p>Is there a better way to achieve this?</p>

## Answers
### Answer ID: 4982333
<p>I'm not sure SQL is the most appropriate tool for the job here. SQL is designed to work on relations of records, not blocks of text.</p>

<p>If you really had to do it in SQL the best way would probably be as JZD suggested, and make a temporary table for the text. You could have a key that is the index of the word in the text (1st word is 1, second is 2, etc), and then the word.</p>

<p>You could then do a join between the temporary table and the synonym table.  This should all run fairly quickly, as any SQL engine can handle the joins efficiently.</p>

<p>You still won't be able to find synonyms for multiple word phrases. If you restrict yourself to two word phrases, you could load all pairs of words into the database and find them in the same manner as above. It will only double the size of your DB so it should be tractable.</p>

<p><em>EDIT</em>
If you really want to do a robust implementation that can handle multi-word phrases, you should use the Rabin-Karp string finding algorithm.</p>

### Answer ID: 4982149
<p>Wouldn't this be better modelled as as normalised schema:</p>

<pre><code>Word Table:
    id        int(11) 
    word      varchar(50) 

Synonym Table
    WordId     int(11)
    SynonymId  int(11)
</code></pre>

<p>The synonyms for a word are then, for instance:</p>

<pre><code>Select W2.Word 
from SynonymTable S
join WordTable W on S.WordId = W.Id
join WordTable W2 on S.SynonymId = W2.Id
where W.word = 'slake' 
</code></pre>

<p>Create an indexes on WordTable(Word), SynonymTable(WordId) and SynonymTable(SynonymId)  </p>

<p>There are several reasons for using this approach:</p>

<ul>
<li>Flexible: No limit of number of synonyms per word</li>
<li>Efficient: Due to normalisation, the Row sizes are very small, so many rows fit into each database page, making more pages fit into available memory</li>
</ul>

### Answer ID: 4982148
<p>If the number of rows is small enough, pull all the values from your database into memory and access them directly.  Also you could insert your text into a temp table in the database and possibly run one query to replace the words.</p>

