# How to best stage large amounts of data with Hibernate/JPA?
[Link to question](https://stackoverflow.com/questions/66090967/how-to-best-stage-large-amounts-of-data-with-hibernate-jpa)
**Creation Date:** 1612719066
**Score:** 1
**Tags:** excel, postgresql, hibernate, spring-data-jpa, staging-table
## Question Body
<p>How can I best stage large amounts of data for migration into our database using Hibernate efficiently? Performance when dealing with &gt;25K records that are 100+ columns are not ideal.</p>
<p>Let me explain:</p>
<p><strong>Background</strong></p>
<p>I'm working for a large company that operates around the world. I've been tasked with leading a team (at least for backend) to create a full stack application that allows for various levels of management to perform their tasks. The current tech stack for backend is Java, Spring Boot, Hibernate, and PostgreSQL. Management would like to upload Excel files to our application and have our application parse them so we can refresh the data in our database.</p>
<p>Unfortunately, these files range from 25K to 50K records. We're aware that these Excel files are generated using SQL queries from Excel. However, we are not permitted to access the database with this data directly. The security is very tight and will not permit us access to any APIs, DB calls, etc. to work around Excel. Due to memory constraints and scalability concerns, we're using SAX parsing to keep a low footprint. Once we parse the Excel files, we're mapping them to a Hibernate entity that represents a staging table. Then we're migrating data from it to our other tables.</p>
<p>Currently to stage 25K records and migrate all the data to our other tables takes 15 minutes, which is unacceptable in the eyes of management. Especially, since this will need to be done on a daily basis.</p>
<p><strong>Things I've tried</strong></p>
<ul>
<li>Enabling batch processing in Hibernate by following Vlad's answer <a href="https://stackoverflow.com/questions/12011343/how-do-you-enable-batch-inserts-in-hibernate">here</a>. This knocked maybe 20 seconds off the overall time for staging.</li>
<li>Rewriting criteria and other queries for fetching data.</li>
<li>Reducing amount of data to process (most fields are required so the amount can't be too heavily reduced).</li>
<li>Indexing important columns in both the staging and destination tables. I'm doing the indexing as part of schema generation.</li>
<li>Optimize parts of code that clean parsed data of imperfections.</li>
</ul>
<p><strong>I cannot post code due to NDA</strong></p>
<p><strong>Summary of Constraints</strong></p>
<ul>
<li>This app needs strong support for generating reports on related data (one of the reasons we went with RDBMS. Also, the data fits well into a relational model).</li>
<li>Must maintain a complete audit history of all records (currently using Hibernate Envers).</li>
<li>We have to approve any new dependency/library through the company's cybersecurity team. This can result in days of lost production while we wait for approval. It's not ideal to request new dependencies for the project.</li>
<li>There are no ways of working around the Excel files at this time. An API call or simple database query would be nice, but that's not an option to us for security reasons.</li>
<li>Scalability is a growing concern. Another team under this project has to parse an Excel file of 50K rows with 100 rows. All of this is only data for the USA. The project owner has said the company eventually wants to expand this app's management capabilities abroad.</li>
</ul>
<p><strong>My Thoughts</strong></p>
<p>Purely regarding the staging issue, I think it's best to get rid of the Hibernate entities responsible for staging. I'll rewrite the migration of staged data into our live tables in SQL using stored procedures. Despite it being vendor-specific (to my knowledge, anyway) I'll use Postgres' COPY command to do the heavy lifting with the large amounts of rows. I can rewrite the parser to direct data to a CSV or other delimited file instead. The only issue I have then is how to migrate the data to tables that use Hibernate sequences and generators. I haven't figured out how to synchronize Hibernate's sequences after a manual update to the database like that. It likes the throw errors about duplicate primary keys until it comes across an ID in the sequence that's not used. But I feel that's another question entirely.</p>
<p><strong>Edit 1:</strong></p>
<p>I should clarify. The 15 minutes is the total time for all of staging. This includes staging and migration. Just the staging of the 25K records takes around 1:30, which also isn't ideal. I've run session metrics a few times and get around the following numbers for Spring Data persisting the 25K records:</p>
<pre><code>2451000 nanoseconds spent acquiring 1 JDBC connection;
0 nanoseconds spent releasing 0 JDBC connections;
96970800 nanoseconds spent preparing 24851 JDBC statements;
9534006000 nanoseconds spent executing 24849 JDBC statements;
21666942900 nanoseconds spent executing 830 JDBC statements;
23513568700 nanoseconds spent executing 2 flushes (flushing a total of 49696 entities and 0 collections)
211588700 nanoseconds spent executing 1 partial-flushes (flushing a total of 24848 entities and 24848 collections)
</code></pre>
<p>For this specific case, I'm staging the roughly 25K entities and then using a stored procedure to move only employee data from staging to live tables (a small fraction of what makes up the 15 total minutes). That procedure seems to run instantly. But there's other data that we have to determine via joins, group by statements, etc., which appear to be costly. I'm just not sure why it's taking Spring Data so long to persist that many records when it would take pure SQL significantly less.</p>

