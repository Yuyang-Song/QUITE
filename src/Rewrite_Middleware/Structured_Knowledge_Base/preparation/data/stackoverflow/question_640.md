# Javascript / Googlescript using set.Formula with complex formulas
[Link to question](https://stackoverflow.com/questions/34688842/javascript-googlescript-using-set-formula-with-complex-formulas)
**Creation Date:** 1452304038
**Score:** 0
**Tags:** multidimensional-array, google-apps-script, google-sheets, formulas, array-formulas
## Question Body
<p>I have researching this but cannot find a suitable solution. The following formula works fine at the formula level when placed in a sheet cell. The issue is I want the formula to run at the script level. The options I am aware of include running a script to:
(1) set.Formula('=complex formula') 
or
(2) rewriting the entire formula as a script</p>

<p>I am new to GAS, and have messed around with both methods. There seems to be a syntax error when using option (1), usually in the form of a missing ")" that I cannot debug. Employing option (2) is currently above my skill level. Any help on either option would be greatly appreciated. </p>

<p>Here is the formula in question:</p>

<blockquote>
  <p>=ARRAYFORMULA(QUERY({UI!A:G,YEAR(UI!A:A),MONTH(UI!A:A), TEXT(UI!A:A, "MMMM"), TEXT(UI!A:A, "MMM-YY"), REPLACE(UI!A:A,1,1000,"GRAND
  TOTAL")}, "SELECT * WHERE Col1 IS NOT NULL AND Col2 IS NOT NULL LABEL
  Col8 'Year',Col9 'MonthMO#',Col10 'MonthMO',Col11 'MonthMOYR',Col12
  'GRAND TOTAL'"))</p>
</blockquote>

## Answers
### Answer ID: 35353685
<h1>Answer</h1>
<p>Formulas doesn't run &quot;at script level&quot; so you will have to rewrite your formula as a Google Apps Script / JavaScript function.</p>
<h1>Escaping formula apostrophes in scripts</h1>
<p>In case that you want a script to add your complex formula to a cell bear in mind that writing complex formulas in one line makes harder to debug them.
Try dividing your formula by functions and parameters and use a tab to align them. IMHO this prevents that the use of <code>\</code> makes the script unreadable (<a href="https://en.wikipedia.org/wiki/Leaning_toothpick_syndrome" rel="nofollow noreferrer">Leaning toothpick syndrome</a>).</p>
<p>Below is a onEdit() function that inserts the complex formula in the question to the cell to the right of a cell where 'Yes'  is wrote. Look to the use of <code>\</code> to escape the apostrophes used in the second parameter of the query function (select statement).</p>
<pre class="lang-js prettyprint-override"><code>function onEdit() {
  var ss = SpreadsheetApp.getActive();
  var rng = ss.getActiveRange();
  var trg = rng.offset(0, 1);
  var formula = 
    '=ARRAYFORMULA('
       + 'QUERY({'
            + 'UI!A:G,YEAR(UI!A:A),MONTH(UI!A:A),' 
            + 'TEXT(UI!A:A, &quot;MMMM&quot;), '
            + 'TEXT(UI!A:A, &quot;MMM-YY&quot;), '
            + 'REPLACE(UI!A:A,1,1000,&quot;GRAND TOTAL&quot;)'
          + '},' 
          + '&quot;SELECT * WHERE Col1 IS NOT NULL AND Col2 IS NOT NULL LABEL Col8 \'Year\', '
            + 'Col9 \'MonthMO#\', Col10 \'MonthMO\', Col11 \'MonthMOYR\', '
            + 'Col12 \'GRAND TOTAL\'&quot;'
       + ')'
     + ')';
  if(rng.getValue() == 'Yes') trg.setFormula(formula);
}
</code></pre>

