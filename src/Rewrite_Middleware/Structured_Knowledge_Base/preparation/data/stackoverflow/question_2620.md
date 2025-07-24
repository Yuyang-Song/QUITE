# Flyway partial migration of legacy application
[Link to question](https://stackoverflow.com/questions/43047184/flyway-partial-migration-of-legacy-application)
**Creation Date:** 1490619579
**Score:** 1
**Tags:** java, database-migration, flyway
## Question Body
<p>In an application with a custom database migrator which we want to replace with Flyway.</p>

<p>These migrations are split into some categories like "account" for user management and "catalog" for the product catalog.
Files are named <code>$category.migration.$version.sql</code>. Here, <code>$category</code> is one of the above categories and <code>$version</code> is an integer version <em>starting from 0</em>. </p>

<p>e.g.  <code>account.migration.23.sql</code></p>

<p>Although one could argue that each category should be a separate database, in fact it isn't and a major refactoring would be required to change that.</p>

<p>Also I could use one schema per category, but again this would require rewriting all SQL queries.</p>

<p>So I did the following:</p>

<ul>
<li>Move <code>$category.migration.$version.sql</code> to <code>/sql/$category/V$version__$category.sql</code> (e.g. <code>account.migration.1.sql</code> becomes <code>/sql/account/V1_account.sql</code>)</li>
<li>Use a metadata table <em>per category</em></li>
<li>set the baseline version to zero</li>
</ul>

<p>In code that would be </p>

<pre class="lang-java prettyprint-override"><code>String[] _categories = new String[] { "catalog", "account" };
for (String _category : _categories) {
  Flyway _flyway = new Flyway();
  _flyway.setDataSource(databaseUrl.getUrl(), databaseUrl.getUser(), databaseUrl.getPassword());
  _flyway.setBaselineVersion(MigrationVersion.fromVersion("0"));
  _flyway.setLocations("classpath:/sql/" + applicationName);
  _flyway.setTarget(MigrationVersion.fromVersion(_version + ""));

  _flyway.setTable(category + "_schema_version");
  _flyway.setBaselineOnMigrate(true); // (1)
  _flyway.migrate();
}
</code></pre>

<p>So there would be the metadata tables <code>catalog_schema_version</code> and <code>account_schema_version</code>.</p>

<p>Now the issue is as follows:
Starting with an empty database I would like to apply all pre-existing migrations per category, as done above.
If I remove <code>_flyway.setBaselineOnMigrate(true);</code> (1), then the <code>catalog</code> migration (the first one) succeeds, but it would complain for <code>account</code> that the schema <code>public</code> is not empty.</p>

<p>Likewise setting <code>_flyway.setBaselineOnMigrate(true);</code> causes the following behavior:
The migration of "catalog" succeeds but <code>V0_account.sql</code> is ignored and Flyway starts with <code>V1_account.sql</code>, maybe because it somehow still thinks the database was already baselined?</p>

<p>Does anyone have a a suggestion for resolving the problem? </p>

## Answers
### Answer ID: 43273366
<p>Your easiest solution is to keep the <code>schema_version</code> tables in another schema each. I've answered a <a href="https://stackoverflow.com/a/43240560/369930">very similar question here</a>.</p>

<p>Regarding your observation on <code>baseline</code>, those are expected traits. The migration of <code>account</code> starts at <code>v1</code> because with the combination of <code>baseline=0</code>, <code>baselineOnMigrate=true</code> and a non empty target schema (because <code>catalog</code> has populated it) Flyway has determined this is a pre-existing database that is equal to the baseline - thus start at <code>v1</code>.</p>

