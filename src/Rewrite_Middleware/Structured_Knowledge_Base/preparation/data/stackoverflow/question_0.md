# Is there a &#39;one-shot&#39; way to pull data from MySql using Perl?
[Link to question](https://stackoverflow.com/questions/10000530/is-there-a-one-shot-way-to-pull-data-from-mysql-using-perl)
**Creation Date:** 1333483490
**Score:** -2
**Tags:** mysql, perl, dbi
## Question Body
<p>I have a MySql database that contains all the text for a multilingual website, with each different language in a separate column. (For example, the column 'en', id 1 = 'Hello', column 'fr', id 1 = 'Bonjour', and so on)</p>

<p>I am using a Perl/DBI script that pulls the text from the database according to the user language and required section in the usual way by preparing a query, executing the query, then copying the resulting records to an array. This all seems terribly cumbersome and inefficient to me though.</p>

<p>Here's the business end of what I'm using now.</p>

<pre><code>omy (@TEXT, $getText);
$getText = $dbh-&gt;prepare("SELECT `$language` FROM text WHERE Page_Section = ? ORDER BY line_number");
$getText-&gt;execute('Section_Name');
while($_ =  $getText-&gt;fetchrow_array){push(@TEXT, $_)};
$getText-&gt;finish;

print qq~
&lt;p&gt;$TEXT[0]&lt;/p&gt;
&lt;p&gt;$TEXT[1]&lt;/p&gt;
&lt;p&gt;$TEXT[2]&lt;/p&gt;
~;
</code></pre>

<p>The problem with this method for me is, what if I want to delete one of those lines from the database, or add in a few new lines? It messes up the whole script which is only incrementing 'blindly' through the array from the beginning. In this example, if I deleted the second row in the database and wanted to insert two new lines, I would have to rewrite the relevant parts of the script, otherwise it will print in the wrong order.</p>

<p>I could of course pull each line of text by 'absolute' ID, but that requires a separate 'execute' statement and 'fetchrow_array' line for every bit of text that I want.</p>

<p>Is there a neater way, like a one-shot 'pull and print' method where I just can grab single fields and output them according to ID? Something like.. (warning - pseudo-code cometh)</p>

<pre><code>$query = $dbh-&gt;prepare(SELECT 'language' FROM 'text' WHERE 'id' = ?);

print qq~
&lt;p&gt;$query-&gt;execute(0)&lt;/p&gt;
&lt;p&gt;$query-&gt;execute(1)&lt;/p&gt;
&lt;p&gt;$query-&gt;execute(2)&lt;/p&gt;
~;
$query-&gt;finish;
</code></pre>

<p>You get the idea.. ;)
Is something like this possible? Thanks in advance!</p>

## Answers
### Answer ID: 10000913
<p>Yes, it's most definitely possible. They're called "subroutines".</p>

<pre><code>sub selectrow_array {
   my $sth = shift;
   $sth-&gt;execute(@_)
      or return ();
   my $row = $sth-&gt;fetch();
      or return ();
   $sth-&gt;finish()
      or return ();
   return @$row;
}

my $sth = $dbh-&gt;prepare(q{SELECT 'language' FROM 'text' WHERE 'id' = ?});

for my $i (0..2) {
   printf "&lt;p&gt;%s&lt;/p&gt;\n", selectrow_array($sth, $i);
}
</code></pre>

<hr>

<p>That said, such a sub already exists (although it has slightly different syntax) as a method of <code>dbh</code>.</p>

<pre><code>my $sth = $dbh-&gt;prepare(q{SELECT 'language' FROM 'text' WHERE 'id' = ?});

for my $i (0..2) {
   printf "&lt;p&gt;%s&lt;/p&gt;\n", $dbh-&gt;selectrow_array($sth, undef, $i);
}
</code></pre>

