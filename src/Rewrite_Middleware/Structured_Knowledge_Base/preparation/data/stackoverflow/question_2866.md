# Postgresql: create a query that uses generate_series with an interval that correctly takes DST changes into account and flattens on true calendar days
[Link to question](https://stackoverflow.com/questions/56257711/postgresql-create-a-query-that-uses-generate-series-with-an-interval-that-corre)
**Creation Date:** 1558530832
**Score:** 2
**Tags:** java, sql, postgresql, time-series, generate-series
## Question Body
<p>As a followup to a comment on my question at <a href="https://stackoverflow.com/questions/55371716/is-this-query-that-tries-to-get-timeseries-statuses-with-truncated-dates-even-po#comment97466583_55371716">Is this query that tries to get timeseries statuses with truncated dates even possible in regular relational databases?</a> I have implemented a timeseries query on postgres that works reasonably well. It flattens time on whole periods (like days) and joins it with some data.</p>

<p>There is a major problem with it though: the query is timezone-dependent which works fine, but when a Daylight Savings Time (DST) happens in the middle of the generated series, this is not reflected in the output. In some timezones it unfortunately is the case that 1 day in the year takes only 23 hours and another day takes 25 hours. I need the data to be aggregated on this 23 or 25 hour period, because those are true calendar days in that timezone. But with the current query it just always adds 1 day to the series. This means that during a DST switch, I get output with data like:</p>

<pre><code>date 1: 00:00
date 2: 00:00
date 3: 00:00
(now a DST change happens)
date 3: 23:00
date 4: 23:00
... and so on
</code></pre>

<p>I'm at a loss on how to rewrite this query to take into account that certain days  take less or more hours in some timezones. Because the generate_series is based on intervals. Any ideas? The actual code has an arbitrary period and amount btw, it could also be 5 months or 3 hours.</p>

<p>Here's the full query, though I imagine only the sub1 query is relevant.</p>

<pre><code>SELECT sub2.fromdate,
       sub2.eventlevel,
       sub2.count
FROM
  (SELECT sub1.fromdate AS fromdate,
          sub1.maxeventlevel AS eventlevel,
          count(*) AS COUNT
   FROM
     (SELECT e.subject_id,
             MAX(e.event_level) AS maxeventlevel,
             d.date AS fromdate
      FROM
        (SELECT generate_series(date_trunc(?, ? AT TIME ZONE ?) AT TIME ZONE ?, date_trunc(?, ? AT TIME ZONE ?) AT TIME ZONE ? , interval '1' DAY)) d(date)
      INNER JOIN event e ON ((e.end_date &gt; d.date
                              AND e.end_date &gt; ?)
                             OR e.end_date IS NULL)
      AND e.date &lt; d.date + interval '1' DAY
      AND e.date &lt; ?
      AND d.date &lt; ?
      INNER JOIN subject ON subject.id = e.subject_id
      INNER JOIN metric ON metric.id = e.metric_id
      INNER JOIN event_configuration_version ON event_configuration_version.id = e.event_configuration_version_id
      INNER JOIN event_configuration ON event_configuration.id = event_configuration_version.event_configuration_id
      WHERE subject.project_id = ?
      GROUP BY e.subject_id,
               fromdate) AS sub1
   GROUP BY sub1.fromdate,
            sub1.maxeventlevel) AS sub2
ORDER BY sub2.fromdate,
         sub2.eventlevel DESC
</code></pre>

<p>I don't think I can do anything in code after the query has already been performed, but I'm open to any code solutions that I've missed, though ideally we get the results back correctly from the SQL query itself. We do need to do most of the aggregation in the database itself but if there's something smart that that can be done elsewhere then that works too. The Java code generating and executing this query and transforming the result runs in a Spring Boot application and looks as follows:</p>

<pre><code>public PeriodAggregationDTO[] getSubjectStatesReport(
    AggregationPeriod aggregationPeriod, Integer aggregationPeriodAmount, UUID projectId,
    List&lt;UUID&gt; eventTriggerIds, List&lt;UUID&gt; subjectIds, List&lt;UUID&gt; metricIds, List&lt;EventLevel&gt; eventLevels,
    Date fromDate, Date toDate) {
    // to avoid an even more complex native query, we obtain the project here so a) we are sure
    // that this user has access
    // and b) we can get the timezone already without additional joins later.

    Project project = serviceUtil.findProjectByIdOrThrowApiException(projectId);
    String timezoneId = project.getTimezoneId();

    boolean skipEventTriggers = eventTriggerIds == null || eventTriggerIds.size() == 0;
    boolean skipSubjects = subjectIds == null || subjectIds.size() == 0;
    boolean skipMetrics = metricIds == null || metricIds.size() == 0;
    boolean skipEventLevels = eventLevels == null || eventLevels.size() == 0;

    StringBuilder whereClause = new StringBuilder();
    whereClause.append(" WHERE subject.project_id = :projectId");
    if (!skipEventTriggers) {
        whereClause.append(" AND event_trigger.id in :eventTriggerIds");
    }
    if (!skipSubjects) {
        whereClause.append(" AND subject_id in :subjectIds");
    }
    if (!skipMetrics) {
        whereClause.append(" AND metric.id in :metricIds");
    }
    if (!skipEventLevels) {
        whereClause.append(" AND e.event_level in :eventLevels");
    }

    String interval = String.format("'%d' %s", aggregationPeriodAmount, aggregationPeriod);

    String series = "SELECT generate_series("
        + "date_trunc(:period, :fromDate AT TIME ZONE :timezoneId) AT TIME ZONE :timezoneId"
        + " , date_trunc(:period, :toDate AT TIME ZONE :timezoneId) AT TIME ZONE :timezoneId"
        + " , interval " + interval + ")";

    String innersubquery = "SELECT e.subject_id" + ",MAX(e.event_level) as maxeventlevel"
        + ",d.date as fromdate"
        + " FROM (" + series + " ) d(date)"
        + " INNER JOIN event e ON ((e.end_date &gt; d.date AND e.end_date &gt; :fromDate)"
        + " OR e.end_date IS NULL) AND e.date &lt; d.date + interval " + interval
        + " AND e.date &lt; :toDate AND d.date &lt; :toDate"
        + " INNER JOIN subject ON subject.id = e.subject_id"
        + " INNER JOIN metric ON metric.id = e.metric_id"
        + " INNER JOIN event_trigger_version ON event_trigger_version.id = e.event_trigger_version_id"
        + " INNER JOIN event_trigger ON event_trigger.id = event_trigger_version.event_trigger_id"
        + whereClause.toString()
        + " GROUP BY e.subject_id, fromdate";

    String outersubquery = "SELECT" + " sub1.fromdate as fromdate"
        + ",sub1.maxeventlevel as eventlevel" + ",count(*) as count" + " FROM"
        + " (" + innersubquery + ") AS sub1"
        + " GROUP BY sub1.fromdate, sub1.maxeventlevel";

    String queryString = "SELECT sub2.fromdate, sub2.eventlevel, sub2.count FROM ("
        + outersubquery + ") AS sub2"
        + " ORDER BY sub2.fromdate, sub2.eventlevel DESC";

    Query query = em.createNativeQuery(queryString);

    query.setParameter("projectId", projectId);
    query.setParameter("timezoneId", timezoneId);
    query.setParameter("period", aggregationPeriod.toString());
    query.setParameter("fromDate", fromDate);
    query.setParameter("toDate", toDate);
    if (!skipEventTriggers) {
        query.setParameter("eventTriggerIds", eventTriggerIds);
    }
    if (!skipSubjects) {
        query.setParameter("subjectIds", subjectIds);
    }
    if (!skipMetrics) {
        query.setParameter("metricIds", metricIds);
    }
    if (!skipEventLevels) {
        List&lt;Integer&gt; eventLevelOrdinals =
            eventLevels.stream().map(Enum::ordinal).collect(Collectors.toList());
        query.setParameter("eventLevels", eventLevelOrdinals);
    }

    List&lt;?&gt; resultList = query.getResultList();

    Stream&lt;AggregateQueryEntity&gt; stream = resultList.stream().map(obj -&gt; {
        Object[] array = (Object[]) obj;
        Timestamp timestamp = (Timestamp) array[0];
        Integer eventLevelOrdinal = (Integer) array[1];
        EventLevel eventLevel = EventLevel.values()[eventLevelOrdinal];
        BigInteger count = (BigInteger) array[2];
        return new AggregateQueryEntity(timestamp, eventLevel, count.longValue());
    });
    return transformQueryResult(stream);
}

private PeriodAggregationDTO[] transformQueryResult(Stream&lt;AggregateQueryEntity&gt; stream) {
    // we specifically use LinkedHashMap to maintain ordering. We also set Linkedlist explicitly
    // because there are no guarantees for this list type with toList()
    Map&lt;Timestamp, List&lt;AggregateQueryEntity&gt;&gt; aggregatesByDate = stream
        .collect(Collectors.groupingBy(AggregateQueryEntity::getTimestamp,
            LinkedHashMap::new, Collectors.toCollection(LinkedList::new)));

    return aggregatesByDate.entrySet().stream().map(entryByDate -&gt; {
        PeriodAggregationDTO dto = new PeriodAggregationDTO();
        dto.setFromDate((Date.from(entryByDate.getKey().toInstant())));
        List&lt;AggregateQueryEntity&gt; value = entryByDate.getValue();
        List&lt;EventLevelAggregationDTO&gt; eventLevelAggregationDTOS = getAggregatesByEventLevel(value);
        dto.setEventLevels(eventLevelAggregationDTOS);
        return dto;
    }).toArray(PeriodAggregationDTO[]::new);
}

private List&lt;EventLevelAggregationDTO&gt; getAggregatesByEventLevel(
    List&lt;AggregateQueryEntity&gt; value) {
    Map&lt;EventLevel, AggregateQueryEntity&gt; aggregatesByEventLevel = value.stream()
        .collect(Collectors.toMap(AggregateQueryEntity::getEventLevel, Function.identity(), (u, v) -&gt; {
            throw new InternalException(String.format("Unexpected duplicate event level %s", u));
        }, LinkedHashMap::new));
    return aggregatesByEventLevel.values().stream().map(aggregateQueryEntity -&gt; {
        EventLevelAggregationDTO eventLevelAggregationDTO = new EventLevelAggregationDTO();
        eventLevelAggregationDTO.setEventLevel(aggregateQueryEntity.getEventLevel());
        eventLevelAggregationDTO.setCount(aggregateQueryEntity.getCount());
        return eventLevelAggregationDTO;
    }).collect(Collectors.toCollection(LinkedList::new));
}
</code></pre>

<p>With another data class:</p>

<pre><code>@Data
class AggregateQueryEntity {

    private final Timestamp timestamp;
    private final EventLevel eventLevel;
    private final long count;
}
</code></pre>

## Answers
### Answer ID: 56281819
<p>If you use <code>timestamp with time zone</code>, it should work just as you expect, because adding 1 day will sometimes add 23 or 25 hours:</p>

<pre><code>SHOW timezone;

   TimeZone    
---------------
 Europe/Vienna
(1 row)

SELECT * from generate_series(
                 TIMESTAMP WITH TIME ZONE '2019-03-28',
                 TIMESTAMP WITH TIME ZONE '2019-04-05',
                 INTERVAL '1' DAY
              );

    generate_series     
------------------------
 2019-03-28 00:00:00+01
 2019-03-29 00:00:00+01
 2019-03-30 00:00:00+01
 2019-03-31 00:00:00+01
 2019-04-01 00:00:00+02
 2019-04-02 00:00:00+02
 2019-04-03 00:00:00+02
 2019-04-04 00:00:00+02
 2019-04-05 00:00:00+02
(9 rows)
</code></pre>

<p>As you can see, this hinges on the current setting of <code>timezone</code>, which is respected by the date arithmetic performed by <code>generate_series</code>.</p>

<p>If you want to use this, you'll have to adjust the parameter for each query. Fortunately this is not difficult:</p>

<pre><code>BEGIN;  -- a transaction
SET LOCAL timezone = 'whatever';  -- for the transaction only
SELECT /* your query */;
COMMIT;
</code></pre>

### Answer ID: 56272537
<p>Simple enough solution will be patching it with java code rather than retrieving it from SQL directly - not saying it's impossible but maybe rather complicated. below is the java code that you can patch in.
Just like simple query get date, time and timezone from SQL result regardless of timezone difference.</p>

<pre><code>date 1: 00:00
date 2: 00:00
date 3: 00:00
(now a DST change happens)
date 3: 23:00
date 4: 23:00
</code></pre>

<p>for example in your case Daylight savings takes place between date 3 and date 4. Consider date 3 as <code>oldDate</code> and date 4 as <code>newDate</code> variable in below java code.
Step 1 : Retrieve timezone from both the dates with <code>newDate.getTimezoneOffset()</code> and <code>oldDate.getTimezoneOffset()</code></p>

<pre class="lang-java prettyprint-override"><code>TimeZone timezone = TimeZone.getDefault();
{
// compare this 2 timezone to see if they are in different timezone that way you will see if Daylight saving changes took place. i.e. (GMT and BST (+1) )
// calculation will only be done if timezones are different
if(!(oldDate.getTimezoneOffset() == newDate.getTimezoneOffset()) ){
//save time to modify it later on
final long newTime = newDate.getTime(); 
//this function will check time difference caused by DST
long timediff = checkTimeZoneDiff(oldDate, newDate)

//update newDate (date 4) based on difference found.
newDate = new Date(time+timediff);
}


private long checkTimeZoneDiff(newDate,oldDate){
if(timezone.inDaylightTime(oldDate))
   // this will add +1 hour
    return timezone.getDSTSavings();
else if (timezone.inDaylightTime(newDate)){
   /* this will remove -1 hour, in your case code should go through this bit resulting in 24 hour correct day*/
    return -timezone.getDSTSavings()
else
    return 0;
}
</code></pre>

<p>Hope that makes sense, you will be adding <code>timediff</code> to newDate(date 4). And continue same process for every other. See bubble short algorithm for checking values in that sequence.   </p>

