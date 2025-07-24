# What new tricks can an old dog learn?
[Link to question](https://stackoverflow.com/questions/9019994/what-new-tricks-can-an-old-dog-learn)
**Creation Date:** 1327589752
**Score:** 1
**Tags:** asp.net, asp.net-mvc, linq-to-sql, ado.net, webforms
## Question Body
<p>Back in 2006 I've created a web site using asp.net 2.0. At that time, I had used Web Forms and classic ADO.NET SQL queries to connect to the underlying database. I've also used a fair amount of XSLT.</p>

<p>Today, the site still stands (it has gone through various upgrades but it is still based on Web Forms and simple SQL queries) but I believe it really needs to be upgraded as far as its technological infrastructure is concerned. </p>

<p>What is the next step I should take to move forward? A bit of ajax? JQuery maybe? Rewrite it in asp.net mvc? Replace SQL with typed datasets or even ling to sql? And what is the best way to embrace APIs such as twitter's?</p>

<p>So, can an old dog learn new tricks?</p>

## Answers
### Answer ID: 9020284
<p>So why do you believe the site's infrastructure needs to be upgraded?  If the site is running and performing well after 6 years of load and data, then what factors are causing you to think you need to upgrade it?</p>

<ul>
<li><p>Are there features that you want to implement (or users are asking for) that you can't implement with the current infrastructure?</p></li>
<li><p>Is maintenance difficult and brittle, and every time you upgrade, you spend weeks fixing bugs introduced?</p></li>
<li><p>Are there integrations that you'd like users to be able to do so that they can extend your application's functionality and/or data to their own applications?</p></li>
</ul>

<p>Those reasons above could be reasons to upgrade, but I can't really tell you.</p>

<p>But as far as some of your questions about what to upgrade:</p>

<ul>
<li><strong>a bit of AJAX?</strong>  It depends on what your current infrastructure looks like, but it's not too hard to introduce and you can isolate it
pretty well with a service layer.   </li>
<li><strong>jQuery?</strong>  Again, it depends on
how your pages are structured.  If you have a lot of master page
re-written IDs and very few classes on your DOM elements, using
jQuery right off the bat may be tough as you'll have to figure out
how to get your selectors in line.   </li>
<li><strong>Replace SQL with Typed
DataSets?</strong>  Please don't do that.  Honestly, if you go with
Linq-to-SQL or EF, you'll probably take a slight performance hit
compared to using ADO.NET with DataReaders (if that's what you're
using).   </li>
<li><strong>Can an old dog learn new tricks?</strong>  Always.  The learning
never stops.</li>
</ul>

<p>I would just advise not to upgrade just to upgrade.  Make sure you have legitimate business reasons for doing so.</p>

<p>Hope this helps.  Good luck!</p>

### Answer ID: 9020066
<p>You could create a persistence layer and learn about entities. This is an extremely useful skill to have. You could do this by using NHibernate. I would also throw in some LINQ to get a great combo. After this i would probably go to the GUI and do some needed features with jQuery</p>

### Answer ID: 9020056
<p>Step 1) figure out what would add value for your users</p>

<p>Step 2) investigate technical solutions to solving those problems</p>

<p>Step 3) learn and build</p>

