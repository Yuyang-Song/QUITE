# Crystal Reports 2008 - parameters from selection criteria are not being used to select to retrieve data from db
[Link to question](https://stackoverflow.com/questions/6219418/crystal-reports-2008-parameters-from-selection-criteria-are-not-being-used-to)
**Creation Date:** 1307043117
**Score:** 0
**Tags:** crystal-reports-2008
## Question Body
<p>I have some reports written in Crystal 2008 using business views. These reports have a date parameter set up and I have a selection on the date defined in the select expert. However, when I run the report it appears to retrieve all the data from the database and only then filter out based on the date. As you can imagine this slows down the report quite a bit. I also clicked on Database-Show SQL Query and confirmed that the date parameter did not appear in the SQL Query. This behavior seems very strange to me. This did not use to happen to me when I used Crystal 8.5 with dictionaries. Is this a limitation using business views?</p>

<p>I did some searching and found that I can create a report using a database command. This helped improve performance on one of my reports but when I tried to do something similar on a different report, even though I was using the database command, it still did not appear in the appear to be doing the selection on the database before retrieving the data and the report took forever to run. I also didn't see the selection in the SQL Query. 
Do I need to add the parameter to the database command? Will I be able to prompt the user to enter the value when they run the report?</p>

<p>I hope there is a way to do this properly using business views because otherwise I'll have to rewrite all my reports to use another method.</p>

<p>Any ideas or advice are welcome. Thank you very much!</p>

## Answers
### Answer ID: 6232551
<p>I figured out what the problem is. My business view had fields in it that were formulas. If you try to use selection criteria using a formula, it does not add the criteria to the WHERE clause in the SQL Query. Luckily, I was able to find other fields besides the formula in the business view to do the selection.</p>

### Answer ID: 6230217
<p>I had a similar problem. I used the command, but my report was still taking longer than i had hoped to run. so i added a where statement into the command to start checking dates starting from 2009. that sped up my report a little. </p>

<p>you may want to consider creating a stored procedure if you think you are pushing CR to the limit. that may also help sped up the report.</p>

