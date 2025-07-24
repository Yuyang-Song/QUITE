# Rewrite JPQL-query with spring-data query from method names
[Link to question](https://stackoverflow.com/questions/69439639/rewrite-jpql-query-with-spring-data-query-from-method-names)
**Creation Date:** 1633366015
**Score:** 0
**Tags:** java, spring, spring-boot, hibernate, jpa
## Question Body
<p>I have two entities with many-to-many relationship:</p>
<pre><code>@Entity
@Table(name = &quot;author&quot;)
public class Author {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Column(name = &quot;author_name&quot;, unique = true)
    private String authorName;

    @ManyToMany // default FetchType.LAZY
    @JoinTable(name = &quot;author_book&quot;,
            joinColumns = @JoinColumn(name = &quot;author_id&quot;),
            inverseJoinColumns = @JoinColumn(name = &quot;book_id&quot;))
    private Set&lt;Book&gt; books;

    // other fields, getters, setters
}
</code></pre>
<p>and</p>
<pre><code>@Entity
@Table(name = &quot;book&quot;)
public class Book {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private long id;

    @Column(name = &quot;title&quot;, unique = true)
    private String title;
  
    // other fields, getters, setters
}
</code></pre>
<p>Let's say, that we have in the database 1 author with author_name '<em>Stephen King</em>' with related 3 books with titles '<em>book-title-1</em>', '<em>book-title-2</em>', '<em>book-title-3</em>'.</p>
<p>I need to get author by name with his books with a certain titles, e.g.:</p>
<blockquote>
<p>find an author named 'Stephen King' with books named 'book-title-1' or 'book-title-2'</p>
</blockquote>
<p>With following query as below, it works, namely I'm getting an author with a set of <strong>two</strong> Book-elements.</p>
<pre><code>public interface AuthorRepository extends JpaRepository&lt;Author, Long&gt; {

    @Query(&quot;select a from Author a join fetch a.books b &quot; +
            &quot;where a.authorName=:authorName and b.title in :titles&quot;)
    Optional&lt;Author&gt; findByNameAndBookTitles(String authorName, Set&lt;String&gt; titles);
}
</code></pre>
<p>Hibernate query for method above (simplified):</p>
<pre><code> select author.id, book.id, author.author_name, book.title, author_book.author_id, author_book.book_id
    from public.author
    inner join public.author_book on author.id= author_book.author_id 
    inner join public.book on author_book.book_id=book.id 
    where author.author_name=? and (book.title in (? , ?))
</code></pre>
<p>Question: <strong>Is there a way to rewrite it with query from method names?</strong></p>
<p>I tried smth like this:</p>
<pre><code>Optional&lt;Author&gt; findByAuthorNameAndBooks_titleIn(String authorName, Set&lt;String&gt; titles);
</code></pre>
<p>but it returns author and <strong>all</strong> related books instead of two books, so hibernate makes two following queries (second hibernate query is made when the <code>Set&lt;Book&gt; books</code> is accessed for the first time):</p>
<pre><code>Hibernate:
select author.id , author.author_name
from public.author
left outer join public.author_book on author.id = author_book.author_id 
left outer join public.book on author_book.book_id= book.id 
where author_name=? and (book.title in (? , ?))

Hibernate: 
select author_book.author_id, author_book.book_id, book.id, book.title 
from public.author_book
inner join public.book on author_book.book_id=book.id 
where author_book.author_id=?
</code></pre>
<p>I suggested that probably it would work with <code>@ManyToMany(fetch = FetchType.EAGER)</code>, but hibernate again made two queries like above, with the only difference that the second query is made before the first call to the set of books.</p>
<p>If you need any clarification, let me know and thanks in advance.</p>

## Answers
### Answer ID: 69566574
<p>I wouldn't recommend you to use the method name convention as that is only a tool for quick prototyping AFAIU. As soon as the requirements change you might have to switch back to a query and then you will have fun to decipher what this method name convention really means.</p>
<p>But even your JPQL/HQL query isn't really safe as you are returning managed entities with filtered collections. A simple change to the collection could lead to deletion of all filtered out books. I would recommend you use DTOs instead to avoid all of the issues.</p>
<p>I think this is a perfect use case for <a href="https://github.com/Blazebit/blaze-persistence#entity-view-usage" rel="nofollow noreferrer">Blaze-Persistence Entity Views</a>.</p>
<p>I created the library to allow easy mapping between JPA models and custom interface or abstract class defined models, something like Spring Data Projections on steroids. The idea is that you define your target structure(domain model) the way you like and map attributes(getters) via JPQL expressions to the entity model.</p>
<p>A DTO model for your use case could look like the following with Blaze-Persistence Entity-Views:</p>
<pre><code>@EntityView(Author.class)
public interface AuthorDto {
    @IdMapping
    Long getId();
    String getAuthorName();
    Set&lt;BookDto&gt; getBooks();

    @EntityView(Book.class)
    interface BookDto {
        @IdMapping
        Long getId();
        String getTitle();
    }
}
</code></pre>
<p>Querying is a matter of applying the entity view to a query, the simplest being just a query by id.</p>
<p><code>AuthorDto a = entityViewManager.find(entityManager, AuthorDto.class, id);</code></p>
<p>The Spring Data integration allows you to use it almost like Spring Data Projections: <a href="https://persistence.blazebit.com/documentation/entity-view/manual/en_US/index.html#spring-data-features" rel="nofollow noreferrer">https://persistence.blazebit.com/documentation/entity-view/manual/en_US/index.html#spring-data-features</a></p>
<pre><code>Page&lt;AuthorDto&gt; findAll(Pageable pageable);
</code></pre>
<p>The best part is, it will only fetch the state that is actually necessary!</p>
<p>In your particular case, you could use this:</p>
<pre><code>Optional&lt;AuthorDto&gt; findByAuthorNameAndBooks_titleIn(String authorName, Set&lt;String&gt; titles) {
    return findOne((root, query, cb) -&gt; {
        return cb.and(
            cb.equal(root.get(&quot;name&quot;), authorName),
            root.get(&quot;books&quot;).get(&quot;title&quot;).in(titles)
         );
    });
}
</code></pre>

