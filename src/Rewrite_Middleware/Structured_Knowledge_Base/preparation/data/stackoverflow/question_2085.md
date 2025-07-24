# How to use Hibernate to query a MySQL database with indexes
[Link to question](https://stackoverflow.com/questions/18261418/how-to-use-hibernate-to-query-a-mysql-database-with-indexes)
**Creation Date:** 1376599218
**Score:** 1
**Tags:** java, mysql, hibernate, dao, indexing
## Question Body
<p>I have an application developed based on MySQL that is connected through Hibernate. I used DAO utility code to query the database. Now I need optimize my database query by indexes. My question is, how can I query data through Hibernate DAO utility code and make sure indexes are used in MySQL database when queries are executed. Any hints or pointers to existing examples are appreciated!</p>

<p>Update: Just want to make the question more understandable a little bit. Following is the code I used to query the MySQL database through Hibernated DAO utility codes. I'm not directly using HQL here. Any suggestions for a best solution? If needed, I will rewrite the database query code and use HQL directly instead.</p>

<pre><code>    public static List&lt;Measurements&gt; getMeasurementsList(String physicalId, String startdate, String enddate) {

    List&lt;Measurements&gt; listOfMeasurements = new ArrayList&lt;Measurements&gt;();
    Timestamp queryStartDate = toTimestamp(startdate);
    Timestamp queryEndDate = toTimestamp(enddate);

    MeasurementsDAO measurementsDAO = new MeasurementsDAO();
    PhysicalLocationDAO physicalLocationDAO = new PhysicalLocationDAO();
    short id = Short.parseShort(physicalId);
    List physicalLocationList = physicalLocationDAO.findByProperty("physicalId", id);
    Iterator ite = physicalLocationList.iterator();
    while(ite.hasNext()) {
        PhysicalLocation physicalLocation = (PhysicalLocation)ite.next();
        List measurementsList = measurementsDAO.findByProperty("physicalLocation", physicalLocation);
        Iterator jte = measurementsList.iterator();
        while(jte.hasNext()){
            Measurements measurements = (Measurements)jte.next();
            if(measurements.getMeasTstime().after(queryStartDate) 
                    &amp;&amp; measurements.getMeasTstime().before(queryEndDate)) {
                listOfMeasurements.add(measurements);
            }
        }
    }

    return listOfMeasurements;
}
</code></pre>

## Answers
### Answer ID: 18261543
<p>Just like with SQL, you don't need to do anything special. Just execute your queries as usual, and the database will use the indices you've created to optimize them, if possible.</p>

<p>For example, let's say you have a HQL query that searches all the products that have a given name:</p>

<pre><code>select p from Product where p.name = :name
</code></pre>

<p>This query will be translated by Hibernate to SQL:</p>

<pre><code>select p.id, p.name, p.price, p.code from product p where p.name = ?
</code></pre>

<p>If you don't have any index set on <code>product.name</code>, the database will have to scan the whole table of products to find those that have the given name.</p>

<p>If you have an index set on <code>product.name</code>, the database will determine that, given the query, it's useful to use this index, and will thus know which rows have the given name thanks to the index. It willl thus be able to only read a small subset of the rows to return the queries data.</p>

<p>This is all transparent to you. You just need to know which queries are slow and frequent enough to justify the creation of an index to speed them up.</p>

