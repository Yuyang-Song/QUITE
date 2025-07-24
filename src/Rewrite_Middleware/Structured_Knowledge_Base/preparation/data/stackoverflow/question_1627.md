# Proving SQL Injection
[Link to question](https://stackoverflow.com/questions/1834396/proving-sql-injection)
**Creation Date:** 1259773960
**Score:** 6
**Tags:** .net, sql, vb.net, sql-injection
## Question Body
<p>I'm trying to simply prove here that this simple function isn't good enough to prevent every sql injection in the world:</p>

<pre><code>Function CleanForSQL(ByVal input As String) As String
    Return input.Replace("'", "''")
End Function
</code></pre>

<p>Here is a typical insert statement from one of our apps:</p>

<pre><code>Database.DBUpdate("UPDATE tblFilledForms SET Text1 = '" + CleanForSQL(txtNote.Text) + "' WHERE FilledFormID = " + DGVNotes.SelectedRows(0).Cells("FilledFormID").Value.ToString)
</code></pre>

<p>I know its not secure, because of googling and looking up other questions on StackOverflow.com.  <a href="https://stackoverflow.com/questions/1800013/does-this-code-prevent-sql-injection/1800447#1800447">Here</a> is one question that I found in which all functions such as the one I presented above are irrelevant and pointless.</p>

<p>So based on the post I linked to, simply typing </p>

<blockquote>
  <p>'Chr(8); update tblMaint SET Value1 = 2 WHERE ValueID = 2--</p>
</blockquote>

<p>into txtNote should be enough to clear every value in text1 in the entire tblFilledForms table, and then update the tblmaint table's second row to be 2 correct? </p>

<p>What SHOULD happen here is that VB will interpret this as </p>

<blockquote>
  <p>UPDATE tblFilledForms SET Text1 = '''Chr(8); update tblMaint SET Value1 = 2 WHERE ValueID = 2--' WHERE FilledFormID = 5120327</p>
</blockquote>

<p>and send it to SQL which will intern execute the Chr(8) to erase the third ' which would produce</p>

<blockquote>
  <p>UPDATE tblFilledForms SET Text1 = ''; update tblMaint SET Value1 = 2 WHERE ValueID = 2--' WHERE FilledFormID = 5120327</p>
</blockquote>

<p>to be actually executed on the database correct?</p>

<p>I then coppied a Chr(8) from the clipboard and replaced the Chr(8) in the textbox with the clipboard contents and still a no-go.  It puts the whole string directly into the field w/o problems.  </p>

<p><strong>So what am I doing wrong here? or what else can I do to break it?</strong></p>

<p>Technologies and background:
I'm using MS SQL Server 2005, and VB .NET 2005.
the Text1 field in the database is a Varchar(600) field (don't ask my why its not MAX, its pointless, i know)
There are certain triggers on the table that would prevent a mass update such as this and throw some errors if the injection actually worked right.</p>

<p>PS. I know parametrized queries are the way to go here and I'm not looking for answers like "well i dunno why it doesn't work, but parametrized queries are the way to go".  I'm looking for the ability to prove that our software is broken and that we need to rewrite it using better principles.</p>

<p>To anyone reading this question to figure out how to better filter your text fields, the answer is DON'T! Use the parameters! they are much better, safer, and easier!</p>

## Answers
### Answer ID: 1834611
<p>Scott Ivey has the classic case that can break it, the lack of quotes protecting a numeric input. (+1'ed that)</p>

<p>Depending on the language and where the string is being 'cleansed' and the database being used your immediate risk is that they language permits the string to be escaped. At that point the single quote you are trying to avoid getting thru goes wrong</p>

<p>\'; DROP yourTable;--  => \''; DROP yourTable;--</p>

<p>That goes into your sql string as </p>

<pre><code>UPDATE tblFilledForms SET Text1 = '" + \''; DROP yourTable;-- + ' etc.
</code></pre>

<p>Which is then:</p>

<pre><code>UPDATE tblFilledForms SET Text1 = '\''; DROP yourTable;-- ' etc.
</code></pre>

<p>'\'' is taken as the literal string of a single quote, if your database supports escaped characters - bingo your compromised.</p>

<p>Equally the protection has to be remembered to be effective, even the example update statement provided failed to protect the parameter in the where clause, was it because DGVNotes.SelectedRows(0).Cells("FilledFormID").Value.ToString) could never be entered by a user? will that hold true for the entire lifetime of the app etc?</p>

### Answer ID: 1834476
<p>Your CleanForSQL method only handles string situations.  What happens when you're not using a string but an INT instead?  In that case, there would be no end tick to close with, so the injection would still happen.  Consider this example...</p>

<pre><code>Database.DBUpdate("UPDATE tblFilledForms SET Int1 = " + CleanForSQL(txtNote.Text) + " WHERE FilledFormID = " + DGVNotes.SelectedRows(0).Cells("FilledFormID").Value.ToString)
</code></pre>

<p>in that case, just entering the following will work...</p>

<p><code>0; update tblMaint SET Value1 = 2 WHERE ValueID = 2--</code></p>

### Answer ID: 1834459
<p>You're not doing anything wrong. This is how SQL Server parses strings. The first quote opens the string, then you've followed that immediately with an escaped quote followed by Chr(8).</p>

<p>As an exercise, what happens if you run this in SQL Server: <code>SELECT '''Hello'</code>? Exactly the same parsing rules are being applied in this case.</p>

### Answer ID: 1834455
<p>I think your problem is that <code>Chr(8)</code> is not executed, you need to find another way to get the leading quote mark in.</p>

### Answer ID: 1834448
<p>The Chr(8) is part of the quoted literal string, as is the update statement, so SQL Server is not going to interpret it as a function call. With this example, Text1 will be set to the literal value:</p>

<pre><code>'Chr(8); update tblMaint SET Value1 = 2 WHERE ValueID = 2--
</code></pre>

<p>(yes, including that single quote)</p>

<p>So, with this example, your code <em>is</em> secure. Most hang-wringing over SQL injection is about accidentally <em>failing</em> to validate and quote values, there is nothing inherently unsafe in a properly-quoted SQL statement.</p>

