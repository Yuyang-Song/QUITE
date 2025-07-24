# PHP 5.5 won&#39;t recognise server when using symfony
[Link to question](https://stackoverflow.com/questions/33874376/php-5-5-wont-recognise-server-when-using-symfony)
**Creation Date:** 1448291554
**Score:** 0
**Tags:** symfony, php-5.5
## Question Body
<p>Im using php 5.5.27 in mac and when I run <code>$php app/console server:run</code> I got:</p>

<pre><code>  [InvalidArgumentException]                                
  There are no commands defined in the "server" namespace. 
</code></pre>

<p>I also review php version by <code>php -v</code>, with <code>php app/check.php</code> and it shows the same version php 5.5.27, any insights?</p>

<p>I install symfony with symfony-installer, and php was already installed in my machine.</p>

<p>Even when I run <code>$php app/console</code> I got:</p>

<pre><code>Symfony version 2.0.12 - app/dev/debug

Usage:
  [options] command [arguments]

Options:
  --help           -h Display this help message.
  --quiet          -q Do not output any message.
  --verbose        -v Increase verbosity of messages.
  --version        -V Display this application version.
  --ansi              Force ANSI output.
  --no-ansi           Disable ANSI output.
  --no-interaction -n Do not ask any interactive question.
  --shell          -s Launch the shell.
  --env            -e The Environment name.
  --no-debug          Switches off debug mode.

Available commands:
  help                                  Displays help for a command
  list                                  Lists commands
assetic
  assetic:dump                          Dumps all assets to the filesystem
assets
  assets:install                        Installs bundles web assets under a public web directory
cache
  cache:clear                           Clears the cache
  cache:warmup                          Warms up an empty cache
container
  container:debug                       Displays current services for an application
doctrine
  doctrine:cache:clear-metadata         Clears all metadata cache for a entity manager
  doctrine:cache:clear-query            Clears all query cache for a entity manager
  doctrine:cache:clear-result           Clears result cache for a entity manager
  doctrine:database:create              Creates the configured databases
  doctrine:database:drop                Drops the configured databases
  doctrine:ensure-production-settings   Verify that Doctrine is properly configured for a production environment.
  doctrine:generate:crud                Generates a CRUD based on a Doctrine entity
  doctrine:generate:entities            Generates entity classes and method stubs from your mapping information
  doctrine:generate:entity              Generates a new Doctrine entity inside a bundle
  doctrine:generate:form                Generates a form type class based on a Doctrine entity
  doctrine:mapping:convert              Convert mapping information between supported formats.
  doctrine:mapping:import               Imports mapping information from an existing database
  doctrine:mapping:info                 Shows basic information about all mapped entities
  doctrine:query:dql                    Executes arbitrary DQL directly from the command line.
  doctrine:query:sql                    Executes arbitrary SQL directly from the command line.
  doctrine:schema:create                Executes (or dumps) the SQL needed to generate the database schema
  doctrine:schema:drop                  Executes (or dumps) the SQL needed to drop the current database schema
  doctrine:schema:update                Executes (or dumps) the SQL needed to update the database schema to match the current mapping metadata
generate
  generate:bundle                       Generates a bundle
  generate:doctrine:crud                Generates a CRUD based on a Doctrine entity
  generate:doctrine:entities            Generates entity classes and method stubs from your mapping information
  generate:doctrine:entity              Generates a new Doctrine entity inside a bundle
  generate:doctrine:form                Generates a form type class based on a Doctrine entity
init
  init:acl                              Mounts ACL tables in the database
mopa
  mopa:generate:crud                    Generates a CRUD based on a Doctrine entity
router
  router:debug                          Displays current routes for an application
  router:dump-apache                    Dumps all routes as Apache rewrite rules
swiftmailer
  swiftmailer:spool:send                Sends emails from the spool
</code></pre>

<p>It won't show server command :(</p>

## Answers
### Answer ID: 33875170
<p>You run Symfony Version 2.0 its too old. Upgrade to the latest version or the LTS version first then you have the server command. Otherweise you can't use them. </p>

<p>The command <code>server:run</code> is for version 2.3 after on higher versions its <code>server:start</code></p>

<p>here is the manual</p>

<p><a href="http://symfony.com/doc/current/cookbook/web_server/built_in.html" rel="nofollow">http://symfony.com/doc/current/cookbook/web_server/built_in.html</a></p>

