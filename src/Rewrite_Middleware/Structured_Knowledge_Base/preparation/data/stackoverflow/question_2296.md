# Proper use of database globally in android
[Link to question](https://stackoverflow.com/questions/28090944/proper-use-of-database-globally-in-android)
**Creation Date:** 1421936216
**Score:** 0
**Tags:** android, database, instance, global, android-4.0-ice-cream-sandwich
## Question Body
<p>I'm developing an application but I had problems with the DB(had multiple instances[however it was a public static in my MainActivity] in every activity and returned wrong values, deleted something but existed on other activies, etc..). So I decided to rewrite the whole thing from scratch, now, I understand the queries(insert, update, delete, select, also had experience from mysql before) but I don't know how to use the database properly between activities, how to have a global instance of it? when to close the database? What to pass in context when calling it in static, or non-contextual class/method? I would very appreciate if someone would give me a good example of how to do these things, I almost read every tutorial on google, but these are more about the base insert, update and delete stuff, than using it globally.
Mostly I have to work with the database in ListAdapters.
My minimum target SDK is 4.0</p>

## Answers
### Answer ID: 28091201
<p>You don't need to hold a database instance trough your app, just get the SQLiteDatabase instance every time you need it and query the database. You can save the names of the tables in a global class, though.</p>

<p>You don't need to open/close it, just create a cursor, query, and close the Cursor after it.</p>

