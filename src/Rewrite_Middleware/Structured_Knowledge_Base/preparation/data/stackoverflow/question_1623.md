# Migrate (monolithic) Classic ASP to ASP.Net
[Link to question](https://stackoverflow.com/questions/1724101/migrate-monolithic-classic-asp-to-asp-net)
**Creation Date:** 1258048157
**Score:** 4
**Tags:** asp.net, asp-classic, vbscript, refactoring, migration
## Question Body
<p>For many years I have had an objective of moving out of ASP/VBScript to a "better" language - my preference would be C# as I have skills in C - but I would consider other languages too (including PHP etc. so not just DotNet)</p>

<p>Objective is to have the code base in a language which does more for us. I hate the lack of data typing in VBScript, I would like a number of different "container objects" - rather than just a Dictionary Object, and so on - in fact I wonder why, having moved from Basic to C in the 80's, and then C++ a while after that, I managed to move "back" to Basic in to 00's.</p>

<p>(I could program the container objects in VBScript, but my instinct is that they would be slow in operation; we have a significant cache of "snippets" of HTML used in the rendering of the page, the ASP Application Object is a pretty blunt instrument!)</p>

<p>My ASP/VBScript is a single large application that is basically an "engine" to deliver web content.</p>

<p>It has been many years in the making, and now the ASP code changes seldom. (So I do need to justify moving it at all, or just living with VBScript "for ever")</p>

<p>It is driven from data in an MS SQL database.</p>

<p>There is only one .ASP page (made up of several include files).</p>

<p>Based on the query string parameters Skin and CMS templates for the page are loaded from database and suitable database Sprocs are run to acquire data which is merged into the CMS templates.</p>

<p>Data about the page (methods to use, etc.) is also retrieved from the database, along with details of access permissions and so on.</p>

<p>From what I have read some these things may make migration easier:</p>

<p>ASP sessions are not used - a session cookie is used to retrieve session data from the DB (so I could easily share a session half-and-half with ASPX</p>

<p>The VBScript uses OPTION EXPLICIT throughout, so all variables are predefined.</p>

<p>All output is via Response.Write (in fact most content is merged into a single variable and then output).  There is no mix of HTML and &lt;% server code %&gt;.</p>

<p>I have some VBScript classes, but not many.</p>

<p>I have lots of VBScript functions, and a few Subroutines.</p>

<p>I have a test suite.  This catches screen shots from the browser and graphically compares them with master images - thus I have the ability to do a regression test.</p>

<p>I don't have the resource to do a complete rewrite; maintenance of the existing code needs to continue during migration; but having said that 99% of our work is in CMS or SQL Sprocs, so the changes to ASP code are infrequent.</p>

<p>I have read of MS's utility to migrate ASP code to VB.NET. Given that my code is 100% VBScript and no mix of HTML/Script I would appreciate opinions on whether this would help me a lot or a little?</p>

<p>I would be happy to refactor STAYING IN VBscript with a view to making the migration to DotNet easier later on (but I'd need to know what my objectives were in doing that :) ).  I could, for example, move some/all the functions to a COM object, and could probably do that piecemeal?</p>

<p>Thanks for your help</p>

## Answers
### Answer ID: 1726912
<p>If you are looking for a way to justify the project to management, it will become increasingly more difficult to find classic ASP developers to continue maintaining the application. Any developer that has a choice would probably not choose to maintain an application built using VBScript. Developers that do take the job might consider it temporary and continue to look for other work.</p>

<p>Although I haven't heard anything from Microsoft, it can't be too many years before they decide to retire classic ASP entirely.</p>

### Answer ID: 1725037
<p>I have a large ASP classic intranet that I was maintaining until last year, and it was getting old, but new pieces were still being added in ASP classic because there was so much library code invested already. You already have a good setup if you are not changing the ASP code often and have some form of testing in place. (I have to admit it's the first time I have heard of the screenshot approach). If everything is driven off the DataBase and working. don't break it. </p>

<p>PHP will give you same problem of variant types, but will give you a world of options and choices that makes ASP classic seem like a childs toy. Out the box PHP does everything I've ever needed to do.</p>

<p>ASP.net is a BIG framework. Understanding it properly and fully is not an easy task, and it surprises me very often. it tries to do things for developers coming from a forms environment automatically that get very obtrusive when you come from a very precise rendering methodology like you sound you have. I found myself fighting the technology all the time, until ASP.net MVC came around. It fit my mind better because of how it worked and did what I asked it to, and nothing more. C# is an awesome language, with brilliant features and the DOT.net framework lets you do anything, if you can just find the right pieces. There is so much of it you will find yourself occasionally writing something that has been done in the framework already, only to find it just after finishing your own implementation.</p>

<p>Actually migrating could lead to some interesting problems. Even though you CAN run a ASP.net page much like an ASP classic page, you will loose many of the benefits of the environment as it is intended. That being said, I did do some test towards looking at migrating the site in question to ASP.net and managed to find ways around most of the stumbling blocks and reached the conclusion that such a migration would in fact be "mere work". The sheer quantity of man-hours it would take to do such a migration though made the undertaking infeasible.</p>

<p>Personally I would not suggest such a migration unless you have a few ASP.net projects under you belt successfully and are aware of the gotchas that asp.net brings with-it.</p>

<p>I have not seen the ASP to ASP.net conversion tool you speak of, but would love to get a link to it.</p>

<p>If you are staying in VBScript and are not aware of the AXE (ASP Xtreme Evolution) project <a href="http://zend.lojcomm.com.br/goodies/" rel="noreferrer">here</a> I can highly suggest looking into it for inspiration on getting past/around several of the ASP classic "limitations" and for the library of functionality it provides.</p>

