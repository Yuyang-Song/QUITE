# Rewriting SQL to ActiveRecord
[Link to question](https://stackoverflow.com/questions/15368422/rewriting-sql-to-activerecord)
**Creation Date:** 1363110493
**Score:** 0
**Tags:** ruby-on-rails-3, activerecord, rails-activerecord
## Question Body
<p>I am trying to rewrite this old Rails 2 stuff such that it will work with Rails 3.2.1:</p>

<p><strong>Rails 2.2.2 query to rewrite</strong></p>

<pre><code> B2bPrivilege.find_by_sql("SELECT b2b_privileges.*, vendors.name AS vendor_name FROM b2b_privileges LEFT JOIN vendors ON vendors.id = b2b_privileges.vendor_id WHERE b2b_user_id = ?", current_user_id)
</code></pre>

<p>This is what I came up with and it creates the same SQL as seen in the Rails 2.2.2 example above but it doesn't bring in the vendors.name column into the stored result and I don't know why. The generated SQL when ran in the database console, does work so the issue is definitely related to Rails.</p>

<pre><code>    B2bPrivilege.select("b2b_privileges.*, vendors.name AS vendor_name").joins('LEFT JOIN  vendors ON vendors.id = b2b_privileges.vendor_id').where('b2b_user_id' =&gt; current_user_id)
</code></pre>

<p><strong>Debug info from .inspect</strong></p>

<pre><code>  B2bPrivilege Load (1.4ms)  SELECT b2b_privileges.*, vendors.name AS vendor_name FROM "b2b_privileges" LEFT JOIN vendors ON vendors.id = b2b_privileges.vendor_id WHERE "b2b_privileges"."b2b_user_id" = 398
[ 
    #&lt;B2bPrivilege id: 1363, b2b_user_id: 398, vendor_id: 53, can_setup_instant_electronic_delivery: true, can_setup_purchase_orders: true, can_setup_advance_ship_notification: true, can_setup_xml_pushes: true&gt;, 
    #&lt;B2bPrivilege id: 1923, b2b_user_id: 398, vendor_id: 103, can_setup_instant_electronic_delivery: false, can_setup_purchase_orders: false, can_setup_advance_ship_notification: true, can_setup_xml_pushes: true&gt;
]
</code></pre>

## Answers
### Answer ID: 15371597
<p>Do</p>

<pre><code>B2bPrivilege.joins('LEFT JOIN  vendors ON vendors.id = b2b_privileges.vendor_id').
  where(:b2bprivileges =&gt; {'b2b_user_id' =&gt; current_user_id} ).
  select("b2b_privileges.*, vendors.name AS 'vendor_name'").first.vendor_name
</code></pre>

### Answer ID: 15392619
<p>It turns out the joined content is there it just doesn't output to console, just the primary relation does. If you are viewing the output in your console window I think that the console output only reflects/inspects the root level object that is returned.</p>

<p>This was a gotcha for me when I was debugging my queries that use joins</p>

