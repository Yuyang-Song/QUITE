# Invalid object name in a query with CASE
[Link to question](https://stackoverflow.com/questions/4712862/invalid-object-name-in-a-query-with-case)
**Creation Date:** 1295265430
**Score:** 0
**Tags:** sql, sql-server, t-sql
## Question Body
<p>I have the following problem:</p>

<p>I have 3 tables:
<img src="https://i.sstatic.net/LWieG.jpg" alt="alt text"><br>
If you want to create a document, there are two options:  </p>

<ol>
<li>You can create a Document from scratch.

<ul>
<li>The program will create a record in the Config table with default configuration. </li>
<li>In this case 1 Config record belongs to exactly 1 Document record</li>
</ul></li>
<li>You can create a Document from a DocumentTemplate

<ul>
<li>DocumentTemplate allows you to pre-define Document configurations where you can base Documents on.</li>
<li>The program will link the new record in the Document table to the same configuration record as the DocumentTemplate configuration record.</li>
<li>1 Config record belongs to exactly 1 DocumentTemplate record and belongs to 0..* Document records</li>
</ul></li>
</ol>

<p>If you have never created a template, the table 'DocumentTemplate' will not exist in the database.</p>

<p>Now I want to select the following columns:  </p>

<ol>
<li>Config.config_data</li>
<li>Document.document_name <strong>OR</strong> DocumentTemplate.template_name

<ul>
<li><strong>If</strong> config is created by a template I want DocumentTemplate.template_name</li>
<li><strong>Else</strong> I want Document.document_name</li>
</ul></li>
</ol>

<p>I have written the following query:</p>

<pre><code>SELECT 
-- //Name must be name of Document or name of DocumentTemplate 
CASE 
    WHEN [c].[config_from_template] = 0 
    THEN -- //Get Document name
        (SELECT [d].[document_name]
        FROM [Document] [d]
        WHERE [d].[document_config_id] = [c].[config_id])
    WHEN [c].[config_from_template] = 1 
    AND OBJECT_ID ('[DocumentTemplate]','U') IS NOT NULL
    THEN -- //Get template name
        (SELECT [t].[template_name]
        FROM [DocumentTemplate] [t]
        WHERE [t].[template_config_id] = [c].[config_id])
END as 'Name',
configNode.value('@Key', 'nvarchar(128)') as 'ConfigKey', -- //Key from xml @Key    
configNode.value('@Value', 'nvarchar(128)') as 'ConfigValue' -- //Value from xml @Value 
FROM [Config] [c]
-- //Create one record for each config option
CROSS APPLY [Config].[config_data].nodes('//ConfigOptions') as ConfigNodes(configNode) 
</code></pre>

<p>This query will throw a syntax error if DocumentTemplate does not exist.  </p>

<blockquote>
  <p>Msg 208, Level 16, State 1, Line 1<br>
  Invalid object name 'DocumentTemplate'.</p>
</blockquote>

<p><strong>How can I rewrite this query to meet my requirements?</strong></p>

<p>thanks in advance</p>

## Answers
### Answer ID: 4712952
<p>I guess this is because the engine always checks the validity of your code, regardless whether it will be executed or not.</p>

<p>Maybe you can work around this check be executing the subquery like this:</p>

<pre><code>EXEC ('SELECT [t].[template_name]
   FROM [DocumentTemplate] [t]
   WHERE [t].[template_config_id] = ' + CAST([c].[config_id] AS VARCHAR(10)')
</code></pre>

<p>I did not check whether this works and may even have a typo in it. But it should serve as a point to start from...</p>

