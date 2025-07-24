# Google Maps v3 and XML implementation approach
[Link to question](https://stackoverflow.com/questions/9041318/google-maps-v3-and-xml-implementation-approach)
**Creation Date:** 1327705989
**Score:** 0
**Tags:** xml, google-maps, xpath
## Question Body
<p>I would like some input on which of the following two approaches is more appropriate.</p>

<p><strong>1.</strong> Should I load a "master" XML file then use XPath on it? With this solution I would only rewrite the "master" XML file when the site updates its local database.<br>
-or-</p>

<p><strong>2.</strong> Should I generate an XML file for each query and then load that specific file?  Then just do some cleanup every so often on all the XML files that would be generated.</p>

<p>NOTES:</p>

<ul>
<li>I am implementing this on a Realty site.</li>
<li>This is kind of obvious, but still going to point it out, queries are formed from a search form that narrows down results based on user input.</li>
<li>The site has a cron job that updates a local database from a remote
database every so often.</li>
<li>The "master" XML file would likely not have more that 600 properties.</li>
<li>This site isn't super busy, about 100 to 150 visitors a day.</li>
<li>I would be using JavaScript to load the XML and parse with XPath.</li>
</ul>

## Answers
### Answer ID: 9052305
<p>First off i personally really like JSON and you should use it because it is lighter.
600 markers are really small number and i suggest to load them  all together once.
Maybe you can also use a marker manager such as <a href="http://google-maps-utility-library-v3.googlecode.com/svn/tags/markerclustererplus/" rel="nofollow">MarkerClustererPlus</a> (example) iff the results are overlapping each other.</p>

<p>So i suggest the first option as the multiple requests are unnecessary.</p>

