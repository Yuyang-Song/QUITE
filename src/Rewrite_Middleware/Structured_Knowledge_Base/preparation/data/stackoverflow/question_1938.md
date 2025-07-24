# display of mysql calendar per months
[Link to question](https://stackoverflow.com/questions/12940276/display-of-mysql-calendar-per-months)
**Creation Date:** 1350496146
**Score:** 0
**Tags:** mysql, sql, pivot
## Question Body
<p>I'm am developing a website featuring a vacancy calendar connected to a database. I have managed to create the table that lists every single day from 2012-10-01 to 2030 with the following fields:</p>

<pre><code>MyTable
-----------                 
 -dt date                       
 -mid smallint (ID for each month)  
 -y smallint (year)         
 -m tinyint (month)         
 -d tinyint (day)                   
 -dw tinyint (day of week)          
 -monthName varchar             
 -isVacant binary   
 -isWeekday  binary
</code></pre>

<p>I would like to display this data on the website showing each month (mid) in a row, showing each day and whether they are vacant or occupied. I need to basically turn data from rows into columns.</p>

<p>I have looked for a query to do that but nothing has worked so far. I have tried to rewrite examples of pivot query but I don't seem to be getting the syntax right. Could anyone help me with this? </p>

<p>here is what the stuff looks like:
<a href="http://www.mathieuleguet.com/display/db-view.html" rel="nofollow">mysql calendar table</a> -
<a href="http://www.mathieuleguet.com/display/final-table.html" rel="nofollow">html table</a></p>

## Answers
### Answer ID: 12941293
<p>I'm not sure but I think this is what you want to get. Could've been better if you supplied table data and result sample:     </p>

<pre><code>select m, (case d when 1 then isVacant),  (case d when 2 then isVacant), 
 (case d when 3 then isVacant), ..... 
from MyTable
group by m
order by m
</code></pre>

<p><strong>EDIT :</strong>  Have a look at <a href="http://sqlfiddle.com/#!2/0ce37/1" rel="nofollow">sqlfiddle</a>
Note that I created isVacant column as integer typed field.</p>

### Answer ID: 12940813
<p>Why do you want to get the data into single rows in the mysql query? I'd just pull the data into php, one row per day, and use php to arrange the data however I want. There probably is a mysql solution, but I don't think it's worth the effort. Just loop through the days, populating your array as you go.</p>

