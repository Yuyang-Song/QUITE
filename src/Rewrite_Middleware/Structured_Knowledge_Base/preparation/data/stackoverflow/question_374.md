# SSRS Calculating Totals
[Link to question](https://stackoverflow.com/questions/23066507/ssrs-calculating-totals)
**Creation Date:** 1397496796
**Score:** 0
**Tags:** reporting-services, ssrs-2008, ssrs-grouping
## Question Body
<p>In SSRS I have a report generated from a stored procedure. I have one column that is named "Price" and the report has various groupings (shown below). So because there are so many groupings there are a lot of totals for price. I need to roll these totals up into the parent grouping of TimeRange as an average. This is so I can know the average price of Z product was X. I obviously know that this is done by adding up all those totals and dividing by the amount of totals but I don't know how this can be done in SSRS. Is it possible to dynamically add up all those totals? Or maybe set some kind of global variables to handle this?</p>

<p><strong>EDIT:</strong> I described the problem a bit wrong. It seems the main problem is the fact that the price data returns all positive "prices" then the report uses the other columns to define if the price is negative or not(if we bought something or sold something). Since I didn't think there was a way to compensate this through the microsoft code. I Grouped them together based on the rules and multiplied the prices that should be negative by -1. I Now want to figure out a way to take these individual totals and combine them into one Subtotal. It would do this by taking a Sum of the totals. Just doing a straight Sum(Price) doesn't help because that will just get all of the values directly from the query before the report touches them and those values are all positive which throws off the report data. </p>

<p>So i guess there are three solutions here:</p>

<p>1.There is some magical SSRS code that allows me add together data that is outputted from an expression instead of the initial database value and does that dynamically..</p>

<p>2.There is some kind of way to define and assign global variables in the report then I could use some kind of psuedo code to add and subtract data from the variable and then take the average of the total</p>

<p>3.This is currently not possible and I will have to completely rewrite the source data's process or come up with another solution that's not SSRS.</p>

<pre><code>   TimeRange 
 _
| Product
|   _
|  |
|  | Time Unit
|  |  _
|  | |
|  | | TransactionType
|  | |  _
|  | | |
|  | | | Pay Status
|  | | |   Price Total Calculated Here  [Sum(Price)]
|  | | |_
|  | |
|  | |_
|  |
|  |_
|   
|
|
|_
</code></pre>

## Answers
### Answer ID: 23069261
<p>Use the <code>Avg</code> function to get an average of all the values in your grouping:</p>

<pre><code>=Avg(Fields!Price.Value)
</code></pre>

### Answer ID: 23068527
<p>Reporting Services makes this very easy - in fact, if you were to just use the wizard (table wizard in Report Builder, report wizard in Visual Studio/BIDS), and add all of your grouping fields to the "groups" section, and then enable subtotals, the summing would be done for you, and you could then alter the field using an expression to divide the two summed fields.</p>

<p>Here's a link to some more useful information on grouping and aggregates:
<a href="http://technet.microsoft.com/en-us/library/ms170712.aspx" rel="nofollow">http://technet.microsoft.com/en-us/library/ms170712.aspx</a></p>

