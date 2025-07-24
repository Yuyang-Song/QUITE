# Modify PDF Forms from a PHP site
[Link to question](https://stackoverflow.com/questions/3681724/modify-pdf-forms-from-a-php-site)
**Creation Date:** 1284081798
**Score:** 3
**Tags:** php, pdf, pdf-generation, itext, pdf-form
## Question Body
<p>We currently use PDForm to grab a blank pdf file (no values, just form fields and text) and list the form fields.  We then query our database for the values which match those field names and create a pdf file with the newly populated data which the user can download from our site.  The thing is PDForm is about $5,000 per machine and we are migrating servers.  We want an alternative which is actively supported and recommended by the community.</p>

<p>I know Zend is working on a PDF manipulation extension, but we need something quick.  I have done testing with PDFtk but the last update for that project was in 2006 and it now seems dead.  It would be fine as it is open source, however it seems to be causing errors with certain files that seem to be generated with PDFPenPro (our pdf form creator).</p>

<p>Another solution I thought up was why not just use iText and write a java wrapper which accepts command line input, so that PHP can call it with passthru() or exec().  There are other applications that will work should we completely rewrite our code but we do not want to do that.</p>

<p>What we need.</p>

<ol>
<li>The ability for PHP to receive the PDF form field names.</li>
<li>PHP to then either create and FDF file (then merge it with the PDF) or send a string to a command line application which will populate the fields with values from our database.</li>
<li>The user can then download the newly created PDF file with the populated form fields.</li>
</ol>

<p>Am I moving in the write direction by creating a java command line application that will use iText to parse and create the PDF files specified by PHP or does anyone know of any cost effective alternatives?</p>

## Answers
### Answer ID: 3728146
<p>So since none of the above solutions would work since TCPDF doesn't work with forms the way we are wanting and since PDFlib converts the form fields to blocks we decided to create a command line wrapper for iText which will grab the form field names from the PDF and then populate them based on the database values.</p>

### Answer ID: 3709715
<p>Thanks, d2burke, for the tip on TCPDF.  I'm not trying to do quite as much as the OP, but the software packages available to accomplish any kind of pdf generation are in the $2k to $3k range.  TCPDF is php based, open source and the guy developing it is very supportive.  </p>

<p>Always donate to these guys!  Where in the world would web development be without it?</p>

### Answer ID: 3682243
<p><a href="http://www.tecnick.com/public/code/cp_dpage.php?aiocp_dp=tcpdf" rel="nofollow noreferrer">TCPDF</a> seems to have the most robust feature set that I have seen so far.</p>

### Answer ID: 3682221
<p>I don't know if another product whose license costs range from $1k -> $3k could be considered "cost effective", but <a href="http://www.pdflib.com/products/pdflib-family/pps/" rel="nofollow noreferrer">PDFlib</a> work quite nicely. And if you don't need the PPS functionality, it does get cheaper.</p>

