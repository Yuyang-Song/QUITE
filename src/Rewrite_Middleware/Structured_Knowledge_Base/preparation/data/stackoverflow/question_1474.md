# Efficiently searching hundreds of thousands of records with .NET listview
[Link to question](https://stackoverflow.com/questions/7768500/efficiently-searching-hundreds-of-thousands-of-records-with-net-listview)
**Creation Date:** 1318599622
**Score:** 4
**Tags:** .net, sql, list, listview, view
## Question Body
<p>this is my first question here on SO although I've been lurking for quite a while. I'm wondering what the best way is to search through around 350,000 records in a product database. I'm rewriting an application that currently searches something like this: As soon as you click Enter on the search textbox, the DB is queried and displays 10 records. Then as you navigate through the records with the up and down arrows within the ListView control, it will query for the next 10 records depending on the direction your going. Looking at other questions, I couldn't find any that specifically addressed doing this with the ListView in VS2010. I've done a little research on the Virtual Mode of the ListView, but figured since it's only displaying 10 records at a time, the normal ListView would be fine.
I'm currently able to display 10 records, but am getting stuck trying to figure out how to keep track of and query for one more record.</p>

<p>Has anyone had any experience with this or possibly have some advice? Thanks!</p>

## Answers
### Answer ID: 7785150
<p>Tom, thanks for the quick response and detailed answer. I've spent some time over the weekend trying different ways to implement this and your insight was very helpful.
What I decided to do was on form load, load the first 10 records that matched the search. Then if they did scroll at all (they have selected the last record on the page AND the key pressed was the down arrow), I queried the database again using SQL similar to this: </p>

<p><code>SELECT TOP 1 Item, Description, BuyPrice, SellPrice FROM Product WHERE ID NOT IN (SELECT TOP &lt;# of records received so far +1&gt; ID FROM PRODUCT WHERE Description like '&lt;search text&gt;%' ORDER BY Description ASC) AND Description like '&lt;search text&gt;%' ORDER BY Description ASC</code></p>

<p>I know this isn't the most efficient way to do it, but it worked surprisingly well, enough so that the speed is fast enough to use in production. I suppose you could also SELECT the next 10 records too, but I'll try that if need be. Again, thanks for your help.</p>

### Answer ID: 7768629
<p>Let me start out by saying that I haven't done a lot of front-end coding in years, but there are certainly some caching options in .NET. Dealing with 350K rows, I don't know if that's really feasible though.</p>

<p>Another option would be to store the cached results in a table (or tables) in the database with a user or connection identifier so that you can keep track of which cache results to use.</p>

<p>A third option is to simply store on the front end the min and max values for whatever your sorting column is in the list. You can then pass these in for the next/previous calls and the database can look up the appropriate page each time. One downside to this is that as people are updating the database you might not have consistent results. For example, I could hit "next", someone might add a row that falls into the range for the previous page and now when I hit "previous" I'm seeing that row along with nine of the original rows instead of the ten rows that I had just been looking at before that.</p>

<p>Now for my own strong opinion on front-end searches. You should <strong>never</strong> allow a user to page through 350K rows. The human mind can't deal with that many things anyway. Do you really think that a user will hit the "next" button 35,000 times? Either require them to enter search criteria that limits the rows to some set and reasonable number OR no matter what they're search criteria is, only allow them to go, for example, 100 pages. If they try to go to page 101 then give them a message that tells them to limit their search. The advantage here is that you can easily use any of the caching methods and the results are limited enough that you don't run into resource issues there.</p>

<p>I hope that this is helpful for you. If you have questions specific to any of the above patterns then you can either post them here or create a new question for that specifically.</p>

