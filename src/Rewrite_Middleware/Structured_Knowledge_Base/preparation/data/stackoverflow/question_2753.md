# Sorting on @Transient column in Spring Data Rest via PagingAndSortingRepository
[Link to question](https://stackoverflow.com/questions/51017267/sorting-on-transient-column-in-spring-data-rest-via-pagingandsortingrepository)
**Creation Date:** 1529907271
**Score:** 0
**Tags:** spring, spring-boot, spring-data-jpa, spring-data, spring-data-rest
## Question Body
<p>Our application uses PagingAndSortingRepository to serve our REST API. This works great, but we ran into a specific edge case that we can't seem to solve:
We have a alphanumeric field that has to be sortable (e.g. SOMETHING-123). One possible solution was to use something like a regex inside the database query's order by. This was ruled out, as we wanted to stay database independant. Thus we split up the column into two columns.</p>

<p>So before we had an Entity with 1 String field:</p>

<pre><code>@Entity
public class TestingEntity {
    @Id
    @GeneratedValue
    private long id;

    private String alphanumeric
}
</code></pre>

<p>And now we have an Entity with 2 additional fields and the old field made @Transient which is filled at @PostLoad:</p>

<pre><code>@Entity
public class Testing {
    @Id
    @GeneratedValue
    private long id;

    @Transient
    public String alphanumeric;

    @PostLoad
    public void postLoad(){
        this.alphanumeric = this.alphabetic + "-" + this.numeric;
    }

    public void setAlphanumeric(String alphanumeric) {
        int index = alphanumeric.indexOf("-");
        this.alphabetic = alphanumeric.substring(0, index);
        this.numeric = Long.parseLong(alphanumeric.substring(index + 1));
    }

    @JsonIgnore
    private String alphabetic;

    @JsonIgnore
    private Long numeric;

}
</code></pre>

<p>This is working great and the additional fields do not get exposed. However the sorting on the field "alphanumeric" does obviously not work anymore. The simplest solution would be to make this request:</p>

<pre><code>localhost:8080/api/testingEntity?sort=alphanumeric,asc
</code></pre>

<p>and internally rewrite it to the working request:</p>

<pre><code>localhost:8080/api/testingEntity?sort=alphabetic,asc&amp;sort=numeric,asc
</code></pre>

<p>What is the best way to tackle this issue?</p>

