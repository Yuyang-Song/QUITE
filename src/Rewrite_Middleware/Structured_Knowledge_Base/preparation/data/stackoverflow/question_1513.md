# Web services are scalable, right?
[Link to question](https://stackoverflow.com/questions/8111932/web-services-are-scalable-right)
**Creation Date:** 1321191625
**Score:** 0
**Tags:** database, performance, web-services
## Question Body
<p>I have a relatively simple question that I think, having scoured the net, I already know some answers, but need more advice.  I am a newbie on the mechanics of database management behind the scenes.  </p>

<p>I want to use REST web services to communicate with mobile users (cell phone users, mainly Android and iPhone).  The web services are written in C# and query a Microsoft SQL Server 2008 database with simple and fast queries like <code>SELECT EmployeeID, FirstName, LastName, HireDate, City FROM Employees WHERE City = 'London'</code>--all these fields being indexed for maximum speed.  The web services are "Per Call" meaning they are stateless and in theory very scalable.</p>

<p>My question though is the web services will be hosted by a third party, like GoDaddy.  I've used this third party in the past and had no problem with them serving up some simple web services, with one or two hits per minute, but if I start getting 100000 people per minute accessing them, what will happen?  I asked them, and I don't think they really understood the question (or maybe they did--but I'm not sure) and they simply said: 'if you exceed your bandwidth, simply buy more at our rate of $xx/MB per month, etc.'  But I wish to ask somebody here:  is my solution scalable?  I ask this because somebody said to buy a server--but for starters I don't want to do that unless I'm sure this third party cannot handle my needs.</p>

<p>So, to be concrete:  REST web services, written in C# passing XML, hosted by Microsoft SQL Server 2008, on a Per Call, databases and web service methods cached, and hosted by a third party (where you pay them for XYZ bandwidth per month), and involving simple, specific, fast SQL queries--is this setup scalable?  Can it handle 2000 hits per second?  20000? (assuming of course you pay the third party hosting these web services and database for more bandwidth)  Somewhere I read Microsoft SQL server can handle 2000 connections per second, but I'm not sure if that's true or even applicable?  I understand web services are not limited to hitting up a single database--or am I wrong?  If web services are limited by one database, I can rewrite my code so two or more databases are used (i.e., have a connection string so if "London" is the SQL query city, then use database #1, if "Paris" is the city, use database #2, etc).  Is this true?</p>

<p>Sorry if this question is too simple for you database pros, but you have to start somewhere.  Thank you in advance.</p>

## Answers
### Answer ID: 8111960
<p>In your description you have nothing that starts the big "not scalable" alarm, but you can not know how scalable your solution is until you have actually tried.</p>

### Answer ID: 8111956
<p>the simplest answer is that there is no simple answer.</p>

<p>when you say "20000" hits per second, are you talking about the average, or at peak? 20000 is a /huge/ amount, and would be better served by a bank of machines than a single machine.</p>

<p>database queries are slow. try cutting down on their usage as much as possible.</p>

<p>start thinking about proxy servers such as nginx or varnish</p>

<p>remove reliance on session-based code, and provide static content where possible</p>

<p>cache, cache, cache.</p>

<p>but I guess the best advice would be: start small, and grow slowly.</p>

