# Decoding ISO-8859-1 and Encoding to UTF-8 before MySQL query
[Link to question](https://stackoverflow.com/questions/38650968/decoding-iso-8859-1-and-encoding-to-utf-8-before-mysql-query)
**Creation Date:** 1469769383
**Score:** 0
**Tags:** php, python, mysql, utf-8, character-encoding
## Question Body
<p>I'm kinda stuck if I'm doing it right. </p>

<p>I have a file which is ISO-8859-1 (pretty certain). My MySQL db is in utf-8 encoding. Which is why I want to convert the file to UTF-8 encoded characters before I can send it as a query. For instance, First I rewrite every line of the <strong>file.txt</strong> into <strong>file_new.txt</strong> using.</p>

<pre><code>line = line.decode('ISO-8859-1').encode('utf-8')
</code></pre>

<p>And then I save it. Next, I create a MySQL connection and create a cursor with the following query so that all the data is received as utf-8.</p>

<pre><code>query = 'SET NAMES "utf8"'
cursor.execute(query)
</code></pre>

<p>Following this, I reopen <strong>file_new.txt</strong> and enter each line into MySQL. Is this the right approach to get the table in MySQL utf-8 encoding? Or Am I missing any crucial part? </p>

<p>Now to receive this data. I use <code>'SET NAMES "utf8""</code> as well. But the received data is giving me question marks � when I set the header content type to </p>

<pre><code>header("Content-Type: text/html; charset=utf-8");
</code></pre>

<p>On the other hand, when I set </p>

<pre><code>header("Content-Type: text/html; charset=ISO-8859-1");
</code></pre>

<p>It works fine, but other utf-8 encoded data from the database is getting scrambled. So I'm guessing the data from <strong>file.txt</strong> is still NOT getting encoded to utf-8. Can any one explain why?</p>

<p>PS: Before I read everyline, I replace a character and save the <strong>file.txt</strong> to <strong>file.txt.tmp</strong>. I then read this file to get <strong>file_new.txt</strong>. I don't know if it causes any problem to the original file encoding.</p>

<pre><code>f1 = codecs.open(tsvpath, 'rb',encoding='iso-8859-1')
f2 = codecs.open(tsvpath + '.tmp', 'wb',encoding='utf8')
for line in f1:
    f2.write(line.replace('\"', '\''))
f1.close()
f2.close()
</code></pre>

<p>In the below example, I've utf-8 encoded persian data which is right but the other non-enlgish text is coming out to be in "question marks". This is precisely my problem.</p>

<p><strong>Example :</strong> Removed.</p>

## Answers
### Answer ID: 38665348
<p>You should <em>not</em> need to do any explicit encode or decode.  <code>SET NAMES ...</code> should match what the <em>client</em> encoding is (for <code>INSERTing</code>) or should become (for <code>SELECTing</code>).</p>

<p>MySQL will convert between the client encoding and the columns's <code>CHARACTER SET</code>.</p>

### Answer ID: 38653078
<p>Alright guys, so my encoding was right. The file was getting encoding to utf-8 just as needed. All the queries were right. It turns out that the other dataset that was in Arabic was in ISO-8859-1. Therefore, only 1 of them was working. No matter what I did.</p>

<p>The Hexeditors did help. But in the end I just used sublime text to recheck if my encoded data was utf-8. It turns out the python script and the sublime editor did the same. So the code is fine. :)</p>

### Answer ID: 38651095
<p>Try this instead:</p>

<pre><code>line = line.decode('ISO-8859-1').encode('utf-8-sig')
</code></pre>

<p>From the docs:</p>

<blockquote>
  <p>As UTF-8 is an 8-bit encoding no BOM is required and any U+FEFF
  character in the decoded string (even if it’s the first character) is
  treated as a ZERO WIDTH NO-BREAK SPACE.</p>
  
  <p>Without external information it’s impossible to reliably determine
  which encoding was used for encoding a string. Each charmap encoding
  can decode any random byte sequence. However that’s not possible with
  UTF-8, as UTF-8 byte sequences have a structure that doesn’t allow
  arbitrary byte sequences. To increase the reliability with which a
  UTF-8 encoding can be detected, Microsoft invented a variant of UTF-8
  (that Python 2.5 calls "utf-8-sig") for its Notepad program: Before
  any of the Unicode characters is written to the file, a UTF-8 encoded
  BOM (which looks like this as a byte sequence: 0xef, 0xbb, 0xbf) is
  written. As it’s rather improbable that any charmap encoded file
  starts with these byte values (which would e.g. map to</p>
  
  <p>LATIN SMALL LETTER I WITH DIAERESIS RIGHT-POINTING DOUBLE ANGLE
  QUOTATION MARK INVERTED QUESTION MARK in iso-8859-1), this increases
  the probability that a utf-8-sig encoding can be correctly guessed
  from the byte sequence. So here the BOM is not used to be able to
  determine the byte order used for generating the byte sequence, but as
  a signature that helps in guessing the encoding. On encoding the
  utf-8-sig codec will write 0xef, 0xbb, 0xbf as the first three bytes
  to the file. On decoding utf-8-sig will skip those three bytes if they
  appear as the first three bytes in the file. In UTF-8, the use of the
  BOM is discouraged and should generally be avoided.</p>
</blockquote>

<p>Source: <a href="https://docs.python.org/3.5/library/codecs.html" rel="nofollow">https://docs.python.org/3.5/library/codecs.html</a></p>

<p><strong>EDIT:</strong></p>

<p>Sample:
<code>"Hello World".encode('utf-8')</code> yields <code>b'Hello World'</code> while <code>"Hello World".encode('utf-8-sig')</code> yields <code>b'\xef\xbb\xbfHello World'</code> highlighting the docs:</p>

<blockquote>
  <p>On encoding the
  utf-8-sig codec will write 0xef, 0xbb, 0xbf as the first three bytes
  to the file. On decoding utf-8-sig will skip those three bytes if they
  appear as the first three bytes in the file.</p>
</blockquote>

<p><strong>Edit:</strong>
I have made a similar function before that converts a file to utf-8 encoding. Here is a snippet:</p>

<pre><code>def convert_encoding(src, dst, unicode='utf-8-sig'):
    return open(dst, 'w').write(open(src, 'rb').read().decode(unicode, 'ignore'))
</code></pre>

<p>Based on your example, try this:</p>

<pre><code>convert_encoding('file.txt.tmp', 'file_new.txt')
</code></pre>

### Answer ID: 38651661
<p>Welcome to the wonderful world of unicode and windows.  I've found this site very helpful in understanding what is going wrong with my strings <a href="http://www.i18nqa.com/debug/utf8-debug.html" rel="nofollow">http://www.i18nqa.com/debug/utf8-debug.html</a>.  The other thing you need is a hex editor like <a href="https://mh-nexus.de/en/hxd/" rel="nofollow">HxD</a>.  There are many places where things can go wrong.  For example, if you are viewing your files in a text editor - it may be trying to be helpful and is silently changing your encoding. </p>

<p>Start with your original data, view it in HxD and see what the encoding is.  View your results in Hxd and see if the changes you expect are being made. Repeat through the steps in your process.</p>

<p>Without your full code and sample data, its hard to say where the problem is.  My guess is your replacing the double quote with single quote on binary files is the culprit.</p>

<p>Also check out <a href="http://www.joelonsoftware.com/articles/Unicode.html" rel="nofollow">The Absolute Minimum Every Software Developer Absolutely, Positively Must Know About Unicode and Character Sets (No Excuses!)
by Joel Spolsky</a></p>

