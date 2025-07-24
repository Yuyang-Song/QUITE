# Making the switch from mdb to accdb (from Access 2003 to 2010)-build or &quot;save as&quot;?
[Link to question](https://stackoverflow.com/questions/20482638/making-the-switch-from-mdb-to-accdb-from-access-2003-to-2010-build-or-save-as)
**Creation Date:** 1386629928
**Score:** 0
**Tags:** database, ms-access, vba, ms-access-2010
## Question Body
<p>We have an Access database we built in Access 2003 that is pretty simple, just a bunch of tables, forms and reports that work in tandem for data entry. We want to repurpose the objects in that database and build a new db in Access 2010, to finally get with the times. </p>

<p>Note, we do not need to upgrade or convert the old database (with all of the existing data). But want to start fresh and create a new database in 2010 that functions just like the old one. </p>

<p>I have tried two methods and they give me different results, I am hoping to get some insight as to why:
ONE:
First, I opened my newly installed Access 2010 app and pointed to a copy of my old .mdb. Opened it and did a "Save Database as" .accdb with a new name. Access thought for awhile then told me "This Database has been upgraded..." Opened the database via my Main Menu like a user would, but the basic functionality of my new database doesn't work. The debugger gets prompted on my first or second button event click. So I think, "Guess I have to rewrite my VBA!"</p>

<p>TWO:
I opened a empty database in Access 2010. Then imported all of the objects right from my old .mdb (tables, forms, queries, macros, modules, reports, blah blah). Opened the new .accdb database via my Main Menu and every button, every field on every form worked like a charm. </p>

<p>Can anyone tell me what Access did during that "upgrade?" If option two worked for me, am I golden without having to do major recoding (once I have finished rigorous testing that is)?</p>

<p>Thanks in advance!</p>

## Answers
### Answer ID: 20503351
<p>Looks like I found a fix. 
My Access 2003 database was running a legacy version of ActiveX Data Object Library (2.1). I think that when Access 2010 did the upgrade, this reference library was too old to operate with 2010. Simply unchecking this library (View Code-->Tools-->References) or updating to ActiveX Data Objects 2.8 restored full functionality of my forms.</p>

<p>This link talks about legacy ActiveX Data Objects.
<a href="http://support.microsoft.com/KB/825440" rel="nofollow">http://support.microsoft.com/KB/825440</a></p>

