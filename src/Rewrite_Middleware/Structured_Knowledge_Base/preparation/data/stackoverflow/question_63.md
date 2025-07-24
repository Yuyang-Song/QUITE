# Strategies for encapsulating the differences between SQL platforms?
[Link to question](https://stackoverflow.com/questions/11540866/strategies-for-encapsulating-the-differences-between-sql-platforms)
**Creation Date:** 1342612818
**Score:** 2
**Tags:** java, sql, encapsulation, robustness
## Question Body
<p>I'm working on accelerating some slow operations here, and one case is a tree of parent-child relations in a table. Currently the system is running on SQLServer, and after some research I found that with common table expressions multiple queries can be compacted into one.</p>

<p>So far so good, but the syntax is specific to SQLServer and doing the same thing with (for example) Oracle would require a completely different syntax.</p>

<p>What can be done to structure the system to allow for future adaption to other RDBMS? My main concerns here are:</p>

<ul>
<li>SQL statements are littered over the code, and what may be possible with <em>one</em> statement in one RDBMS may require multiple statements in another, thus even the program logic may need changes.</li>
<li>Even things that can be encapsulated nicely in one RDBMS (I'm using stored functions to hide some of the complexity in the DB) have subtle difference along different DB's or are not available at all.</li>
</ul>

<p>So far I feel that everything that goes beyond the most simple SQL statements seems to always require vendor specific extensions, making it impossible to keep the differences hidden neatly in a few classes/stored SQL's (sure on <em>can</em> use a <em>framework</em> that has most of the abstraction already build in. But that also rules out many of the more useful features of the DB).</p>

<p>What strategies can be used to at least <em>ease</em> the pain of vendor differences? I'm aware that this is a very broad question that has no cure-all answer. But I'm hoping for some pointers and patterns to lessen the impact the DB has on the application.</p>

<p>EDIT: Implementation language is Java, simply using an ORM (like e.g. Hibernate) is not what I'm looking for (would more or less require to rewrite ~50% of the code base).</p>

<p>EDIT2: I'm looking mainly for possibilities to push the specifics out into the database in a as-commonly-compatible way as possible, ideally I want the SQL's used by the java part to be the same for all platforms (or only require very slight changes due to syntactic differences). For the example with the CTE I gave, I currently pushed that out into a stored function in the hope that when it needs to be ported the functionality can be reproduced in a function as well.</p>

<p>EDIT3: Currently I <em>don't have a pressing need</em> to support other RDBMs. Nobody will blame me if it works only with SQLServer. But where possible I like to avoid to tie the java code more than necessary to a specific DB vendor.</p>

<p>EDIT4: Some background - The current work is adding functionality to the system - functionality it was not designed nor planned for. The requirements trickle in bit by bit from the buisness guys and its hard to plan ahead. While each requirement by itself isn't terribly hard to solve, I'm afraid we will accumulate a big mess of tagged on stuff that is impossible to port without going trough every query in great detail. Since SQLServer itself also introduced various incompatibilites with itself with each major new release I'm worried that even switching to a newer SQLServer may become a major obstacle in the future (we did one such upgrade from 2005 to 2008 in the past - that one went smoothly for the stuff I'm maintaining but it caused already a number of issues for one of our suppliers).</p>

## Answers
### Answer ID: 11544923
<ol>
<li><p>Stay away from ORMs. They do have their purpose in projects, but if you only want database independence, it is like buying a General Factory Factory when all you need is a hammer and some nails.</p></li>
<li><p>Isolate your data access layer behind a set of interfaces. Nothing in your code base should be database dependent, but the implementation of these interfaces. So no class outside those implementation should access anything with 'jdbc', 'jpa' or 'hibernate' in the class path. You might consider writing actual tests for that using JDepend or DependencyFinder.</p></li>
<li><p>Make your current database access implement those interfaces.</p></li>
<li><p>Have automated tests that run against the actual database and that are prepared to run against a set of different databases.</p></li>
<li><p>When you have to support a second database, modify your tests to run against both databases. Make the interface implementation a copy of the original implementation, then fix the failing tests.</p></li>
<li><p>Now look at your two implementation and find stuff that is worth extracting and refactor your code accordingly. </p></li>
</ol>

<p>If you try to move step 6 further up in the chain you're going to encounter bad cases of YAGNI and WrongAbstractionException.</p>

<p>If you decide to use any kind of ORM or some other database access technology, the same rules apply.</p>

### Answer ID: 11543203
<p>You might look into using the MyBatis framework.  MyBatis maps SQL queries and result sets into Java objects, and it also has some support for DB specific query generation.  It's extremely lightweight to drop into an existing application, and it'll probably reduce your total lines of code dramatically.  Take a look at <a href="http://www.mybatis.org/core/dynamic-sql.html" rel="nofollow">the section on Multi-db vendor support in their documentation</a> for a quick example mapping file that demonstrates the functionality.</p>

### Answer ID: 11542536
<p>Given you are in legacy code, I'd go for one interface, and initially one implementation, add methods to it for each db related function e.g. SaveOrder, that takes a simple class e.g. Order :) , or at a push a Dataset.  Bolt more stuff in as you go along, until all your sql is in the implementation and everything that uses it goes through the interface. </p>

<p>Then when you want to implement to another db, or perhaps other persistence layers such as NoSQL, Xml or an ORM, you know what you have to do and you have a battery of unit tests as well.</p>

### Answer ID: 11542118
<p>You did not specify what application platform yuo are using. But I would assume that you are using either .Net or Java. Your first line of defence is to use ODBC or JDBC escape sequences in the SQL statements in your application and push anything that cannot be handled by this approach into the stored procs.</p>

<p>If you have a license for a more thorough refactoring of the application, you should consider switching to an ORM library for your application platform.</p>

<p>EDIT: I see you edited your question clarifying that you are using Java and swithcing to an ORM library is not an option. Quite some time ago I was working on developing a product for large enterprise customers. Each of the customers had their standard reference architecture, so we had to accommodate Oracle, Microsoft SQL Server and UDB/DB2. We might have supported other platforms, but some details do tend to get fuzzy after 10-12 years. We achieved that by religiously using JDBC escapes for time constansts, functions and stored proecedure calls and by pushing the more sensitive operations into database-specific stored procedures. So I can tell you based on my expereince that this approach works. Currently, through a chain of acquisitions, this product is part of the Oracle middleware portfolio, so I don't even know whether it supports anything other that Oracle anymore.</p>

<p>My another experience was on a big data warehousing project. In that case we so heavily used Oracle-specific features that moving to another database platform was not an option at all.</p>

<p>So, my advise is to evaluate whether using SQL Server - specific features is inherent to your application. If it is, you should just accept that moving to another platform is not an option without a major re-write. Although if it is not, see if you can improve your sprincled around SQL by using JDBC escapes.</p>

