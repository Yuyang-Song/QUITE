# How do I write a finder when I have a belongs_to relationship but no underlying database column?
[Link to question](https://stackoverflow.com/questions/61964596/how-do-i-write-a-finder-when-i-have-a-belongs-to-relationship-but-no-underlying)
**Creation Date:** 1590185223
**Score:** 1
**Tags:** ruby-on-rails, ruby-on-rails-5, belongs-to
## Question Body
<p>I have a Rails 5 application and I'm having a problem writing a finder.  I have a PostGres 10 database.  I want to query all the invoices that belong to a particular business.  I have these models ...</p>

<pre><code>class Business &lt; ApplicationRecord
  belongs_to :owner, :optional =&gt; true

class Owner &lt; ApplicationRecord
  has_many :invoices, :through =&gt; :accountants
  has_one :business, :dependent =&gt; :nullify

class Accountant &lt; ApplicationRecord
  belongs_to :owner, :optional =&gt; false, :inverse_of =&gt; :accountants, :touch =&gt; true
  has_many :invoices, :dependent =&gt; :nullify
</code></pre>

<p>I would like to get all Invoices given a small business, so I tried this</p>

<pre><code>@invoices = Invoice.joins(:accountant =&gt; :owner).where(:owners =&gt; { :business_id =&gt; @business_id })
</code></pre>

<p>but this results in the below error</p>

<pre><code>ActiveRecord::StatementInvalid:
       PG::UndefinedColumn: ERROR:  column owners.business_id does not exist
       LINE 1: ...owners"."id" = "accountants"."owner_id" WHERE "owners"...
                                                                    ^
       : SELECT "invoices".* FROM "invoices" INNER JOIN "accountants" ON "accountants"."id" = "invoices"."accountant_id" INNER JOIN "owners" ON "owners"."id" = "accountants"."owner_id" WHERE "owners"."business_id" = $1 ORDER BY "invoices"."created_at" DESC
</code></pre>

<p>It is not an option to add an additional database column.  Is there a way I can rewrite the above query to satisfy my models?</p>

