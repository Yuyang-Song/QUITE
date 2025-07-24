# Scala - calling a method with generic type parameter given a string value that determines the correct type
[Link to question](https://stackoverflow.com/questions/25500719/scala-calling-a-method-with-generic-type-parameter-given-a-string-value-that-d)
**Creation Date:** 1409039708
**Score:** 3
**Tags:** scala, generics
## Question Body
<p>I am designing an API interface in a 2-tier architecture. It takes a string parameter fieldName from URL and returns a JSON string. fieldName refers to a field in my database table. You can think of its signature as:</p>

<pre><code>def controller(fieldName: String): String
</code></pre>

<p>In the controller, I would like to call a method in my data access layer to perform the following query:</p>

<pre><code>SELECT fieldName, SUM(salary) FROM Employee GROUP BY fieldName
</code></pre>

<p>because the type of the field varies, the type of the query result will be different. This method is parametrized by a generic type parameter T which corresponds to the type of the field with name fieldName.</p>

<pre><code>def getTotalSalaryByField[T](fieldName: String): Map[T, Long]
</code></pre>

<ul>
<li>if fieldName is "age", T should be Int.</li>
<li>if fieldName is "name", T should be String.
and so on.</li>
</ul>

<p>given a particular fieldName at runtime, how do I call this method giving it the correct type?</p>

<p>I don't want to write a lot of if-else or pattern matching statements to select the type. It would look like this:</p>

<pre><code>fieldName match {
    case "age" =&gt; serializeToJson(getTotalSalaryByField[Int]("age"))
    case "name" =&gt; serializeToJson(getTotalSalaryByField[String]("name"))
    ...
    // 100 more for 100 more fields
}
</code></pre>

<p>This is ugly. If I were to write this in Python, it will take only one line:</p>

<pre><code>json.dumps(getTotalSalaryByField(fieldName))
</code></pre>

<p>Is Scala somehow not suitable for rest backend programming? because this seems to be a common pattern people will encounter, and static typing gets in the way. I would like to see some suggestions as to how I should approach the whole problem in scala-ish way, even if it means remodeling, rewriting the DAL and controllers.</p>

<p><strong>EDIT</strong>:
@drexin, the actual signature of the DAL method is</p>

<pre><code>def myDAOMethod[T](tf: Option[TimeFilter], cf: CrossFilter)
    (implicit attr: XFAttribute[T]): Map[T, Long]
</code></pre>

<p>T is the type of fieldName. Long is the type of y. As you can see, I need to select a type to be T based on fieldName from url parameter.</p>

<p><strong>EDIT</strong>:
added some code and made the usecase clear</p>

## Answers
### Answer ID: 25586117
<p>If you are using Play framework then I would recommend you to use Play JSON APIs.</p>

<p><a href="https://www.playframework.com/documentation/2.1.1/ScalaJson" rel="nofollow">https://www.playframework.com/documentation/2.1.1/ScalaJson</a></p>

<p>Instead of</p>

<pre><code>def getTotalSalaryByField[T](fieldName: String): Map[T, Long] = ???
</code></pre>

<p>you can write </p>

<pre><code>def getTotalSalaryByField(fieldName: String): Map[JsValue, Long] = ???
</code></pre>

<p>since all types like <code>JsNumber</code>, <code>JsString</code>, <code>JsNull</code> are inherit from the generic JSON trait, <code>JsValue</code>.</p>

<p>wrap your queryResult with <code>Json.toJson()</code></p>

<p><strong>OR</strong></p>

<pre><code>def getTotalSalaryByField(fieldName: String): JsObject = ???
</code></pre>

### Answer ID: 25583558
<p>I think you have three options here:</p>

<ul>
<li>use pattern matching (which is something you wanted to avoid)</li>
<li>use AnyRef and then try to guess proper type at runtime; maybe serializeToJson can do it itself?</li>
<li>use Type Providers: <a href="http://docs.scala-lang.org/overviews/macros/typeproviders.html" rel="nofollow">http://docs.scala-lang.org/overviews/macros/typeproviders.html</a></li>
</ul>

<p>Third option is probably what you are looking for, but it bases on experimental scala features (i.e. macros). What I imagine it would be doing is connecting to your database during the compilation phase and inspecting the schema. If you are generating schema using some separate sql file(s) then it should be even easier. Then macro will generate all boilerplate with proper types hard-coded.</p>

<p>Probably you won't find working example for exactly what you need but there is one for RFC files which you can use as inspiration: <a href="https://github.com/travisbrown/type-provider-examples" rel="nofollow">https://github.com/travisbrown/type-provider-examples</a></p>

### Answer ID: 25546230
<p>There is a difference between knowing the type of a variable at compile time and at runtime.</p>

<p>If the <code>fieldName</code> is not known at compile time (i.e. it's a parameter), and if the type of the column varies by <code>fieldName</code>, then you are not going to be able to specify the return type of the method at compile time.</p>

<p>You will need to use a DAO method that returns <code>AnyRef</code>, rather than one which returns <code>T</code> for a compile-time-specified type <code>T</code>.</p>

<h3>Old answer:</h3>

<p>The database access library can return the values without needing to know their type, and your code needs to do the same.</p>

<p>You are looking to use a DAO method which takes a type param <code>T</code>:</p>

<pre><code>def myDAOMethod[T](tf: Option[TimeFilter], cf: CrossFilter)
    (implicit attr: XFAttribute[T]): Map[T, Long]
</code></pre>

<p>... but as you state, you don't know the type <code>T</code> in advance, so this method is inapplicable. (<code>T</code> is used to convert the database column data into a String or an Int).</p>

<p>Your DAO should offer an untyped version of this method, something more like:</p>

<pre><code>def doSelect(tf: Option[TimeFilter], cf: CrossFilter): Map[AnyRef, Long]
</code></pre>

<p>What database access library are you using?</p>

### Answer ID: 25502756
<p>I'm not 100% sure I understand your question, so apologies if I'm answering something else entirely.</p>

<p>You need Scala to be able to guess the type of your field based on the expected return type. That is, in the following code:</p>

<pre><code>val result : Map[String, Long] = myDAOMethod(tf, cf)
</code></pre>

<p>You expect Scala to correctly infer that since you want a <code>Map[String, Long]</code>, your <code>x</code> variable is of type <code>T</code>.</p>

<p>It seems to me that you already have everything you need for that. I do not know what <code>XFAttribute[T]</code> is, but I suspect it allows you to transform entries in a result set to instances of type <code>T</code>.</p>

<p>What's more, you've already declared it as a implicit parameter.</p>

<p>Provided you have an implicit <code>XFAttribute[String]</code> in scope, then, the previous code should compile, run, and be type-safe.</p>

<p>As a small improvement, I'd change the signature of your method to use context bounds, but that's primarily a matter of taste:</p>

<pre><code>// Declare the implicit "parsers"
implicit val IntAttribute: XFAttribute[Int] = ???
implicit val StringAttribute: XFAttribute[String] = ???

// Empty implementation, fill it with your actual code.
def myDAOMethod[T: XFAttribute](tf: Option[TimeFilter], cf: CrossFilter): Map[T, Long] = ???

// Scala will look for an implicit XFAttribute[Int] in scope, and find IntAttribute.
val ages: Map[Int, Long] = myDAOMethod(tf, cf)

// Scala will look for an implicit XFAttribute[String] in scope, and find StringAttribute.
val names: Map[String, Long] = myDAOMethod(tf, cf)
</code></pre>

<p>I'm not sure whether your question implies that you'd also like to strongly tie the String <code>"age"</code> to the type <code>Int</code>. That's also possible, of course, but it's another answer entirely and I don't want to pollute this question with unnecessary rambling.</p>

