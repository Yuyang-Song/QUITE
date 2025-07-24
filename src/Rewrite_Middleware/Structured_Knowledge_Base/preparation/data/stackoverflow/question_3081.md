# Conditional statement not giving desired output in PHP 7.4
[Link to question](https://stackoverflow.com/questions/65512117/conditional-statement-not-giving-desired-output-in-php-7-4)
**Creation Date:** 1609354311
**Score:** 0
**Tags:** php
## Question Body
<p>I have a PHP script that queries the database and produces results based on the condition. In PHP 7.1 all worked well. But the server the website is hosted has requested I change the server PHP language to 7.4.</p>
<p>After the change I noticed the issue of the desired results not appearing as it should.</p>
<p>Below are my codes.</p>
<pre><code>&lt;?Php if (($checkday != &quot;Sunday&quot;)&amp;&amp;($phdate == &quot;&quot;)) {  

    $davsquery = &quot;SELECT davsID, davs, davsslots FROM dailyavailableslotsus WHERE YEAR(davs)=? AND MONTH(davs)=? AND DAY(davs)=?&quot;;
    $davsstmt = $connQlife-&gt;prepare($davsquery);
    $davsstmt-&gt;bind_param('sss', $year, $month, $day);
    $davsstmt-&gt;execute();
    $davsstmt-&gt;store_result();
    $davsstmt-&gt;bind_result($davsID, $davs, $davsslots);
    $davsstmt-&gt;fetch();
    $davsstmt-&gt;close();

    if (($davsslots!=&quot;&quot;)&amp;&amp;($totalnumrows!=&quot;&quot;)) {
        $availableslots = $davsslots - $totalnumrows;
    } 
    if (($davsslots!=&quot;&quot;)&amp;&amp;($totalnumrows==&quot;&quot;)) {
        $availableslots = $davsslots;
    }  
    if (($totalnumrows==&quot;&quot;)&amp;&amp;($davsslots==&quot;&quot;)) {
        $availableslots = $defaultusimslots;
    }  
    if (($checkday == &quot;Saturday&quot;)&amp;&amp;($davsslots==&quot;&quot;)) {
        $availableslots = $usimslots20 - $totalnumrows;
    }  
    if (($checkday == &quot;Saturday&quot;)&amp;&amp;($davsslots!=&quot;&quot;)) {
        $availableslots = $davsslots - $totalnumrows;
    }
    
?&gt;
    &lt;div class=&quot;calendarheadercont&quot;&gt;
        &lt;div class=&quot;calendarday&quot;&gt;&lt;?Php echo date(&quot;l&quot;, mktime(0, 0, 0,$month,$day,$year)); ?&gt;&lt;/div&gt;
    &lt;/div&gt;
    &lt;div class=&quot;clear_1&quot;&gt;&lt;/div&gt;
    &lt;div class=&quot;calendarsubcont&quot;&gt;
        &lt;div class=&quot;calendardatecont&quot;&gt;
            &lt;div class=&quot;calendarmonth&quot;&gt;&lt;?Php echo date(&quot;M&quot;, mktime(0,0,0, $month,$day,$year)); ?&gt;&lt;/div&gt;
            &lt;div class=&quot;calendardate&quot;&gt;&lt;?Php echo date(&quot;j&quot;, mktime(0,0,0,$month,$day,$year)); ?&gt;&lt;/div&gt;
        &lt;/div&gt;
        &lt;?Php if ($day &gt; $curday){ ?&gt;
            &lt;div class=&quot;calendartextcont&quot;&gt;
                &lt;?Php if ($availableslots &gt; 5){ ?&gt;
                    &lt;div class=&quot;calendartextg&quot;&gt;Available slots: &lt;?Php echo $availableslots; ?&gt;&lt;/div&gt;
                &lt;?php } ?&gt;
                &lt;?Php if (($availableslots &gt;= 1)&amp;&amp;($availableslots &lt;= 5)) { ?&gt;
                    &lt;div class=&quot;calendartexto&quot;&gt;Available slots: &lt;?Php echo $availableslots; ?&gt;&lt;/div&gt;
                &lt;?php } ?&gt;
                &lt;?Php if ($availableslots &lt;= 0){ ?&gt;
                    &lt;div class=&quot;calendartextr&quot;&gt;No Slots Available!&lt;/div&gt;
                &lt;?php } ?&gt;
            &lt;/div&gt;
            &lt;?Php if ($availableslots &gt;= 1){ ?&gt;
                &lt;label class=&quot;calendarcheckbox&quot;&gt;Select
                    &lt;input type=&quot;checkbox&quot; name=&quot;screening&quot; id=&quot;screening&quot; value=&quot;&lt;?Php if ($screeningdate==&quot;&quot;) {echo date('Y-m-d', mktime(0,0,0,$month,$day,$year)); }else{ echo $screeningdate; } ?&gt;&quot;&gt;
                    &lt;span class=&quot;checkmark&quot;&gt;&lt;/span&gt;
                &lt;/label&gt;
            &lt;?php } ?&gt;
        &lt;?php } else { ?&gt;                           
            &lt;div class=&quot;calendartextcont&quot;&gt;
                &lt;div class=&quot;calendartextr&quot;&gt;Booking Closed!&lt;/div&gt;
            &lt;/div&gt;
        &lt;?php } ?&gt;
    &lt;/div&gt;                        
&lt;?Php } ?&gt;
&lt;?Php if ($checkday == &quot;Sunday&quot;) { ?&gt;
    &lt;div class=&quot;calendarheadercont&quot;&gt;
        &lt;div class=&quot;calendarday&quot;&gt;&lt;?Php echo date(&quot;l&quot;, mktime(0, 0, 0,$month,$day,$year)); ?&gt;&lt;/div&gt;
    &lt;/div&gt;
    &lt;div class=&quot;clear_1&quot;&gt;&lt;/div&gt;
    &lt;div class=&quot;calendarsubcont&quot;&gt;
        &lt;div class=&quot;calendardatecont&quot;&gt;
            &lt;div class=&quot;calendarmonth&quot;&gt;&lt;?Php echo date(&quot;M&quot;, mktime(0,0,0, $month,$day,$year)); ?&gt;&lt;/div&gt;
            &lt;div class=&quot;calendardate&quot;&gt;&lt;?Php echo date(&quot;j&quot;, mktime(0,0,0,$month,$day,$year)); ?&gt;&lt;/div&gt;
        &lt;/div&gt;
        &lt;div class=&quot;calendartextcont&quot;&gt;
            &lt;div class=&quot;calendartextr&quot;&gt;Closed On Sundays!&lt;/div&gt;
        &lt;/div&gt;
    &lt;/div&gt;
&lt;?Php } ?&gt;
&lt;?Php if ($phdate != &quot;&quot;){ ?&gt;
    &lt;div class=&quot;calendarheadercont&quot;&gt;
        &lt;div class=&quot;calendarday&quot;&gt;&lt;?Php echo date(&quot;l&quot;, mktime(0, 0, 0,$month,$day,$year)); ?&gt;&lt;/div&gt;
    &lt;/div&gt;
    &lt;div class=&quot;clear_1&quot;&gt;&lt;/div&gt;
    &lt;div class=&quot;calendarsubcont&quot;&gt;
        &lt;div class=&quot;calendardatecont&quot;&gt;
            &lt;div class=&quot;calendarmonth&quot;&gt;&lt;?Php echo date(&quot;M&quot;, mktime(0,0,0, $month,$day,$year)); ?&gt;&lt;/div&gt;
            &lt;div class=&quot;calendardate&quot;&gt;&lt;?Php echo date(&quot;j&quot;, mktime(0,0,0,$month,$day,$year)); ?&gt;&lt;/div&gt;
        &lt;/div&gt;
        &lt;div class=&quot;calendartextcont&quot;&gt;
            &lt;div class=&quot;calendartextr&quot;&gt;&lt;?Php echo $phdetail; ?&gt;&lt;/div&gt;
        &lt;/div&gt;
    &lt;/div&gt;
&lt;?Php } ?&gt;
</code></pre>
<p>What changed in PHP 7.4 that may be affecting the script? Or is there a better way to rewrite this that produces the same results but in code practice favorable to PHP 7.4</p>
<p>To put this into context, this is a subset of a larger script that loops through the days of each month and shows how many slots are available for someone who wants to make a booking for that day.
There is a default value of 30 slots per day. There is also a table that takes entries of a particular number of slots for any particular day specified. There is also a table that takes public holidays. The script is supposed to check if there is a manual entry of slots for a particular day and if there is, check the number of slots available for that day and subtract from the manual entry to determine how many slots are left. If not manual entry, the default slots is then used for that day.</p>
<p>On PHP 7.4, if I specify a manual entry of say 10 slots for a particular day, the output when the entire script is run is that all days of the current month now shows 10 as the slots available rather than 30 and only show 10 for the particular day specified.</p>
<p>The other issue I noticed is that, if I specify a public holiday, all days after that day also show as the public holiday.</p>
<p>But when I switch back to PHP 7.1 all works perfectly.</p>

