# Accessing existing postgres database with ormlite
[Link to question](https://stackoverflow.com/questions/22345235/accessing-existing-postgres-database-with-ormlite)
**Creation Date:** 1394611028
**Score:** 1
**Tags:** java, postgresql, ormlite
## Question Body
<p>I just started writing an application that should use ormlite to access a postgreSQL database that I already created. It uses the database scheme and the domain object classes below. However, I am not able to create a new user running the test method below. Accessing the database using this classes works without problems. And the Exception I get just tells me that postgre was not able to insert:</p>

<pre><code>java.sql.SQLException: Unable to run insert stmt on object net.avedo.spozz.models.User@78412176: INSERT INTO "users" ("id" ,"cdate" ,"mdate" ,"name" ,"email" ,"password" ,"avatar_id" ) VALUES (?,?,?,?,?,?,?)
    at com.j256.ormlite.misc.SqlExceptionUtil.create(SqlExceptionUtil.java:22)
    at com.j256.ormlite.stmt.mapped.MappedCreate.insert(MappedCreate.java:135)
    at com.j256.ormlite.stmt.StatementExecutor.create(StatementExecutor.java:450)
    at com.j256.ormlite.dao.BaseDaoImpl.create(BaseDaoImpl.java:310)
    at net.avedo.spozz.models.UserTest.testUserCreation(UserTest.java:178)
    at sun.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at sun.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:57)
    at sun.reflect.DelegatingMethodAccessorImpl.invoke(DelegatingMethodAccessorImpl.java:43)
    at java.lang.reflect.Method.invoke(Method.java:606)
    at org.junit.runners.model.FrameworkMethod$1.runReflectiveCall(FrameworkMethod.java:47)
    at org.junit.internal.runners.model.ReflectiveCallable.run(ReflectiveCallable.java:12)
    at org.junit.runners.model.FrameworkMethod.invokeExplosively(FrameworkMethod.java:44)
    at org.junit.internal.runners.statements.InvokeMethod.evaluate(InvokeMethod.java:17)
    at org.junit.internal.runners.statements.RunBefores.evaluate(RunBefores.java:26)
    at org.junit.internal.runners.statements.RunAfters.evaluate(RunAfters.java:27)
    at org.junit.runners.ParentRunner.runLeaf(ParentRunner.java:271)
    at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:70)
    at org.junit.runners.BlockJUnit4ClassRunner.runChild(BlockJUnit4ClassRunner.java:50)
    at org.junit.runners.ParentRunner$3.run(ParentRunner.java:238)
    at org.junit.runners.ParentRunner$1.schedule(ParentRunner.java:63)
    at org.junit.runners.ParentRunner.runChildren(ParentRunner.java:236)
    at org.junit.runners.ParentRunner.access$000(ParentRunner.java:53)
    at org.junit.runners.ParentRunner$2.evaluate(ParentRunner.java:229)
    at org.junit.runners.ParentRunner.run(ParentRunner.java:309)
    at org.apache.maven.surefire.junit4.JUnit4Provider.execute(JUnit4Provider.java:264)
    at org.apache.maven.surefire.junit4.JUnit4Provider.executeTestSet(JUnit4Provider.java:153)
    at org.apache.maven.surefire.junit4.JUnit4Provider.invoke(JUnit4Provider.java:124)
    at org.apache.maven.surefire.booter.ForkedBooter.invokeProviderInSameClassLoader(ForkedBooter.java:200)
    at org.apache.maven.surefire.booter.ForkedBooter.runSuitesInProcess(ForkedBooter.java:153)
    at org.apache.maven.surefire.booter.ForkedBooter.main(ForkedBooter.java:103)
Caused by: org.postgresql.util.PSQLException: ERROR: column "cdate" is of type timestamp without time zone but expression is of type character varying
  Hint: You will need to rewrite or cast the expression.
  Position: 100
    at org.postgresql.core.v3.QueryExecutorImpl.receiveErrorResponse(QueryExecutorImpl.java:2103)
    at org.postgresql.core.v3.QueryExecutorImpl.processResults(QueryExecutorImpl.java:1836)
    at org.postgresql.core.v3.QueryExecutorImpl.execute(QueryExecutorImpl.java:257)
    at org.postgresql.jdbc2.AbstractJdbc2Statement.execute(AbstractJdbc2Statement.java:512)
    at org.postgresql.jdbc2.AbstractJdbc2Statement.executeWithFlags(AbstractJdbc2Statement.java:388)
    at org.postgresql.jdbc2.AbstractJdbc2Statement.executeUpdate(AbstractJdbc2Statement.java:334)
    at com.j256.ormlite.jdbc.JdbcDatabaseConnection.insert(JdbcDatabaseConnection.java:170)
    at com.j256.ormlite.stmt.mapped.MappedCreate.insert(MappedCreate.java:91)
    ... 28 more
</code></pre>

<p>So what do I miss? And how do I have to extend the Avatar class in order to support a bytea field like <code>avatar bytea NOT NULL</code>?</p>

<p><strong>The postgreSQL database scheme</strong></p>

<pre><code>CREATE TABLE avatars (
   id BIGSERIAL PRIMARY KEY,
   cdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   mdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE users (
   id BIGSERIAL PRIMARY KEY,
   cdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   mdate TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
   name VARCHAR(160) UNIQUE NOT NULL,
   email VARCHAR (355) UNIQUE NOT NULL,
   password VARCHAR(30) NOT NULL,
   avatar_id BIGINT,
   CONSTRAINT user_avatar_id FOREIGN KEY (avatar_id)
      REFERENCES avatars (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);
</code></pre>

<p><strong>A simple test case</strong></p>

<pre><code>@Test
public void testUserCreation() throws Exception {
    try {
        // Setup the user database object, ...
        Dao&lt;User, Integer&gt; userDao = getUserDao();

        // ... create a new user ...
        User user = new User();
        user.setName("Andi");
        user.setEmail("info@avedo.net");
        user.setPassword("geheim");
        userDao.create(user);

        // ... and finally query all users.
        List&lt;User&gt; userList = userDao.query(
                    userDao.queryBuilder().where()
             .eq("name", "Andi")
             .prepare());

        Assert.assertTrue("User creation failed.", userList.get(0).getName().equals("Andi"));
        Assert.assertTrue("User creation failed." + userList.get(0).getName(), userList.get(0).getName().equals("Andi"));
    } catch (SQLException e) {
        throw new Exception("Failed to create user: " + e.getMessage());
    }
}
</code></pre>

<p><strong>Avatar.java</strong></p>

<pre><code>@DatabaseTable(tableName = "avatars")
public class Avatar {
    @DatabaseField(generatedIdSequence = "avatars_id_seq", useGetSet = true)
    private long id;

    @DatabaseField(canBeNull = false, defaultValue="CURRENT_TIMESTAMP", useGetSet = true)
    private String cdate;

    @DatabaseField(canBeNull = false, defaultValue="CURRENT_TIMESTAMP", useGetSet = true)
    private String mdate;

    public Avatar() {
        // ORMLite needs a no-arg constructor 
    }

    // Getter and setter methods.
}
</code></pre>

<p><strong>User.java</strong></p>

<pre><code>@DatabaseTable(tableName = "users")
public class User {
    @DatabaseField(generatedIdSequence = "users_id_seq", useGetSet = true)
    private long id;

    @DatabaseField(canBeNull = false, defaultValue="CURRENT_TIMESTAMP", useGetSet = true)
    private String cdate;

    @DatabaseField(canBeNull = false, defaultValue="CURRENT_TIMESTAMP", useGetSet = true)
    private String mdate;

    @DatabaseField(canBeNull = false, useGetSet = true)
    private String name;

    @DatabaseField(canBeNull = false, useGetSet = true)
    private String email;

    @DatabaseField(canBeNull = false, useGetSet = true)
    private String password;

    @DatabaseField(columnName = "avatar_id", foreign = true, useGetSet = true)
    private Avatar avatar;

    public User() {
        // ORMLite needs a no-arg constructor 
    }

    // Getter and setter methods.
}
</code></pre>

## Answers
### Answer ID: 22349893
<p>I was able to solve my problem by changing the attribute type of cdate and mdate from <code>String</code> to <code>Date</code>. Furthermore I had to remove the <code>defaultValue</code> and <code>canBeNull</code> parameters from the @DatabaseField annotation. Which leaves me with the follwing class:</p>

<pre><code>@DatabaseTable(tableName = "users")
public class User {
    @DatabaseField(generatedIdSequence = "users_id_seq", useGetSet = true)
    private long id;

    @DatabaseField(useGetSet = true)
    private Date cdate;

    @DatabaseField(useGetSet = true)
    private Date mdate;

    @DatabaseField(canBeNull = false, useGetSet = true)
    private String name;

    @DatabaseField(canBeNull = false, useGetSet = true)
    private String email;

    @DatabaseField(canBeNull = false, useGetSet = true)
    private String password;

    @DatabaseField(columnName = "avatar_id", foreign = true, useGetSet = true)
    private Avatar avatar;

    public User() {
        // ORMLite needs a no-arg constructor 
    }

    // Getter and setter methods.
}
</code></pre>

<p>Finally, I had to adjust the database scheme accordingly: </p>

<pre><code>CREATE TABLE avatars (
   id BIGSERIAL PRIMARY KEY,
   cdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   mdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP
--   avatar bytea NOT NULL
);

CREATE TABLE users (
   id BIGSERIAL PRIMARY KEY,
   cdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   mdate TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
   name VARCHAR(160) NOT NULL,
   email VARCHAR (355) UNIQUE NOT NULL,
   password VARCHAR(30) NOT NULL,
   avatar_id BIGINT,
   CONSTRAINT user_avatar_id FOREIGN KEY (avatar_id)
      REFERENCES avatars (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
);
</code></pre>

<p>In order to avoid NULL values, I set the default value of cdate and mdate to CURRENT_TIMESTAMP and added a trigger, which will automatically update the value of mdate if the corresponding row changes:</p>

<pre><code>CREATE OR REPLACE FUNCTION update_timestamp() RETURNS TRIGGER AS 
$update_timestamp$
    BEGIN
        NEW.mdate := CURRENT_TIMESTAMP;
        RETURN NEW;
    END;
$update_timestamp$ 
LANGUAGE plpgsql;

CREATE TRIGGER update_timestamp BEFORE INSERT OR UPDATE ON avatars
    FOR EACH ROW EXECUTE PROCEDURE update_timestamp();

CREATE TRIGGER update_timestamp BEFORE INSERT OR UPDATE ON users
    FOR EACH ROW EXECUTE PROCEDURE update_timestamp();
</code></pre>

