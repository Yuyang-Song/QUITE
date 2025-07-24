# Subquery with an Exist
[Link to question](https://stackoverflow.com/questions/72118417/subquery-with-an-exist)
**Creation Date:** 1651692133
**Score:** -1
**Tags:** sql, subquery, inner-join, exists, adventureworks
## Question Body
<p>I am a user working in inventory management attempting to return information regarding product name, location, and its availability at the location from the adventure works 2017 database. While trying to run the query, I am getting an error message that states I have too many expressions in my subquery list and that I can only do that if I start the subquery with 'Exists'. I suppose I do not understand what I am doing wrong, maybe someone could explain how 'Exists' works? Is there a way I can rewrite this so I can return both expressions in the subquery? I will include the syntax and error message below.</p>
<pre><code>SELECT Production.Product.Name
       ,(SELECT Production.Location.Name
         ,Production.Location.Availability
         FROM Production.Location
         WHERE Production.Location.LocationID = Production.ProductInventory.LocationID)
FROM Production.Product
    INNER JOIN Production.ProductInventory
    ON Production.Product.ProductID = Production.ProductInventory.ProductID;
</code></pre>

## Answers
### Answer ID: 72118518
<p>You don't need a <em>subquery</em> here this appears to be just an outer join:</p>
<pre><code>select p.Name, l.Name Location, l.Availability
from Production.Product p
join Production.ProductInventory i
left join Production.Location l on l.LocationID = i.LocationID
on p.ProductID = i.ProductID;
</code></pre>
<p>Note how tidier the query is by using table aliases.</p>

