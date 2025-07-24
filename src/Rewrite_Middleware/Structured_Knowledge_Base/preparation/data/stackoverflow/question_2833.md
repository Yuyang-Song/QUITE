# Can gradual migration be possible for a Vaadin JavaEE to Vaadin Spring?
[Link to question](https://stackoverflow.com/questions/54726439/can-gradual-migration-be-possible-for-a-vaadin-javaee-to-vaadin-spring)
**Creation Date:** 1550342672
**Score:** 1
**Tags:** java, spring, hibernate, vaadin, vaadin8
## Question Body
<p>We have an existing Vaadin 8 JavaEE webapp that was adapted and heavily modified from the Tickets Dashboard demo. We are in the process of planning a schedule to migrate the app to using Spring (non-boot) and adopt the MVC model for the next version. However, after reading through the Vaadin Spring documentation and going comparing source codes between the current app, the sample bakery app (spring, with Framework 8), and an older project using Hibernate 4 and Spring 4, we still had a few key questions that required to help improve our approach to migration:</p>

<ol>
<li><p>Is gradual migration possible where some of the functions are migrated to Spring first followed by others in subsequent minor releases? If yes, which classes should I start modifying / adapt (apart from those below) to Spring first before moving into the smaller releases?</p></li>
<li><p>We've established that 75% of our application is using complex native select queries, with 25% on CRUD operations. We are still sticking to Hibernate as most of the dev team are familiar with it. Is it better to stick to using the DAO generics approach (encapsulating the implementation e.g <a href="https://www.baeldung.com/simplifying-the-data-access-layer-with-spring-and-java-generics" rel="nofollow noreferrer">https://www.baeldung.com/simplifying-the-data-access-layer-with-spring-and-java-generics</a>) or just using the JPARepository interfaces as seen in the baker app?   </p></li>
<li><p>We're deploying the application into Azure cloud with TomEE Plume (an 8.5 equivalent of Tomcat) as a starting deployment. Are there any special settings that should be included to accommodate that deployment?</p></li>
</ol>

<p>We have asked this question on gradual migration previously in the Vaadin forum but without any replies: <a href="https://vaadin.com/forum/thread/17468362/17468363" rel="nofollow noreferrer">https://vaadin.com/forum/thread/17468362/17468363</a></p>

<p>Our immediate goals after the planned migration exercise would be:</p>

<ol>
<li><p>Making it modular and easier to incorporate subsequent features such as dynamic data routing, circuit breaker /rerouting, email notification, internationalization, keeping the number of manageable instances to a 5-10 in a production level, etc..</p></li>
<li><p>Keeping the avenue for upgrading open without having to rewrite everything from scratch e.g (Java 8 to Java 11, Framework 8 to Vaadin 12) within the next few years. </p></li>
</ol>

<p>As said above, this is for running at Azure Cloud with MSSQL database and TomEE Plume container.</p>

<p>We've done some preliminary code modifications including: </p>

<ol>
<li><p>Modifying the main pom.xml and include a better maven profiling (using <a href="https://www.mkyong.com/maven/maven-profiles-example/" rel="nofollow noreferrer">https://www.mkyong.com/maven/maven-profiles-example/</a> as reference)</p></li>
<li><p>Moved the hibernate and spring settings to application.properties files </p></li>
<li><p>Added the application-context.xml and divide it again to application-context-dao.xml and application-context-service.xml to make it manageable.</p></li>
</ol>

<p>Web.xml </p>

<pre><code>&lt;context-param&gt;
    &lt;param-name&gt;contextConfigLocation&lt;/param-name&gt;
    &lt;param-value&gt;classpath*:applicationContext.xml&lt;/param-value&gt;
&lt;/context-param&gt;

&lt;listener&gt;
    &lt;listener-class&gt;org.springframework.web.context.ContextLoaderListener&lt;/listener-class&gt;
&lt;/listener&gt;
&lt;listener&gt;
    &lt;listener-class&gt;org.springframework.web.context.request.RequestContextListener&lt;/listener-class&gt;
&lt;/listener&gt;

&lt;servlet&gt;
    &lt;servlet-name&gt;SycardaDashboard2&lt;/servlet-name&gt;
    &lt;servlet-class&gt;com.example.dashboard.DashboardServlet&lt;/servlet-class&gt;
    &lt;init-param&gt;
        &lt;param-name&gt;UI&lt;/param-name&gt;
        &lt;param-value&gt;com.example.dashboard.DashboardUI&lt;/param-value&gt;
    &lt;/init-param&gt;
&lt;/servlet&gt;
&lt;servlet-mapping&gt;
    &lt;servlet-name&gt;SycardaDashboard2&lt;/servlet-name&gt;
    &lt;url-pattern&gt;/*&lt;/url-pattern&gt;
&lt;/servlet-mapping&gt;
</code></pre>

<p>application-context.xml</p>

<pre><code>&lt;beans&gt;
    &lt;bean class="org.springframework.beans.factory.config.PropertyPlaceholderConfigurer"&gt;
        &lt;property name="locations"&gt;
            &lt;list&gt;
                &lt;value&gt;classpath*:application-development.properties&lt;/value&gt;
                &lt;value&gt;classpath*:application-production.properties&lt;/value&gt;
            &lt;/list&gt;
        &lt;/property&gt;

    &lt;/bean&gt;
&lt;import resource="classpath*:applicationContext-dao.xml" /&gt;
&lt;import resource="classpath*:applicationContext-service.xml" /&gt;

&lt;context:component-scan base-package="com.example.dashboard"&gt;
    &lt;context:exclude-filter type="annotation" expression="org.springframework.stereotype.Controller"/&gt;
&lt;/context:component-scan&gt;
&lt;/beans&gt;
</code></pre>

<p>application-dao-context.xml</p>

<pre><code>&lt;!-- Activates scanning of @Autowired --&gt;
&lt;context:annotation-config/&gt;

&lt;!-- Activates scanning of @Repository --&gt;
&lt;context:component-scan base-package="com.igi.sycarda.dashboard.dao"/&gt;

&lt;bean class="org.springframework.orm.hibernate4.HibernateExceptionTranslator"/&gt;
&lt;bean class="org.springframework.dao.annotation.PersistenceExceptionTranslationPostProcessor"/&gt;

&lt;bean id="sessionFactory" class="org.springframework.orm.hibernate5.LocalSessionFactoryBean" destroy-method="destroy"&gt;
    &lt;property name="dataSource" ref="dataSource" /&gt;
    &lt;property name="packagesToScan"&gt;
        &lt;list&gt;
            &lt;value&gt;com.example.dashboard.entities&lt;/value&gt;
        &lt;/list&gt;
    &lt;/property&gt;
    &lt;property name="hibernateProperties"&gt;
        &lt;props&gt;
            &lt;prop key="hibernate.dialect"&gt;${hibernate.dialect}&lt;/prop&gt;
            &lt;prop key="hibernate.query.substitutions"&gt;true 'Y', false 'N'&lt;/prop&gt;
            &lt;prop key="hibernate.cache.use_second_level_cache"&gt;true&lt;/prop&gt;
            &lt;prop key="hibernate.cache.use_query_cache"&gt;true&lt;/prop&gt;
            &lt;prop key="hibernate.cache.region.factory_class"&gt;org.hibernate.cache.ehcache.EhCacheRegionFactory&lt;/prop&gt;
            &lt;prop key="current_session_context_class"&gt;thread&lt;/prop&gt;

            &lt;prop key="show_sql"&gt;${hibernate.show.sql}&lt;/prop&gt;
            &lt;prop key="format_sql"&gt;${hibernate.format.sql}&lt;/prop&gt;
            &lt;prop key="use_sql_comments"&gt;${hibernate.use.sql.comments}&lt;/prop&gt;
        &lt;/props&gt;
    &lt;/property&gt;
&lt;/bean&gt;

&lt;!-- Transaction manager for a single Hibernate SessionFactory (alternative to JTA) --&gt;
&lt;bean id="transactionManager" class="org.springframework.orm.hibernate5.HibernateTransactionManager"&gt;
    &lt;property name="sessionFactory" ref="sessionFactory"/&gt;
&lt;/bean&gt;
</code></pre>

<p>For a start, after first week of migration, we expect the app to still be 90% JavaEE, and one or two functions will be in Spring. After each week of updates, the number of existing features will shift into using Spring until it is fully incorporated.</p>

## Answers
### Answer ID: 54731863
<p>Such migration is possible. You have multiple questions in the question I will answer only two of them.</p>

<ol>
<li><strong>Is gradual migration possible ?</strong>  Yes it is possible, and you can either center it first on the bottom layers - your DAOs and Repositories in the case of complex monolith. Or you can try to slice your application into small logical units and try to migrate those unit. Example of such slicing would be if we have e-commerce site a service calculating the price of an Item. It is a clearly defined service that can be easily isolated. Doing such approach would also give you better overview over how you would like to modularize your application. Sometimes though such approach may be too difficult with big monoliths where the code is just to sphagetti.</li>
<li><strong>Spring Data usage and migration of existing Daos</strong>. It is not a must that you use spring-data. Having DAOS or manually written Repositories is perfectly fine. No need to put extra effort, or doing extra work with such migration in my opinion.</li>
</ol>

<p>IMO your main target during the migration should be doing sensible modularisation and spitting the monolith into logical units. I am not talking about separate deployables and microservices, it is not necessary to go so far. But splitting it logically may provide you with migration map.</p>

