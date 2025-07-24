# Spring Boot Test, Transactions and seeding db with data before test
[Link to question](https://stackoverflow.com/questions/77740093/spring-boot-test-transactions-and-seeding-db-with-data-before-test)
**Creation Date:** 1704046787
**Score:** 1
**Tags:** spring-boot, transactions, spring-jdbc, spring-test, spring-transactions
## Question Body
<p>After configuring Transaction propagation in my Spring Boot application, the tests I had created are failing and I am unable to make them pass again. I am using:</p>
<ul>
<li>Spring Boot 3.1.3</li>
<li>Spring Data JDBC</li>
<li>Ktorm 3.6.0 (Kotlin ORM based on JDBC)</li>
</ul>
<p>For testing purposes, I have created <code>BaseTestConfiguaration</code> class that:</p>
<ul>
<li>is a parent class for all test classes,</li>
<li>contains utility functions for inserting sample data to the database,</li>
<li>imports <code>TestFoodWarehouseApplication</code> class that defines <code>PostgreSQLContainer</code> bean (a container instance powered by TestContainers).</li>
</ul>
<pre class="lang-kotlin prettyprint-override"><code>@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
@Import(TestFoodWarehouseApplication::class)
@TestInstance(TestInstance.Lifecycle.PER_CLASS)
class BaseTestConfiguration(@Autowired protected val db: Database) {
  protected fun seedDbWithCategories() { /* Inserts a couple of categories to DB */ }
  protected fun truncateCategories() { /* Truncates categories table */ } 
}
</code></pre>
<h2>The problem</h2>
<p>Now coming to the actual test class, the problem arises when I try to execute <code>seedDbWithCategories()</code> inside a test method (see last test method). The function executes normally and a proper query is generated, but the database stays <strong>empty</strong>. The database however is populated normally when <code>seedDbWithCategories()</code> is called in a method annotated with <code>@BeforeTransaction</code> (see the first nested test class).</p>
<pre class="lang-kotlin prettyprint-override"><code>@Transactional
class CategoriesControllerTest(@Autowired db: Database) : BaseTestConfiguration(db) {

  @Nested
  @TestInstance(TestInstance.Lifecycle.PER_CLASS)
  inner class DeleteCategoryCases {
    @BeforeTransaction
    fun setup() = seedDbWithCategories()

    @AfterTransaction
    fun cleanup() = truncateCategories()

    @Test
    fun `should remove category and its children`() { 
      /* REST Assured assertions - everything OK here */
    }    
  }

  @Nested
  @TestInstance(TestInstance.Lifecycle.PER_CLASS)
  inner class GetParentCategoriesCases {
    @Test
    fun `when no categories exists, should return empty array`() {
      /* REST Assured assertions - everything OK as db should be empty now */
    }

    @Test
    fun `should return categories without parents`() {
      seedDbWithCategories()
      
      /* REST Assured assertions - NOT OK, the db is empty, but should contain my sample data */

      truncateCategories()
    }
}
</code></pre>
<h2>The Question</h2>
<p>Is it possible in any way to make <code>seedDbWithCategories()</code> work in both cases?</p>
<h3>Efforts until now</h3>
<p>What I expect is of course that my database is seeded with sample data correctly and then truncated after the test.</p>
<p>So far I have tried:</p>
<ol>
<li>wrapping the call of <code>seedDbWithCategories()</code> in <code>TestTransaction.start()/.end()</code></li>
<li>wrapping the body of <code>seedDbWithCategories()</code> in <code>TestTransaction.start()/.end()</code></li>
<li>Annotating <code>seedDbWithCategories()</code> with <code>@Transactional</code> with propagation set to Propagation.NESTED/REQUIRES_NEW/REQUIRED</li>
<li>Annotating the method like before, but also with <code>@Commit</code></li>
<li>Doing steps from 3. and 4. the same for the entire class</li>
<li>Various combination of previous steps altogether</li>
</ol>
<p>Previous attempts failed for different reasons:</p>
<ol>
<li>TransactionContext is not active</li>
<li>Cannot start a new transaction without ending the existing transaction first</li>
</ol>
<p>What I am really trying to avoid, is rewriting about 50 tests, that use calls like <code>seedDbWithCategories()</code> inside a test method or wrapping them in a <code>@Nested</code> class with just one test method inside.</p>
<p>Any help is appreciated and thank you for answers in advance.</p>

