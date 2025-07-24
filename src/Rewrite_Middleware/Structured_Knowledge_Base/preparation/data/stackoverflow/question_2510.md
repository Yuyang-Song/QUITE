# How should one use Where-Queries and DetachedCriteria in Grails?
[Link to question](https://stackoverflow.com/questions/37819795/how-should-one-use-where-queries-and-detachedcriteria-in-grails)
**Creation Date:** 1465929788
**Score:** 4
**Tags:** hibernate, grails, grails-orm, hibernate-criteria, detachedcriteria
## Question Body
<p><strong>EDIT1:</strong> I also accept answers that guide me in reusing <code>DetachedCriteria</code> without where queries. Where queries are my preference, but if regular DetachedCriteria is less hassle and more mature, I  am willing to use it instead.</p>
<p>I've been trying to wrap my head around 'where' queries in Grails for some time now. At first, I was amazed by how powerful they are:  I can build queries without leaving my business logic layer. I thought they were a solution for some performance issues I was facing with complex actions that require a lot of transactional logic.</p>
<p>However, I feel like the documentation omits all the problems with where queries. I have no idea how to use them in my application, although I have been reading about them and playing around with them a lot. Here is how I want to use them:</p>
<p>In my application, there are a lot of subqueries that are redundant when using HQL or native SQL, but I cannot reuse them, because I don't want them all be executed after another. I want them to be <strong>executed in one database query.</strong></p>
<p>As far as I'm concerned, <code>DetachedCriteria</code> or where-queries are the way to go for me. I decided to use where queries, since I like the approach and syntax much better than regular criteria.</p>
<p>Here is the issue: <strong>In many variations, my where queries are ignored</strong>! Depending on the situation, I have to memorize a certain order or structure.</p>
<h2>Reuse DetachedCriteria Objects</h2>
<p>I think the most logical thing a developer would try to do is encapsulate often used where queries and access them when desired. So, I put some where queries in service methods as so:</p>
<pre><code>DetachedCriteria&lt;Customer&gt; allCustomersForProjektCriteria(DetachedCriteria&lt;Customer&gt; criteria, Project project){
    criteria.where{projekt == project}
}
</code></pre>
<p>I like that where queries return objects of <code>DetachedCriteria.</code> Theoretically. Maybe it is just syntactic sugar, I don't know. I tried to do something like that and the behaviour feels weird, to say the least.</p>
<pre><code>someService.allCustomersForProjectCriteria(Customer.where{name != null}, Project.get(1))
        .where{representatives {type != 'Manager'}}
        .list()
</code></pre>
<p>The first where query as well as the one in my service method work fine, but the last one does not. That is how I found out that you are only allowed to chain where queries <strong>within the same method or closure</strong>. But is that the expected behaviour? A similar approach can also be found in the <a href="http://docs.grails.org/latest/guide/GORM.html#whereQueries" rel="nofollow noreferrer">grails documentation</a> under &quot;Query Composition&quot;.</p>
<p>What is the use case where I put all my where queries in one method? And how can it be that <code>DetachedCriteria</code> offers the method <code>DetachedCriteria where(Closure)</code> if it is being ignored in some cases silently? Why is no exception thrown?</p>
<h2>Reuse Where Query Closures</h2>
<p>My next approach is also mentioned in the same part of the grails documentation as mentioned above. Rather than chaining together where queries that are encapsulated in different methods, I tried to encapsulate just the closures to reuse it at will. I tried the following:</p>
<pre><code>Closure allCustomersForProjectCriteria(Project proj){
    ({project == proj} as DetachedCriteria&lt;Customer&gt;)
}
</code></pre>
<p>Then use it like that:</p>
<pre><code>Customer.where(allCustomersForProjectCriteria(Projekt.get(1))
        .where{name != null &amp;&amp; representatives {type != 'Manager'}}
        .list()
</code></pre>
<p>Now that fails with the following Stacktrace:</p>
<pre><code>org.codehaus.groovy.runtime.typehandling.GroovyCastException: Error casting closure to grails.gorm.DetachedCriteria, Reason: null

    at org.springsource.loaded.ri.ReflectiveInterceptor.jlrMethodInvoke(ReflectiveInterceptor.java:1276)

    at ConsoleScript148$_run_closure2.doCall(ConsoleScript148:9)

    at org.springsource.loaded.ri.ReflectiveInterceptor.jlrMethodInvoke(ReflectiveInterceptor.java:1276)

    at ConsoleScript148.run(ConsoleScript148:12)

    at org.springsource.loaded.ri.ReflectiveInterceptor.jlrMethodInvoke(ReflectiveInterceptor.java:1276)
</code></pre>
<p>I played around a little and found out that I cannot declare the closure, cast it and return it in one line of code. I had to rewrite my method as follows:</p>
<pre><code>Closure allCustomersForProjectCriteria(Project proj){
    def criteria = {project == proj} as DetachedCriteria&lt;Customer&gt;
    criteria
}
</code></pre>
<p>This is a minor annoyance, but I could easily live with it. I thought I got it all figured out now, because no exception was raised. But, again, only the where query from my method was executed, the other one was ignored. That was the point where my confusion reached its peak. What is happening? That does not feel consistent. When can I trust my criteria to be considered if it is ignored sometimes without an exception?</p>
<p>Weirdly enough, if I put my second where query in a closure, it works again!!</p>
<pre><code>    def additionalCriteria = {name != null &amp;&amp; representatives {type != 'Manager'}} as DetachedCriteria&lt;Customer&gt;
    Customer.where(allCustomersForProjectCriteria(Projekt.get(1))
        .where(additionalCriteria)
        .list()
</code></pre>
<h2>Now to get to the point...</h2>
<p>So this is how I try to make sense of it: I can chain multiple where queries with a newly defined closure after each other <strong>if, and only if, they are located in the same method or closure</strong>.</p>
<pre><code>def results = Customer.where{...}
        .where{...}
        .list()
</code></pre>
<p>If they are in different methods, all but the first where query are ignored:</p>
<pre><code>def getQuery(){
    Customer.where{...}
}
query.where{ ... } //This one is ignored
</code></pre>
<p>The first one was returned from a method or closure, so it is not a 'normal' where query anymore, it is a 'returned where query'. Closure definition at method call does not work now, and I have to use it like that:</p>
<pre><code>def getQuery(){Customer.where{...}}
def myWhereClosure = { ... }
query.where(myWhereClosure) //This one is NOT ignored anymore!
</code></pre>
<p>If I encapsulate the closures for my queries, it is the same; as soon as I execute one where query with an encapsulated where closure as a parameter, it is now a 'returned where query' and cannot be used regularly anymore:</p>
<pre><code>def getCustomerCrit(){
    def clos = {...} as DetachedCriteria&lt;Customer&gt;
    clos 
}
def results = Customer.where(customerCrit)
        .where{...} //This one is ignored
        .list()  
</code></pre>
<p>So, to make it work I use a predefined closure for the second where query, so that it is also a 'returned where query' and is not ignored:</p>
<pre><code>...

def additionalCrit = {...}
def results = Customer.where(customerCrit)
        .where(additionalCrit) //This one is NOT ignored anymore
        .list()  
</code></pre>
<p>So what is the intended way to use these queries, how do they work under the hood and where can I find more resources on that topic than in the documentation?</p>

