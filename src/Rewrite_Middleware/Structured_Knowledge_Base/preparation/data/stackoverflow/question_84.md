# Flash embed source redirect does not handle query parameters added by redirect (IE &amp; Chrome only)
[Link to question](https://stackoverflow.com/questions/12274484/flash-embed-source-redirect-does-not-handle-query-parameters-added-by-redirect)
**Creation Date:** 1346819151
**Score:** 0
**Tags:** flash, internet-explorer, google-chrome, http-redirect, parameters
## Question Body
<p>I have a problem with a redirected source of a swf file in chrome and IE only. This is needed for a theme management system that redirects the virtual theme swf (mod-rewrite) to the original swf with additional color parameters. The user can select the color with a combobox, for example: default, black, gold, orange etc.</p>

<p>For example:</p>

<pre><code>User select 'black' in combobox
virtual source: http://myserver/mytheme/black.swf
redirects to: http://myserver/mytheme/default.swf?color1=0000&amp;color2=&amp;FFFFFF&amp; ......
</code></pre>

<p>The virtual source is linked to a theme manager called theme.php. This theme manager applies the correct parameters for the default.swf file (from a database) and redirects it to the default.swf file with applied parameters.</p>

<p>Finally, the swf 'default.swf' applies the color query parameters and change some objects to the colors specified.</p>

<p>This is working OK in Firefox and Opera. But in Chrome and IE the query parameters are lost, the swf shows the default colors. I think that this is because the src parameter is still pointing to the virtual file (the one without query parameters)?</p>

<p>Can somebody explain to me what is going on? or better, does anyone know a solution to this?  </p>

## Answers
### Answer ID: 12415836
<p>Allright, no answer to this question.</p>

<p>Solved this differently. Instead of redirect the (for example) black.swf to the default.swf with applied parameters, i change the code to first request the server for the color parameters for the color black. Then i apply the default.swf with the received parameters directly to the object and this working OK.</p>

<p>Not a real solution but a workaround. Still not clear why redirection of a file in an object tag/embed tag is not working.  </p>

