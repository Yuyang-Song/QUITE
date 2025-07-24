# CriteriaBuilder left join unrelated entities
[Link to question](https://stackoverflow.com/questions/75569127/criteriabuilder-left-join-unrelated-entities)
**Creation Date:** 1677368330
**Score:** 1
**Tags:** java, spring-data-jpa, jpql
## Question Body
<p>This is my database schema:</p>
<ul>
<li>The <code>title</code> and <code>content</code> columns have a 1 to 1 relationship with the <code>translations_keys</code></li>
<li>There are many <code>translations_values</code> for each <code>translations_keys</code></li>
</ul>
<p><a href="https://i.sstatic.net/pVMr0.png" rel="nofollow noreferrer"><img src="https://i.sstatic.net/pVMr0.png" alt="Database Schema" /></a></p>
<p>I'm trying to read posts with related fields translated according to the requested language. This the working query written in JPQL</p>
<pre><code>@Query(value = &quot;&quot;&quot;
    SELECT i AS template,
           tv_n.value AS title,
           tv_d.value AS content
      FROM Post i
 LEFT JOIN TranslationValue tv_n
        ON tv_n.key = i.title
       AND tv_n.languageIdentifier = ?1
 LEFT JOIN TranslationValue tv_d
        ON tv_d.key = i.content
       AND tv_d.languageIdentifier = ?1
&quot;&quot;&quot;)
public Page&lt;PostView&gt; findAll(int languageIdentifier);
</code></pre>
<p>I need to rewrite this query using the CriteriaBuilder. This is what I tried but it doesn't work...</p>
<pre><code>CriteriaBuilder criteriaBuilder = entityManager.getCriteriaBuilder();
CriteriaQuery&lt;PostView&gt; query = criteriaBuilder.createQuery(PostView.class);
Root&lt;Post&gt; root = query.from(Post.class);

Root&lt;TranslationValue&gt; translation = query.from(TranslationValue.class);
root.join(&quot;title&quot;, JoinType.LEFT).on(
    criteriaBuilder.equal(translation.get(&quot;key&quot;), root.get(&quot;title&quot;)),
    criteriaBuilder.equal(translation.get(&quot;languageIdentifier&quot;), 3)
);
root.join(&quot;title&quot;, JoinType.LEFT).on(
    criteriaBuilder.equal(translation.get(&quot;key&quot;), root.get(&quot;content&quot;)),
    criteriaBuilder.equal(translation.get(&quot;languageIdentifier&quot;), 3)
);
</code></pre>
<p>The problem is that the post entity has no direct relationship with the TranslationValue entity so I don't know how to perform the left join</p>
<p>This is my mapped Post entity</p>
<pre><code>@Entity
@Data
@Table(title = &quot;posts&quot;)
@NamedQuery(title = &quot;Post.findAll&quot;, query = &quot;SELECT i FROM Post i&quot;)
public class Post implements Serializable {

    private static final long serialVersionUID = 1L;

    @Column(title = &quot;identifier&quot;)
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Integer identifier;

    @Column(title = &quot;title&quot;, insertable = false, updatable = false)
    private Integer titleIdentifier;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(title = &quot;title&quot;)
    public TranslationKey title;

    @Column(title = &quot;content&quot;, insertable = false, updatable = false)
    private Integer contentIdentifier;

    @OneToOne(fetch = FetchType.LAZY)
    @JoinColumn(title = &quot;content&quot;)
    private TranslationKey content;

    // Getter &amp; Setter

}
</code></pre>

