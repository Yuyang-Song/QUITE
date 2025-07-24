# Creating a flexible latex table from perl
[Link to question](https://stackoverflow.com/questions/14396152/creating-a-flexible-latex-table-from-perl)
**Creation Date:** 1358502343
**Score:** 1
**Tags:** perl, latex
## Question Body
<p>I have a perl script that outputs monthly statistics from a database. These are summarised in a table using the following snippet of code</p>

<pre><code>print $fh &lt;&lt;END; 
This report details clinical and imaging statistics from $date_start to $date_stop.

\\large \\bf Clinical Statistics

\\normalsize \\rm 

\\begin{table}[h]
\\centering 
\\begin{tabular}{p{4cm}cccccccc} 
\\hline
  &amp; $operator[0] &amp; $operator[1] &amp; $operator[2] &amp; $operator[3] &amp; $operator[4] &amp; $operator[5] &amp; $operator[6] &amp; $operator[7] \\\\
\\hline

    Cannulations &amp; $venflons[0] &amp; $venflons[1] &amp; $venflons[2] &amp; - &amp; $venflons[4] &amp; $venflons[5] &amp; $venflons[6] &amp; $venflons[7] \\\\
    Clinical Assessments &amp; $clin_ass[0] &amp; $clin_ass[1] &amp; $clin_ass[2] &amp; - &amp; $clin_ass[4] &amp; $clin_ass[5] &amp; $clin_ass[6] &amp; - \\\\
    Lead Stressor &amp; $etlead[0] &amp; $etlead[1] &amp; $etlead[2] &amp; - &amp; $etlead[4] &amp; $etlead[5] &amp; $etlead[6] &amp; $etlead[7] \\\\
    Assistant Stressor &amp; $etass[0] &amp; $etass[1] &amp; $etass[2] &amp; - &amp; $etass[4] &amp; $etass[5] &amp; $etass[6] &amp; - \\\\
    ECG Preparation &amp; $ecg_prep[0] &amp; $ecg_prep[1] &amp; $ecg_prep[2] &amp; $ecg_prep[3] &amp; $ecg_prep[4] &amp; $ecg_prep[5] &amp; $ecg_prep[6] &amp; - \\\\Patient Identification &amp; $patient_id[0] &amp; $patient_id[1] &amp; $patient_id[2] &amp; $patient_id[3] &amp; $patient_id[4] &amp; $patient_id[5] &amp; $patient_id[6] &amp; - \\\\
    \\hline
    \\end{tabular}
    \\end{table}

    END
</code></pre>

<p>Basically the perl script queries various tasks for each operator and stores the number of counts in each field. Operator is a perl array and is likely to change size by 1 or 2 values, i.e is likely It is likely that the operator array may change with time (i.e new initials added or removed). In such cases I would have rewrite the latex table part of my script i.e adding $operator[8] etc. I'm sure there is a more sensible approach to this problem using loops but I can't work out how to achieve this.</p>

<p>Any ideas?</p>

## Answers
### Answer ID: 14396668
<p>Define a function, which prints a row</p>

<pre><code>sub print_row
{
    my($fh) = shift;
    print $fh join(' &amp; ', @_), "\\\\\n";
}
</code></pre>

<p>This function prints a row to <code>$fh</code>, composed of all arguments to <code>print_row</code>. If you want more columns printed, just give more arguments.</p>

<p>Now use this in your table </p>

<pre><code>print $fh &lt;&lt;END; 
This report details clinical and imaging statistics from $date_start to $date_stop.

\\large \\bf Clinical Statistics

\\normalsize \\rm 

\\begin{table}[h]
\\centering 
\\begin{tabular}{p{4cm}cccccccc} 
\\hline
END

print_row($fh, '', @operator);
print $fh "\\hline\n";
print_row($fh, 'Cannulations', @venflons, '-');
print_row($fh, 'Clinical Assessments', @clin_ass, '-');
print_row($fh, 'Lead Stressor', @etlead);
print_row($fh, 'Assistant Stressor', @etass, '-');
print_row($fh, 'ECG Preparation', @ecg_prep, '-');
print_row($fh, 'Patient Identification', @patient_id, '-');

print $fh &lt;&lt;END; 
\\hline
\\end{tabular}
\\end{table}

END
</code></pre>

### Answer ID: 14397099
<p>to seperate every three items with a dash add into the printrow function</p>

<pre><code>#inserts dash if no remainder from division of four of the array index  
for (0..$#columns){
splice(@columns,$_,0,'-') unless ($_ % 4)
}
</code></pre>

<p>before the print statement.</p>

<p>coyote</p>

### Answer ID: 14396458
<p>You can use <code>join</code>:</p>

<pre><code>print '&amp;', join('&amp;', @operator), '\\';
</code></pre>

