# Spring Batch with unknown datasource
[Link to question](https://stackoverflow.com/questions/66125497/spring-batch-with-unknown-datasource)
**Creation Date:** 1612897690
**Score:** 0
**Tags:** spring-boot, spring-data-jpa, spring-batch
## Question Body
<p>I have a working Spring Boot application which embeds a Spring Batch Job. The job is not run on a schedule, instead we kick it with an endpoint. It is working as it should. The basics of the batch are</p>
<ul>
<li>Kick the endpoint to start the job</li>
<li>Reader reads from input file</li>
<li>Processor reads from oracle database using jpa repository and simple spring datasource config</li>
<li>Writer writes to output file</li>
</ul>
<p>However there are new requirements:
The schema of the repository database is from here on unknown on application startup. The tables are the same, it is just an unknown schema. This fact is out of our control and you might think it is stupid but there are reasons for it and this cant be changed. This means that with current functionality we need to reconfigure the datasource when we know the new schema name, and restart the application. This is a job that we will run for a number of times when migrating from one system to another, so it has a limited lifecycle and we just need a &quot;quick fix&quot; to be able to use it without rewriting the whole app. So what I would like to do is:
Send the schema name as a query param to the application, put it in job parameters and then - get a new datasource when the processor reads from the repository. Would this be doable at all using Spring Batch? Any help appreciated!</p>

