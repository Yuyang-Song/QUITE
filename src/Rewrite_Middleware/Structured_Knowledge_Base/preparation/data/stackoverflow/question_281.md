# batching DataFieldMaxValueIncrementer
[Link to question](https://stackoverflow.com/questions/19140871/batching-datafieldmaxvalueincrementer)
**Creation Date:** 1380728207
**Score:** 0
**Tags:** jdbc, jdbctemplate, spring-jdbc
## Question Body
<p>I am using a DataFieldMaxValueIncrementer (specifically, OracleSequenceMaxValueIncrementer) to get the value of the next available primary key before I do an insert.  For performance reasons, I am rewriting the insert queries to be batched.  Is there a similar way to use the DataFieldMaxValueIncrementer to batch retrieve the next couple of primary keys rather than retrieving each individually?</p>

<p>I am using spring-jdbc 3.0.4 on an oracle 10g database.</p>

## Answers
### Answer ID: 19576014
<p>I wrote a custom solution based off of the query located here:
<a href="https://forums.oracle.com/thread/1115582" rel="nofollow">https://forums.oracle.com/thread/1115582</a></p>

