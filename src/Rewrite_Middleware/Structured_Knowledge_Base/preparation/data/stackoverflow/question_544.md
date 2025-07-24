# How to insert value of UUID?
[Link to question](https://stackoverflow.com/questions/30985604/how-to-insert-value-of-uuid)
**Creation Date:** 1434992000
**Score:** 7
**Tags:** postgresql, scala, playframework, anorm
## Question Body
<p>I'm using anorm 2.4 in play framework 2.3 backed postgresql 9.4</p>

<p>Give a model like this:</p>

<pre><code>case class EmailQueue(id:UUID,
                  send_from:String,
                  send_to:String,
                  subject:String,
                  body:String,
                  created_date:Date,
                  is_sent:Boolean,
                   email_template:String)
</code></pre>

<p>This is my parser:</p>

<pre><code>val parser: RowParser[EmailQueue] = {
get[UUID]("id") ~
  get[String]("send_from") ~
  get[String]("send_to") ~
  get[String]("subject") ~
  get[String]("body") ~
  get[Date]("created_date") ~
  get[Boolean]("is_sent") ~
  get[String]("email_template") map {
  case id ~ send_from ~ send_to ~ subject ~ body ~
    created_date ~ is_sent ~ email_template=&gt; EmailQueue(id,
    send_from,
    send_to,
    subject,
    body,
    created_date,
    is_sent,
    email_template)
}
</code></pre>

<p>}</p>

<p>And this is my insert statement:</p>

<pre><code>def insert(email:EmailQueue): Unit ={
DB.withTransaction { implicit c =&gt;
  SQL(s"""
        INSERT INTO "email_queue" ( "body", "created_date", "id", "is_sent", "send_from", "send_to", "subject", "email_template")
        VALUES ( {body}, {created_date}, {id}, {is_sent}, {send_from}, {send_to}, {subject}, {email_template} );
      """).on(
      "body" -&gt; email.body,
      "created_date" -&gt; email.created_date,
      "id" -&gt; email.id,
      "is_sent" -&gt; email.is_sent,
      "send_from" -&gt; email.send_from,
      "send_to" -&gt; email.send_to,
      "subject" -&gt; email.subject,
      "email_template" -&gt; email.email_template
    ).executeInsert()
}
</code></pre>

<p>}</p>

<p>I receive following error when inserting:</p>

<blockquote>
  <p>[error]    PSQLException: : ERROR: column "id" is of type uuid but
  expression is  of type character varying [error]   Hint: You will need
  to rewrite or cast the expression. [error]   Position: 153 
  (xxxxxxxxxx.java:2270)</p>
</blockquote>

<p>The database table is created by this query:</p>

<pre><code>CREATE TABLE email_queue (
   id UUID PRIMARY KEY,
   send_from VARCHAR(255) NOT NULL,
   send_to VARCHAR(255) NOT NULL,
   subject VARCHAR(2000) NOT NULL,
   body text NOT NULL,
   created_date timestamp without time zone DEFAULT now(),
   is_sent BOOLEAN NOT NULL DEFAULT FALSE,
   email_template VARCHAR(2000) NOT NULL
);
</code></pre>

## Answers
### Answer ID: 30997029
<p>Anorm is DB agnostic, as JDBC, so vendor specific datatype are not supported by default.</p>

<p>You can use <code>{id}::uuid</code> in the statement, so that the <code>java.util.UUID</code> passed as String in JDBC parameters is then converted from passed <code>VARCHAR</code> to a specific PostgreSQL <code>uuid</code>.</p>

<blockquote>
  <p>Using string interpolation in <code>SQL(s"...")</code> is not recommanded (SQL injection), but Anorm interpolation can be used.</p>
</blockquote>

<pre><code>def insert(email:EmailQueue): Unit = DB.withTransaction { implicit c =&gt;
  SQL"""
    INSERT INTO "email_queue" ( "body", "created_date", "id", "is_sent", "send_from", "send_to", "subject", "email_template")
    VALUES ( ${email.body}, ${email.created_date}, ${email.id}::uuid, ${email.is_sent}, ${email.send_from}, ${email.send_to}, ${email.subject}, ${email.email_template} )
  """).executeInsert()
}
</code></pre>

<blockquote>
  <p>Not recommended, but can be useful sometimes for vendor specific type, the <code>anorm.Object</code> can be used to pass an opaque value as JDBC parameter (there the <code>::uuid</code> is nicer for me).</p>
  
  <p>You can also implement a custom <code>ToStatement[java.util.UUID]</code>.</p>
</blockquote>

