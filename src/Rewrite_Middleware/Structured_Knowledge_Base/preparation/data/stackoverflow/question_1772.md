# SQL Queries in loops with PHP
[Link to question](https://stackoverflow.com/questions/7301517/sql-queries-in-loops-with-php)
**Creation Date:** 1315163296
**Score:** 1
**Tags:** php, mysql, optimization, content-management-system
## Question Body
<p>So I have recently taken over maintenance of an in-house Content Management System, and database optimization is not really my area of expertise.</p>

<p>Anyway a couple of things fell out to my eye when I was looking over the code.</p>

<p>The php code is a little bit "spaghetti with meatballs" with little to no comments.</p>

<p>But the biggest thing: As far as I can tell, the original programmer decided to forgo table joins entirely in the database code (both implicit and explicit).</p>

<p>For example here is the process to display a page column:</p>

<p>Fetch element list from the database
For each element call a subroutine to check display permissions and if successful, call another subroutine to fetch the element's html data.</p>

<p>Each of the subroutines effectively calls a separate query for each element. And the permissions step, I believe, involves querying two separate tables.</p>

<p>Performance isn't really a problem at the moment, and I wasn't asked to look into this. Although the page requests are a bit slow in my opinion.</p>

<p>Is it worth trying to rewrite the SQL stuff? I am thinking that the increase in maintainability will be worth it in the end, and that it will make things easier for me should scalability become an issue in the future.</p>

<p>Or is it not really as bad as I think? Maybe I am just overreacting. An expert opinion would be appreciated.</p>

## Answers
### Answer ID: 7301745
<p>Refactoring is an important part of development process. Ignoring this fact means more problems in the future. The part of the problem is that not many managers understand the importance of continuous refactoring.<br>
I'd recommend you to read "Refactoring to Patterns" by Joshua Kerievsky that has many good examples of how to safely change existing code by implementing new design approaches. </p>

<p>As of your question about SQL queries, it may or may not be the first thing you need to change. </p>

### Answer ID: 7301610
<p>Your question is a bit too generic to give a good answer to and you haven't provided enough information to make educated guesses either, for your particular situtaion.</p>

<p>Things to take in to account:</p>

<p>Will the system grow over time? And how?
If there will be more users online, more preassure on the system - then there's cause for alarm. Systems with bad design does not scale well.</p>

<p>Bad code is one thing, but bad database- and general system design is worse. I think the key might be your comment about "next few years". If you intend to stick with the sytem for that long - then a serious look at the basics is a good idea. If your system might be up for replacement by something else (inhouse CMS's tend to be replaced) then you can patch along while shopping for the right thing.</p>

<p>But as your question stands - rewrite some of the questions, make sure your DB is normalized and refactor your code. Tell your boss it's the right thing to do if you're going to stick with the system.</p>

### Answer ID: 7301579
<p>If its about making your job in the future easier, I would start refactoring the spaghetti code before fixing the queries. Once you have a nice design, it should also be more straight forward how to integrate (and maybe even eleminate) some of those manual joins.</p>

### Answer ID: 7301563
<p>I think it would be worth rewriting while you have the time to do so. You don&rsquo;t want to put it off until it becomes a problem. I say, let the database do what it does best. In this case, table joins would certainly perform better than multiple queries in a loop.</p>

