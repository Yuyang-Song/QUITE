# How to use Symfony console to init:bundle?
[Link to question](https://stackoverflow.com/questions/6477175/how-to-use-symfony-console-to-initbundle)
**Creation Date:** 1308997379
**Score:** 8
**Tags:** symfony
## Question Body
<p>i run this command: php app/console</p>

<pre><code>Symfony version 2.0.0-RC1 - app/dev/debug

Usage:
  [options] command [arguments]

Options:
  --help           -h Display this help message.
  --quiet          -q Do not output any message.
  --verbose        -v Increase verbosity of messages.
  --version        -V Display this program version.
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
  assets:install                        
cache
  cache:clear                           Clear the cache
  cache:warmup                          Warms up an empty cache
container
  container:debug                       Displays current services for an application
doctrine
  doctrine:cache:clear-metadata         Clear all metadata cache for a entity manager
  doctrine:cache:clear-query            Clear all query cache for a entity manager
  doctrine:cache:clear-result           Clear result cache for a entity manager
  doctrine:database:create              Create the configured databases
  doctrine:database:drop                Drop the configured databases
  doctrine:ensure-production-settings   Verify that Doctrine is properly configured for a production environment.
  doctrine:generate:crud                Generates a CRUD based on a Doctrine entity
  doctrine:generate:entities            Generate entity classes and method stubs from your mapping information
  doctrine:generate:entity              Generates a new Doctrine entity inside a bundle
  doctrine:generate:form                Generates a form type class based on a Doctrine entity
  doctrine:mapping:convert              Convert mapping information between supported formats.
  doctrine:mapping:import               Import mapping information from an existing database
  doctrine:mapping:info                 Show basic information about all mapped entities
  doctrine:query:dql                    Executes arbitrary DQL directly from the command line.
  doctrine:query:sql                    Executes arbitrary SQL directly from the command line.
  doctrine:schema:create                Executes (or dumps) the SQL needed to generate the database schema.
  doctrine:schema:drop                  Executes (or dumps) the SQL needed to drop the current database schema.
  doctrine:schema:update                Executes (or dumps) the SQL needed to update the database schema to match the current mapping metadata.
generate
  generate:bundle                       Generates a bundle
  generate:doctrine:crud                Generates a CRUD based on a Doctrine entity
  generate:doctrine:entities            Generate entity classes and method stubs from your mapping information
  generate:doctrine:entity              Generates a new Doctrine entity inside a bundle
  generate:doctrine:form                Generates a form type class based on a Doctrine entity
init
  init:acl                              
router
  router:debug                          Displays current routes for an application
  router:dump-apache                    Dumps all routes as Apache rewrite rules
swiftmailer
  swiftmailer:spool:send                Send emails from the spool
</code></pre>

<p>i'm following official Symfony documentation (http://symfony.com/doc/current/book/page_creation.html) and i cannot run command: </p>

<pre><code>php app/console init:bundle Acme/HelloBundle src

[InvalidArgumentException]             
  Command "init:bundle" is not defined. 
</code></pre>

<p>How to create my first "Bundle"?</p>

## Answers
### Answer ID: 14272754
<p>Please refer this site for generating bundle. It's very useful</p>

<p><a href="http://symfony.com/blog/symfony2-getting-easier-interactive-generators" rel="nofollow">http://symfony.com/blog/symfony2-getting-easier-interactive-generators</a></p>

### Answer ID: 6477886
<p>I just had the same problem and found your post. It seems that the way to create bundle had changed and the book was not updated.</p>

<p>Just use the <code>generate:bundle</code> instead of <code>init:bundle</code>, without parameters. An assistant will then help you create the bundle.</p>

### Answer ID: 6477979
<p>I am also currently reading this documentation. I have the same problem as you, as a result I used the <code>generate:bundle</code> and manually did something that follows in the manual.</p>

