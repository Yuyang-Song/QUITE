# MySQL - Most restrictive permission
[Link to question](https://stackoverflow.com/questions/19592474/mysql-most-restrictive-permission)
**Creation Date:** 1382711030
**Score:** 0
**Tags:** php, mysql, recursion, where-clause
## Question Body
<p>I'll explain my case:</p>

<h2>The problem</h2>

<p>I've got the following database table:</p>

<pre><code>+----+----------+---------+------------+---------+---------------+-----------+---------+------+
| id | owner_id | user_id | group_mode | item_id | capability_id | from_date | to_date | deny |
+----+----------+---------+------------+---------+---------------+-----------+---------+------+
</code></pre>

<p>The id and owner_id field are not relevant for this question.</p>

<p>The group_mode can have 3 modes: 0 for a single user, 1 if the item is being shared for a group of users, or 2 if it's being shared in a team way.</p>

<p>The deny field can have 0 or 1. In case it's 1, the user won't be able to do anything that needs this permission. If it has a 0, the user will be able to do so. The "default" value means that no permission has been assigned to this user and object, and it's if the user is not found in the table with that item_id assigned.</p>

<p>I've managed to receive what I want from this query, but it's an extremely large query and with code repeated, since every comparison is made to every "user mode".</p>

<h2>What I'd like to get</h2>

<p>I'd like to make a query in order to receive the most restrictive permission of an object. If a user has permission 1 (edit) to an object, but a group to which he belongs is denied this permission (1), the result should be denied, and viceversa. If a group has the permission but the user has it denied, the permission is denied.</p>

<p>Also, if the user is the owner of the item all permissions are granted, even if they are not listed in the table (I explain this in order for you to understand the query I'll write).</p>

<p>All these must be if NOW() - today - is inside the date range. So, a denied permission from X to Y, if we are out from this range, is not denied anymore: is set to default (like it didn't exist).</p>

<p>When it complicates is when, if the user has not any permission set but a group or a team he belongs to has it, the permission is applied. I mean: it might be possible that the user won't have any permission granted, but a group to which he belongs yes, so he has this permission granted (herency).</p>

<h2>What I've thought: The query explained</h2>

<p>It's very simple, but very long at the end. What I do is to check:</p>

<p>IF the user has THIS PERMISSION to THIS OBJECT in THIS RANGE of dates, ONLY WHEN any group from which he belongs has not THIS PERMISSION denied NOR ANY TEAM in THIS RANGE of dates
OR if ANY GROUP to which THIS USER belongs has set THIS PERMISSION in THIS RANGE for THIS OBJECT, ONLY WHEN the user itself has not THIS PERMISSION denied NOR ANY TEAM to which he belongs 
OR the same for the teams.</p>

<h2>What I've thought: The query written</h2>

<pre><code>SELECT ITEM_SELECT_TABLE_FIELDS 
        FROM ITEM_ORIGINAL_TABLE
        WHERE deleted IS NULL  
            AND (user_id = 'USER_ID'  
                OR unique_id IN 
                    (SELECT sh.item_id 
                    FROM SHARED_ITEMS_TABLE sh 
                    WHERE (sh.user_id = 'USER_ID' 
                        AND sh.deny = 0 
                        AND sh.capability_id != 0 

                        AND sh.from_date &lt; NOW() 
                        AND (sh.to_date &gt; NOW() 
                            OR sh.to_date IS NULL) 
                        AND sh.user_id NOT IN 
                            (SELECT gr.user_id 
                            FROM GROUPS_TABLE gr 
                            WHERE group_id IN 
                                (SELECT sh2.user_id 
                                FROM SHARED_ITEMS_TABLE sh2 
                                WHERE sh2.group_mode = 1 
                                    AND sh2.deny = 1 
                                    AND sh2.from_date &lt; NOW() 
                                    AND (sh2.to_date &gt; NOW() 
                                        OR sh2.to_date IS NULL) 
                                    AND sh2.capability_id = sh.capability_id 
                                )
                            )
                        AND sh.user_id NOT IN 
                            (SELECT tm1.user_id 
                            FROM TEAMS_TABLE tm1 
                            WHERE tm1.team_id IN (
                                SELECT sh8.user_id 
                                FROM SHARED_ITEMS_TABLE sh8 
                                WHERE sh8.group_mode = 1 
                                    AND sh8.deny = 1 
                                    AND sh8.from_date &lt; NOW() 
                                    AND (sh8.to_date &gt; NOW() 
                                        OR sh8.to_date IS NULL) 
                                    AND sh8.capability_id = sh.capability_id 
                                )
                            )
                        ) 

                        OR 

                        (sh.user_id IN 
                            (SELECT grus2.group_id 
                            FROM GROUPS_TABLE grus2 
                            WHERE grus2.user_id = 'USER_ID' 
                            AND grus2.user_id NOT IN
                                (SELECT sh3.user_id 
                                FROM SHARED_ITEMS_TABLE sh3 
                                WHERE sh3.group_mode = 0 
                                AND sh3.deny = 1 
                                AND sh3.from_date &lt; NOW() 
                                AND (sh3.to_date &gt; NOW() 
                                    OR sh3.to_date IS NULL) 
                                AND sh3.capability_id = sh.capability_id 
                                AND sh3.user_id NOT IN 
                                    (SELECT grus3.group_id 
                                    FROM GROUPS_TABLE grus3 
                                    WHERE grus3.user_id IN 
                                        (SELECT sh5.user_id 
                                        FROM SHARED_ITEMS_TABLE sh5 
                                        WHERE sh5.group_mode = 0 
                                            AND sh5.deny = 1 
                                            AND sh5.from_date &lt; NOW() 
                                            AND (sh5.to_date &gt; NOW() 
                                                OR sh5.to_date IS NULL) 
                                            AND sh5.capability_id = sh.capability_id 
                                        )
                                    )
                                )
                            AND grus2.user_id NOT IN 
                                (SELECT tm3.user_id 
                                FROM TEAMS_TABLE tm3
                                WHERE tm3.team_id IN (
                                    SELECT sh9.user_id 
                                    FROM SHARED_ITEMS_TABLE sh9 
                                    WHERE sh9.group_mode = 2 
                                        AND sh9.deny = 1 
                                        AND sh9.from_date &lt; NOW() 
                                        AND (sh9.to_date &gt; NOW() 
                                            OR sh9.to_date IS NULL) 
                                        AND sh9.capability_id = sh.capability_id 
                                    )
                                )
                            ) 
                            AND sh.deny = 0 
                            AND group_mode = 1 
                            AND sh.from_date &lt; NOW() 
                            AND (sh.to_date &gt; NOW() 
                                OR sh.to_date IS NULL)
                        )

                        OR

                        (sh.user_id IN 
                            (SELECT tm4.team_id 
                            FROM TEAMS_TABLE tm4 
                            WHERE tm4.user_id = 'USER_ID' 
                                AND sh.deny = 0 
                                AND group_mode = 2 
                                AND sh.from_date &lt; NOW() 
                                AND (sh.to_date &gt; NOW() 
                                    OR sh.to_date IS NULL) 
                                AND sh.user_id NOT IN 
                                    (SELECT gr2.user_id 
                                    FROM GROUPS_TABLE gr2
                                    WHERE gr2.group_id IN 
                                        (SELECT sh10.user_id 
                                        FROM SHARED_ITEMS_TABLE sh10 
                                        WHERE sh10.group_mode = 1 
                                            AND sh10.deny = 1 
                                            AND sh10.from_date &lt; NOW() 
                                            AND (sh10.to_date &gt; NOW() 
                                                OR sh10.to_date IS NULL) 
                                            AND sh10.capability_id = sh.capability_id 
                                        )
                                    )
                                AND sh.user_id NOT IN 
                                    (SELECT grus7.group_id 
                                    FROM GROUPS_TABLE grus7
                                    WHERE grus7.user_id IN 
                                        (SELECT sh11.user_id 
                                        FROM SHARED_ITEMS_TABLE sh11 
                                        WHERE sh11.group_mode = 0 
                                            AND sh11.deny = 1 
                                            AND sh11.from_date &lt; NOW() 
                                            AND (sh11.to_date &gt; NOW() 
                                                OR sh11.to_date IS NULL) 
                                            AND sh11.capability_id = sh.capability_id 
                                        )
                                    )
                                )

                        )
                    )
                )  ORDER BY created_timestamp DESC
</code></pre>

<h2>What I see</h2>

<p>It's an extremely large query and if I add another group_mode (for example, maybe I want to add a group of groups to the permissions), I have to rewrite every WHERE condition to add the new one, in every case. It's a problem.</p>

<p>I know it must be some way to simplify all this, because the code in every WHERE condition is the same: just make sure that any correlatives of the user (group, team or the user itself) have not THIS PERMISSION denied.</p>

<h2>Conclusion</h2>

<p>I don't need you to write me the query. If you could explain me how to make somehow something recursive (without using procedures if it's possible) to check what I told before would be great.</p>

<p><em>Sorry for the large question and for my bad "MySQL language".</em></p>

<p>Thank you very much for your time and your answers!</p>

## Answers
### Answer ID: 19592756
<p>I think that it could be much more simply if you make one query for each kind of request and validate individually with PHP. </p>

<p>For example, you have a deny item like property of the $item object (<code>$item-&gt;deny</code>).</p>

<p>If <code>$item-&gt;deny=1</code> and the user wants to do something with this item, he will find:</p>

<pre><code>if($item-&gt;deny==1)
{
   $message = "You are not allowed";
   echo $message;
} 
else 
{
   //do whatever
}
</code></pre>

<p>Just an example, but you can do that with every kind of request.</p>

