# Lower-case all text in a datatable, or lower-case all text on a page to use css text-transform: capitalize?
[Link to question](https://stackoverflow.com/questions/15367185/lower-case-all-text-in-a-datatable-or-lower-case-all-text-on-a-page-to-use-css)
**Creation Date:** 1363106816
**Score:** -3
**Tags:** c#, javascript, asp.net, css
## Question Body
<p>I've run into the problem that CSS cannot use <code>text-transform: capitalize</code> on text that's already capitalized. Unfortunately the text being returned from my database is capitalized in many cases. Rather than putting a <code>LOWER(X)</code> ahead of every single field I'm requesting from the database, or call a JS function on every field, it seems like it'd be easier to use a solution that just targets the entire datatable returned, and then use <code>text-transform: capitalize</code> in the page's CSS.</p>

<p>Any suggestions for an easy way to do this? Alternatively, a way to target all the text on the page (JS, perhaps?) and lowercase it, then have the CSS part recapitalize would be fine. I'm looking for the easiest possible solution, whatever that may be (and rewriting a large number of queries simply isn't it.)</p>

## Answers
### Answer ID: 15367633
<p>Ben you can use this Select Query against your DataTable 
you will need to adjust the field(s) based on your Table. I am only showing this using 1 field name called <code>DESC</code></p>

<pre><code>select
    DESC =
    -- Adjust the length of your filed(s) for example DESC is varchar(500)
    convert(varchar(500),
    upper(substring(DESC,1,1))+
    lower(substring(DESC,2,499)))
from
    YouTable Name
</code></pre>

### Answer ID: 15367259
<p>Easiest would be to change the data in your database so that you don't have capitalized strings, and let CSS do its thing. In any case, doing it on JS/CSS alone is not the way to go.</p>

### Answer ID: 15367221
<p>Using CSS to do that is incorrect. Lowercase what’s in your database, easier or not.</p>

