# xpath query not working in BizTalk orchestration
[Link to question](https://stackoverflow.com/questions/19822538/xpath-query-not-working-in-biztalk-orchestration)
**Creation Date:** 1383770975
**Score:** 1
**Tags:** biztalk, biztalk-2010
## Question Body
<p>I'm trying to rewrite a BizTalk 2010 application and do away with an external assembly, but I seem to be running into xpath problems.</p>

<p>We have a process that stores a healthcare claim (837P) as xml in the database, and we need to extract it later. I have a WCF port calling a stored procedure that returns an xml message that looks something like this:</p>

<pre><code>&lt;ClaimXml_SEL_GetClaimXmlResponse xmlns="http://schemas.microsoft.com/Sql/2008/05/TypedProcedures/dbo"&gt;
   &lt;StoredProcedureResultSet0&gt;
      &lt;StoredProcedureResultSet0 xmlns="http://schemas.microsoft.com/Sql/2008/05/ProceduresResultSets/dbo/ClaimXml_SEL_GetClaimXml"&gt;
         &lt;Claim&gt;&lt;![CDATA[&lt;ns0:X12_00401_837_P (etc.)
</code></pre>

<p>So what I need to do is extract the actual 837P message - the part that starts with ns0:X12_00401_837_P.</p>

<p>The helper class is very simple, just has a method like this:</p>

<pre><code>public XmlDocument ExtractClaimXml(XmlDocument xDoc)
{
   XmlDocument xReturn = new XmlDocument();

   XmlNode node = xDoc.SelectSingleNode("/*[local-name()='ClaimXml_SEL_GetClaimXmlResponse' and namespace-uri()='http://schemas.microsoft.com/Sql/2008/05/TypedProcedures/dbo']/*[local-name()='StoredProcedureResultSet0' and namespace-uri()='http://schemas.microsoft.com/Sql/2008/05/TypedProcedures/dbo']/*[local-name()='StoredProcedureResultSet0' and namespace-uri()='http://schemas.microsoft.com/Sql/2008/05/ProceduresResultSets/dbo/ClaimXml_SEL_GetClaimXml']/*[local-name()='Claim' and namespace-uri()='http://schemas.microsoft.com/Sql/2008/05/ProceduresResultSets/dbo/ClaimXml_SEL_GetClaimXml']");

   xReturn.LoadXml(node.InnerText);

   return xReturn;
}
</code></pre>

<p>and then the Message Assignment shape has this code:</p>

<pre><code>rawClaimXml = ClaimXmlResponse;
strippedClaim = XmlHelperClass.ExtractClaimXml(rawClaimXml);
Claim837P = strippedClaim;
</code></pre>

<p>...where ClaimXmlResponse; is the message shown above, Claim837P is an 837P message, and rawClaimXml &amp; strippedClaim are xml variables. This works just fine, but it seems excessive to call an external assembly.</p>

<p>I tried this in the assingment shape:</p>

<pre><code>rawClaimXml = xpath(ClaimXmlResponse, "same xpath as above");
strippedClaim.LoadXml(rawClaimXml.InnerText);
Claim837P = strippedClaim;
</code></pre>

<p>...but get the error "'UnderlyingXmlDocument.InnerText': .NET property is write-only because it does not have a get accessor".</p>

<p>So then I tried just getting a string from the xpath query:</p>

<pre><code>rawClaimString = xpath(ClaimXmlResponse, "string(same xpath as above)");
rawClaimString = rawClaimString.Replace("&lt;![CDATA[", "");
rawClaimString = rawClaimString.Replace("&gt;]]&gt;","&gt;");
strippedClaim.LoadXml(rawClaimString);
Claim837P = strippedClaim;
</code></pre>

<p>...but that's no good. Also tried a variant:</p>

<pre><code>rawClaimXml = xpath(ClaimXmlResponse, "same xpath as above");
rawClaimString = rawClaimXml.InnerXml.ToString();
rawClaimString = rawClaimString.Replace("&lt;![CDATA[", "");
rawClaimString = rawClaimString.Replace("&gt;]]&gt;","&gt;");
strippedClaim.LoadXml(rawClaimString);
Claim837P = strippedClaim;
</code></pre>

<p>...but still no good. Any suggestions?</p>

<p>Thanks!</p>

## Answers
### Answer ID: 19823048
<p>1-
Here's a couple of things you can try:</p>

<ul>
<li>Wrap the xpath in the <code>string()</code> function.  <code>xpath(ClaimXmlResponse,
"string(same xpath as above)");</code></li>
<li>Append the <code>/text()</code> node to the xpath.  <code>xpath(ClaimXmlResponse, "same
xpath as above/text()");</code></li>
<li>A combination of the two.</li>
</ul>

<p>Can you elaborate on the goal here?  There's nothing wrong with using the helper class.  If it's the extra Assembly that's bothering you, you can always add the .cs to the BizTalk Project.</p>

<p>2-
Coming from a different direction, you can use Path option for the Inbound BizTalk message body on the Messages Tab of the WCF-Custom Adpater configuration.</p>

### Answer ID: 25826445
<p>I was also facing the similar issue but when I gone through your various solution I got the solution for my question.</p>

<p>For me this worked **</p>

<blockquote>
  <p>rawClaimString = xpath(ClaimXmlResponse, "string(same xpath as
  above)");</p>
</blockquote>

<p>**</p>

<p>thanks for that phew ;)</p>

<p>Coming to the solution for your problem you can distinguishly promote the node that holding your response and try to access that node using .notation and assign it to the sting this ll return the expected output to you :) </p>

