# Combine Class with Database first model
[Link to question](https://stackoverflow.com/questions/26124189/combine-class-with-database-first-model)
**Creation Date:** 1412089687
**Score:** 0
**Tags:** c#, sql, asp.net-mvc-4
## Question Body
<p>I've got an older ASP project that is being re-written into a responsive MVC4 w/bootstrap web application. The original version used direct SQL queries to interact with the application backend SQL database, and a custom class called EmployeeUserInfo that directly queries the ERP system for current employee information(current tasks, hours worked, etc). That connection is strictly read-only.</p>

<p>Using Entity Framework, it was extremely easy to create the models for the various writable databases that make up the application, but how can I add the original EmployeeUserInfo class to this EDMX model? I'd prefer not to rewrite the class because it does a lot of querying and analyzing to build the EmployeeUserInfo object. Is it possible to combine another class with an EF database-first generated model?</p>

<p>I'm stuck now because I can use the EmployeeUserInfo as the model for a view, but then I cannot access the EF generated model to read/write to the application database. I feel like I'm overlooking something here and making this more difficult than it needs to be.</p>

