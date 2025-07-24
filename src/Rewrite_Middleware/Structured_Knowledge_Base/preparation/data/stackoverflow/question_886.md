# Read javax annotations with custom doclet
[Link to question](https://stackoverflow.com/questions/48263894/read-javax-annotations-with-custom-doclet)
**Creation Date:** 1516022649
**Score:** 0
**Tags:** java, javadoc, javax, doclet
## Question Body
<p>I got a bunch of DTO's which are not commented at all. However, there are comments in the SQL-Database. I can get these comments by sending a query and then retrieving the ResultSet.</p>

<p>My task is to create a javadoc-API (as HTML) with the comments from the SQL-Database in order to make the codebase better understandable.</p>

<p>After asking about this task already <a href="https://stackoverflow.com/questions/48204100/can-i-generate-javadoc-comments-with-the-help-of-a-custom-doclet">HERE</a>, I tried to looked into creating my own doclet. I then wrote my own doclet by rewriting the Standard-, Abstract- and HtmlDoclet from Java.Tools. My results are working fine and I can create javadoc html pages WITH the comments from the database.</p>

<p>HOWEVER its a massive hack imho. There are two main tasks that need to be done in order to get the Database comments. </p>

<ol>
<li>know the table name</li>
<li>know the column name</li>
</ol>

<p><strong>How it should be done:</strong> <em>(which is what I want to ask - How do I implement it like this?)</em></p>

<p>For 1. : Find the @Table annotation. Read name = "tablename".</p>

<p>For 2. : For each variable: </p>

<p>Is there a @Column annotation ? return "columnName" : return ""</p>

<p><strong>How I do it right now:</strong></p>

<p>For 1. : I read the RootDoc.name() variable and then read the String char by char. Find a capital letter. Insert '_'. And at the end, turn everything .toUpperCase(). So "testFile" turns into "TEST_FILE".</p>

<p>This sometimes does not work. If you read carefully in the example class. Its name is "SaklTAdrkla" but the Databasetable name is SAKL_T_ADRKLAS. Parsing the name from RootDoc.name() would result in "SAKL_T_ADRKLA" which is missing the character 'S' at the end, therefore it wont find the table in the database.</p>

<p>For 2. : I get all Fields from the ClassDoc. I then parse Field.name() the same way I parsed the RootDoc.name() variable.</p>

<p>This wont work for the same reason as 1.; but also because some fieldnames are not the same as their mapped names. In the example Class - field sakgTAklgrpAklAkgid is mapped in the database as AKL_AKGID</p>

<hr>

<p>I am able to find the Annotation itselfe by calling FieldDoc.annotations(). But thats ONLY the annotation without the String (name = "xyz") which is the most important part for me!</p>

<p>I have found the Jax-Doclet, which can parse the javax annotations. However after downloading the jar-source file and implementing the java files, there are numerous dependency issues which are not resolvable because the referenced classes no longer exist in java 8 tools.jar. </p>

<p><strong>Is there another solution, that is capable of reading the javax annotations?</strong></p>

<p><strong>Can I implement something into my doclet so it can read the javax annotations?</strong></p>

<hr>

<p>Edit:</p>

<p>I found out you can call .elementValues() on the AnnotationDesc class which I can get from FieldDoc.annotations(). However I always get a com.sun.jdi.ClassNotLoadedException Type has not been loaded occurred while retrieving component type of array. To fix it I manually load the classes AnnotationDesc and AnnotationDesc.ElementValuePair by calling Class.forName(). However now the Array with the elementValuePairs is empty..?</p>

<p>Example class:</p>

<pre><code>    /**
 * The persistent class for the SAKL_T_ADRKLAS database table.
 */
@Entity
@IdClass(SaklTAdrklaPK.class)
@Table(name = "SAKL_T_ADRKLAS")
@NamedQuery(name = "SaklTAdrkla.findAll", query = "SELECT s FROM SaklTAdrkla s")
public class SaklTAdrkla implements Serializable, IModelEntity {
   private static final long serialVersionUID = 1L;

   @Id @Column(name = "AKL_AKLID") private String aklAklid;

   @Id
   // uni-directional many-to-one association to SakgTAklgrp
   @JsonBackReference(value = "sakgTAklgrpAklAkgid") @ManyToOne @JoinColumn(name = "AKL_AKGID") private SakgTAklgrp sakgTAklgrpAklAkgid;

   @Temporal(TemporalType.TIMESTAMP) @Column(name = "AKL_AEND") private Date aklAend;

   @Column(name = "AKL_DEFLT") private BigDecimal aklDeflt;

   @Column(name = "AKL_SPERRE") private BigDecimal aklSperre;

   @Column(name = "AKL_T_BEZ") private String aklTBez;

   @Column(name = "AKL_USRID") private String aklUsrid;

   public SaklTAdrkla() {
   }
</code></pre>

## Answers
### Answer ID: 48296660
<p>It took me quite a while to figure this out now, but I finnally did.</p>

<p>The Problem was that my doclet could find all the annotations, which it displayed in the console as errors. </p>

<blockquote>
  <p>error: cannot find symbol    @Column(name = "TST_USER") private
  String tstUser;</p>
</blockquote>

<p>What I also found was this message in the lot of errors that got thrown:</p>

<blockquote>
  <p>error: package javax.persistence does not exist import
  javax.persistence.*;</p>
</blockquote>

<p>So I imported javax.persistance.jar into my project.
I also added com.fasterxml.jaxkson.annotations.jar into the project since it would also not work without it.</p>

<p>Surprise Surprise! IT WORKS!</p>

<p>I can get all the annotations and annotation values by using annotation.elementValues().
 I no longer get an empty Array nor do I get an ClassNotLoadedException.</p>

