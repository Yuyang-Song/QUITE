# Mocking groovy.sql.Sql.call(_,_,_) method
[Link to question](https://stackoverflow.com/questions/35299942/mocking-groovy-sql-sql-call-method)
**Creation Date:** 1455043973
**Score:** 0
**Tags:** grails, groovy, mocking, spock
## Question Body
<p>I am trying to mock the groovy.sql.Sql call(query, params[], closure) class.
Below is method, within a DatabaseService class file, that I am attempting this on.</p>

<pre><code>public void getUsers(List&lt;User&gt; developerList, Sql sql) {
    sql.call("{? = call GETUSERS()}", [Sql.resultSet(OracleTypes.CURSOR)]) { result -&gt;
        while (result.next()) {
            User user = new User()
            user .email = result.EMAIL
            user .lastName = result.LASTNAME
        }
    }
}
</code></pre>

<p>My mock does achieve the task, however, I do not want the mocked closure to execute. I want to mock the .call(<em>,</em>,_) method to only skip the database logic, and return back a list to the closure in the getUsers() method. I want the closure to execute in getUsers() method, not the mocked up method.</p>

<p>Below is the mockup I have written in SPOCK. </p>

<pre><code>void "test getUsers(list,sql) some results"() {
    DataSource mockedSource = Mock(DataSource)
    Sql mockedSql = Mock(Sql)
    DatabaseService databaseService = new DatabaseService()
    databaseService.dataSource = mockedSource
    List&lt;User&gt; userList= new ArrayList&lt;&gt;();

    when:
    databaseService.getUsers(userList, mockedSql)

    then:
    1 * mockedSql.call(_, _, _) &gt;&gt; { return [[EMAIL: "A", LASTNAME: "B"]] }
    userList.size() == 1
}
</code></pre>

<p>As imagined, this mockup overwrites the original method closure, and my list is never populated.. I certainly do not want to rewrite my class to use Java, nor can I change the stored procedure that is executed.</p>

## Answers
### Answer ID: 35300587
<pre><code>try :
int resultSetIdx = 0
def resutSet = Mock(ResultSet)
  ...
then:
  1 * mockedSql.call(_, _, _) &gt;&gt; { args -&gt; args[2].call(resultSet) }
  2 * mockedResultset.next() &gt;&gt; { ++resultSetIdx &gt; 1 ? false: true}
  1 * mockedResultset.getString("EMAIL") &gt;&gt; "A"
</code></pre>

<p>In the getUsers method() change</p>

<pre><code>user.lastName = result.LASTNAME
user.email = result.EMAIL
</code></pre>

<p>To</p>

<pre><code>user.lastName = result.getString("LASTNAME")
user.email = result.getString("EMAIL")
</code></pre>

<p>However, you shouldn't mock <code>Sql</code>, but rewrite your service/dao layer to be more testable. test the dao with an inmemory db, and the service layer with a mocked dao.</p>

