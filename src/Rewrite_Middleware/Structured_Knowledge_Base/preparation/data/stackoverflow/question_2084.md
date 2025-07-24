# Conditions in FOR EACH which is TRUE regardless of database records?
[Link to question](https://stackoverflow.com/questions/18256484/conditions-in-for-each-which-is-true-regardless-of-database-records)
**Creation Date:** 1376581817
**Score:** 1
**Tags:** progress-4gl, openedge, progress-db
## Question Body
<pre><code>FOR EACH loan WHERE /* Condition1 */ loan.date = SomeDate
                AND /* Condition2 */ loan.type = SomeType
                AND /* Condition3 */ (IF SpecMode THEN TRUE ELSE loan.spec = SomeSpec)
</code></pre>

<p>Condition3 = TRUE when SpecMode = TRUE. So I wonder if code above and code below would work exact the same (incl. speed) when SpecMode = TRUE?</p>

<pre><code>FOR EACH loan WHERE Condition1 
                AND Condition2
                AND TRUE
</code></pre>

<p>Or even like this?</p>

<pre><code>FOR EACH loan WHERE Condition1 
                AND Condition2
</code></pre>

<p>Generally speaking question is how Progress manages conditions which can be evaluated regardless of database records. Does it take more time? Also links about how Progress works in more deep view would be appreciated.</p>

<hr>

<p>Add 08/16/13:
Code I'm working with initially was:</p>

<pre><code>IF SpecMode THEN
  FOR EACH loan WHERE Condition1 AND Condition2:
    RUN Proc.
ELSE
  FOR EACH loan WHERE Condition1 AND Condition2 AND Condition3:
    RUN Proc.
</code></pre>

<p>Dynamic queries was first idea came to my mind, but I realized that it mean rewriting of all nested code with dynamic queries style (which is imo has worse readabilty, I moved this to <a href="https://stackoverflow.com/questions/18267870/static-vs-dynamic-queries-in-openedge">separate question</a>). I want to go with modern approach so I will do it if it's most reasonable solution.</p>

<p>There is third way which keeps code in "static style". It is using include files with parameters. But it means another <code>.i</code> file in already huge codebase. And I generally hate this approach (as well as "cheating" with preprocessor constants containing code). Our system is big and old and full of this kind of things, which is harder to analyze and basically seems to be just not right.</p>

## Answers
### Answer ID: 23269102
<p>Define variable v_user_can_read_items init false.</p>

<p>For each item where item.code begins "4" and</p>

<pre><code>            v_user_can_read_items = true:
</code></pre>

<p>display item.code.  /* will display nothing but read all items starting by 4 */</p>

<p>End.</p>

### Answer ID: 18535985
<p>I can't see any sense in use a for each that does not mention any field of the table..... the whole table will be selected regardless if the condition is true or false, since there is no inquiry to the table.</p>

<p>In any case Progress evaluates the full condition and retrieve the set of record that matches that condition.</p>

<p>Example 1.</p>

<p>def var as logical init false.</p>

<p>for each items where a:</p>

<p>display item.code.    /* Will display nothing but read all records of the table */</p>

<p>end.</p>

<p>Example 2:</p>

<p>def var a as logical init true.</p>

<p>for each items where a:</p>

<pre><code>  display item.code.    /* Will display all records of the table */
</code></pre>

<p>end.</p>

<p>Example 3:</p>

<p>Define variable v_user_can_read_items init false.</p>

<p>For each item where item.code begins "4" and</p>

<pre><code>                v_user_can_read_items = true:


 display item.code.  /* will display nothing but read all items starting by 4 */
</code></pre>

<p>End.</p>

<p>The time taken will depend on the where condition, on the first 2 cases  will be slow, because is reading ALL the records. In teh third case will be fast, because is first selecting the set of items starting by 4 and then don't displying because the condition return false.</p>

<p>The shortest tilme is when is using an appripiate index (where condition does) and the retrieved set is a short set of data.</p>

### Answer ID: 18523652
<p>for your case:</p>

<pre><code>EACH loan WHERE /* Condition1 */ loan.date = SomeDate
        AND /* Condition2 */ loan.type = SomeType
        AND /* Condition3 */ (IF SpecMode THEN TRUE ELSE loan.spec = SomeSpec)
</code></pre>

<p>You can try like this:</p>

<pre><code>your_loop:
EACH loan WHERE /* Condition1 */ loan.date = SomeDate
    AND         /* Condition2 */ loan.type = SomeType
    : 
    /* Condition3 */ 
    IF not SpecMode THEN DO:
        If loan.spec &lt;&gt; SomeSpec THEN
            NEXT your_loop. /* both false, next loop */
    END.

    /* ........ do your work ...... */

END. 
</code></pre>

### Answer ID: 18268289
<p>As an addon to Toms excellent answer, a tip is to compile with xref whenever you are unsure of what indices are used.</p>

<pre><code>COMPILE file.p [SAVE] XREF file.txt.
</code></pre>

<p>That will genereate a file containing index usage (amongst other things). Look for rows like this:</p>

<pre><code>c:\temp\program.p c:\temp\include.i 21 SEARCH db.webkonv tkn WHOLE-INDEX
</code></pre>

<p>SEARCH indicates that index "tkn" of the table "webkonv" is used in this example. WHOLE-INDEX indicating that the entire index has been scanned (in this case that was expected - this code was used before the TABLE-SCAN directive). Check the ABL Reference on the COMPILE statement.</p>

### Answer ID: 18257084
<p>The ( IF ... THEN ... ELSE ... ) embedded in the WHERE clause is treated as a function.</p>

<p>In general it is preferable to avoid having function calls in a WHERE clause.  Some, but not all, can be resolved on the server side.  (User-defined functions and CAN-DO() are two examples that must be evaluated on the client.)</p>

<p>In your case I don't know that the IF is always true.  If specMode is true then it is but if it is false the ELSE portion is evaluated and I can't know how that works out without looking at the data.  So it would not necessarily be correct to replace it as you suggest.</p>

<p>If specMode is <strong>always</strong> true then, yes, replacing it as you suggest (both versions) will work.</p>

<p>From an efficiency point of view the use of the IF function eliminates the ability to bracket on the loan.spec field.  If loan.date and loan.type are leading components of an index then they will be used to bracket.  If loan.spec is also an index component it cannot, however, be used to improve the selection and the whole subset of records carved out by the other criteria will need to be examined individually.</p>

<p>I think that the code you are showing is probably being used to provide a "clever" option of showing either ALL records with date and type, or just a subset of date, type and spec.  This might have been an attractive (but hard to read and inefficient) approach back in the old days.  It would have allowed a single block of code to handle whatever is inside the loop body.</p>

<p>In today's world you don't need to do that. You would just write a dynamic query and populate a proper WHERE clause as a string that you then use QUERY-PREPARE on.  That way if loan.spec is part of an index it can be used to help support the query and those cases will run <strong>much</strong> faster.</p>

