# How to build a query that would add an extra nested level in the recordset
[Link to question](https://stackoverflow.com/questions/41769138/how-to-build-a-query-that-would-add-an-extra-nested-level-in-the-recordset)
**Creation Date:** 1484932892
**Score:** 1
**Tags:** php, cakephp-3.0
## Question Body
<p>The goal is to obtain the following output:</p>

<pre><code>SeasonA
    Leagues
        - LeagueA
        - LeagueB
        ...
    Tournaments
        - TournamentA
        - TournamentB
        ...
SeasonB
    ...
</code></pre>

<p>So far, I get this output:</p>

<pre><code>SeasonA
        - LeagueA
        - LeagueB
        ...
        - TournamentA
        - TournamentB
        ...
SeasonB
    ...
</code></pre>

<p>The resultset returned seems to be missing a nesting level and would force me to add logic to detect/maintain the "Leagues" or "Tournaments" parent list items. Ideally, I would simply like to add an extra nested foreach in the mix. </p>

<p>Database structure</p>

<pre><code>games
-----
id
season_id
league_id

leagues
-------
id
league_tournament_type_id
name
user_id

seasons
-------
id
name
user_id

league_tournament_types
-----------------------
id
name
</code></pre>

<p>Current controller query in Stats/index:</p>

<pre><code>$this-&gt;loadModel("Seasons");

$seasons = $this-&gt;Seasons-&gt;find()
-&gt;contain([
        'Games' =&gt; function($q){
            return $q-&gt;autoFields(false);
            //-&gt;select(['season_id','league_id'])
            //-&gt;group(['Games.season_id','Games.league_id']);
        }, 
        'Games.Leagues' =&gt; function ($q){
            return $q-&gt;autoFields(false)
            -&gt;select(['id','name'])
            -&gt;group('Leagues.id');
        },
        'Games.Leagues.LeagueTournamentTypes' =&gt; function ($q){
        return $q-&gt;autoFields(false)
        -&gt;select(['id','name'])
        -&gt;group('LeagueTournamentTypes.id');
        }
    ])
-&gt;select(['id','name'])
-&gt;where(['Seasons.user_id' =&gt; $this-&gt;Auth-&gt;user('id')])
-&gt;group('Seasons.id');

$this-&gt;set(compact('seasons'));
$this-&gt;set('_serialize', ['seasons']);
</code></pre>

<p>Current loop in view:</p>

<pre><code>&lt;ul&gt;
&lt;?php
foreach ($seasons as $season):
?&gt;
    &lt;li&gt;
    &lt;?= $season-&gt;name?&gt;
    &lt;?= $this-&gt;Html-&gt;link(__('Summary'), ['action'=&gt;'summary',$season-&gt;id])?&gt;
    &lt;?= $this-&gt;Html-&gt;link(__('Detailed'), ['action'=&gt;'detailed',$season-&gt;id])?&gt;

    &lt;?php 
    if(count($season-&gt;games)):
        echo "&lt;ul&gt;";
        foreach ($season-&gt;games as $g):?&gt;
            &lt;li&gt;&lt;?= $g-&gt;league-&gt;name?&gt;
            &lt;?= $this-&gt;Html-&gt;link(__('Summary'), ['action'=&gt;'summary',$season-&gt;id,$g-&gt;league-&gt;id])?&gt;
            &lt;?= $this-&gt;Html-&gt;link(__('Detailed'), ['action'=&gt;'detailed',$season-&gt;id,$g-&gt;league-&gt;id])?&gt;
            &lt;/li&gt;
        &lt;?php 
        endforeach;
        echo "&lt;/ul&gt;";
    endif;
    ?&gt;
    &lt;/li&gt;
&lt;?php 
endforeach;
?&gt;
&lt;/ul&gt;
</code></pre>

<p>I'm coming from a Coldfusion background and this was trivial to do using nested CFOUTPUT with a group attribute, and a basic query with inner join:</p>

<pre><code>&lt;cfoutput group="season_id"&gt;
    #season_name#
    &lt;cfoutput group="league_tournament_id"&gt;
        #league_tournament_type_name#
        &lt;cfoutput group="league_id"&gt;
            #league_name#
        &lt;/cfoutput&gt;
    &lt;/cfoutput&gt;
&lt;/cfoutput&gt;
</code></pre>

<p>In Grails, I was able to rewrite a recordset into something that could easily be looped. Could this be a solution for CakePHP 3.0 too? If so, any libraries dedicated to this?</p>

<p><strong>Edit #1</strong></p>

<p>I suspect I may have to work with Collections (and use map or append)?</p>

