# Peristence Web Service for Rich Client Java (Swing) applications
[Link to question](https://stackoverflow.com/questions/4488732/peristence-web-service-for-rich-client-java-swing-applications)
**Creation Date:** 1292840763
**Score:** 4
**Tags:** java, web-services, http, jpa, persistence
## Question Body
<p>I am rewriting my client-server rich client database application (Swing) to a three-tiered application with a Netbeans RCP rich-client.</p>

<p><strong>By default</strong> Hibernate and other <strong>JPA</strong> providers can be used only in a <strong>very cumbersome</strong> way from rich clients (native database connection not cutting through firewalls, loosing lazy-loading, conceptual problems with managing Session/EntityManager lifecycles...etc other problems). So one needs some kind of extension for using them comfortably in rich clients.</p>

<p>Normally, rich clients call <strong>webservices</strong> in the business logic tier (on the server). Usually, <strong>dedicated</strong> web-service methods handle the <strong>CRUD</strong> operations of every object type.
Now, <strong>I wouldn't</strong> like to write a custom web-service for the CRUD operations of <strong>each and every persistent class</strong> of my application so I thought there may be a <strong>generic</strong> persistence web-service for these kind of operations which can handle at least all of the <strong>CRUD operations</strong> of the application.</p>

<p>Is there such a persistence service???</p>

<p>Here are the <strong>details</strong> of my ideas/requirements:</p>

<p>The service should work with <strong>JPA-annotated POJOs</strong> so it should use some kind JPA persistence provider on the server. Currently, I am using Hibernate so if it actively supports Hibernate, it is a plus. Of course the POJO classes must be included in the server side JPA configuration, I don't expect to handle ANY KIND of unknown POJOs.</p>

<p>I wouldn't like to create separate <strong>Value Objects</strong> or Data Transfer Objects for sending data between the client and server parts of the service. I would like to use <strong>only JPA annotated POJOs</strong> even for <strong>transfer</strong>. I believe this is standard practice nowadays.</p>

<p>The client should receive data and send data with <strong>HTTP requests</strong> to the server-side of the service, in order to lessen firewall communication problems. HTTP <strong>proxy</strong> usage should be configurable.</p>

<p>The client side of the persistence service can get POJO list results for its executed <strong>JPA QL queries</strong> (sent as a simple <strong>query string,</strong> optionally ** named parameters** also sent in the request). These queries are sent from the client in the form of a <strong>webservice</strong> call or simple HTTP request to a <strong>servlet.</strong> It would be nice if several JPA queries could be sent in one request. The client receives the result of the requests as lists of POJOs which may have <strong>lazy-loaded</strong> collections and object references (these are not sent from the server in query-time).</p>

<p>The <strong>client side</strong> of the persistence service should be able to fulfill <strong>lazy-loading</strong> requests <strong>automatically/transparently</strong>, when the client application accesses a lazy-loaded attribute in a POJO (at a later point in time, not at the initial query). So, transparent lazy loading <strong>should remain working</strong> after the POJO has been transferred to the <strong>client</strong>.</p>

<p>New, updated/dirty or to-be-deleted POJOs can be <strong>sent by the client</strong> side of the persistence service to the server where the changes <strong>get persisted</strong> and success/failure statuses are sent back (e.g. the ID which was given to the newly persisted POJOs). Several to-be-saved POJOs could be sent in one request.</p>

<p>It should have a mechanism for marking <strong>transaction boundaries,</strong> so more than one independent HTTP service calls could be executed in one database transaction (keeping something like Session/EntityManager.<strong>beginTransaction()</strong>, commit() and rollback()).</p>

<p>Would be nice if <strong>validation</strong> and <strong>access control</strong> checks could be plugged into the server component.</p>

<p>Is there such a persistence service project???
Possibly as an extension shipped with a JPA persistence provider?</p>

## Answers
### Answer ID: 4709548
<p>When I designed a similar app back in 2002, we searched far and wide for a framework to use, but finally had to run our own.
Transporting sub-graphs of persistent objects to the swing client was done by translating those to DTO (DataTransferObjects) objects, which maintained an attribute mapping and information if an attribute was being dirtied by the client. On the way back to the server, only the dirtied attributes were updated in a trx.</p>

<p>You might want to use JDO 2.0 as a persistence layer. It supports detaching objects or sub-trees from a persistent object graph, sending those detached objects over the wire and re-attaching those in a later transaction.</p>

<p>However, you lose the ability to minimize the data you send across the wire.</p>

<p>Best bet so far: Run your own mechanism and add a createDTO and updateFromDTO method to your persistent objects, but I'd be very happy to be proven wrong.</p>

### Answer ID: 4704614
<p>I will use Spring with JPA. Spring provides reasonable defaults to most persistence management issue you mentioned.(Transaction management, lazy loading)</p>

### Answer ID: 4509633
<p>Transactions, server request handling, validation, and access control are all things that, like you said, are way beyond the realm of the persistence layer.  You will not find a persistence service that implements these things.</p>

<p>That being said, there are many web frameworks that quickly provide you with a basic implementation of the CRUD operations.  In particular the term you're looking for is <a href="http://en.wikipedia.org/wiki/Scaffold_%28programming%29" rel="nofollow">scaffolding</a>.</p>

<p><a href="http://www.grails.org/" rel="nofollow">Grails</a> is a popular web framework for Java that provides <a href="http://www.grails.org/Scaffolding" rel="nofollow">scaffolding</a>.  I'm sure there are many others.  I would suggest taking a look at Grails.</p>

