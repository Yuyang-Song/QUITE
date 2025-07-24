# Rails 3 ActiveRecord save() Method and Autoincrement Primary Key Fields
[Link to question](https://stackoverflow.com/questions/16218133/rails-3-activerecord-save-method-and-autoincrement-primary-key-fields)
**Creation Date:** 1366901721
**Score:** 0
**Tags:** postgresql, activerecord, ruby-on-rails-3.1
## Question Body
<p>I migrated a Rails site that was running on 2.2.2 to Rails 3.1.</p>

<p>I noticed now, on Rails 3 the save() calls (INSERTS) that used to work in 2.2.2 don't in 3.1</p>

<p>The id field in the database is a primary key so it has the following properties:</p>

<p>not null <br />
auto-increment</p>

<p><img src="https://i.sstatic.net/sstWB.png" alt="enter image description here"></p>

<p>Now, when the save() method runs on these tables, I get:</p>

<pre><code>ActiveRecord::StatementInvalid (PG::Error: ERROR:  null value in column "id" violates not-null constraint
</code></pre>

<p>Hmm so I looked at the generated SQL that the save() creates and indeed it's including the id field in the column list and assigning it nil:</p>

<pre><code>   PG::Error: ERROR:  null value in column "id" violates not-null constraint
: INSERT INTO "server_updates" ("action", "created_at", "field_number", "id", "status", "table_number", "value") VALUES ($1, $2, $3, $4, $5, $6, $7) RETURNING "id"
</code></pre>

<p>So, my question is how do I get ActiveRecord to not include the id column when it generates the SQL from a save() call?</p>

<p>I certainly don't want to remove the NOT NULL rule from the column nor do I want to rewrite all of these save() calls with raw SQL queries.</p>

<p>Adding <code>set_primary_key "id"</code> to the models fixes this issue but seems really messy and un-rails/ruby to me</p>

<p>What do you all do to work around this?</p>

<p>Thanks for helping</p>

<p>Here is one of the models that is getting the error:</p>

<pre><code>class ServerUpdate &lt; ActiveRecord::Base



   def ServerUpdate.run_code code
     su = ServerUpdate.new
     su.action = 3 # run code
     su.value = code
     su.status = 1
     su.save
   end

   def ServerUpdate.new_insert_for_table table
      su = ServerUpdate.new
      su.action = 1  # Create New Record
      su.table_number = table.to_i
      su.save
      return su
   end



   def ServerUpdate.new_update_for_table_where_field_equals_value table, field, value
      su = ServerUpdate.new
      su.action = 2  # Update Record
      su.table_number = table.to_i
      su.field_number = field.to_i
      su.value = value.to_s
      su.status = 1 ## This used to be in process() method below
      su.save
      return su
   end

   def ServerUpdate.new_delete_for_table_where_field_equals_value table, field, value
      su = ServerUpdate.new
      su.action = 999  # Delete Record
      su.table_number = table.to_i
      su.field_number = field.to_i
      su.value = value.to_s
      su.save
      return su
   end

   def set_value_for_field value, field, behavior=0
      sui = ServerUpdateItem.new




      sui.server_update_id = self.id
      sui.field_number = field.to_i
      sui.value = value.to_s

      b = 0
      b = 1 if behavior == "prepend" or behavior == 1
      b = 2 if behavior == "append" or behavior == 2
      sui.behavior = b


      sui.save
   end

   def process
      We are now setting status=1 in method:  
      ServerUpdate.new_update_for_table_where_field_equals_value table, field, value
     self.status = 1
     self.save
   end

end
</code></pre>

## Answers
### Answer ID: 16238526
<p>Adding <code>set_primary_key "id"</code> to the models fixes this issue but seems really messy and unnecessary to me </p>

