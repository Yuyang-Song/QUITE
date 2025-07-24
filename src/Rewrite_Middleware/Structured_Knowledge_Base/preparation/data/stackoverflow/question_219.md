# Symfony2 - generate:bundle is not defined
[Link to question](https://stackoverflow.com/questions/17049568/symfony2-generatebundle-is-not-defined)
**Creation Date:** 1370969430
**Score:** 4
**Tags:** php, symfony
## Question Body
<p>I want to generate a new bundle however it says the the command generate:bundle is not defined.</p>

<p>When I try this command:</p>

<pre><code>php app/console list --raw
</code></pre>

<p>generate:bundle is not shown...</p>

<p><em>Output of command:</em></p>

<pre><code>help                                  Displays help for a command
list                                  Lists commands
assetic:dump                          Dumps all assets to the filesystem
assets:install                        Installs bundles web assets under a public web directory
cache:clear                           Clears the cache
cache:warmup                          Warms up an empty cache
config:dump-reference                 Dumps default configuration for an extension
container:debug                       Displays current services for an application
doctrine:cache:clear-metadata         Clears all metadata cache for an entity manager
doctrine:cache:clear-query            Clears all query cache for an entity manager
doctrine:cache:clear-result           Clears result cache for an entity manager
doctrine:database:create              Creates the configured databases
doctrine:database:drop                Drops the configured databases
doctrine:ensure-production-settings   Verify that Doctrine is properly configured for a production environment.
doctrine:generate:entities            Generates entity classes and method stubs from your mapping information
doctrine:mapping:convert              Convert mapping information between supported formats.
doctrine:mapping:import               Imports mapping information from an existing database
doctrine:mapping:info                 Shows basic information about all mapped entities
doctrine:query:dql                    Executes arbitrary DQL directly from the command line.
doctrine:query:sql                    Executes arbitrary SQL directly from the command line.
doctrine:schema:create                Executes (or dumps) the SQL needed to generate the database schema
doctrine:schema:drop                  Executes (or dumps) the SQL needed to drop the current database schema
doctrine:schema:update                Executes (or dumps) the SQL needed to update the database schema to match the current mapping metadata
doctrine:schema:validate              Validates the doctrine mapping files
fos:user:activate                     Activate a user
fos:user:change-password              Change the password of a user.
fos:user:create                       Create a user.
fos:user:deactivate                   Deactivate a user
fos:user:demote                       Demote a user by removing a role
fos:user:promote                      Promotes a user by adding a role
generate:doctrine:entities            Generates entity classes and method stubs from your mapping information
init:acl                              Mounts ACL tables in the database
init:jms-secure-random                
orm:convert:mapping                   Convert mapping information between supported formats.
router:debug                          Displays current routes for an application
router:dump-apache                    Dumps all routes as Apache rewrite rules
router:match                          Helps debug routes by simulating a path info match
swiftmailer:spool:send                Sends emails from the spool
translation:update                    Updates the translation file
twig:lint                             Lints a template and outputs encountered errors
</code></pre>

<p>What is happening here ?</p>

## Answers
### Answer ID: 47985128
<p>You should do <code>composer require sensio/generator-bundle</code> first.</p>

### Answer ID: 17055602
<p>Do you have this line in your composer.json ?</p>

<pre><code>"sensio/generator-bundle": "2.3.*"
</code></pre>

<p>And this one is your AppKernel.php (in the dev, test section) ?</p>

<pre><code>new Sensio\Bundle\GeneratorBundle\SensioGeneratorBundle();
</code></pre>

