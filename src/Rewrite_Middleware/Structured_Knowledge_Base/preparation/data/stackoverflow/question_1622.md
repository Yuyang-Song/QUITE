# listagg using when overflow of varchar2 occures - what to do?
[Link to question](https://stackoverflow.com/questions/1714904/listagg-using-when-overflow-of-varchar2-occures-what-to-do)
**Creation Date:** 1257942728
**Score:** 1
**Tags:** sql, oracle10g
## Question Body
<p>Could somebody advice what to do when using listagg leads to varchar2 overflow because of lots of aggregated strings (during aggregation in SQL query via Group etc.) in One field?</p>

<p>I use report (It just ONE SQL query) where I aggregate Phone Codes by ZoneName (Country etc.) and some of them have tons of codes for one Zone - so I could get "oveflow" error cause listagg using varchar2 that have 32767 limitation.</p>

<p>So what to do in such situations? Rewrite query and use cursors? Is there a workaround to detect "oveflow" and split, for example, such "BIG FIELD" in TWO rows so that in every one there would be enough space for "BIG list of Codes"???</p>

<p>Because I'm on 10gR2 now I'm using "Tab to string" technic from Tom Kyte.
it uses Type:</p>

<pre><code>CREATE OR REPLACE TYPE t_varchar2_tab AS TABLE OF VARCHAR2(32767);
</code></pre>

<p>And proc, that converts from Table of Varchar2 to One String that has 32767 chars limitation.</p>

<pre><code>CREATE OR REPLACE FUNCTION tab_to_string (p_varchar2_tab  IN  t_varchar2_tab,
                                          p_delimiter     IN  VARCHAR2 DEFAULT ',') RETURN VARCHAR2 IS
  l_string     VARCHAR2(32767);
BEGIN
  FOR i IN p_varchar2_tab.FIRST .. p_varchar2_tab.LAST LOOP
    IF i != p_varchar2_tab.FIRST THEN
      l_string := l_string || p_delimiter;
    END IF;
    l_string := l_string || p_varchar2_tab(i);
  END LOOP;
  RETURN l_string;
END tab_to_string;
/
</code></pre>

<p>And for the present Moment I got "overflow" error in my case. </p>

<p>I suppose that listagg proc will have the same problem because of using Varchar2. </p>

<p>Any advices?</p>

<p><strong>UPD:</strong> I ONLY need this (aggregation of codes in One field during generation of Report) to OUTPUT data for Report (in .pdf or while Printing). In Database all the Data is Normalized. </p>

## Answers
### Answer ID: 1715010
<p>The best way would be to normalise the data so that you have each string n a separate row then the number of items you can have is limited to te database not a single field.</p>

<p>tab_to_string is only useful for output and I doubt you want to see a field > 32K characters.</p>

