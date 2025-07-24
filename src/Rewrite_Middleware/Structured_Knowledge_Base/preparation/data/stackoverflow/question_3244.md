# How to attach Room database to a SQLiteDatabase?
[Link to question](https://stackoverflow.com/questions/73277711/how-to-attach-room-database-to-a-sqlitedatabase)
**Creation Date:** 1659960835
**Score:** 2
**Tags:** android, sqlite, android-room
## Question Body
<p>I have an old database (connected using <code>SQLiteDatebaseHelper</code>) in my android code, which is pretty legacy and has lots of tables, views, and more. The query is run directly and cursors are parsed. The data in DB is used for rendering an Activity.</p>
<p>Now we have another DB maintained by a different team which is implemented using android room. I need to <code>ATTACH</code> this to be old DB, to render some combined UI element whose data comes from both these DBs.</p>
<p>We are not going to migrate the legacy DB to room because it will take an eternity to rewrite all the usages</p>
<p>We were able to <code>ATTACH</code> the DBs and get this working, but now the problem is, often when I attach the DB and insert a record into the room DB (simultaneously), the app crashes with <code>DatabaseLockedException</code>.</p>
<p>I understand that this might be because room can't handle multiple writable connections, but not sure.
Is there a better way to circumvent the issue? I can't find any ways to make the attach db connection ready only.
We were also thinking of trying the other way around, attaching old db to the room DB and trying if that works. (As we can play around old DB params better)</p>
<p>Please help!</p>

