# Hibernate custom query on Maps generates unwanted subqueries
[Link to question](https://stackoverflow.com/questions/55076090/hibernate-custom-query-on-maps-generates-unwanted-subqueries)
**Creation Date:** 1552125339
**Score:** 0
**Tags:** java, spring, hibernate, jpa
## Question Body
<p>I have a class Purchase with a map inside.</p>

<pre><code>@Entity
public class Purchase {

    @Id
    @GeneratedValue(strategy= GenerationType.IDENTITY)
    private Integer purchaseId;

    @ManyToOne
    @JoinColumn(name = "customer_id")
    private User customer;

    @ManyToOne
    @JoinColumn(name = "item_id")
    private Item item;

    private String customization;

    @ElementCollection
    @MapKeyEnumerated(value = EnumType.STRING)
    @CollectionTable(name = "purchase_status")
    @MapKeyColumn(name = "status")
    @Column(name = "date")
    private Map&lt;PurchaseStatus, Date&gt; statusTransitions = new HashMap&lt;&gt;();

    private Date expectedDeliveryDate;

    @ManyToOne
    @JoinColumn(name = "purchase_cart_id")
    @JsonIgnore
    private PurchaseCart purchaseCart;

    @OneToOne
    @JoinColumn(name = "destination_address_id")
    private DestinationAddress destinationAddress;

    @Transient
    @JsonIgnore
    private Date purchaseDate;
</code></pre>

<p>It represent a purchase. PurchaseStatus is an enumerator. statusTransitions represents all the status this purchase got. In particular it can be 'READY_TO_BE_PAID' and 'PAID'. The status has it relative date, which is the VALUE of the map, and the status itself is the KEY of the map just because a purchase can be in a precise status only once.
I would like to get from the database all the Purchases with a specific User (username, which is an attribute of User) and with a specific (KEY, VALUE) pair inside the statusTransitions HashMap. 
In particular I would like to create a query which returns all the purchases where the Date (VALUE) is between two dates (fromDate and toDate) and the PurchaseStatus (KEY) is equal to the enum value 'READY_TO_BE_PAID'.</p>

<p>I created this custom query:</p>

<pre><code>@Query("select p from Purchase p JOIN p.customer c JOIN p.statusTransitions s WHERE c.username = :username and " +
            "(KEY(s) = 'READY_TO_BE_PAID' and " +
            "VALUE(s) &gt;= :fromDate and " +
            "VALUE(s) &lt;= :toDate)")
List&lt;Purchase&gt; findByUsernameAndByDate(@Param("fromDate") Date fromDate, @Param("toDate") Date toDate, @Param("username") String username);
</code></pre>

<p>The only problem is that the SQL query that generates is the following:</p>

<pre><code>select 
*
from 
  purchase purchase0_ 
    inner join user user1_ on purchase0_.customer_id=user1_.user_id 
    inner join purchase_status statustran2_ on purchase0_.purchase_id=statustran2_.purchase_purchase_id 
  where 
    statustran2_.status='READY_TO_BE_PAID' and 
    user1_.username=? and 
      (select 
        statustran2_.date 
      from 
        purchase_status statustran2_ 
      where 
        purchase0_.purchase_id=statustran2_.purchase_purchase_id
        )&gt;=? and 
      (select 
        statustran2_.date 
      from 
        purchase_status statustran2_ 
      where 
        purchase0_.purchase_id=statustran2_.purchase_purchase_id
      )&lt;=?
</code></pre>

<p>Which is not what I want. It generates two subqueries and the result is that it throws this error:</p>

<pre><code>java.sql.SQLException: Subquery returns more than 1 row
</code></pre>

<p>That's because when it executes the subquery it doesn't filter the rows on the PurchaseStatus, returning in that way more than one row.
The point is that I don't know how to rewrite the query in order to avoid these two subqueries or to put inside the WHERE clause this (KEY(s) = 'READY_TO_BE_PAID') condition. I found other people which have had the same issue but I couldn't find any solution.</p>

## Answers
### Answer ID: 55076505
<p>I found the solution! It seems that when you have this query</p>

<pre><code>SELECT p 
FROM Purchase p 
    JOIN p.customer c 
    JOIN p.statusTransitions s
</code></pre>

<p>the alias 's' of the statusTransactions Map, is already the value and not the pair (KEY, VALUE) which you are led to believe. It's a bit counter intuitive because KEY returns the key but VALUE does not return the value, but instead it generates automatically a subquery which inevitably leads you to errors.</p>

<pre><code>java.sql.SQLException: Subquery returns more than 1 row
</code></pre>

<p>So the correct way to rewrite this:</p>

<pre><code>SELECT p 
FROM Purchase p 
    JOIN p.customer c 
    JOIN p.statusTransitions s 
WHERE 
    c.username = :username and
    KEY(s) = 'READY_TO_BE_PAID' and
    VALUE(s) &gt;= :fromDate and
    VALUE(s) &lt;= :toDate
</code></pre>

<p>is:</p>

<pre><code>SELECT p 
FROM Purchase p 
    JOIN p.customer c 
    JOIN p.statusTransitions s 
WHERE 
    c.username = :username and
    KEY(s) = 'READY_TO_BE_PAID' and
    s &gt;= :fromDate and
    s &lt;= :toDate
</code></pre>

<p>or more compactly:</p>

<pre><code>SELECT p 
FROM Purchase p 
    JOIN p.customer c 
    JOIN p.statusTransitions s 
WHERE 
    c.username = :username and
    KEY(s) = 'READY_TO_BE_PAID' and
    s BETWEEN :fromDate and :toDate
</code></pre>

<p>where, as I already said, the alias 's' is already the value of the (key,value) pair!</p>

