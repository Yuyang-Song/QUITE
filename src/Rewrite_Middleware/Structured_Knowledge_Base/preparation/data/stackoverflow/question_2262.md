# How to find the data source (dataTable) in Java with Primefaces?
[Link to question](https://stackoverflow.com/questions/26530242/how-to-find-the-data-source-datatable-in-java-with-primefaces)
**Creation Date:** 1414073886
**Score:** 0
**Tags:** java, jsf, jsf-2, primefaces, datatable
## Question Body
<p>PHP programmer here. Absolute beginner in Java and Primefaces.</p>

<p>Simple question. How I find the source SQL of this dataTable? I need to rewrite the SELECT (or similar method of querying the database) of this dataTable.</p>

<pre><code>...
&lt;p:dataTable id="pendentList" var="ava" value="#{avaBean.avaTut}" rowKey="#{ava.id_ava}" emptyMessage="Empty records"&gt;
    &lt;p:column headerText="Ativ" sortBy="#{ava.pos}" width="400"&gt;
...
</code></pre>

<p>The application uses Primefaces running on Glassfish3.</p>

<p>Thanks.</p>

## Answers
### Answer ID: 26530440
<p>You have to trace the code and examine how avaTut object on avaBean class is being filled. Find avaBean and see where avaTut instances are initialized, as you go deeper you will eventually find where the data is being gathered</p>

