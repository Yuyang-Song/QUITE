# Mautic cron setup issue
[Link to question](https://stackoverflow.com/questions/62233347/mautic-cron-setup-issue)
**Creation Date:** 1591454774
**Score:** 2
**Tags:** php, linux, cron, mautic
## Question Body
<p>I recently setup mautic and I also setup cron jobs for mautic but how should i check if they are working or what is the error if its not working?</p>

<p>Here is my cron.. of course I have multiple crons setup according to the docs. But they all look like this.</p>

<pre><code>/usr/bin/php /home/xyz/public_html/mautic/app/console mautic:messages:send &gt; /home/xyz/public_html/mautic/cron_logs/messages_send.log 2&gt;&amp;1
</code></pre>

<p>I also checked the logs but the logs look like this..</p>

<pre><code>Mautic version 2.16.0 - app/prod

Usage:
  command [options] [arguments]

Options:
  -h, --help               Display this help message
  -q, --quiet              Do not output any message
  -V, --version            Display this application version
      --ansi               Force ANSI output
      --no-ansi            Disable ANSI output
  -n, --no-interaction     Do not ask any interactive question
  -s, --shell              Launch the shell.
      --process-isolation  Launch commands from shell as a separate process.
  -e, --env=ENV            The Environment name. [default: "prod"]
      --no-debug           Switches off debug mode.
  -v|vv|vvv, --verbose     Increase the verbosity of messages: 1 for normal output, 2 for more verbose output and 3 for debug

Available commands:
  help                                    Displays help for a command
  list                                    Lists commands
 assets
  assets:install                          Installs bundles web assets under a public web directory
 bazinga
  bazinga:oauth-server:clean              Clean expired tokens
 cache
  cache:clear                             Clears the cache
  cache:warmup                            Warms up an empty cache
 config
  config:debug                            Dumps the current configuration for an extension
  config:dump-reference                   Dumps the default configuration for an extension
 container
  container:debug                         Displays current services for an application
 debug
  debug:config                            Dumps the current configuration for an extension
  debug:container                         Displays current services for an application
  debug:event-dispatcher                  Displays configured listeners for an application
  debug:router                            Displays current routes for an application
  debug:swiftmailer                       Displays current mailers for an application
  debug:translation                       Displays translation messages information
  debug:twig                              Shows a list of twig functions, filters, globals and tests
 doctrine
  doctrine:cache:clear                    Flush a given cache
  doctrine:cache:clear-collection-region  Clear a second-level cache collection region.
  doctrine:cache:clear-entity-region      Clear a second-level cache entity region.
  doctrine:cache:clear-metadata           Clears all metadata cache for an entity manager
  doctrine:cache:clear-query              Clears all query cache for an entity manager
  doctrine:cache:clear-query-region       Clear a second-level cache query region.
  doctrine:cache:clear-result             Clears result cache for an entity manager
  doctrine:cache:contains                 Check if a cache entry exists
  doctrine:cache:delete                   Delete a cache entry
  doctrine:cache:flush                    Flush a given cache
  doctrine:cache:stats                    Get stats on a given cache provider
  doctrine:database:create                Creates the configured database
  doctrine:database:drop                  Drops the configured database
  doctrine:database:import                Import SQL file(s) directly to Database.
  doctrine:ensure-production-settings     Verify that Doctrine is properly configured for a production environment.
  doctrine:fixtures:load                  Load data fixtures to your database.
  doctrine:generate:entities              Generates entity classes and method stubs from your mapping information
  doctrine:mapping:convert                Convert mapping information between supported formats.
  doctrine:mapping:import                 Imports mapping information from an existing database
  doctrine:mapping:info
  doctrine:migrations:diff                Generate a migration by comparing your current database to your mapping information.
  doctrine:migrations:execute             Execute a single migration version up or down manually.
  doctrine:migrations:generate            Generate a blank migration class.
  doctrine:migrations:latest              Outputs the latest version number
  doctrine:migrations:migrate             Execute a migration to a specified version or the latest available version.
  doctrine:migrations:status              View the status of a set of migrations.
  doctrine:migrations:version             Manually add and delete migration versions from the version table.
  doctrine:query:dql                      Executes arbitrary DQL directly from the command line.
  doctrine:query:sql                      Executes arbitrary SQL directly from the command line.
  doctrine:schema:create                  Executes (or dumps) the SQL needed to generate the database schema
  doctrine:schema:drop                    Executes (or dumps) the SQL needed to drop the current database schema
  doctrine:schema:update                  Executes (or dumps) the SQL needed to update the database schema to match the current mapping metadata.
  doctrine:schema:validate                Validate the mapping files.
 fos
  fos:oauth-server:clean                  Clean expired tokens
 generate
  generate:doctrine:entities              Generates entity classes and method stubs from your mapping information
 leezy
  leezy:pheanstalk:delete-job             Delete the specified job if it exists.
  leezy:pheanstalk:flush-tube             Delete all job in a specific tube.
  leezy:pheanstalk:kick                   Kick buried jobs from a specific tube.
  leezy:pheanstalk:kick-job               Kick the specified job if it has a valid buried status, regardless of what tube it is in.
  leezy:pheanstalk:list-tube              The names of all tubes on the server.
  leezy:pheanstalk:next-ready             Gives the next ready job from a specified tube.
  leezy:pheanstalk:pause-tube             Temporarily prevent jobs being reserved from the given tube.
  leezy:pheanstalk:peek                   Inspect a job in the system, regardless of what tube it is in.
  leezy:pheanstalk:peek-tube              Take a peek at the first job in a tube, ready or burried.
  leezy:pheanstalk:put                    Puts a job on the queue.
  leezy:pheanstalk:stats                  Gives statistical information about the beanstalkd system as a whole.
  leezy:pheanstalk:stats-job              Gives statistical information about the specified job if it exists.
  leezy:pheanstalk:stats-tube             Gives statistical information about a specified tube, or about all tubes.
 lint
  lint:twig                               Lints a template and outputs encountered errors
  lint:yaml                               Lints a file and outputs encountered errors
 mautic
  mautic:assets:generate                  Combines and minifies asset files from each bundle into single production files
  mautic:broadcasts:send                  Process contacts pending to receive a channel broadcast.
  mautic:campaigns:execute                Execute specific scheduled events.
  mautic:campaigns:messagequeue           Process sending of messages queue.
  mautic:campaigns:messages               Process sending of messages queue.
  mautic:campaigns:rebuild                Rebuild campaigns based on contact segments.
  mautic:campaigns:trigger                Trigger timed events for published campaigns.
  mautic:campaigns:update                 Rebuild campaigns based on contact segments.
  mautic:campaigns:validate               Validate if a contact has been inactive for a decision and execute events if so.
  mautic:citrix:sync                      Synchronizes registrant information from Citrix products
  mautic:contacts:deduplicate             Merge contacts based on same unique identifiers
  mautic:email:fetch                      Fetch and process monitored email.
  mautic:emails:fetch                     Fetch and process monitored email.
  mautic:emails:send                      Processes SwiftMail's mail queue
  mautic:import                           Imports data to Mautic
  mautic:install:data                     Installs Mautic with sample data
  mautic:integration:fetchleads           Fetch leads from integration.
  mautic:integration:pipedrive:fetch      Pulls the data from Pipedrive and sends it to Mautic
  mautic:integration:pipedrive:push       Pushes the data from Mautic to Pipedrive
  mautic:integration:pushactivity         Push lead activity to integration.
  mautic:integration:pushleadactivity     Push lead activity to integration.
  mautic:integration:synccontacts         Fetch leads from integration.
  mautic:iplookup:download                Fetch remote datastores for IP lookup services that leverage local lookups
  mautic:maintenance:cleanup              Updates the Mautic application
  mautic:messages:send                    Process sending of messages queue.
  mautic:migrations:generate              Generate a blank migration class.
  mautic:plugins:install                  Installs, updates, enable and/or disable plugins.
  mautic:plugins:reload                   Installs, updates, enable and/or disable plugins.
  mautic:plugins:update                   Installs, updates, enable and/or disable plugins.
  mautic:queue:process                    Process queues
  mautic:reports:scheduler                Processes scheduler for report's export
  mautic:segments:check-builders          Compare output of query builders for given segments
  mautic:segments:rebuild                 Update contacts in smart segments based on new contact data.
  mautic:segments:update                  Update contacts in smart segments based on new contact data.
  mautic:social:monitoring                Looks at the records of monitors and iterates through them.
  mautic:theme:json-config                Converts theme config to JSON from PHP
  mautic:transifex:pull                   Fetches translations for Mautic from Transifex
  mautic:transifex:push                   Pushes Mautic translation resources to Transifex
  mautic:translation:createconfig         Create config.php files for translations
  mautic:translation:debug                Displays translation messages informations
  mautic:unusedip:delete                  Deletes IP addresses that are not used in any other database table
  mautic:update:apply                     Updates the Mautic application
  mautic:update:find                      Fetches updates for Mautic
  mautic:webhooks:process                 Process queued webhook payloads
 oneup
  oneup:uploader:clear-chunks             Clear chunks according to the max-age you defined in your configuration.
  oneup:uploader:clear-orphans            Clear orphaned uploads according to the max-age you defined in your configuration.
 orm
  orm:convert:mapping                     Convert mapping information between supported formats.
 rabbitmq
  rabbitmq:anon-consumer                  Executes an anonymous consumer
  rabbitmq:batch:consumer                 Executes a Batch Consumer
  rabbitmq:consumer                       Executes a consumer
  rabbitmq:delete                         Delete a consumer's queue
  rabbitmq:dynamic-consumer               Executes context-aware consumer
  rabbitmq:multiple-consumer              Executes a consumer that uses multiple queues
  rabbitmq:purge                          Purge a consumer's queue
  rabbitmq:rpc-server                     Start an RPC server
  rabbitmq:setup-fabric                   Sets up the Rabbit MQ fabric
  rabbitmq:stdin-producer                 Executes a producer that reads data from STDIN
 router
  router:debug                            Displays current routes for an application
  router:dump-apache                      [DEPRECATED] Dumps all routes as Apache rewrite rules
  router:match                            Helps debug routes by simulating a path info match
 security
  security:encode-password                Encodes a password.
 server
  server:run                              Runs PHP built-in web server
  server:start                            Starts PHP built-in web server in the background
  server:status                           Outputs the status of the built-in web server for the given address
  server:stop                             Stops PHP's built-in web server that was started with the server:start command
 social
  social:monitor:twitter:hashtags         Looks at our monitoring records and finds hashtags
  social:monitor:twitter:mentions         Searches for mentioned tweets
 swiftmailer
  swiftmailer:debug                       Displays current mailers for an application
  swiftmailer:email:send                  Send simple email message
  swiftmailer:spool:send                  Sends emails from the spool
 translation
  translation:debug                       Displays translation messages information
  translation:update                      Updates the translation file
 twig
  twig:debug                              Shows a list of twig functions, filters, globals and tests
 yaml
  yaml:lint                               Lints a file and outputs encountered errors
</code></pre>

<p>The emails are not being sent, I've checked spam folder as well. What am I exactly missing?</p>

## Answers
### Answer ID: 68204520
<p>There is one thing missing in the cron setup, to processing the emails in queue.<br />
That is <code>php /path/to/mautic/bin/console mautic:emails:send</code><br />
<code>php bin/console mautic:messages:send</code> is used for <strong>To send frequency rules rescheduled marketing campaign messages</strong><br />
Check this for more info <a href="https://docs.mautic.org/en/setup/cron-jobs" rel="nofollow noreferrer">https://docs.mautic.org/en/setup/cron-jobs</a></p>
<p>Due to this only the emails are not processing, if your queue setup is good.<br />
Just add the command and give it a try it will work perfectly.</p>

### Answer ID: 62350600
<p>First have you tried testing your email configuration and can you confirm Test email is sending fine ?</p>

<p>second you always have option to generate logs from your cron jobs that's what I do for example:</p>

<p><code>2,12,22,32,42,52 * * * *        php /var/www/mautic2/app/console mautic:campaigns:trigger &gt;&gt;/tmp/camp-cron.log 2&gt;&amp;1</code></p>

<p>And If I compare mine with yours perhaps you have missed the timings for the job ?</p>

<p>Finally can you try with a simple command which may be not use any queue, like segment:update or maybe campaign:trigger etc.</p>

<p>Finally from your comment on Ruth's answer I see you have problem with queue, so why don't you check if queue is configured properly ? As far as log you have posted they are result of php app/console command and not real logs from the cron. </p>

<p>Please also ensure the directory is writable. check for errors in app/logs and server logs as well.</p>

### Answer ID: 62260142
<p>Have you tried running the cron tasks at the command line? That will give immediate feedback as to whether you have the correct paths for your server configuration and using the right commands.  </p>

<p>Also worth noting that the cron job is only used when you queue email instead of send immediately - can you send test emails or send using immediate rather than queued? Are the campaigns being triggered successfully?</p>

