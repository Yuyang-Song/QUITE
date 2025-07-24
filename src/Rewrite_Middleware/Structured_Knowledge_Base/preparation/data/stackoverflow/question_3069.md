# SQLite3 not setting field&#39;s value to the specified value
[Link to question](https://stackoverflow.com/questions/64951716/sqlite3-not-setting-fields-value-to-the-specified-value)
**Creation Date:** 1606030861
**Score:** 0
**Tags:** python, database, sqlite, discord.py
## Question Body
<p>So, I'm making a discord bot, and I wanted to add a leveling system, but it just doesn't work (I'm getting no errors). Here's the problem: Whenever I level up, I don't. What I mean is that when I level up, it says: &quot;@Crabby has reached level 2, GG!&quot; but when I look at the database I was level 1. It did reset the exp though, but that just makes it more confusing as to why the level up part isn't working. Anyway, here's the code:</p>
<pre class="lang-py prettyprint-override"><code>    @commands.Cog.listener()
    async def on_message(self, message):
        # Role variables
        lvl_5_role = discord.utils.get(message.guild.roles, name='Memeling (Level 5+)')
        lvl_10_role = discord.utils.get(message.guild.roles, name='Memer (Level 10+)')
        lvl_15_role = discord.utils.get(message.guild.roles, name='Ultimate Memer (Level 15+)')
        # Checking if the author is not a bot (This prevents a loop)
        if not message.author.bot:
            # Database variables
            db = sqlite3.connect('database\main.sqlite3')
            cursor = db.cursor()
            cursor.execute(f&quot;SELECT user_id FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'&quot;)
            result = cursor.fetchone()
            #  End of primary variables
            if result is None:
                sql = (&quot;INSERT INTO levels(guild_id, user_id, exp, lvl) VALUES(?, ?, ?, ?)&quot;)
                val = (message.guild.id, message.author.id, 10, 0)
                cursor.execute(sql, val)
                db.commit()
            else:
                cursor.execute(f&quot;SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'&quot;)
                result1 = cursor.fetchone()
                exp = int(result1[1])
                sql = (&quot;UPDATE levels SET exp = ? WHERE guild_id = ? and user_id = ?&quot;)
                val = (exp + random.randint(1, 5), str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()

                cursor.execute(f&quot;SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{message.guild.id}' and user_id = '{message.author.id}'&quot;)
                result2 = cursor.fetchone()

                xp_start = int(result2[1])
                lvl_start = int(result2[2])
                xp_end = math.floor(5 * (lvl_start ^ 2) + 50 * lvl_start + 100)

                if xp_end &lt; xp_start:
                    await message.channel.send(f&quot;{message.author.mention} has reached level {lvl_start + 1}, GG!&quot;)
                    
                    if lvl_start == 5:
                        message.author.add_roles(lvl_5_role)
                    elif lvl_start == 10:
                        message.author.add_roles(lvl_10_role)
                    elif lvl_start == 15:
                        message.author.add_roles(lvl_15_role)
                    sql = &quot;UPDATE levels SET lvl = ? and user_id = ?&quot;
                    val = str(lvl_start + 1), str(message.author.id)
                    cursor.execute(sql, val)
                    db.commit()
                    sql = &quot;UPDATE levels SET exp = ? and guild_id = ? and user_id = ?&quot;
                    val = 0, str(message.guild.id), str(message.author.id)
                    cursor.execute(sql, val)
                    db.commit()
                    cursor.close()
                    db.close()
        # if the author is a bot
        else:
            pass
</code></pre>
<p>NOTE: I am using Python 3.8.6 and discord.py rewrite</p>
<p>EDIT: I've narrowed the code down to the on_message() listener since I think that is where the issue is. Also, I have tested it, and it does properly level me up from level 0 to level 1, but after that, it doesn't level me up at all when I get enough XP for the level up, but it still resets my XP to 0</p>
<p>EDIT 2: I added a condition to the exp reset and level up queries but they still don't work</p>

