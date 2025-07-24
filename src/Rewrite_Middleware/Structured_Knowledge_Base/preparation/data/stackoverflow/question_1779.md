# Multilingual Support for Classic ASP
[Link to question](https://stackoverflow.com/questions/7663541/multilingual-support-for-classic-asp)
**Creation Date:** 1317827470
**Score:** 3
**Tags:** asp-classic, multilingual
## Question Body
<p>I have a client who called me this morning to retrofit a site for multilingual support.  The site is a Classic ASP application, and the client has no desire/budget to rewrite is as ASP.NET (or anything else...).</p>

<p>We talked about the difficulties with this, but much of the text happens to be short strings that are read from a database and he would be happy with just being able to translate this text.</p>

<p>If this were not Classic ASP, I would use a GNU gettext() based solution.  However, I have not been able to find an equivalent for Classic ASP.</p>

<p>I could add a table to his database to store the string translations, and then just query this, but it would also mean making an admin interface so he can edit the strings (rather than just editing a plain text file).</p>

<p>I could also create my own flatfile solution, likely based around <strong>Scripting.Dictionary</strong>, but I would really prefer not to roll my own here.</p>

<p>Are there any alternates solutions here?  Thanks.</p>

## Answers
### Answer ID: 7672565
<p>We use an XML based solution, we have XML files with the following structure:</p>

<pre><code>&lt;?xml version="1.0" encoding="Windows-1252"?&gt;
&lt;resource&gt;
    &lt;language LCID="1043" name="nederlands"&gt;
        &lt;label id="pageheader"&gt;&lt;![CDATA[Over deze applicatie]]&gt;&lt;/label&gt;
        &lt;label id="warning"&gt;&lt;![CDATA[]]&gt;&lt;/label&gt;
    &lt;/language&gt;
    &lt;language LCID="2067" name="vlaams"&gt;
        &lt;label id="pageheader"&gt;Over deze applicatie&lt;/label&gt;
        &lt;label id="warning"&gt;&lt;![CDATA[]]&gt;&lt;/label&gt;
    &lt;/language&gt;
    &lt;language LCID="2057" name="english (uk)"&gt;
        &lt;label id="pageheader"&gt;&lt;![CDATA[About this software]]&gt;&lt;/label&gt;
        &lt;label id="warning"&gt;&lt;![CDATA[]]&gt;&lt;/label&gt;
        &lt;label id=""&gt;&lt;![CDATA[]]&gt;&lt;/label&gt;
    &lt;/language&gt;
&lt;/resource&gt;
</code></pre>

<p>We chose to have every directory to have its own XML file, but if there aren't many translations in your site you could have one big XML in the root. This will impact your performance though.
We wrote a WSC to handle translations so we can just open a translation WSC at the top of each ASP page, and use a method to translate like so:</p>

<p>At the start of each page:</p>

<pre><code>dim translate
set translate = GetObject("script:"&amp;Server.MapPath("/~components/DLL/Translation.wsc"))
call translate.OpenWithLCID(session.LCID)
</code></pre>

<p>In the HTML:</p>

<pre><code>&lt;%= translate.label("systemerror") %&gt;
</code></pre>

<p>At the end of the page:</p>

<pre><code>call translate.close()
set translate = nothing
</code></pre>

<p>The impact on performance is minimal; just make sure that in your function to fetch a translation, to exit the loop and return the value as soon as you find the corresponding XML node. We made this mistake in the beginning, resulting in the complete XML file being processed when we called Translate.label().</p>

<p>My solution probably means you'll have to find out about using WSC's in ASP, but once you start using them, you'll never want to go back. It completely solves spaghetti code in ASp and enables separation of concerns and code re-use.</p>

<p>HTH,
Erik
Hope this helps</p>

### Answer ID: 7663825
<p>perhaps something like babelfish</p>

<p><a href="http://babelfish.yahoo.com/free_trans_service" rel="nofollow">http://babelfish.yahoo.com/free_trans_service</a></p>

