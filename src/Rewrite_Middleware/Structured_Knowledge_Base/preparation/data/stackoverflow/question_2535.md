# LINQ query with joins returns 0 results (potential bug)
[Link to question](https://stackoverflow.com/questions/38768485/linq-query-with-joins-returns-0-results-potential-bug)
**Creation Date:** 1470316710
**Score:** 1
**Tags:** c#, linq-to-sql, asp.net-core-mvc, entity-framework-core
## Question Body
<p>I've been fighting with this on and off for a while, and I really can't tell if I'm doing something wrong or if this is a bug with EF Core, basically the issue is my query with two joins always returns zero results, I've tried rewriting it in various different ways to no avail (I just get various different errors) and I don't want to keep fighting it if it's just a bug. The query works as expected in LINQPad, however. The query is as follows:</p>

<pre><code>var playerholder = (from player in db.Players
                    join assignment in db.TeamAssignments on player.PlayerID equals assignment.PlayerID into assignments
                    from assignment in assignments.DefaultIfEmpty()
                    join team in db.Teams on assignment == null ? 0 : assignment.TeamID equals team.TeamID into teams
                    from team in teams.DefaultIfEmpty()
                    select new PlayerListItem_PDVMI
                    {
                        PlayerID = player.PlayerID,
                        FirstName = player.FirstName,
                        LastName = player.LastName,
                        TeamName = (assignment == null ? "Not Assigned" : team.Name)
                    }).ToList();
</code></pre>

<p>Where a Player can have 0 or more TeamAssignments, and a TeamAssignment has exactly one Team.</p>

<p>The resulting SQL, from my log file. This functions correctly when running it against the database directly as well:</p>

<pre><code>SELECT [assignment].[ID], [assignment].[PlayerID], [assignment].[PlayerNumber], [assignment].[Position], [assignment].[SeasonID], [assignment].[TeamID], [player].[PlayerID], [player].[FirstName], [player].[LastName]
FROM [Players] AS [player]
LEFT JOIN [TeamAssignments] AS [assignment] ON [player].[PlayerID] = [assignment].[PlayerID]
ORDER BY [player].[PlayerID]
</code></pre>

<p>and directly following that is the query against the Teams table:</p>

<pre><code>SELECT [assignment.Team].[TeamID], [assignment.Team].[Name]
FROM [Teams] AS [assignment.Team]
</code></pre>

<p>This is my TeamAssignment class (with irrelevant properties removed):</p>

<pre><code>public class TeamAssignment : IModel
{
    [Key]
    public int ID { get; set; }

    public int PlayerID { get; set; }

    public int TeamID { get; set; }

    [ForeignKey("PlayerID")]
    public virtual Player Player { get; set; }

    [ForeignKey("TeamID")]
    public virtual Team Team { get; set; }
}
</code></pre>

<p>Team:</p>

<pre><code>public class Team : IModel
{
    [Key]
    public int TeamID { get; set; }

    public string Name { get; set; }

    public virtual ICollection&lt;TeamAssignment&gt; CurrentPlayers { get; set; }

}
</code></pre>

<p>Player:</p>

<pre><code>public class Player : IModel
{
    [Key]
    public int PlayerID { get; set; }

    public string FirstName { get; set; }

    public string LastName { get; set; }

    public virtual ICollection&lt;TeamAssignment&gt; TeamAssignments { get; set; }

}
</code></pre>

