# Filtering existing query by date
[Link to question](https://stackoverflow.com/questions/56678579/filtering-existing-query-by-date)
**Creation Date:** 1561001407
**Score:** 5
**Tags:** php, laravel-5, laravel-5.8
## Question Body
<p><strong>This has yet to be answered with a functional answer.</strong></p>

<p>I have a few methods that Ive put together for some fun stats on a game I play often.</p>

<p>The method below will take the total count of all games played, match a player to the player list then show a summation of the total wins/loss/ties.</p>

<p>This is great, and functional.</p>

<p>However, due to popular demand Ive been asked to adjust the query to now take into account the date in which the game has played. I would like to filter it down to the last 30 days of summation. How can I do this?</p>

<p>I wanted to ask around before spending the time to rewrite the entire thing. Preferably, everything stays the same just filter down by date.</p>

<p>The date key for the database is <code>checkSumID</code> it is a UNIX timestamp.</p>

<pre><code>private function topPlayers() {

        $topPlayersList = array();

        $playersList = DB::table('pickup_results')
            -&gt;select(DB::raw("playerID"),
                DB::raw("COUNT(CASE WHEN gameResult = 'Win'  THEN 1 END) AS wins"),
                DB::raw("COUNT(CASE WHEN gameResult = 'Loss' THEN 1 END) AS loss"),
                DB::raw("COUNT(CASE WHEN gameResult = 'Tie' THEN 1 END) AS tie")
            )
            -&gt;groupBy('playerID')
            -&gt;orderBy('wins','DESC')
            -&gt;get();

        $i = 0;

        foreach ($playersList as $playerListData) {

            if ($playerListData-&gt;wins + $playerListData-&gt;loss + $playerListData-&gt;tie &gt;= 25) {

                $avgPick = $this-&gt;getPlayerAvgPickCount($playerListData-&gt;playerID);

                $playerRecordID = $playerListData-&gt;playerID;

                $playerNameLookup = Players::where([
                    'player_id' =&gt; $playerListData-&gt;playerID
                ])-&gt;first();

                $playerListData-&gt;playerID = $playerNameLookup-&gt;player_name;

                $topPlayersList[$i] = array(
                    'name' =&gt; $playerNameLookup-&gt;player_name,
                    'total' =&gt; +$playerListData-&gt;wins + +$playerListData-&gt;loss + +$playerListData-&gt;tie,
                    'wins' =&gt; +$playerListData-&gt;wins,
                    'loss' =&gt; +$playerListData-&gt;loss,
                    'tie' =&gt; +$playerListData-&gt;tie,
                    'percent' =&gt; +$playerListData-&gt;loss == 0 ? 0 : round(
                            (+$playerListData-&gt;wins / (+$playerListData-&gt;wins + +$playerListData-&gt;loss) * 100),
                            2
                        ) . ' %',
                    'avg_pick' =&gt; $avgPick[0]-&gt;average,
                    'player_id' =&gt; $playerRecordID
                );

                $i++;

            }

        }

        return $this-&gt;sortArray($topPlayersList,'percent','DESC');
    }
</code></pre>

<p>There is a method that I wrote that does something similar, but more on a single person basis, but not sure how I can stitch the two together without a complete rewrite.</p>

<p>Here is that method</p>

<pre><code>private function getTotalGamesPlayed30DayWinLossTies() {

        //PickupResults::where('playerID', '=', $this-&gt;getPlayerID())-&gt;where('checkSumID', '=', Carbon::now()-&gt;subDays(30)-&gt;timestamp)-&gt;count()
        $results = PickupResults::get();

        //$results = PickupResults::where('playerID', '=', $this-&gt;getPlayerID())-&gt;get();

        $count = 0;
        $wins = 0;
        $loss = 0;
        $tie = 0;
        foreach ($results as $result) {

            if ($result-&gt;playerID === $this-&gt;playerID) {
                $timeStamp = $result-&gt;checkSumID;

                $converted = date('m/d/Y', $timeStamp / 1000);
                if (strtotime($converted) &gt; strtotime('-30 days')) {
                    $count = $count + 1;
                    if ($result-&gt;gameResult === 'Win') {
                        $wins = $wins + 1;
                    }
                    if ($result-&gt;gameResult === 'Loss') {
                        $loss = $loss + 1;
                    }
                    if ($result-&gt;gameResult === 'Tie') {
                        $tie = $tie + 1;
                    }

                }
            }

        }

        return
            array(
                'total' =&gt; $count,
                'wins' =&gt; $wins,
                'loss' =&gt; $loss,
                'tie' =&gt; $tie,
                'percent' =&gt; $loss == 0 ? 0 : round(($wins / ( $wins + $loss) * 100 ),2) . ' %'
            );
    }
</code></pre>

<p>Any help would be greatly appreciated.</p>

<hr>

<p>When using the answer by Arun P</p>

<pre><code>$playersList = DB::table('pickup_results')
    -&gt;select(DB::raw("playerID"),
        DB::raw("COUNT(CASE WHEN gameResult = 'Win'  THEN 1 END) AS wins"),
        DB::raw("COUNT(CASE WHEN gameResult = 'Loss' THEN 1 END) AS loss"),
        DB::raw("COUNT(CASE WHEN gameResult = 'Tie' THEN 1 END) AS tie"))
    -&gt;where('checksumID','&lt;',$now)-&gt;where('checksumID','&gt;',$thirty_days_ahead)
    -&gt;groupBy('playerID')
    -&gt;orderBy('wins', 'DESC')
    -&gt;get();
</code></pre>

<p>It will return 0 results. This is incorrect; I am trying to gather all games a player has played within the last 30 days only. Nothing more, nor less.</p>

<p>You can visit <a href="http://www.Krayvok.com/t1" rel="nofollow noreferrer">http://www.Krayvok.com/t1</a> and view the stats page for a working example.</p>

<p>I am trying to take the current leader-boards which displays all players total games played. I would like to filter it down to show only the players whom has had a game played in the last 30 days from today's date (rolling 30 day).</p>

## Answers
### Answer ID: 56923244
<p>I have made some changes to your existing query,</p>

<pre><code>$timestamp_from = date('Y-m-d', strtotime('-30 days'));

$playersList = DB::table('pickup_results')
    -&gt;select(DB::raw("playerID"),
        DB::raw("COUNT(CASE WHEN gameResult = 'Win'  THEN 1 END) AS wins"),
        DB::raw("COUNT(CASE WHEN gameResult = 'Loss' THEN 1 END) AS loss"),
        DB::raw("COUNT(CASE WHEN gameResult = 'Tie' THEN 1 END) AS tie")
    )
    -&gt;where(DB::raw("DATE((checkSumID/1000)) &gt;= '{$timestamp_from}'"))
    -&gt;groupBy('playerID')
    -&gt;orderBy('wins','DESC')
    -&gt;get();
</code></pre>

<p>In your method <code>getTotalGamesPlayed30DayWinLossTies</code> there is a division by 1000 for <code>checkSumID</code> and I have included it in the query. The where clause for <code>checkSumID</code> has been altered to compare dates.</p>

<p>Try this an comment if you need any assistance.</p>

### Answer ID: 56911901
<p>Try this -</p>

<pre><code>$playersList = DB::table('pickup_results')
        -&gt;select(DB::raw("playerID"),
            DB::raw("COUNT(CASE WHEN gameResult = 'Win' AND checkSumID &gt; '".now()-&gt;subDays(30)-&gt;toDateString()."' THEN 1 END) AS wins"),
            DB::raw("COUNT(CASE WHEN gameResult = 'Loss' AND checkSumID &gt; '".now()-&gt;subDays(30)-&gt;toDateString()."' THEN 1 END) AS loss"),
            DB::raw("COUNT(CASE WHEN gameResult = 'Tie' AND checkSumID &gt; '".now()-&gt;subDays(30)-&gt;toDateString()."' THEN 1 END) AS tie")
        )
        -&gt;groupBy('playerID')
        -&gt;orderBy('wins','DESC')
        -&gt;get();
</code></pre>

<p>Laravel creates the <a href="https://carbon.nesbot.com/" rel="nofollow noreferrer">carbon</a> date instance for <code>now()</code> as mentioned in its <a href="https://laravel.com/docs/5.8/eloquent-mutators#date-mutators" rel="nofollow noreferrer">documentation</a>. Chaining the above carbon methods (<a href="https://carbon.nesbot.com/docs/" rel="nofollow noreferrer">carbon docs</a>) returns the date 30 days ago.</p>

<p>All the <code>SELECT</code> statements would convert to something like this (when the current date is '2019-07-06') -</p>

<p><code>COUNT(CASE WHEN gameResult = 'Win' AND checkSumID &gt; '2019-06-06' THEN 1 END) AS wins</code></p>

<p>This would count the results which were created <strong>after</strong> '2019-06-06' (in the last 30 days) <strong>including</strong> the current date.</p>

### Answer ID: 56833844
<p>Try this one, Update your query like this</p>

<pre><code> $thirty_days_ahead = date('Y-m-d H:i:s', strtotime("-30 days"));
    $now = date('Y-m-d H:i:s', strtotime("0 days"));


    $results = DB::table('pickup_results')
    -&gt;select(DB::raw("playerID"),
    DB::raw("COUNT(CASE WHEN gameResult = 'Win'  THEN 1 END) AS wins"),
    DB::raw("COUNT(CASE WHEN gameResult = 'Loss' THEN 1 END) AS loss"),
    DB::raw("COUNT(CASE WHEN gameResult = 'Tie' THEN 1 END) AS tie"))
    -&gt;where('checksumID','&lt;',$now)-&gt;where('checksumID','&gt;',$thirty_days_ahead)
    -&gt;groupBy('playerID')
    -&gt;orderBy('wins', 'DESC')
    -&gt;get();
</code></pre>

### Answer ID: 56681575
<p>try this 
<code>from_unixtime()</code> returns a date/datetime from unix timestamp</p>

<pre><code>$playersList = DB::table('pickup_results')
        -&gt;select(DB::raw("playerID"),
            DB::raw("COUNT(CASE WHEN gameResult = 'Win'  THEN 1 END) AS wins"),
            DB::raw("COUNT(CASE WHEN gameResult = 'Loss' THEN 1 END) AS loss"),
            DB::raw("COUNT(CASE WHEN gameResult = 'Tie' THEN 1 END) AS tie")
        )
        -&gt;where(DB::raw("from_unixtime(checkSumID) &gt; date_sub(now(), interval 30 day)"))
        -&gt;groupBy('playerID')
        -&gt;orderBy('wins','DESC')
        -&gt;get();
</code></pre>

