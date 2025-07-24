# Rails - Complex queries with ActiveRecord
[Link to question](https://stackoverflow.com/questions/34179046/rails-complex-queries-with-activerecord)
**Creation Date:** 1449664742
**Score:** 0
**Tags:** sql, ruby-on-rails, activerecord
## Question Body
<p>I have many complex queries to execute like the one bellow.
Is it possible (and worth the effort) to rewrite them using Rails ActiveRecord?</p>

<pre><code>select a.name as athlete_name, a.nickname, t.name as team_name, top_scorers.goals
from (
  select g.athlete_id, g.team_id, count(*) as goals
  from goal g
  join tournament_edition te on te.tournament_edition_id = g.tournament_edition_id and te.tournament_edition_id = #{tournament_edition_id}
  group by g.athlete_id, g.team_id
  order by count(*) desc
  ) as top_scorers
left join athlete a on a.athlete_id = top_scorers.athlete_id
left join team t on t.team_id = top_scorers.team_id;
</code></pre>

<p>How can I rewrite it using ActiveRecord?</p>

<p>Model structure (legacy database):</p>

<pre><code>class Athlete &lt; ActiveRecord::Base
  self.table_name = 'athlete'
  self.primary_key = 'athlete_id'

  has_many :goals
  belongs_to :team
end

class Goal &lt; ActiveRecord::Base
  self.table_name = 'goal'
  self.primary_key = 'goal_id'

  belongs_to :athlete
  belongs_to :team
  belongs_to :tournament_edition
end

class Team &lt; ActiveRecord::Base
  self.table_name = 'team'
  self.primary_key = 'team_id'

  has_many :goals
  has_many :athletes
end

class TournamentEdition &lt; ActiveRecord::Base
  self.table_name = 'tournament_edition'
  self.primary_key = 'tournament_edition_id'

  has_many :goals
end
</code></pre>

<p><strong>One Solution:</strong></p>

<p>After many tries I found this 'solution'. But I would like to get all information without use the map workaround, and a better way to use count as well...</p>

<pre><code>goals = Goal.select(:athlete_id, :team_id, 'count(*) as goals')
            .joins(:tournament_edition)
            .where(tournament_edition: {tournament_edition_id: tournament_edition_id})
            .group(:athlete_id, :team_id)
            .order('goals desc')

goals.map { |goal| 
  {
    name: goal.athlete.name,
    nickname: goal.athlete.nickname,
    team: goal.team.name,
    goals: goal.goals
  }
}
</code></pre>

