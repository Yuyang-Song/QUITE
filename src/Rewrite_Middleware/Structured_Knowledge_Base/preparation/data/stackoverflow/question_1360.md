# Typeorm global where clause
[Link to question](https://stackoverflow.com/questions/72564192/typeorm-global-where-clause)
**Creation Date:** 1654794641
**Score:** 1
**Tags:** javascript, typescript, orm, typeorm
## Question Body
<p>in my database, all tables have a boolean column &quot;active&quot; which is used to know if the row should be returned or not on the query.</p>
<p>As we use TypeORM as our back-end ORM, Is it possible to have a global statement/clause that is &quot;concatenated&quot; on every query made by TypeORM, like:</p>
<p>WHERE column.active = true</p>
<p>So, like this, the rows with the column active with 0 as a value, don't return on TypeORM queries during the main application flow, instead of rewriting it on every queryBuilder or repositories premade queries like &quot;find&quot; or &quot;findOrfail&quot; where we dont even write anything.</p>
<ul>
<li>Need to be in TypeORM because it should be returned on manual queries on sgbd and things like this</li>
<li>We use postgre as SGBD</li>
<li>Typeorm v0.2.24</li>
</ul>

## Answers
### Answer ID: 76415642
<p>This lib supports Scopes for both Active Record pattern (working with Entitiies), and Data Mapper pattern (working with Repositories) (for typeorm both versions 2.x and 3.x). I think this will be very useful for all of you.</p>
<p><a href="https://www.npmjs.com/package/typeorm-scoped" rel="nofollow noreferrer">enter link description here</a></p>
<p><div class="snippet" data-lang="js" data-hide="false" data-console="true" data-babel="false">
<div class="snippet-code">
<pre class="snippet-code-js lang-js prettyprint-override"><code>import { DefaultScopes } from "typeorm-scoped"

@DefaultScopes&lt;User&gt;({
  existed: (qb, alias) =&gt; qb.andWhere(`${alias}.deletedAt IS NULL`),
  ...
})
@Entity()
export class User extends BaseEntity {
  // ...
}

// in Your service

User.find({where: {name: "John"}})
// or
userRepository.find({where: {name: "John"}})

// will produce an SQL query like
// SELECT "User"."id" AS "User_id", "User"."name" AS "User_name" 
// FROM "user" "User" 
// WHERE "User"."name" = ? AND "User"."deletedAt" IS NULL
// -- PARAMETERS: ["John"]</code></pre>
</div>
</div>
</p>

