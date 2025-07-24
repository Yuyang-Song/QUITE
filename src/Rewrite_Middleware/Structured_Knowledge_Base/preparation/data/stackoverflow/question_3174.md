# Getting entityManageFactory error. Schema-validation: missing table [hibernate_sequence]
[Link to question](https://stackoverflow.com/questions/70076486/getting-entitymanagefactory-error-schema-validation-missing-table-hibernate-s)
**Creation Date:** 1637650198
**Score:** 0
**Tags:** java, spring, hibernate, spring-data-jpa
## Question Body
<p>I have 2 databases. One is set up and and it works. After I add second db I am having following error entityManageFactory error. Schema-validation: missing table [hibernate_sequence].</p>
<p>My db schema looks like this: db schema screenshot</p>
<p><a href="https://i.sstatic.net/Upmbo.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/Upmbo.png" alt="enter image description here" /></a></p>
<p>I have two classes for two tables:</p>
<pre><code>@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity(name = &quot;nightly_rate_amounts&quot;)
@Table(name = &quot;nightly_rate_amounts&quot;)
public class BookedNightlyRate {
@Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    @Column(name = &quot;bnr_meta_id&quot;)
    private Long id;
    @Column(name = &quot;unit_uuid&quot;)
    private UUID unitUuid;
    private LocalDate firstLiveDate;
    private LocalDate date;
    private BigDecimal amount;
    @Column(name = &quot;currency_code&quot;)
    private String currencyCode;

    public ImmutableTriple&lt;UUID, LocalDate, String&gt; toUnitDateCurrencyKey() {
        return new ImmutableTriple&lt;&gt;(unitUuid, date, currencyCode);
    }

    public ImmutablePair&lt;UUID, String&gt; toUnitCurrencyKey() {
        return new ImmutablePair&lt;&gt;(unitUuid, currencyCode);
    }
}
</code></pre>
<p>and:</p>
<pre><code>@Data
@AllArgsConstructor
@NoArgsConstructor
@Builder
@Entity(name = &quot;unit_attributes&quot;)
@Table(name = &quot;unit_attributes&quot;)
public class BookedUnitAttributes {
    @Id
    @Column(name = &quot;unit_uuid&quot;)
    private UUID unitUuid;
    @Column(name = &quot;first_date_available&quot;)
    private LocalDate firstLiveDate;
}
</code></pre>
<p>and Repository files:</p>
<pre><code>public interface BookedNightlyRatesDao extends CrudRepository&lt;BookedNightlyRate, Long&gt; {

@Query(value = &quot;SELECT DISTINCT bnr.unit_uuid as unitUuid, bnr.date, bnr.amount, bnr.currency_code as currencyCode &quot; +
        &quot;FROM nightly_rate_amounts AS bnr &quot; +
        &quot;WHERE bnr.unit_uuid IN (&lt;unitUuids&gt;) AND (bnr.date BETWEEN :fromDate AND :toDate)&quot;, nativeQuery = true)
List&lt;BookedNightlyRate&gt; findBookedNightlyRates(@Param(&quot;unitUuids&quot;) List&lt;String&gt; unitUuids, @Param(&quot;fromDate&quot;) LocalDate fromDate, @Param(&quot;toDate&quot;) LocalDate toDate);

@Query(value = &quot;SELECT DISTINCT opb.unit_uuid as unitUuid, opb.date, opb.amount, opb.currency_code as currencyCode &quot; +
        &quot;FROM opb_nightly_rate_amounts AS opb &quot; +
        &quot;JOIN opb_sync_enabled_for_unit AS sync ON opb.unit_uuid = sync.unit_uuid WHERE sync.enabled = 1 AND opb.is_active = 1 &quot; +
        &quot;AND sync.unit_uuid IN (&lt;unitUuids&gt;) AND (opb.date BETWEEN :fromDate AND :toDate)&quot;, nativeQuery = true)
List&lt;BookedNightlyRate&gt; findOPBRates(@Param(&quot;unitUuids&quot;) List&lt;String&gt; unitUuids, @Param(&quot;fromDate&quot;) LocalDate fromDate, @Param(&quot;toDate&quot;) LocalDate toDate);
}
</code></pre>
<p>second interface:</p>
<pre><code>public interface BookedUnitAttributesDao extends CrudRepository&lt;BookedUnitAttributes, UUID&gt; {

@Query(value = &quot;SELECT ua.unit_uuid as unitUuid, ua.first_date_available as firstLiveDate &quot; +
        &quot;FROM unit_attributes AS ua &quot; +
        &quot;WHERE ua.unit_uuid IN (&lt;unitUuids&gt;)&quot;, nativeQuery = true)
List&lt;BookedUnitAttributes&gt; findUnitAttributes(@Param(&quot;unitUuids&quot;) List&lt;String&gt; unitUuids);
}
</code></pre>
<p>I am rewriting my db from jdbi to jpa. So Data classes didn't have any annotations and I refactored my model files regarding it queries in repository files.</p>

## Answers
### Answer ID: 70079286
<p>Since you add two database Spring dosn't know what kind of database it connect. You have to exactly showed what kind of database you want to connect.
You might confiugure connection with two different database here is example of  working with JdbcTemplate connection.</p>
<pre><code>@Configuration
@ComponentScan(&quot;uz.dbo.dbocallcenter&quot;)
@PropertySource(&quot;classpath:database.properties&quot;)
public class Config2 {

    @Autowired
    Environment environment;

    private final String DRIVER = &quot;driver&quot;;
    private final String URL1 = &quot;url1&quot;;
    private final String USER1 = &quot;dbusername1&quot;;
    private final String PASSWORD1 = &quot;dbpassword1&quot;;
    private final String URL2 = &quot;url2&quot;;
    private final String USER2 = &quot;dbusername2&quot;;
    private final String PASSWORD2 = &quot;dbpassword2&quot;;


    private DataSource dataSource1() {
        return getDataSource(URL1, USER1, PASSWORD1);
    }
    private DataSource dataSource2() {
        return getDataSource(URL2, USER2, PASSWORD2);
    }

    private DataSource getDataSource(String url1, String user1, String password1) {
        DriverManagerDataSource driverManagerDataSource = new DriverManagerDataSource();
        driverManagerDataSource.setUrl(environment.getProperty(url1));
        driverManagerDataSource.setUsername(environment.getProperty(user1));
        driverManagerDataSource.setPassword(environment.getProperty(password1));
        driverManagerDataSource.setDriverClassName(environment.getProperty(DRIVER));
        return driverManagerDataSource;
    }




    @Bean(name = &quot;jdbcTemplate2&quot;)
    public JdbcTemplate jdbcTemplate2() {
        return new JdbcTemplate(dataSource2());
    }
    @Bean(name = &quot;jdbcTemplate1&quot;)
    public JdbcTemplate jdbcTemplate1() {
        return new JdbcTemplate(dataSource1());
    }

}
</code></pre>
<p>you have to do with JpaRepository connection. More precisely you can gain knowledge about this source</p>
<blockquote>
<p><a href="https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#reference" rel="nofollow noreferrer">https://docs.spring.io/spring-data/jpa/docs/current/reference/html/#reference</a></p>
</blockquote>
<p>Here is also good explanation how to connect two differnet database in one spring boot project</p>
<blockquote>
<p><a href="https://www.baeldung.com/spring-data-jpa-multiple-databases" rel="nofollow noreferrer">https://www.baeldung.com/spring-data-jpa-multiple-databases</a></p>
</blockquote>

