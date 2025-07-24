# Rewrite Hibernate Criteria with IN clause so can reuse same PreparedStatement with different number of IN clauses
[Link to question](https://stackoverflow.com/questions/56769759/rewrite-hibernate-criteria-with-in-clause-so-can-reuse-same-preparedstatement-wi)
**Creation Date:** 1561542275
**Score:** 1
**Tags:** sql, hibernate, hibernate-criteria
## Question Body
<p>I use the following Hibernate query alot when retrieving multiple records by their primary key</p>

<pre><code>       Criteria c = session
                .createCriteria(Song.class)
                .setLockMode(LockMode.NONE)
                .setResultTransformer(Criteria.DISTINCT_ROOT_ENTITY)
                .add(Restrictions.in("recNo", ids));
        List&lt;Song&gt; songs = c.list();
</code></pre>

<p>The problem is the number of ids can vary from 1 - 50, and every different number of ids requires a different PreparedStatement. That, combined with the fact that any particular prepared statement is tied to a particular database pool connection means that the opportunity to reuse a PreparedStatement is quite low.</p>

<p>Is there way I can rewrite this so that the same statement can be used with different number of in values, I think I read somewhere it could be done by using ANY instead but cannot find the reference.</p>

## Answers
### Answer ID: 67210094
<p>If you're still on an old version of Hibernate as suggested in the comments to <a href="https://stackoverflow.com/a/56773287/521799">Simon's answer here</a>, as a workaround, you could use <a href="https://www.jooq.org/doc/latest/manual/sql-execution/parsing-connection/" rel="nofollow noreferrer">jOOQ's <code>ParsingConnection</code></a> to transform your SQL by applying the <a href="https://www.jooq.org/doc/dev/manual/sql-building/dsl-context/custom-settings/settings-in-list-padding/" rel="nofollow noreferrer"><code>IN</code> list padding feature</a> transparently behind the scenes. You can just wrap your <code>DataSource</code> like this:</p>
<pre class="lang-java prettyprint-override"><code>// Input DataSource ds1:
DSLContext ctx = DSL.using(ds1, dialect);
ctx.settings().setInListPadding(true);

// Use this DataSource for your code, instead:
DataSource ds2 = ctx.parsingDataSource();
</code></pre>
<p><a href="https://blog.jooq.org/2021/04/22/use-in-list-padding-to-your-jdbc-application-to-avoid-cursor-cache-contention-problems/" rel="nofollow noreferrer">I've written up a blog post to explain this more in detail here</a>.</p>
<p>(Disclaimer: I work for the company behind jOOQ)</p>

### Answer ID: 58593517
<p>With some help I ended up getting a usual SQL connection from Hibernate, and then using standard SQL with ANY instead of IN. As far as I know using ANY means we only need a single prepared statement per connection so is better then using padded IN's. But because just using SQL not much use if you need to modify the data returned</p>

<pre><code> public static List&lt;SongDiff&gt; getReadOnlySongDiffs(List&lt;Integer&gt; ids)
    {
        Connection connection = null;
        try
        {
            connection = HibernateUtil.getSqlSession();
            String SONGDIFFSELECT = "select * from SongDiff where recNo = ANY(?)";
            PreparedStatement ps = connection.prepareStatement(SONGDIFFSELECT);

            ps.setObject(1,  ids.toArray(new Integer[ids.size()]));
            ResultSet rs = ps.executeQuery();
            List&lt;SongDiff&gt; songDiffs = new ArrayList&lt;&gt;(ids.size());
            while(rs.next())
            {
                SongDiff sd = new SongDiff();
                sd.setRecNo(rs.getInt("recNo"));
                sd.setDiff(rs.getBytes("diff"));
                songDiffs.add(sd);
            }
            return songDiffs;
        }
        catch (Exception e)
        {
            MainWindow.logger.log(Level.SEVERE, "Failed to get SongDiffsFromDb:" + e.getMessage(), e);
            throw new RuntimeException(e);
        }
        finally
        {
            SessionUtil.close(connection);
        }
    }

 public static Connection getSqlSession() throws SQLException {
        if (factory == null || factory.isClosed()) {
            createFactory();
        }

        return ((C3P0ConnectionProvider)factory.getSessionFactoryOptions().getServiceRegistry().getService(C3P0ConnectionProvider.class)).getConnection();
    }
</code></pre>

### Answer ID: 56773287
<p>This is called "in clause parameter padding" and can be activated with a hibernate property:</p>

<pre><code>&lt;property
    name="hibernate.query.in_clause_parameter_padding"
    value="true"
&lt;/property&gt;
</code></pre>

<p>Read more about this topic here: <a href="https://vladmihalcea.com/improve-statement-caching-efficiency-in-clause-parameter-padding/" rel="nofollow noreferrer">https://vladmihalcea.com/improve-statement-caching-efficiency-in-clause-parameter-padding/</a></p>

