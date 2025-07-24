# SELECTing MySQL rows with unusual characters using PHP and querystrings
[Link to question](https://stackoverflow.com/questions/9544143/selecting-mysql-rows-with-unusual-characters-using-php-and-querystrings)
**Creation Date:** 1330757022
**Score:** -2
**Tags:** php, mysql
## Question Body
<p>Table name Styles.
Referenced Column: Style</p>

<p>Coding with PHP 5.</p>

<p>Problem:
My SELECT query to MySQL returns 0 rows.</p>

<p>I'm using the column name in querystring as identifier (something like <code>example.com.php?style=paper-pencils</code>). For SEO purposes I've removed any odd characters and replaced spaces with '-'. Using url rewrite to end up with <code>example.com/paper-pencils</code>.</p>

<p>Working on a database I inherited which uses characters such as <code>'&amp;'</code> or <code>':'</code> in the Style column. On the database side, the Style column would contain a row with something like <code>"Paper &amp; Pencils"</code> as compared to my slugged version of "paper-pencils". </p>

<p>Things I've Tried:
I de-slug the url so i end up with 'paper pencils' (see below in query example).</p>

<p>I tried </p>

<pre><code>SELECT * ,REPLACE( 'Style', '&amp;', ' ' ) AS Style, REPLACE( 'Style', ':', ' ' ) AS Style FROM Styles
WHERE Style = 'paper pencils'
</code></pre>

<p>to no avail. The query I have runs fine, it just comes back with 0 results.</p>

<p>My next step would be to do a PHP SWITCH statement. Something like </p>

<pre><code>case: $_GET['style'] = 'paper-pencils' 
</code></pre>

<p><code>$DBstyle = 'Paper &amp; Pencils'</code> but I feel like there has to be some other way around it. I have 30 different possibilities and would prefer something better.</p>

<p>Any suggestions on how I can account for these unusual characters with random occurrences?</p>

## Answers
### Answer ID: 9544233
<p>Just like Gohn said or, a better one - use an approach which is used on this site - have both an unique identifier and a slug in the url.</p>

<pre><code>example.com/2356356/paper-pencils
</code></pre>

<p>will cajole SEO and make your life easy.</p>

### Answer ID: 9544195
<p>Maybe you can add another column to this table called style_slug. This column will contain the slugged version that you use in your urls and will allow you to retrieve the Style column in your query.</p>

