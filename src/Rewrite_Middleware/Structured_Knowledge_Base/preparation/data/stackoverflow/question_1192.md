# Hibernate uses wrong column name despite all anotations
[Link to question](https://stackoverflow.com/questions/62696664/hibernate-uses-wrong-column-name-despite-all-anotations)
**Creation Date:** 1593693982
**Score:** 0
**Tags:** java, postgresql, hibernate, spring-data-jpa
## Question Body
<p>I am trying to configure simple database using Spring JPA, and I encountered, which seems simular to some questions here, but solution to this aren`t working.</p>
<p>I am trying to insert following POJO into PostgreSQL database :</p>
<pre><code>@Entity
@Table(name = &quot;students&quot;, schema = &quot;public&quot;)
public class Student {

    @Id
    @Column(name = &quot;ID&quot;)
    private UUID id = UUID.randomUUID();
    @Column(name = &quot;First_Name&quot;)
    private String firstName;
    @Column(name = &quot;Last_Name&quot;)
    private String lastName;
    @Column(name = &quot;Age&quot;)
    private Integer age;
    @Column(name = &quot;Passport_Number&quot;)
    private Integer passNumber;
    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = &quot;Group_ID&quot;, referencedColumnName = &quot;ID&quot;)
    private Group group;

    public UUID getId() {
        return id;
    }

    public void setId(@NonNull UUID id) { this.id = id; }

    public String getFirstName() {
        return firstName;
    }

    public void setFirstName(String firstName) {
        this.firstName = firstName;
    }

    public String getLastName() {
        return lastName;
    }

    public void setLastName(String lastName) {
        this.lastName = lastName;
    }

    public Integer getAge() {
        return age;
    }

    public void setAge(Integer age) {
        this.age = age;
    }

    public Integer getPassNumber() {
        return passNumber;
    }

    public void setPassNumber(Integer passNumber) {
        this.passNumber = passNumber;
    }

    public Group getGroup() { return group; }

    public void setGroup(Group group) { this.group = group; }

    public void setUpdate(@NonNull Student student) {
        setFirstName(student.getFirstName());
        setLastName(student.getLastName());
        setAge(student.getAge());
        setPassNumber(student.getPassNumber());
    }
}

</code></pre>
<p>Table of my database is created using following sql :</p>
<pre><code>CREATE TABLE students (
    &quot;ID&quot; UUID,
    &quot;First_Name&quot; VARCHAR(50),
    &quot;Last_Name&quot; VARCHAR(50),
    &quot;Age&quot; INT,
    &quot;Passport_Number&quot; INT,
    &quot;Group_ID&quot; UUID,
    UNIQUE(&quot;First_Name&quot;, &quot;Last_Name&quot;),
    UNIQUE(&quot;Passport_Number&quot;),
    FOREIGN KEY(&quot;Group_ID&quot;) REFERENCES groups(&quot;ID&quot;),
    PRIMARY KEY (&quot;ID&quot;)
);
</code></pre>
<p>When trying to insert new Student, Hibernate builds following sql (message in console) :</p>
<pre><code>Hibernate: 
    select
        student0_.ID as id1_0_0_,
        student0_.Age as age2_0_0_,
        student0_.First_Name as first_na3_0_0_,
        student0_.Group_ID as group_id6_0_0_,
        student0_.Last_Name as last_nam4_0_0_,
        student0_.Passport_Number as passport5_0_0_ 
    from
        public.students student0_ 
    where
        student0_.ID=?
</code></pre>
<p>And here is the problem. There is no <code>student0_</code>, and so psql off course gives <code>org.postgresql.util.PSQLException: ERROR: column student0_.id does not exist</code></p>
<p>I tryied also to give name variable to <code>@Entity</code> specifically, but to no effect. Also I tried to change naming stratagies : <strong>implicit naming strategy</strong>, <strong>improved naming strategy</strong>, <strong>physical naming strategy</strong>, <strong>implicit legacy naming strategy</strong>. And I already tried to change dialect, but also nothing.</p>
<p>My current hibernate properties are :</p>
<pre><code>#Hibernate
hibernate.dialect = org.hibernate.dialect.PostgreSQLDialect
hibernate.show_sql = true
hibernate.format_sql = true
hibernate.hbm2ddl.auto = none
hibernate.ejb.naming_strategy = org.hibernate.boot.model.naming.PhysicalNamingStrategyStandardImpl
</code></pre>
<p>Also this is <em>Configuration</em> that I use :</p>
<pre><code>@Configuration
@EnableTransactionManagement
@PropertySource({&quot;classpath:dao.properties&quot;})
@EnableJpaRepositories(basePackages = {&quot;com.university.dao&quot;})
public class ApplicationConfig {

    @Autowired
    private Environment environment;

    public ApplicationConfig() {
        super();
    }

    @Bean
    public DataSource dataSource() {
        final BasicDataSource dataSource = new BasicDataSource();
        dataSource.setDriverClassName(Preconditions.checkNotNull(environment.getProperty(&quot;jdbc.driverClassName&quot;)));
        dataSource.setUrl(Preconditions.checkNotNull(environment.getProperty(&quot;jdbc.url&quot;)));
        dataSource.setUsername(Preconditions.checkNotNull(environment.getProperty(&quot;jdbc.user&quot;)));
        dataSource.setPassword(Preconditions.checkNotNull(environment.getProperty(&quot;jdbc.password&quot;)));

        return dataSource;
    }

    @Bean
    public LocalContainerEntityManagerFactoryBean entityManagerFactory(DataSource dataSource,
                                                                       Environment environment) {
        LocalContainerEntityManagerFactoryBean entityManagerFactory = new LocalContainerEntityManagerFactoryBean();
        entityManagerFactory.setDataSource(dataSource);
        entityManagerFactory.setJpaVendorAdapter(new HibernateJpaVendorAdapter());
        entityManagerFactory.setJpaProperties(getHibernateProperties());
        entityManagerFactory.setPackagesToScan(&quot;com.university.domain&quot;);

        return entityManagerFactory;
    }

    @Bean
    public PlatformTransactionManager transactionManager() {
        final JpaTransactionManager transactionManager = new JpaTransactionManager();
        transactionManager.setEntityManagerFactory(entityManagerFactory(dataSource(),environment).getObject());

        return transactionManager;
    }

    @Bean
    public PersistenceExceptionTranslationPostProcessor exceptionTranslation() {
        return new PersistenceExceptionTranslationPostProcessor();
    }

    final Properties getHibernateProperties() {
        final Properties hibernateProperties = new Properties();
        hibernateProperties.setProperty(&quot;hibernate.hbm2ddl.auto&quot;, environment.getProperty(&quot;hibernate.hbm2ddl.auto&quot;));
        hibernateProperties.setProperty(&quot;hibernate.dialect&quot;, environment.getProperty(&quot;hibernate.dialect&quot;));
        hibernateProperties.setProperty(&quot;hibernate.show_sql&quot;, environment.getProperty(&quot;hibernate.show_sql&quot;));
        hibernateProperties.setProperty(&quot;hibernate.format_sql&quot;, environment.getProperty(&quot;hibernate.format_sql&quot;));
        hibernateProperties.setProperty(&quot;hibernate.ejb.naming_strategy&quot;, environment.getProperty(&quot;hibernate.ejb.naming_strategy&quot;));

        return hibernateProperties;
    }
}
</code></pre>
<p>As for versions, I am using Spring JPA 2.3.1.Release and Hibernate 5+, here is full maven pom file :</p>
<pre><code>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot;?&gt;
&lt;project xmlns=&quot;http://maven.apache.org/POM/4.0.0&quot;
         xmlns:xsi=&quot;http://www.w3.org/2001/XMLSchema-instance&quot;
         xsi:schemaLocation=&quot;http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd&quot;&gt;
    &lt;modelVersion&gt;4.0.0&lt;/modelVersion&gt;
    &lt;parent&gt;
        &lt;artifactId&gt;spring-boot-starter-parent&lt;/artifactId&gt;
        &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
        &lt;version&gt;2.3.1.RELEASE&lt;/version&gt;
        &lt;relativePath/&gt;
    &lt;/parent&gt;
    &lt;groupId&gt;com.example&lt;/groupId&gt;
    &lt;artifactId&gt;university&lt;/artifactId&gt;
    &lt;version&gt;1.0-SNAPSHOT&lt;/version&gt;

    &lt;properties&gt;
        &lt;project.build.sourceEncoding&gt;UTF-8&lt;/project.build.sourceEncoding&gt;
        &lt;project.build.reporting.outputEncoding&gt;UTF-8&lt;/project.build.reporting.outputEncoding&gt;
        &lt;java.version&gt;1.8&lt;/java.version&gt;
        &lt;maven.compiler.source&gt;1.8&lt;/maven.compiler.source&gt;
        &lt;maven.compiler.target&gt;1.8&lt;/maven.compiler.target&gt;
        &lt;junit-jupiter.version&gt;5.6.1&lt;/junit-jupiter.version&gt;
        &lt;junit.version&gt;4.13&lt;/junit.version&gt;
        &lt;org.springframework.version&gt;5.2.7.RELEASE&lt;/org.springframework.version&gt;
        &lt;org.springframework.boot.version&gt;2.3.1.RELEASE&lt;/org.springframework.boot.version&gt;
        &lt;org.hibernate.validator.version&gt;6.1.5.Final&lt;/org.hibernate.validator.version&gt;
        &lt;org.apache.tomcat.version&gt;9.0.36&lt;/org.apache.tomcat.version&gt;
        &lt;com.vaadin.version&gt;16.0.0&lt;/com.vaadin.version&gt;
        &lt;org.junit.jupiter.version&gt;5.6.2&lt;/org.junit.jupiter.version&gt;
    &lt;/properties&gt;

    &lt;build&gt;
        &lt;plugins&gt;
            &lt;plugin&gt;
                &lt;groupId&gt;org.apache.maven.plugins&lt;/groupId&gt;
                &lt;artifactId&gt;maven-compiler-plugin&lt;/artifactId&gt;
                &lt;version&gt;3.8.1&lt;/version&gt;
                &lt;configuration&gt;
                    &lt;source&gt;1.8&lt;/source&gt;
                    &lt;target&gt;1.8&lt;/target&gt;
                &lt;/configuration&gt;
            &lt;/plugin&gt;
            &lt;plugin&gt;
                &lt;groupId&gt;org.apache.maven.plugins&lt;/groupId&gt;
                &lt;artifactId&gt;maven-surefire-plugin&lt;/artifactId&gt;
                &lt;version&gt;3.0.0-M4&lt;/version&gt;
            &lt;/plugin&gt;
            &lt;plugin&gt;
                &lt;groupId&gt;org.apache.maven.plugins&lt;/groupId&gt;
                &lt;artifactId&gt;maven-deploy-plugin&lt;/artifactId&gt;
                &lt;version&gt;3.0.0-M1&lt;/version&gt;
            &lt;/plugin&gt;
            &lt;plugin&gt;
                &lt;groupId&gt;org.apache.maven.plugins&lt;/groupId&gt;
                &lt;artifactId&gt;maven-assembly-plugin&lt;/artifactId&gt;
                &lt;version&gt;3.2.0&lt;/version&gt;
                &lt;executions&gt;
                    &lt;execution&gt;
                        &lt;phase&gt;package&lt;/phase&gt;
                        &lt;goals&gt;
                            &lt;goal&gt;single&lt;/goal&gt;
                        &lt;/goals&gt;
                    &lt;/execution&gt;
                &lt;/executions&gt;
                &lt;configuration&gt;
                    &lt;archive&gt;
                        &lt;manifest&gt;
                            &lt;addClasspath&gt;true&lt;/addClasspath&gt;
                            &lt;classpathPrefix&gt;lib/&lt;/classpathPrefix&gt;
                            &lt;mainClass&gt;com.university.Main&lt;/mainClass&gt;
                        &lt;/manifest&gt;
                    &lt;/archive&gt;
                    &lt;descriptorRefs&gt;
                        &lt;descriptorRef&gt;jar-with-dependencies&lt;/descriptorRef&gt;
                    &lt;/descriptorRefs&gt;
                &lt;/configuration&gt;
            &lt;/plugin&gt;
            &lt;plugin&gt;
                &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
                &lt;artifactId&gt;spring-boot-maven-plugin&lt;/artifactId&gt;
                &lt;version&gt;${org.springframework.boot.version}&lt;/version&gt;
            &lt;/plugin&gt;
            &lt;plugin&gt;
                &lt;groupId&gt;com.vaadin&lt;/groupId&gt;
                &lt;artifactId&gt;vaadin-maven-plugin&lt;/artifactId&gt;
                &lt;version&gt;${com.vaadin.version}&lt;/version&gt;
            &lt;/plugin&gt;
        &lt;/plugins&gt;
    &lt;/build&gt;

    &lt;dependencyManagement&gt;
        &lt;dependencies&gt;
            &lt;dependency&gt;
                &lt;groupId&gt;com.vaadin&lt;/groupId&gt;
                &lt;artifactId&gt;vaadin-bom&lt;/artifactId&gt;
                &lt;version&gt;${com.vaadin.version}&lt;/version&gt;
                &lt;type&gt;pom&lt;/type&gt;
                &lt;scope&gt;import&lt;/scope&gt;
            &lt;/dependency&gt;
        &lt;/dependencies&gt;
    &lt;/dependencyManagement&gt;

    &lt;dependencies&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter&lt;/artifactId&gt;
            &lt;version&gt;${org.springframework.boot.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-jdbc&lt;/artifactId&gt;
            &lt;version&gt;${org.springframework.boot.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-web&lt;/artifactId&gt;
            &lt;version&gt;${org.springframework.boot.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-context&lt;/artifactId&gt;
            &lt;version&gt;${org.springframework.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework&lt;/groupId&gt;
            &lt;artifactId&gt;spring-orm&lt;/artifactId&gt;
            &lt;version&gt;${org.springframework.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.springframework.boot&lt;/groupId&gt;
            &lt;artifactId&gt;spring-boot-starter-data-jpa&lt;/artifactId&gt;
            &lt;version&gt;${org.springframework.boot.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.hibernate&lt;/groupId&gt;
            &lt;artifactId&gt;hibernate-validator&lt;/artifactId&gt;
            &lt;version&gt;${org.hibernate.validator.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.apache.tomcat&lt;/groupId&gt;
            &lt;artifactId&gt;tomcat-dbcp&lt;/artifactId&gt;
            &lt;version&gt;${org.apache.tomcat.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;com.vaadin&lt;/groupId&gt;
            &lt;artifactId&gt;vaadin-spring-boot-starter&lt;/artifactId&gt;
            &lt;version&gt;${com.vaadin.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;com.vaadin&lt;/groupId&gt;
            &lt;artifactId&gt;vaadin&lt;/artifactId&gt;
            &lt;version&gt;${com.vaadin.version}&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;com.google.guava&lt;/groupId&gt;
            &lt;artifactId&gt;guava&lt;/artifactId&gt;
            &lt;version&gt;29.0-jre&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.postgresql&lt;/groupId&gt;
            &lt;artifactId&gt;postgresql&lt;/artifactId&gt;
            &lt;version&gt;42.2.12.jre7&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.mybatis&lt;/groupId&gt;
            &lt;artifactId&gt;mybatis&lt;/artifactId&gt;
            &lt;version&gt;3.4.5&lt;/version&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;com.h2database&lt;/groupId&gt;
            &lt;artifactId&gt;h2&lt;/artifactId&gt;
            &lt;version&gt;1.4.200&lt;/version&gt;
            &lt;scope&gt;test&lt;/scope&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.junit.jupiter&lt;/groupId&gt;
            &lt;artifactId&gt;junit-jupiter-api&lt;/artifactId&gt;
            &lt;version&gt;${org.junit.jupiter.version}&lt;/version&gt;
            &lt;scope&gt;test&lt;/scope&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.junit.jupiter&lt;/groupId&gt;
            &lt;artifactId&gt;junit-jupiter-engine&lt;/artifactId&gt;
            &lt;version&gt;${org.junit.jupiter.version}&lt;/version&gt;
            &lt;scope&gt;test&lt;/scope&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.junit.vintage&lt;/groupId&gt;
            &lt;artifactId&gt;junit-vintage-engine&lt;/artifactId&gt;
            &lt;version&gt;${org.junit.jupiter.version}&lt;/version&gt;
            &lt;scope&gt;test&lt;/scope&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;junit&lt;/groupId&gt;
            &lt;artifactId&gt;junit&lt;/artifactId&gt;
            &lt;version&gt;4.13&lt;/version&gt;
            &lt;scope&gt;test&lt;/scope&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;com.github.stefanbirkner&lt;/groupId&gt;
            &lt;artifactId&gt;system-rules&lt;/artifactId&gt;
            &lt;version&gt;1.19.0&lt;/version&gt;
            &lt;scope&gt;test&lt;/scope&gt;
        &lt;/dependency&gt;
        &lt;dependency&gt;
            &lt;groupId&gt;org.powermock&lt;/groupId&gt;
            &lt;artifactId&gt;powermock-reflect&lt;/artifactId&gt;
            &lt;version&gt;2.0.7&lt;/version&gt;
            &lt;scope&gt;test&lt;/scope&gt;
        &lt;/dependency&gt;
    &lt;/dependencies&gt;
&lt;/project&gt;
</code></pre>
<p>How may I remove this error without explicitly(manually) rewriting hibernate queries in configuration (so hibernate would use correct column/table names automatically)?</p>
<p>Regardless if your answer/comment helps or not, thank you very much for your effort:)</p>

## Answers
### Answer ID: 62696941
<p>There is a <code>student0_</code>, it's the table alias declared in <code>from student student0_</code>. It's the column that's not being found since it wasn't escaped properly, so <code>student0_.ID</code> <strong>really</strong> is treated as <code>student0_.id</code>.</p>
<p>Using case sensitive names isn't <a href="https://stackoverflow.com/a/20880247/2541560">recommended</a> in Postgres, whereas it's common with other databases. So instead of <code>&quot;First_name&quot;</code>, just use <code>first_name</code>. Otherwise you need to <a href="https://stackoverflow.com/a/36398277/2541560">escape the names</a> everywhere e.g.</p>
<pre><code>@Column(name = &quot;\&quot;First_Name\&quot;&quot;)
</code></pre>
<p>and that's not pretty, and all other Postgres users will frown upon your database schema.</p>

