# How can I unit test my project, when most of it access a database with a poor schema that I cannot change?
[Link to question](https://stackoverflow.com/questions/26735153/how-can-i-unit-test-my-project-when-most-of-it-access-a-database-with-a-poor-sc)
**Creation Date:** 1415104041
**Score:** 2
**Tags:** c#, asp.net, linq, unit-testing
## Question Body
<p>I'm working on a asp.net Webforms project.</p>

<p>The project isn't covered by any tests at all, besides from the few unit tests I wrote myself to cover a small static method of mine. I would like to write unit tests for the entire project so that I can refactor, and add code to the project more efficiently (I have the support from the CTO about this), but I've run into a problem.</p>

<p>The web application mostly consists of linq queries to the database, with no abstraction between the database and the code, in other words we don't use something like a repository instead we just type the linq queries where ever we need them. </p>

<p>From my understanding, unit tests should not call a database directly as that would be to slow, so I would like to decouple them from the database. I first tried that with a mocking framework called MOQ, it seemed to work but then I read that LINQ-queries to a database has a different behaviour to LINQ-queries to objects so the tests passing doesn't mean that my methods work</p>

<p>This made me consider the repository pattern, hiding the linq queries in repository classes and then mock these classes in my tests. There are (as far as I can tell) two problems with this.</p>

<ul>
<li>Changing the project to using the repository pattern is a massive job, and I'm not sure that the repository pattern is the right tool work the job. So I would like to know beforehand if it is suitable or not.</li>
<li>The database schema isn't very good, It was made for us by another company, and they simply took a generic schema and added a few rows in a few tables to "customize it" for us. Many of the tables and columns are poorly named, it can't contain all the data we need it to contain, and the logical structure doesn't suit us very well, which require complicated queries. I'm pretty sure that the correct solution is to rewrite the schema to suit us, but the CTO wants it to remain the same so the project can be more easily modified by the company who made the database and project if we want them to, so that's not an option.</li>
</ul>

<p>Assuming that a repository pattern is what I should use, my question is, how do I deal with the poor database schema. I assume that I need to hide it behind an abstraction that handles the complicated quering for me, maybe draw an er-diagram to figure out how the schema should look like, but I could be wrong, and I'm not sure about the details.</p>

<p>I would love if you could give me links to examples, and tutorials, and tell me if my assumtions are wrong.</p>

<p>Thank you in advance for your patience and help.</p>

## Answers
### Answer ID: 26735966
<p>Database schema should not matter when we are writing unit tests because we are going to block the calls to database by mocking it. There are number of things you can do</p>

<ol>
<li>If the database calls are already in their own project like DAL then
best thing to do is create interface and implement by the DAL class,
e.g. CustomerClass : ICustomerClass this will help you alot in the
mocking.</li>
<li>If time and budget allows it then repository pattern is the way to
go but write integration tests first which will cover the whole
system. Once integration tests are written then you can refactor the
code. you can always verify the refactored code by running
integration tests. once the class has been refactored write unit
tests for it. you can/should always write scenarios which will help
understanding the business as well by using <a href="http://www.specflow.org/getting-started/" rel="nofollow">SPECFLOW</a> for
integration/unit tests.</li>
</ol>

<p>do not dive in the code and re-factor it, do some analysis work and make a document, believe me this doc will come in handy.</p>

### Answer ID: 26735777
<p>If this was me I would not focus on unit tests for this. I would first try and get a suite of End-To-End tests which characterize the behaviour of the system as it stands. Then as you refactor parts of the system you have some confidence that things are no more broken that they were before.</p>

<p>As you point out, different linq providers have different behaviour so having the end to end tests will ensure that you are actually testing the the system works.</p>

<p>I can recommend SpecFlow as a great tool for building your behaviour based tests, and I can recommend watching <a href="http://www.pluralsight.com/courses/executable-specifications-specflow" rel="nofollow noreferrer">this video on pluralsight</a> for a great overview of SpecFlow and a good explanation of why you might be better with end to end tests than having unit tests.</p>

<p>You'll also get a lot out of reading <a href="https://rads.stackoverflow.com/amzn/click/com/0131177052" rel="nofollow noreferrer" rel="nofollow noreferrer">'Working effectively with legacy code'</a> and reading some of the links and comments <a href="https://softwareengineering.stackexchange.com/questions/122014/what-are-the-key-points-of-working-effectively-with-legacy-code">here</a> might be useful as well.</p>

<p>You'll notice that some of the comments linked above point out that you need to write unit tests, but often you need to refactor before you can write the tests *as the code isn't currently testable), but that this isn't safe without unit tests. Catch-22. Writing End-To-End tests can often get you out of this catch-22, at the expense of having a slow running test suite.</p>

