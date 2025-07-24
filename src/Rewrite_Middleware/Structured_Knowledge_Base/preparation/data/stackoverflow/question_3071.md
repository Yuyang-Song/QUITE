# How to rewrite this H2 query using an unsupported feature
[Link to question](https://stackoverflow.com/questions/65170267/how-to-rewrite-this-h2-query-using-an-unsupported-feature)
**Creation Date:** 1607271486
**Score:** 0
**Tags:** java, sql, jpa, h2
## Question Body
<p>I have a JPA Entity</p>
<pre><code>public class GenericRecord {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private LocalDate localDate;

    private String category;

    private Double amount;
}
</code></pre>
<p>At the moment I have some code that generates a <code>Map&lt;String, Map&lt;String, Double&gt;&gt;</code> that looks like this:
<a href="https://i.sstatic.net/Qp1Ha.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/Qp1Ha.png" alt="enter image description here" /></a></p>
<p>I'd like to generate this map using a query on a H2 database (the data is already in the DB). However, it seems that I'm using an unsupported feature (is it the '+' operator?):</p>
<p><a href="https://i.sstatic.net/T5b5g.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/T5b5g.png" alt="enter image description here" /></a></p>
<p>How can I rewrite the query, so that it runs on H2 (but possibly with wide compatibility)?</p>
<p><strong>EDIT 1</strong></p>
<p>This is the working query:</p>
<pre><code>SELECT CATEGORY, CAST( MONTH(LOCAL_DATE) AS VARCHAR(2)) || '-' || CAST(YEAR(LOCAL_DATE) AS VARCHAR(4)) AS mi, SUM(AMOUNT)
FROM GENERIC_RECORD 
GROUP BY CATEGORY, CAST( MONTH(LOCAL_DATE) AS VARCHAR(2)) || '-' || CAST(YEAR(LOCAL_DATE) AS VARCHAR(4)) 
</code></pre>

## Answers
### Answer ID: 65170405
<p>H2 supports it but you have to use it as sql server mode, Please check the below link.
<a href="http://h2database.com/html/features.html#compatibility" rel="nofollow noreferrer">http://h2database.com/html/features.html#compatibility</a></p>
<p>To use it, append ;MODE=MSSQLServer to the database URL. Example URL:
jdbc:h2:~/test;MODE=MSSQLServer</p>
<p>See also: <a href="http://h2database.com/html/grammar.html#operand" rel="nofollow noreferrer">http://h2database.com/html/grammar.html#operand</a></p>

### Answer ID: 65170365
<p>In the <a href="http://h2database.com/html/main.html" rel="nofollow noreferrer"><strong>H2</strong></a> SQL database, the <a href="http://h2database.com/html/grammar.html#operand" rel="nofollow noreferrer">string concatenation operator</a> is <code>||</code>, not <code>+</code>.</p>

