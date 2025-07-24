# Getting records from MySQL based on a DateTime column ignoring the time portion using JPA along with Joda-Time
[Link to question](https://stackoverflow.com/questions/20205013/getting-records-from-mysql-based-on-a-datetime-column-ignoring-the-time-portion)
**Creation Date:** 1385419589
**Score:** 0
**Tags:** mysql, datetime, jpa, criteria, jodatime
## Question Body
<p>How to filter rows from MySQL database ignoring the time portion of a given DateTime field in MySQL using JPA?</p>

<p>For example, the following segment of code counts the number of rows from a database table that lie between the two dates given in a column of type <code>DateTime</code> in MySQL.</p>

<pre><code>CriteriaBuilder criteriaBuilder=entityManager.getCriteriaBuilder();
CriteriaQuery&lt;Long&gt;criteriaQuery=criteriaBuilder.createQuery(Long.class);
Root&lt;Discount&gt; root = criteriaQuery.from(entityManager.getMetamodel().entity(Discount.class));
criteriaQuery.select(criteriaBuilder.countDistinct(root));

DateTimeFormatter dateTimeFormatter=DateTimeFormat.forPattern("dd-MMM-yyyy hh:mm:ss aa");
DateTime firstDate = dateTimeFormatter.parseDateTime("01-Oct-2013 11:34:26 AM").withZone(DateTimeZone.UTC);
DateTime secondDate = dateTimeFormatter.parseDateTime("31-Oct-2013 09:22:23 PM").withZone(DateTimeZone.UTC);

criteriaQuery.where(criteriaBuilder.between(root.get(Discount_.discountStartDate), firstDate, secondDate));
Long rowCount = entityManager.createQuery(criteriaQuery).getSingleResult();
</code></pre>

<p>The two parameters <code>firstDate</code> and <code>secondDate</code> will be in turn dynamic. </p>

<p>How to rewrite this query so that the comparison does not include the time portion in the SQL query which is to be delegated to MySQL.</p>

<p>The column <code>discount_start_date</code> in the entity <code>Discount</code> is designated as follows.</p>

<pre><code>@Column(name = "discount_start_date")
@Type(type="org.jadira.usertype.dateandtime.joda.PersistentDateTime")
private DateTime discountStartDate;
</code></pre>

## Answers
### Answer ID: 20206217
<p>Seems like you are working too hard. </p>

<p>(a) Apparently, MySQL offers a <a href="http://www.w3schools.com/sql/sql_dates.asp" rel="nofollow"><code>DATE()</code></a> function that extracts the date portion of a date-
time field. (I'm a <a href="https://en.wikipedia.org/wiki/PostgreSQL" rel="nofollow">Postgres</a> guy, and don't know MySQL.) You could pursue an approach using that function call as part of your query. But I'm guessing it would faster performance if you first obtained your start and stop time by calculating with <a href="http://www.joda.org/joda-time/" rel="nofollow">Joda-Time</a> in Java before executing the SQL query, as seen below.</p>

<p>(b) Why not do this with a simple SQL query, a two criteria SELECT?</p>

<p>In pseudo-code:</p>

<pre><code>Find Discount records that go into effect from the moment this month starts up until the moment the next month starts.
</code></pre>

<p>Use Java and Joda-Time to give you the start &amp; stop values.</p>

<pre class="lang-java prettyprint-override"><code>org.joda.time.DateTime startOfThisMonth = new org.joda.time.DateTime().dayOfMonth().withMinimumValue().withTimeAtStartOfDay();
org.joda.time.DateTime startofNextMonth = startOfThisMonth.plusMonths( 1 ).dayOfMonth().withMinimumValue().withTimeAtStartOfDay();
</code></pre>

<p>Caution: Above code uses default time zone. You should specify a time zone in the constructor.</p>

<p>MySql seems to lack sophisticated time-date handling with time zones etc. So I suppose you would convert those time zoned DateTime objects to UTC.</p>

<pre class="lang-java prettyprint-override"><code>org.joda.time.DateTime startOfThisMonthInUtc = startOfThisMonth.toDateTime( org.joda.time.DateTimeZone.UTC );
org.joda.time.DateTime startofNextMonthInUtc = startofNextMonth.toDateTime( org.joda.time.DateTimeZone.UTC );
</code></pre>

<p>Then do what you do to get date-time values for MySQL.</p>

<p>Then form a query that looks something like this… (Note the use of <code>&gt;=</code> versus <code>&lt;</code> without the Equals sign.)</p>

<pre class="lang-sql prettyprint-override"><code>SELECT title_, amount_, start_date_ 
FROM discount_
WHERE discount_.start_datetime_ &gt;= startOfThisMonthFromJodaTime
AND discount_.start_datetime_ &lt; startOfNextMonthFromJodaTime
;
</code></pre>

<p>When working with date and time, it's generally better to work with the first moment of the day, first moment of the first day of month, etc. rather than try to find the last moment or end time. So my query is based on the idea of find rows whose values go up to, but do not include, the moment after the time frame in which I'm interested.</p>

