# Bizzare Database.Close (DAO) issue in Excel Userform
[Link to question](https://stackoverflow.com/questions/42097540/bizzare-database-close-dao-issue-in-excel-userform)
**Creation Date:** 1486493055
**Score:** 1
**Tags:** excel, ms-access, vba, dao
## Question Body
<p>I have an Excel Add-in (with a Userform) which connects to an Access database (using DAO) to perform various functions. I've been using this combo for over a decade. Neither the code in Excel nor the database have been changed recently. Just last week, a user reported that one of their functions was taking much longer than usual, so I looked into it. It ended up that the function itself ran just fine, but when the code was cleaning up and ran db.Close it hung up. It doesn't produce an error, it still eventually succeeds, but it takes around a minute to close the db and move on.</p>

<p>I'll go through all of the symptoms and attempted solutions to see if anyone else has any ideas because I'm at a loss.</p>

<p>This only happens when you run db.Execute. I can open the database and close it right away and it closes just fine. If I open it, run a SELECT query to populate a recordset, then close it, it also closes just fine. But if I open it and run a single UPDATE/SELECT INTO/INSERT/ALTER/DROP statement, the Close method will take a minute to run.</p>

<p>My first thought was to compact the db. I cleared out several unused, old tables and compact/repaired, but this did nothing. Same problem.</p>

<p>My next attempt was to recreate the db. I made a brand new TEST db, imported all of the tables from the old one, pointed my Excel Add-in at the new db and did the same tests. Same results.</p>

<p>My next attempt was to try moving it to a local drive (it's on a network share). This <em>slightly</em> reduced the hang at Close, but it's still there. Not that it matters, because this db has to be hosted on a network share.</p>

<p>My next attempt was to delete a bunch of tables from my TEST database. I cleared out about half of them and the hang at Close was reduced a good deal. Clearing out even more reduced it even more. Deleting all but one table eliminated it. So now I know my problem has to do with the size of the db, but why? It maxed out at 500MB after the compact, which isn't that large. It's been running just fine for years. Why all of a sudden would the size/number of tables be such a huge issue? I obviously can't delete all of the tables in the production database just to solve an issue with Closing the connection.</p>

<p>As I mentioned, this code has been around a long time and the prod db was actually in Access 2000 format (mdb), so my next attempt was to change the format. I tried importing it all into both an Access 2003 format (mdb) and the latest Access 2016 format (accdb). The results were the same.</p>

<p>On a lark, I figured I'd trying hitting the db from somewhere other than the Add-in (on the off chance that the problem was in my Excel file). I copied and pasted my test code into a Word 2016 module... and it ran just fine.</p>

<p>That's odd.</p>

<p>So then I tried a brand new Excel file. Also ran just fine.</p>

<p>So I go back to my Add-in and try the code pasted into a Module.</p>

<p>Again, runs fine.</p>

<p>??</p>

<p>So I open the Userform and run my test code again. Hangs up.</p>

<p>??????</p>

<p>I create a brand new Excel file, make an empty Userform, paste my test code in the form's Initialize event.... hangs up.</p>

<p>I immediately run that same code in a Module afterwards... still hangs up. Even though a minute ago it ran just fine in a module in a different file.</p>

<p>But if I close the file, open a new one, paste in the code WITHOUT opening the Userform, and run it, it works fine. Creating/opening a userform will cause all subsequent attempts to run the code to hang.</p>

<p><strong>So here's the Cliff's Notes version:</strong></p>

<p>Excel 2016 DAO connection to large-ish Access database hangs on db.Close under the following circumstances:</p>

<p>1) The db is large (deleting most of the tables helps but obviously isn't a solution).</p>

<p>2) You have <em>opened</em> any Userform at any time during your Excel session. All attempts during OR after the opening of the form, no matter where the code is run from, will hang. Running the code before opening a Userform does not hang.</p>

<p>These results are duplicated on multiple Windows 7 machines, all with what appear to be the latest updates to Office.</p>

<hr>

<p>EDIT: I was able to try this out on a remote machine running Excel 2013 and there is no hang (using the original Add-in/db that first exhibited the problem). However, that machine is in our data center which is the same place that the network shares are located, so there are at least two possible reasons why it doesn't hang: 1) Different version of Excel and 2) Different/faster network connection.</p>

<hr>

<p>If you're wondering why I'm using DAO instead of ADO, it's because of what these functions do (lots of stuff with looping through Tabledefs to modify indexes and even create/modify the table Description, which can't be accessed via ADO. If it weren't for all that, I'd just switch to ADO and be done with it. It's possible that I might be able to come up with ADO alternatives/work-arounds for everything that it's currently doing, but I'd rather not rewrite this entire Add-in if I can help it.</p>

<p>I'm at a complete loss on this one, so if anyone has any ideas, I'm all ears.</p>

