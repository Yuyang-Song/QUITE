# How to view modules and forms in a locked VBA Access application
[Link to question](https://stackoverflow.com/questions/76016523/how-to-view-modules-and-forms-in-a-locked-vba-access-application)
**Creation Date:** 1681484791
**Score:** 1
**Tags:** vba, ms-access
## Question Body
<p>At my workplace we have a 20 year old VBA Access application. We tried to buy the source code from the guy 10 years ago, but he didn't want anyone to call him. He died five years ago. I've been tasked to rewrite this application using SQL and .NET, but it would be nice to be able to see what is going on inside.</p>
<p>The database administrators have to compact the file every week, because it wasn't meant to handle the amount of data we have in it. If something breaks, we are in trouble.</p>
<p>When I open the MBD file (while holding down SHIFT), I can see the tables and some queries. However, when I go to Visual Basic, I only see one blank project called master60, with no modules or forms visible. I can trick it a little bit by going to the performance analyzer, and on Current Database I select &quot;VBA Project&quot;. Now, another project appears in the Project Explorer called acwztool. I can see forms and modules, but when I click on one of them, I get a &quot;Project Locked&quot; pop-up saying &quot;Project is unviewable&quot;.</p>
<p>I tried adding a trusted location, I tried exporting all objects into a new Access database, and I tried some online suggestion of changing a value in a hex editor to unlock it. Nothing seems to work. I'm not sure what kinds of locks people can put on these databases. I'm never prompted for a password...it is just locked.</p>
<p>Any ideas on how to tackle this? I'm using Office 365.</p>

## Answers
### Answer ID: 76019853
<p>Access was and is often used as the database. But, the code and application may very well have been developed using c++, VB5, VB6, maybe even delphi (pascal). So, you might try to look at the .exe file with some kind of inspector. But, if that folder has a .exe file, then that means the application part was not written in ms-access, but in some other system - only the database looks to be access. So, even some commercial products like Simply accounting at one time used Access database, but the application was not written using access.</p>
<p>Sometimes, by just looking at the application, you can make a guess as to the tools used, sometimes not.  But, since there seems to be a .exe in that folder?</p>
<p>You can open that .exe with say a hex editor - often you see bits and parts in the header that hints, suggests and &quot;tells&quot; what tools were used to create the application in question.</p>
<p>There are also a number of tools that can at least &quot;open&quot; a .exe file and give information about the .exe file -- often then one can determine the tools used to create the .exe.</p>
<p>Maybe your lucky, and it was written in say vb.net (I say lucky, since there are a number of de-compilers - that would in theory create/generate the source code used to create the .exe. However, if this is not a .net .exe, then things become more difficult to de-compile.</p>
<p>As noted, often just looking at a few of the other .dll's and what not will &quot;suggest&quot; what system was used. This is especially the case if you used such tools in the past.</p>

### Answer ID: 76016606
<p>Knowing it's an MDB and not an MDE, you should be able to unlock it by following this procedure: <a href="https://www.devhut.net/access-unlocking-an-access-vba-project/" rel="nofollow noreferrer">https://www.devhut.net/access-unlocking-an-access-vba-project/</a></p>
<p>which is quite similar to what's here for Excel: <a href="https://superuser.com/questions/807926/how-to-bypass-the-vba-project-password-from-excel">https://superuser.com/questions/807926/how-to-bypass-the-vba-project-password-from-excel</a></p>

