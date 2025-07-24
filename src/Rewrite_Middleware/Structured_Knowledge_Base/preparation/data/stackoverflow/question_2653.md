# Unresolvable circular reference in SpringBoot
[Link to question](https://stackoverflow.com/questions/44977592/unresolvable-circular-reference-in-springboot)
**Creation Date:** 1499452507
**Score:** 1
**Tags:** java, spring, hibernate, spring-mvc, spring-boot
## Question Body
<p>I am learning <strong>Spring Framework</strong> and now I am trying to make a simple <strong>Spring Boot application</strong> that would list all entries from a database (using <strong>Hibernate</strong>).</p>

<p>First I had a problem when SessionFactory would not be defined, but I managed to define it in Config Class. However, when I try to run the app now, I get the following error:</p>

<pre><code>Description:

The dependencies of some of the beans in the application context form a cycle:

   indexController (field private com.prvi.dao.CustomerDAO com.prvi.controllers.IndexController.customerDAO)
      ↓
   customerDAOImpl (field private org.hibernate.SessionFactory com.prvi.dao.CustomerDAOImpl.sessionFactory)
┌─────┐
|  sessionFactory defined in class path resource [com/prvi/ConfigPrvi.class]
└─────┘
</code></pre>

<p>Basically, I have <strong>IndexController</strong>, who gets <strong>GET /</strong> request, then it calls <strong>customerDAO</strong> to get list of customers and customerDAO uses <strong>sessionFactory</strong> to get Session and performs a query on DB. (I have omitted Service layer from the app for sake of simplicity)</p>

<p>Now, I have read that this error happens when a bean is dependent on a bean that is dependent on a first bean, making cyclical dependency. However, I do not understand where I made this cycle and how to fix it. Also, other answers on this topic have not provided me enough information to correct the error. They were mostly oversimplifies where cycle is clear, which is not the case here.</p>

<p>Here is what I have tried so far:</p>

<p><strong>PrviApplication.java - entry point for Spring Boot</strong></p>

<pre><code>@SpringBootApplication
public class PrviApplication {
    public static void main(String[] args) {
        SpringApplication.run(PrviApplication.class, args);
    }
}
</code></pre>

<p><strong>ConfigPrvi.java - My Configuration file</strong></p>

<pre><code>@Configuration
@EnableAutoConfiguration
public class ConfigPrvi {
    @Bean
    public HibernateJpaSessionFactoryBean sessionFactory(EntityManagerFactory emf){
        HibernateJpaSessionFactoryBean factory = new HibernateJpaSessionFactoryBean();
        factory.setEntityManagerFactory(emf);
        return factory;
    }
}
</code></pre>

<p><strong>IndexController.java - my Controller class, which handles GET /</strong></p>

<pre><code>@Controller
@RequestMapping("/")
public class IndexController {

    @Autowired
    private CustomerDAO customerDAO;

    @GetMapping("/")
    public String listCustomers(Model model){
        model.addAttribute("customers", customerDAO.getAllCustomers());
        return "index";
    }
}
</code></pre>

<p><strong>CustomerDAO.java - just an interface</strong></p>

<pre><code>public interface CustomerDAO {
    public List&lt;Customer&gt; getAllCustomers();
}
</code></pre>

<p><strong>CustomerDAOImpl.java - implementation, retrieves data from database</strong></p>

<pre><code>@Repository
public class CustomerDAOImpl implements CustomerDAO {

    @Autowired
    private SessionFactory sessionFactory;

    @Transactional
    public List&lt;Customer&gt; getAllCustomers(){
        Session session = sessionFactory.getCurrentSession();
        Query&lt;Customer&gt; query = session.createQuery("from Customer order by lastName", Customer.class);
        List&lt;Customer&gt; customers = query.getResultList();
        return customers;
    }
}
</code></pre>

<p>Is it perhaps that cycle was made here:</p>

<p>main --> controller --> dao --> sessionFactory --> config --> main</p>

<p>If so, how can I rewrite the code so that I get rid of it?</p>

<p><strong>EDIT: Added pom.xml:</strong></p>

<pre><code>&lt;?xml version="1.0" encoding="UTF-8"?&gt;
&lt;project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"&gt;
    &lt;modelVersion&gt;4.0.0&lt;/modelVersion&gt;

    &lt;groupId&gt;com.prvi&lt;/groupId&gt;
    &lt;artifactId&gt;prvi&lt;/artifactId&gt;
    &lt;version&gt;0.0.1&lt;/version&gt;
    &lt;packaging&gt;jar&lt;/packaging&gt;

    &lt;name&gt;prvi&lt;/name&gt;
    &lt;description&gt;Demo project for Spring Boot&lt;/description&gt;

    &lt;parent&gt;
        &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
        &lt;artifactId&gt;spring-boot-starter-parent&lt;/artifactId&gt;
        &lt;version&gt;1.5.4.RELEASE&lt;/version&gt;
        &lt;relativePath /&gt; &lt;!-- lookup parent from repository --&gt;
    &lt;/parent&gt;

    &lt;properties&gt;
        &lt;project.build.sourceEncoding&gt;UTF-8&lt;/project.build.sourceEncoding&gt;
        &lt;project.reporting.outputEncoding&gt;UTF-8&lt;/project.reporting.outputEncoding&gt;
        &lt;java.version&gt;1.8&lt;/java.version&gt;
    &lt;/properties&gt;

    &lt;dependencies&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-aop&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-thymeleaf&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-data-jpa&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;mysql&lt;/groupId&gt;
            &lt;artifactId&gt;mysql-connector-java&lt;/artifactId&gt;
            &lt;scope&gt;runtime&lt;/scope&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-test&lt;/artifactId&gt;
            &lt;scope&gt;test&lt;/scope&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.hibernate&lt;/groupId&gt;
            &lt;artifactId&gt;hibernate-core&lt;/artifactId&gt;
            &lt;version&gt;5.2.10.Final&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.hibernate&lt;/groupId&gt;
            &lt;artifactId&gt;hibernate-entitymanager&lt;/artifactId&gt;
            &lt;version&gt;5.2.10.Final&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-devtools&lt;/artifactId&gt;
            &lt;optional&gt;true&lt;/optional&gt;
        &lt;/dependency&gt;
    &lt;/dependencies&gt;

    &lt;build&gt;
        &lt;plugins&gt;
            &lt;plugin&gt;
                &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
                &lt;artifactId&gt;spring-boot-maven-plugin&lt;/artifactId&gt;
            &lt;/plugin&gt;
        &lt;/plugins&gt;
    &lt;/build&gt;


&lt;/project&gt;
</code></pre>

