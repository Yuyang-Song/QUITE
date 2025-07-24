# Postgresql - can&#39;t create a role
[Link to question](https://stackoverflow.com/questions/31203380/postgresql-cant-create-a-role)
**Creation Date:** 1435915952
**Score:** 0
**Tags:** ruby-on-rails, postgresql
## Question Body
<p>Hello i'm tryng to create a datbase in a ruby on rails application but i've got this error</p>

<pre><code>    FATAL:  role "giovanni" does not exist
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/postgresql_adapter.rb:661:in `rescue in connect'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/postgresql_adapter.rb:651:in `connect'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/postgresql_adapter.rb:242:in `initialize'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/postgresql_adapter.rb:44:in `new'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/postgresql_adapter.rb:44:in `postgresql_connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:436:in `new_connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:446:in `checkout_new_connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:422:in `acquire_connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:349:in `block in checkout'
/usr/lib/ruby/2.1.0/monitor.rb:211:in `mon_synchronize'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:348:in `checkout'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:263:in `block in connection'
/usr/lib/ruby/2.1.0/monitor.rb:211:in `mon_synchronize'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:262:in `connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:565:in `retrieve_connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_handling.rb:113:in `retrieve_connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_handling.rb:87:in `connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/postgresql_database_tasks.rb:8:in `connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/postgresql_database_tasks.rb:17:in `create'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/database_tasks.rb:93:in `create'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/database_tasks.rb:107:in `block in create_current'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/database_tasks.rb:275:in `block in each_current_configuration'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/database_tasks.rb:274:in `each'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/database_tasks.rb:274:in `each_current_configuration'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/database_tasks.rb:106:in `create_current'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/railties/databases.rake:17:in `block (2 levels) in &lt;top (required)&gt;'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:240:in `call'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:240:in `block in execute'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:235:in `each'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:235:in `execute'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:179:in `block in invoke_with_call_chain'
/usr/lib/ruby/2.1.0/monitor.rb:211:in `mon_synchronize'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:172:in `invoke_with_call_chain'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:165:in `invoke'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:150:in `invoke_task'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:106:in `block (2 levels) in top_level'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:106:in `each'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:106:in `block in top_level'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:115:in `run_with_threads'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:100:in `top_level'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:78:in `block in run'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:176:in `standard_exception_handling'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:75:in `run'
/var/lib/gems/2.1.0/gems/rake-10.4.2/bin/rake:33:in `&lt;top (required)&gt;'
/usr/local/bin/rake:23:in `load'
/usr/local/bin/rake:23:in `&lt;main&gt;'
Couldn't create database for {"adapter"=&gt;"postgresql", "encoding"=&gt;"unicode", "pool"=&gt;5, "database"=&gt;"app_angular_rails_development"}
FATAL:  role "giovanni" does not exist
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/postgresql_adapter.rb:661:in `rescue in connect'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/postgresql_adapter.rb:651:in `connect'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/postgresql_adapter.rb:242:in `initialize'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/postgresql_adapter.rb:44:in `new'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/postgresql_adapter.rb:44:in `postgresql_connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:436:in `new_connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:446:in `checkout_new_connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:422:in `acquire_connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:349:in `block in checkout'
/usr/lib/ruby/2.1.0/monitor.rb:211:in `mon_synchronize'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:348:in `checkout'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:263:in `block in connection'
/usr/lib/ruby/2.1.0/monitor.rb:211:in `mon_synchronize'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:262:in `connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_adapters/abstract/connection_pool.rb:565:in `retrieve_connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_handling.rb:113:in `retrieve_connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/connection_handling.rb:87:in `connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/postgresql_database_tasks.rb:8:in `connection'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/postgresql_database_tasks.rb:17:in `create'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/database_tasks.rb:93:in `create'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/database_tasks.rb:107:in `block in create_current'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/database_tasks.rb:275:in `block in each_current_configuration'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/database_tasks.rb:274:in `each'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/database_tasks.rb:274:in `each_current_configuration'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/tasks/database_tasks.rb:106:in `create_current'
/var/lib/gems/2.1.0/gems/activerecord-4.2.0/lib/active_record/railties/databases.rake:17:in `block (2 levels) in &lt;top (required)&gt;'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:240:in `call'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:240:in `block in execute'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:235:in `each'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:235:in `execute'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:179:in `block in invoke_with_call_chain'
/usr/lib/ruby/2.1.0/monitor.rb:211:in `mon_synchronize'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:172:in `invoke_with_call_chain'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/task.rb:165:in `invoke'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:150:in `invoke_task'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:106:in `block (2 levels) in top_level'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:106:in `each'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:106:in `block in top_level'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:115:in `run_with_threads'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:100:in `top_level'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:78:in `block in run'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:176:in `standard_exception_handling'
/var/lib/gems/2.1.0/gems/rake-10.4.2/lib/rake/application.rb:75:in `run'
/var/lib/gems/2.1.0/gems/rake-10.4.2/bin/rake:33:in `&lt;top (required)&gt;'
/usr/local/bin/rake:23:in `load'
/usr/local/bin/rake:23:in `&lt;main&gt;'
Couldn't create database for {"adapter"=&gt;"postgresql", "encoding"=&gt;"unicode", "pool"=&gt;5, "database"=&gt;"app_angular_rails_test"}
</code></pre>

<p>It seems that there isn't a role called "giovanni" in my local computer so i tried to create one by log in in the postgresql console and insert the query for create one user: </p>

<pre><code>sudo -u postgress -i
CREATE ROLE giovanni WITH PASSWORD 'password' CREATEDB LOGIN CREATEROLE CREATEUSER SUPERUSER;
</code></pre>

<p>but i recive this error: </p>

<blockquote>
  <p>ERROR:  conflicting or redundant options</p>
</blockquote>

<p>I tried to rewrite this query in some other ways following the official documentation of the database but it didn't worked</p>

## Answers
### Answer ID: 55035860
<p>It is because you are using CREATEUSER and CREATEROLE both. Chnage your query to <code>CREATE ROLE test WITH SUPERUSER LOGIN CREATEDB CREATEROLE ENCRYPTED PASSWORD 'password';</code></p>

### Answer ID: 31203881
<p>This is what i usually do to set up postgres,create DB and its role to be use in database.yml on ubuntu terminal</p>

<pre><code>add-apt-repository ppa:pitti/postgresql
##or use sudo apt-get install postgresql instead of repository
apt-get -y update
apt-get -y install postgresql libpq-dev
sudo -u postgres psql
# \password
# create user blog with password 'secret';
# create database blog_production owner blog;
# \q
</code></pre>

<p>use the above role in <code>database.yml</code></p>

<pre><code>development:
  adapter: postgresql
  encoding: unicode
  database: blog_production 
  pool: 5
  host: localhost
  username: blog
  password:secret
</code></pre>

<p>once its done,you just need to run <code>bundle exec rake db:setup</code>....and you will have all the tables in your db ready.</p>

### Answer ID: 31203709
<p>You can try to create a user with <a href="http://www.postgresql.org/docs/8.1/static/app-createuser.html" rel="nofollow"><code>createuser</code></a>  program, it has the same functionality as <a href="http://www.postgresql.org/docs/8.1/static/sql-createrole.html" rel="nofollow"><code>CREATE ROLE</code></a> (in fact, it calls this command) but can be run from the command shell.</p>

<pre><code>$ createuser giovanni
Shall the new role be a superuser? (y/n) y
Shall the new role be allowed to create databases? (y/n) y
Shall the new role be allowed to create more new roles? (y/n) y
CREATE USER
</code></pre>

<p>or with <code>command line</code> options:</p>

<pre><code>$ createuser -P -s -e giovanni
Enter password for new role: xyzzy
Enter it again: xyzzy
CREATE ROLE giovanni PASSWORD 'xyzzy' SUPERUSER CREATEDB CREATEROLE INHERIT LOGIN;
CREATE ROLE
</code></pre>

