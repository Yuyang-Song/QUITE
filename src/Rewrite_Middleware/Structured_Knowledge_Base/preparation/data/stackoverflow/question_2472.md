# Grails multiple databases for a single deployed application
[Link to question](https://stackoverflow.com/questions/36221234/grails-multiple-databases-for-a-single-deployed-application)
**Creation Date:** 1458913789
**Score:** 0
**Tags:** spring, hibernate, grails, database-design, multiple-databases
## Question Body
<p>We have a current application written in grails 3, which we want to deploy for multiple different clients. The application and the database schema is the same for every client, only the data changes. </p>

<p>We don't want to have a single database because then we will need to rewrite sql queries, code will be harder to manage, indexes will get bigger etc. </p>

<p>We come up with 2 results:</p>

<ol>
<li><p>Defining multiple datasources. Each time a new client is registered, a new database should be created, and added (by a script probably) to application.yml. The client will login, and then ideally the datasource will be set at a single point of the code. (Which we haven't found yet a way to do it, on documentation it appears that it can be statically defined at each service). <strong>That way we will have one compiled application for all clients, with one database per client.</strong></p></li>
<li><p>Setting a different environment for each client. That means we will have <strong>one compiled application for each client</strong> and then use a folder based structure for deployment. (So that clients will use for example myapplication.com/clientid where the compiled application will be). Again a new environment and database should be created each time a new client registers.</p></li>
</ol>

<p>The application is a b2b service so we are talking about tens or hundreds of clients.</p>

<p><strong>EDIT</strong></p>

<p>Which one of the 2 approaches would be better and why ? We would prefer to have one compiled application as it is easier to manage the deployment, <strong>but it doesn't seem to be feasible with grails to define dynamically a datasource based on the user logged in</strong> (Feel free to coreect me on that if i'm wrong). Thus it's important to have a structure of myapplication.com/clientid, which probably is easier to manage with different environments. </p>

