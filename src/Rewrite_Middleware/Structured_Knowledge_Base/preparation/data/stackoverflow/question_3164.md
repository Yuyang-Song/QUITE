# A root node &lt;kml&gt; with kml namespace does not parse in basex xquery
[Link to question](https://stackoverflow.com/questions/69571389/a-root-node-kml-with-kml-namespace-does-not-parse-in-basex-xquery)
**Creation Date:** 1634217277
**Score:** 0
**Tags:** xml, xslt, xquery, kml
## Question Body
<p>Trying to understand a vertical industry use of XML in KML mapping.</p>
<p>Related answers ( 58961408; 1541744 ; 1535869) provide idiosynctratic workarounds but not an explanation. I generated <em><strong>KML</strong></em> of a voter demarcation map shape file(s) using a web service and the resulting <em><strong>KML</strong></em> is structured similar to cited problems where &lt;kml&gt; is root node AND a namespace at the same time:</p>
<pre><code>&lt;kml xmlns=&quot;http://www.opengis.net/kml/2.2&quot; ...&gt; .... &lt;/kml&gt;
</code></pre>
<p>My problem with it is that BaseX's XQuery consistently returns 0 results unless I fn:translate() first; and the result is then a jumble of selectively escaped XML sub-trees depending on Nodes inside of the file. Looking at BaseX parser log, it considers the source a pre-formatted result with nothing to parse through.</p>
<p>By trial and error and using XSL's pro-forma as hint I fashioned an XSLT work-around:</p>
<pre><code>&lt;KMLSource xmlns:kml=&quot;http://www.opengis.net/kml/2.2&quot; ... &gt; ... &lt;/KMLSource&gt;
</code></pre>
<p>Which renames the &lt;kml&gt; root node with &lt;KMLSource&gt; and kml is invoked as a name space attribute. With that change BaseX.XQuery runs the KML through its normal gamut of FLOWRs.</p>
<p>But my introducing &lt;KMLSource&gt; as root node is arbitrary and bound to have untold side-effects of worse impact downstream; so what is a benign work-around for <em><strong>KML</strong></em>, or even an <em><strong>SVG</strong></em> (seemingly more chaotic in that regard) for that matter?</p>
<p>If there is a such generic and benign translation can that be made the standard XML export in those verticals?
I have not been able to test answer 58961408 that adds an xsi namespace to the  root in case that is the benign generic solution.</p>
<p>EDITS: As per comments, a minimal but lame[*] parsable example sans Style overhead:</p>
<pre><code>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;
&lt;kml xmlns=&quot;http://www.opengis.net/kml/2.2&quot; xmlns:kml=&quot;http://www.opengis.net/kml/2.2&quot; xmlns:gx=&quot;http://www.google.com/kml/ext/2.2&quot;  xmlns:atom=&quot;http://www.w3.org/2005/Atom&quot;&gt;
  &lt;Document id=&quot;&quot;&gt;
    &lt;name&gt;Are999&lt;/name&gt;
    &lt;open&gt;0&lt;/open&gt;
    &lt;Placemark id=&quot;&quot;&gt;
      &lt;Snippet maxLines=&quot;0&quot;&gt;
      &lt;/Snippet&gt;
      &lt;name&gt;1&lt;/name&gt;
      &lt;description&gt;&amp;lt;br&amp;gt;&amp;lt;br&amp;gt;&amp;lt;table class='data' &amp;gt;&amp;lt;tr class='o'&amp;gt;&amp;lt;td&amp;gt;shpFID:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;0&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='e'&amp;gt;&amp;lt;td&amp;gt;OBJECTID:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;3889&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='o'&amp;gt;&amp;lt;td&amp;gt;Province:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;AREA&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='e'&amp;gt;&amp;lt;td&amp;gt;CAT_B:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;AREA999&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='o'&amp;gt;&amp;lt;td&amp;gt;WardNo:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;1&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='e'&amp;gt;&amp;lt;td&amp;gt;WardID:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;93504001&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='o'&amp;gt;&amp;lt;td&amp;gt;MapCode:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;AREA999_1&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='e'&amp;gt;&amp;lt;td&amp;gt;MunicName:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;Nonland&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='o'&amp;gt;&amp;lt;td&amp;gt;Shape_Leng:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;1.971403&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='e'&amp;gt;&amp;lt;td&amp;gt;Shape_Area:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;0.1172304&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;/table&amp;gt;&lt;/description&gt;
      &lt;visibility&gt;1&lt;/visibility&gt;
      &lt;Point&gt;
        &lt;extrude&gt;1&lt;/extrude&gt;
        &lt;tessellate&gt;0&lt;/tessellate&gt;
        &lt;altitudeMode&gt;clampToGround&lt;/altitudeMode&gt;
        &lt;coordinates&gt;29.359397617,-24.0573315119999,0 &lt;/coordinates&gt;
      &lt;/Point&gt;
      &lt;styleUrl&gt;#default&lt;/styleUrl&gt;
    &lt;/Placemark&gt;
    &lt;Placemark id=&quot;994&quot;&gt;
      &lt;Snippet maxLines=&quot;0&quot;&gt;
      &lt;/Snippet&gt;
      &lt;name&gt;995&lt;/name&gt;
      &lt;description&gt;&amp;lt;br&amp;gt;&amp;lt;br&amp;gt;&amp;lt;table class='data' &amp;gt;&amp;lt;tr class='o'&amp;gt;&amp;lt;td&amp;gt;shpFID:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;994&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='e'&amp;gt;&amp;lt;td&amp;gt;OBJECTID:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;3933&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='o'&amp;gt;&amp;lt;td&amp;gt;Province:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;AREA&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='e'&amp;gt;&amp;lt;td&amp;gt;CAT_B:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;AREA999&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='o'&amp;gt;&amp;lt;td&amp;gt;WardNo:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;995&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='e'&amp;gt;&amp;lt;td&amp;gt;WardID:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;935040995&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='o'&amp;gt;&amp;lt;td&amp;gt;MapCode:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;AREA999_99&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='e'&amp;gt;&amp;lt;td&amp;gt;MunicName:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;Nonland&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='o'&amp;gt;&amp;lt;td&amp;gt;Shape_Leng:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;0.6676676&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;tr class='e'&amp;gt;&amp;lt;td&amp;gt;Shape_Area:&amp;lt;/td&amp;gt;&amp;lt;td&amp;gt;0.01426437&amp;lt;/td&amp;gt;&amp;lt;/tr&amp;gt;&amp;lt;/table&amp;gt;&lt;/description&gt;
      &lt;visibility&gt;1&lt;/visibility&gt;
      &lt;styleUrl&gt;#default&lt;/styleUrl&gt;
      &lt;Polygon id=&quot;&quot;&gt;
        &lt;extrude&gt;1&lt;/extrude&gt;
        &lt;tessellate&gt;0&lt;/tessellate&gt;
        &lt;altitudeMode&gt;clampToGround&lt;/altitudeMode&gt;
        &lt;outerBoundaryIs&gt;
          &lt;LinearRing&gt;
            &lt;coordinates&gt;-29.1979840860001,33.577018037,0 -29.1928647940001,33.5760201429999,0 -29.1928101830001,33.5759909999999,0&lt;/coordinates&gt;
          &lt;/LinearRing&gt;
        &lt;/outerBoundaryIs&gt;
      &lt;/Polygon&gt;
    &lt;/Placemark&gt;
  &lt;/Document&gt;
&lt;/kml&gt;
</code></pre>
<p>The plain identity query returns the KML wrapped in &lt;text&gt;/&lt;line&gt;. One that returns '0 Results / hits' without BaseX.XQuery syntax error:</p>
<pre><code>let $database := db:open(&quot;nonland&quot;)

for $ballot_station in $database/kml/Document/Placemark
 return $ballot_station
</code></pre>
<p>BaseX Trace / Log:
Compiling:</p>
<ul>
<li><p>open database &quot;nonland&quot;</p>
</li>
<li><p>rewrite db:open(database[,path]) to document-node() item: db:open(&quot;nonland&quot;) -&gt; db:open-pre(&quot;nonland&quot;, 0)</p>
</li>
<li><p>remove step without results: kml</p>
</li>
<li><p>rewrite cached step to empty sequence: kml -&gt; ()</p>
</li>
<li><p>rewrite cached path to empty sequence: $database_0/()/Document/Placemark -&gt; ()</p>
</li>
<li><p>inline for $ballot_station_1 in ()</p>
</li>
<li><p>inline let $database_0 := db:open-pre(&quot;nonland&quot;, 0)</p>
</li>
<li><p>simplify FLWOR expression: ()
Optimized Query:
()
Query:</p>
<p>let $database := db:open(&quot;nonland&quot;)
for $ballot_station in $database/kml/Document/Placemark
return $ballot_station</p>
</li>
</ul>
<p>Result:</p>
<ul>
<li>Hit(s): 0 Items
...</li>
</ul>
<p>PS [*]: Lame in that it does not have enough content for a quick and dirty FLOWR as definitive counterexample. In this GIS jurisdiction Location pins are called Balloon that have Point Placemarks in one section and Polygon Border Placemarks in the later bottom section.</p>
<p>PPS[*] See comment by @MartinHonnen on adding a declaration:</p>
<pre><code>declare default element namespace &quot;http://www.opengis.net/kml/2.2&quot;;
let $database := db:open(&quot;nonland&quot;)
 for $ballot_station in $database/kml/Document/Placemark/Point
 return $ballot_station
</code></pre>
<p>which XQuery returns:</p>
<pre><code>&lt;Point xmlns=&quot;http://www.opengis.net/kml/2.2&quot; xmlns:kml=&quot;http://www.opengis.net/kml/2.2&quot; xmlns:gx=&quot;http://www.google.com/kml/ext/2.2&quot; xmlns:atom=&quot;http://www.w3.org/2005/Atom&quot;&gt;
  &lt;extrude&gt;1&lt;/extrude&gt;
  &lt;tessellate&gt;0&lt;/tessellate&gt;
  &lt;altitudeMode&gt;clampToGround&lt;/altitudeMode&gt;
  &lt;coordinates&gt;29.359397617,-24.0573315119999,0&lt;/coordinates&gt;
&lt;/Point&gt;
</code></pre>
<p>But only after excising the magic string opening 'xml' file:</p>
<pre><code>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;
</code></pre>
<p>So the assumed standard does not tolerate it in a presumed XML stream (error: &quot;The processing instruction target matching &quot;[xX][mM][lL]&quot; is not allowed.&quot;) but it is thrown in by vertical subject domain implementations where payloads are not explicitly XML, as XML advisories in cases like KML or SVG streams. My appreciation to @MartinHonnen for the insight, so perhaps someone can now tackle the rhetorical question on a generic but benign workaround as XML continues to show up in numerous unexpected contexts? I can think of explicit checks: ... if payload is XML drop processing instruction magic string ... There's got to be a reason they do not do a no-Op there instead ...</p>

## Answers
### Answer ID: 69580590
<p>Do you expect to be able to select elements declared in a namespace like <code>&lt;kml xmlns=&quot;http://www.opengis.net/kml/2.2&quot; ...&gt; .... &lt;/kml&gt;</code> with XQuery without declaring a namespace (e.g. <code>declare namespace kml = &quot;http://www.opengis.net/kml/2.2&quot;; kml:kml/</code>) or default element namespace (e.g. <code>declare default element namespace &quot;http://www.opengis.net/kml/2.2&quot;;  kml/</code>)?</p>
<p>I would expect you to need e.g.</p>
<pre><code>declare default element namespace &quot;http://www.opengis.net/kml/2.2&quot;; 
let $database := db:open(&quot;nonland&quot;) 
for $ballot_station in $database/kml/Document/Placemark
</code></pre>
<p>But with any XQuery processor, not only BaseX. And with any XML document using namespaces, you need to declare the namespace(s) in the query prolog to use them in the XQuery, that is not KML specific.</p>

