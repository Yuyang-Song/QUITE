# Migrating from EF 6.1.2 to EF Core (2.1). How to deal with the Migrations?
[Link to question](https://stackoverflow.com/questions/49966207/migrating-from-ef-6-1-2-to-ef-core-2-1-how-to-deal-with-the-migrations)
**Creation Date:** 1524402313
**Score:** 1
**Tags:** entity-framework-core, entity-framework-6, ef-code-first, entity-framework-migrations, ef-database-first
## Question Body
<p>As performance of our application is lack lustre we may try to migrate it from using Entity Framework 6.1.2 to Entity Framework Core 2.1. I cannot find a clear overview what pitfalls there will be. I do not expect too much problems arising from the need to rewrite some queries, but I am especially wondering what needs to be done about our 30+ migrations that we have for the database.</p>

<p>Are there examples on how to migrate Migrations from EF 6 to EF-core 2.1?</p>

## Answers
### Answer ID: 49967279
<p>If you have EF 6 as Database-First and EF Core is Code-First. You can use <a href="https://github.com/ErikEJ/SqlCeToolbox/wiki/EF-Core-Power-Tools" rel="nofollow noreferrer">reverse POCO generator</a>. Then run <code>Add-Migration</code> to generate migration. Now you have to take care, You need to remove the changes from Up method. Now run <code>Update-Database</code>. From now onwards follow Code-first approach. you make changes in model, generate migration and run <code>Update-Database</code>.</p>

<p>Welcome yo EF Core. </p>

