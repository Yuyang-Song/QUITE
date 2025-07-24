# Ormlite and PostgreSQL - Error inserting text array with custom persister
[Link to question](https://stackoverflow.com/questions/25332399/ormlite-and-postgresql-error-inserting-text-array-with-custom-persister)
**Creation Date:** 1408128702
**Score:** 2
**Tags:** postgresql, ormlite
## Question Body
<p>I have been working to setup Ormlite as the primary data access layer between a PostgreSQL database and Java application.  Everything has been fairly straightforward, until I started messing with PostgreSQL's array types.  In my case, I have two tables that make use of text[] array type.  Following the documentation, I created a custom data persister as below:</p>

<pre><code>public class StringArrayPersister extends StringType {

    private static final StringArrayPersister singleTon = new StringArrayPersister();

    private StringArrayPersister() {
        super(SqlType.STRING, new Class&lt;?&gt;[]{String[].class});
    }

    public static StringArrayPersister getSingleton() {
        return singleTon;
    }


    @Override
    public Object javaToSqlArg(FieldType fieldType, Object javaObject) {
        String[] array = (String[]) javaObject;


        if (array == null) {
            return null;
        } else {

            String join = "";
            for (String str : array) {
                join += str +",";
            }

            return "'{" + join.substring(0,join.length() - 1) + "}'";
        }

    }

    @Override
    public Object sqlArgToJava(FieldType fieldType, Object sqlArg, int columnPos) {
        String string = (String) sqlArg;

        if (string == null) {
            return null;
        } else {
            return string.replaceAll("[{}]","").split(",");
        }
    }
}
</code></pre>

<p>And then in my business object implementation, I set up the persister class on the column likeso:</p>

<pre><code>   @DatabaseField(columnName = TAGS_FIELD, persisterClass = StringArrayPersister.class)
    private String[] tags;
</code></pre>

<p>When ever I try inserting a new record with the Dao.create statement, I get an error message saying tags is of type text[], but got character varying... However, when querying existing records from the database, the business object (and text array) load just fine.</p>

<p>Any ideas?</p>

<p><strong>UPDATE:</strong></p>

<p>PostGresSQL 9.2.  The exact error message:</p>

<blockquote>
  <p>Caused by: org.postgresql.util.PSQLException: ERROR: column "tags" is
  of type text[] but expression is of type character varying   Hint: You
  will need to rewrite or cast the expression.</p>
</blockquote>

## Answers
### Answer ID: 25333686
<p>I've not used <em>ormlite</em> before (I generally use <em>MyBatis</em>), however, I believe the proximal issue is this code:</p>

<pre><code> private StringArrayPersister() {
        super(SqlType.STRING, new Class&lt;?&gt;[]{String[].class});
    }
</code></pre>

<p><code>SqlType.String</code> is mapped to <code>varchar</code> in <em>SQL</em> in the <em>ormlite</em> code, and so therefore I believe is the proximal cause of the error you're getting. See <a href="http://ormlite.com/data_types.shtml" rel="nofollow">ormlite SQL Data Types info</a> for more detail on that.</p>

<p>Try changing it to this:</p>

<pre><code>private StringArrayPersister() {
        super(SqlType.OTHER, new Class&lt;?&gt;[]{String[].class});
    }
</code></pre>

<p>There may be other tweaks necessary as well to get it fully up and running, but that should get you passed this particular error with the <code>varchar</code> type mismatch.</p>

