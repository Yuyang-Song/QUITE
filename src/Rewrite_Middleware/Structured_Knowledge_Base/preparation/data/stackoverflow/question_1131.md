# Convert specific query into JPQL or Criteria Builder query
[Link to question](https://stackoverflow.com/questions/60382298/convert-specific-query-into-jpql-or-criteria-builder-query)
**Creation Date:** 1582570533
**Score:** 0
**Tags:** spring-data-jpa, jpql, hibernate-criteria
## Question Body
<p>Here is the code for 2 entities (it generates three tables in the database). A <code>Book</code> entity:</p>

<pre><code>@Entity
public class Book {
    @Id
    private long id;

    private String name;

    @ManyToMany
    private List&lt;Author&gt; authors;
}
</code></pre>

<p>An <code>Author</code> entity:</p>

<pre><code>@Entity
public class Author {
    @Id
    private long id;

    @Column(unique=true)
    private String name;
}
</code></pre>

<p>I'm trying to find books by the list of authors. Here is a sql query:</p>

<pre><code>select book.id, ARRAY_AGG(author.name)
from book 
join book_authors ba on book.id=ba.book_id 
join author on ba.authors_id=author.id
group by book.id
having  ARRAY_AGG(distinct author.name order by author.name)=ARRAY['a1', 'a2']::varchar[]
</code></pre>

<p><code>['a1', 'a2']</code> is a list of book authors, it must be passed as a parameter. The idea is to aggregate authors and then compare them with the list of passed parameters.</p>

<p>How to rewrite this SQL-query into either a JPQL or CriteriaBuilder query?</p>

## Answers
### Answer ID: 60394368
<p>If the exact match is necessary you can use <code>Specification</code> like this</p>

<pre><code>public class BookSpecifications {
        public static Specification&lt;Book&gt; byAuthorsNames(List&lt;String&gt; names) {
            return (root, query, builder) -&gt; {
                Join&lt;Book, Author&gt; author = root.join("authors", JoinType.LEFT);

                Predicate predicate = builder.conjunction;
                for(String name : names) {
                    Predicate namePredicate = builder.and(author.get("name"), name);
                    predicate = builder.and(predicate, namePredicate);
                }

                return predicate;
            }
        }
}
</code></pre>

<p><code>BookRepository</code> have to extend <code>JpaSpecificationExecutor</code>.</p>

<p>Usage:</p>

<pre><code>BookRepository repository;

public List&lt;Book&gt; findByAuthorsNames(List&lt;String&gt; names) {
    return repository.findAll(BookSpecifications.byAuthorsNames(names));
}
</code></pre>

### Answer ID: 60392813
<pre><code>@Query("select distinct b from Book b join b.authors a where a.name in(:names)")
List&lt;Book&gt; findByAuthorsNames(@Param("names") List&lt;String&gt; names)
</code></pre>

<p>If you want to fetch <code>b.authors</code> use <code>join fetch</code> instead of <code>join</code> </p>

