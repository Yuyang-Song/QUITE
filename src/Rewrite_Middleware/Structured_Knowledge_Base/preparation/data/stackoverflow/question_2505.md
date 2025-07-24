# unexpected error error_class=Errno::EADDRINUSE error=&quot;Address already in use - bind(2) for \&quot;0.0.0.0\&quot; port 24233&quot;
[Link to question](https://stackoverflow.com/questions/37719112/unexpected-error-error-class-errnoeaddrinuse-error-address-already-in-use-b)
**Creation Date:** 1465456258
**Score:** 1
**Tags:** mysql, elasticsearch, kibana, fluentd
## Question Body
<p>I am working ion Fluentd + ElasticSearch + Kibana  I need to push mysql data to td-agent.log using stdout.  while i start td-agent it show some error in td-agent log.</p>

<p>This is my error:</p>

<pre><code>2016-06-09 12:21:36 +0530 [info]: Worker 0 finished unexpectedly with status 1
2016-06-09 12:21:37 +0530 [info]: reading config file path="/etc/td-agent/td-agent.conf"
2016-06-09 12:21:37 +0530 [info]: starting fluentd-0.14.0 without supervision
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-mixin-config-placeholders' version '0.4.0'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-mixin-config-placeholders' version '0.3.1'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-mixin-plaintextformatter' version '0.2.6'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-elasticsearch' version '1.5.0'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-grok-parser' version '0.3.1'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-mongo' version '0.7.13'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-mongo' version '0.7.12'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-mysql' version '0.1.3'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-mysql-query' version '0.3.0'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-mysql-replicator' version '0.5.2'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-rewrite-tag-filter' version '1.5.5'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-s3' version '0.6.8'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-s3' version '0.6.5'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-scribe' version '0.10.14'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-secure-forward' version '0.4.1'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-snmp' version '0.0.8'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-tail-ex' version '0.1.1'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-td' version '0.10.28'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-td-monitoring' version '0.2.2'
2016-06-09 12:21:37 +0530 [info]: gem 'fluent-plugin-webhdfs' version '0.4.1'
2016-06-09 12:21:37 +0530 [info]: gem 'fluentd' version '0.14.0'
2016-06-09 12:21:37 +0530 [info]: gem 'fluentd' version '0.12.20'
2016-06-09 12:21:37 +0530 [warn]: 'type' is deprecated parameter name. use '@type' instead.
2016-06-09 12:21:37 +0530 [info]: adding match pattern="replicator.*" type="stdout"
2016-06-09 12:21:37 +0530 [warn]: 'type' is deprecated parameter name. use '@type' instead.
2016-06-09 12:21:37 +0530 [info]: adding source type="forward"
2016-06-09 12:21:37 +0530 [warn]: 'type' is deprecated parameter name. use '@type' instead.
2016-06-09 12:21:37 +0530 [info]: adding source type="http"
2016-06-09 12:21:37 +0530 [warn]: 'type' is deprecated parameter name. use '@type' instead.
2016-06-09 12:21:37 +0530 [info]: adding source type="debug_agent"
2016-06-09 12:21:37 +0530 [warn]: 'type' is deprecated parameter name. use '@type' instead.
2016-06-09 12:21:37 +0530 [info]: adding source type="mysql_replicator"
2016-06-09 12:21:37 +0530 [info]: adding mysql_replicator worker. :tag=&gt;replicator.livechat.chat_chennaibox.${event}.${primary_key} :query=&gt;SELECT chat_name FROM chat_chennaibox; :prepared_query=&gt; :interval=&gt;10sec :enable_delete=&gt;true
2016-06-09 12:21:37 +0530 [info]: using configuration file: &lt;ROOT&gt;
  &lt;source&gt;
    type forward
  &lt;/source&gt;
  &lt;source&gt;
    type http
    port 8888
  &lt;/source&gt;
  &lt;source&gt;
    type debug_agent
    bind "0.0.0.0"
    port 24233
  &lt;/source&gt;
  &lt;source&gt;
    type mysql_replicator
    host "localhost"
    username "root"
    password xxxxxx
    database "livechat"
    query "SELECT chat_name FROM chat_chennaibox;"
    primary_key "chat_id"
    interval "10s"
    enable_delete yes
    tag "replicator.livechat.chat_chennaibox.${event}.${primary_key}"
  &lt;/source&gt;
  &lt;match replicator.*&gt;
    type stdout
  &lt;/match&gt;
&lt;/ROOT&gt;
2016-06-09 12:21:37 +0530 [warn]: super was not called in #start: called it forcedly plugin=Fluent::MysqlReplicatorInput
2016-06-09 12:21:37 +0530 [info]: listening dRuby uri="druby://0.0.0.0:24233" object="Engine"
2016-06-09 12:21:37 +0530 [error]: unexpected error error_class=Errno::EADDRINUSE error="Address already in use - bind(2) for \"0.0.0.0\" port 24233"
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/2.1.0/drb/drb.rb:879:in `initialize'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/2.1.0/drb/drb.rb:879:in `open'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/2.1.0/drb/drb.rb:879:in `open_server'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/2.1.0/drb/drb.rb:764:in `block in open_server'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/2.1.0/drb/drb.rb:762:in `each'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/2.1.0/drb/drb.rb:762:in `open_server'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/2.1.0/drb/drb.rb:1373:in `initialize'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/plugin/in_debug_agent.rb:55:in `new'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/plugin/in_debug_agent.rb:55:in `start'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/compat/call_super_mixin.rb:42:in `start'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/root_agent.rb:138:in `block in start'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/root_agent.rb:127:in `block (2 levels) in lifecycle'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/root_agent.rb:126:in `each'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/root_agent.rb:126:in `block in lifecycle'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/root_agent.rb:113:in `each'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/root_agent.rb:113:in `lifecycle'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/root_agent.rb:137:in `start'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/engine.rb:211:in `start'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/engine.rb:175:in `run'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/supervisor.rb:580:in `run_engine'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/supervisor.rb:382:in `block in run_worker'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/supervisor.rb:509:in `call'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/supervisor.rb:509:in `main_process'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/supervisor.rb:378:in `run_worker'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/lib/fluent/command/fluentd.rb:266:in `&lt;top (required)&gt;'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/site_ruby/2.1.0/rubygems/core_ext/kernel_require.rb:69:in `require'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/site_ruby/2.1.0/rubygems/core_ext/kernel_require.rb:69:in `require'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/lib/ruby/gems/2.1.0/gems/fluentd-0.14.0/bin/fluentd:5:in `&lt;top (required)&gt;'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/bin/fluentd:23:in `load'
  2016-06-09 12:21:37 +0530 [error]: /opt/td-agent/embedded/bin/fluentd:23:in `&lt;top (required)&gt;'
  2016-06-09 12:21:37 +0530 [error]: /usr/sbin/td-agent:7:in `load'
  2016-06-09 12:21:37 +0530 [error]: /usr/sbin/td-agent:7:in `&lt;main&gt;'
2016-06-09 12:21:37 +0530 [error]: unexpected error error="Address already in use - bind(2) for \"0.0.0.0\" port 24233"
  2016-06-09 12:21:37 +0530 [error]: suppressed same stacktrace
</code></pre>

<p>This is My <strong>Configuration</strong> File: </p>

<pre><code> ####
## Output descriptions:
##

# Treasure Data (http://www.treasure-data.com/) provides cloud based data
# analytics platform, which easily stores and processes data from td-agent.
# FREE plan is also provided.
# @see http://docs.fluentd.org/articles/http-to-td
#
# This section matches events whose tag is td.DATABASE.TABLE
#&lt;match td.*.*&gt;
#  type tdlog
#  apikey YOUR_API_KEY

#  auto_create_table
#  buffer_type file
#  buffer_path /var/log/td-agent/buffer/td

#  &lt;secondary&gt;
#    type file
#    path /var/log/td-agent/failed_records
#  &lt;/secondary&gt;
#&lt;/match&gt;

## match tag=debug.** and dump to console
#&lt;match debug.**&gt;
#  type stdout
#&lt;/match&gt;

####
## Source descriptions:
##

## built-in TCP input
## @see http://docs.fluentd.org/articles/in_forward
&lt;source&gt;
  type forward
&lt;/source&gt;

## built-in UNIX socket input
#&lt;source&gt;
#  type unix
#&lt;/source&gt;

# HTTP input
# POST http://localhost:8888/&lt;tag&gt;?json=&lt;json&gt;
# POST http://localhost:8888/td.myapp.login?json={"user"%3A"me"}
# @see http://docs.fluentd.org/articles/in_http
&lt;source&gt;
  type http
  port 8888
&lt;/source&gt;

## live debugging agent
&lt;source&gt;
  type debug_agent
  bind 0.0.0.0
  #port 24230
  port 24233
&lt;/source&gt;

####
## Examples:
##

## File input
## read apache logs continuously and tags td.apache.access
#&lt;source&gt;
#  type tail
#  format apache
#  path /var/log/httpdaccess.log
#  tag td.apache.access
#&lt;/source&gt;

## File output
## match tag=local.** and write to file
#&lt;match local.**&gt;
#  type file
#  path /var/log/td-agent/apache.log
#&lt;/match&gt;

## Forwarding
## match tag=system.** and forward to another td-agent server
#&lt;match system.**&gt;
#  type forward
#  host 192.168.0.11
#  # secondary host is optional
#  &lt;secondary&gt;
#    host 192.168.0.12
#  &lt;/secondary&gt;
#&lt;/match&gt;

## Multiple output
## match tag=td.*.* and output to Treasure Data AND file
#&lt;match td.*.*&gt;
#  type copy
#  &lt;store&gt;
#    type tdlog
#    apikey API_KEY
#    auto_create_table
#    buffer_type file
#    buffer_path /var/log/td-agent/buffer/td
#  &lt;/store&gt;
#  &lt;store&gt;
#    type file
#    path /var/log/td-agent/td-%Y-%m-%d/%H.log
#  &lt;/store&gt;
#&lt;/match&gt;
#&lt;source&gt;
#  @type tail
#  format apache
#  tag apache.access
#  path /var/log/td-agent/apache_log/ssl_access_log.1
#  read_from_head true
# pos_file /var/log/httpd/access_log.pos
#&lt;/source&gt;
#&lt;match apache.access*&gt;
#  type stdout
#&lt;/match&gt;

#&lt;source&gt;
#  @type tail
#  format magento_system 
#  tag magento.access
#  path /var/log/td-agent/Magento_log/system.log
#  pos_file /tmp/fluentd_magento_system.pos
#  read_from_head true 
#&lt;/source&gt;

#&lt;match apache.access
#  type stdout
#&lt;/match&gt;
#&lt;source&gt;
#  @type http
#  port 8080
#  bind localhost
#  body_size_limit 32m
#  keepalive_timeout 10s
#&lt;/source&gt;
#&lt;match magento.access*&gt;
# type stdout
#&lt;/match&gt;
#&lt;match magento.access*&gt;
#  @type elasticsearch
#  logstash_format true
#  host localhost
# port 9200
#&lt;/match&gt;
&lt;source&gt;
  type mysql_replicator
  host localhost
  username root
  password gworks.mobi2
  database livechat
  query SELECT chat_name FROM chat_chennaibox;
  #query SELECT t2.firstname,t2.lastname, t1.* FROM status t1 INNER JOIN student_detail t2 ON t1.number = t2.number;
  primary_key chat_id # specify unique key (default: id)
  interval 10s  # execute query interval (default: 1m)
  enable_delete yes
  tag replicator.livechat.chat_chennaibox.${event}.${primary_key}
&lt;/source&gt;
&lt;match replicator.*&gt;
type stdout
&lt;/match&gt;
</code></pre>

<p>Suggest me I am wrong? and How to solve this Problem?   </p>

## Answers
### Answer ID: 74353930
<p>on windows use <code>tasklist | find &quot;ruby&quot;</code>:</p>
<pre><code>c:\opt\td-agent&gt;tasklist | find &quot;ruby&quot;
ruby.exe                     24408 Services                   0     15,648 K
ruby.exe                     28888 Services                   0     68,612 K
c:\opt\td-agent&gt;taskkill /pid 24408 /f
SUCCESS: The process with PID 24408 has been terminated.
</code></pre>

### Answer ID: 37728489
<p>I solved my  problem. My problem is ruby running multiple PID's.</p>

<p>So, I find out Ruby running PID's  using this command:</p>

<pre><code>  ps aux | grep ruby 
</code></pre>

<p>above command show all ruby running port then, kill all the Process. Then Run td-agent. 
its working for me. </p>

### Answer ID: 37723131
<p>Subject of your post says the reason: Address already in use for port 24233.
Search the process which uses port 24233 by lsof command or something else, and then kill it.</p>

