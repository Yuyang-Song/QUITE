# phpUnit and models which inherit ADODB_Active_Record, stubbing ADODB_mysql
[Link to question](https://stackoverflow.com/questions/6615515/phpunit-and-models-which-inherit-adodb-active-record-stubbing-adodb-mysql)
**Creation Date:** 1310064148
**Score:** 0
**Tags:** unit-testing, phpunit, adodb
## Question Body
<p>I've searched high and low and, astonishingly, cannot find an answer.</p>

<p>When trying to unit test my models with phpUnit how can I stub the database?</p>

<p>I'm using a PHP framework CMS which has a number of classes which inherit from a class ("Model") which inherits from ADODB_Active_Record. Model's constructor grabs a db object (from ADOConnection) and passes it to Active_Record's constructor.</p>

<p>It might not be Best Practice, but in order to change the code as little as possible, I'm thinking of tweaking grabDBObject()  to return a stub object when in testing. That stub gets passed to ADODB_Active_Record, and, in theory, I can test my models.</p>

<p>However, I can't figure out how to create the stub. ADODB_Connection isn't simple. It's not going to be a matter of replacing Execute(). There are a bunch of other functions, like qstr(), that it appears I'll have to worry about and rewrite as necessary.</p>

<p>What's surprising is I can't find any discussions of people doing this. This has got to be a common problem. Am I going in the wrong direction? I understand that I can use something like dbUnit to actually do db queries rather than stubbing ADODB_connection, but I also understand that I should stub as much as possible, and that it's bad to rely on a db for unit tests of a model's methods.</p>

<p>So,
1. Should I be stubbing the db connection for unit testing?
2. How?</p>

## Answers
### Answer ID: 6814374
<p>Have you tried the getMock() method of phpunit ? </p>

<p>It allows you to provide a fake object for testing, without touching your production code. </p>

<p>But in that case, you have to build the expected result by yourself. </p>

<p>The doc is here : </p>

<p><a href="http://www.phpunit.de/manual/3.0/en/mock-objects.html" rel="nofollow">http://www.phpunit.de/manual/3.0/en/mock-objects.html</a></p>

