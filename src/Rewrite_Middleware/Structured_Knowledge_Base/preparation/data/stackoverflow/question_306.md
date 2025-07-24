# Events display only on first load, not after clicking next or previous
[Link to question](https://stackoverflow.com/questions/20099825/events-display-only-on-first-load-not-after-clicking-next-or-previous)
**Creation Date:** 1384960805
**Score:** 0
**Tags:** php, jquery, ajax
## Question Body
<p>I am working on a simple event calendar. When I first load the page the calendar loads. Then when I click next or previous it takes me to the next month but the events do not load and the month headings do not change but the correct calendar is drawn. I tried taking my event script from the code and putting it in the function that controls the ajax but it didn't work.</p>

<p>Here is a link to the page.
<a href="http://hartslogmuseum.com/bookhjr10/cal/final/ajcal3.php" rel="nofollow">http://hartslogmuseum.com/bookhjr10/cal/final/ajcal3.php</a>
(Yes its ugly for now)</p>

<p>Could someone point me in the right direction. Thanks.
Here is the code.</p>

<pre><code>  &lt;?php
/* Open up a connection to the mysql database on the same server as website */
    $dbhost =   '';
    $dblogin = '';
    $dbpass = '!';
    $dbbase = '';
    $conn = mysql_connect($dbhost, $dblogin, $dbpass, $dbbase)
        or die("Unable to connect to mysql database");

    function isAjax() {
     return isset($_SERVER['HTTP_X_REQUESTED_WITH']) &amp;&amp;
         $_SERVER ['HTTP_X_REQUESTED_WITH']  == 'XMLHttpRequest';
    }

    if(isAjax() &amp;&amp; isset($_POST['month']))
    {
        $month = $_POST['month'];
        $year = !isset($_POST['year']) ? date('Y', $current_time) : $_POST['year'];
        $events = array();

    die(draw_calendar($month,$year,$events));
        die(draw_calendar($month,$year,$events));
    }




    /* Select our database (there is more than one in my server) */
    mysql_select_db("", $conn);


    /* draws a calendar */
    function draw_calendar($month,$year,$events = array()){
        echo '&lt;div id="calendar_wrapper"&gt;';

        /* draw table */
        $calendar = '&lt;table cellpadding="0" cellspacing="0" class="calendar"&gt;';

        /* table headings */
        $headings = array('Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday');
        $calendar.= '&lt;tr class="calendar-row"&gt;&lt;td class="calendar-day-head"&gt;'.implode('&lt;/td&gt;&lt;td class="calendar-day-head"&gt;',$headings).'&lt;/td&gt;&lt;/tr&gt;';

        /* days and weeks vars now ... */
        $running_day = date('w',mktime(0,0,0,$month,1,$year));
        $days_in_month = date('t',mktime(0,0,0,$month,1,$year));
        $days_in_this_week = 1;
        $day_counter = 0;
        $dates_array = array();

        /* row for week one */
        $calendar.= '&lt;tr class="calendar-row"&gt;';

        /* print "blank" days until the first of the current week */
        for($x = 0; $x &lt; $running_day; $x++):
            $calendar.= '&lt;td class="calendar-day-np"&gt;&amp;nbsp;&lt;/td&gt;';
            $days_in_this_week++;
        endfor;

        /* keep going with days.... */
        for($list_day = 1; $list_day &lt;= $days_in_month; $list_day++):
        $calendar.= '';
    /* add leading zero in the day number */
        if($list_day &lt; 10) {
             $list_day = str_pad($list_day, 2, '0', STR_PAD_LEFT);
             }
    /* add leading zero in the month number */
        if($month &lt; 10) {
             $month = str_pad($month, 2, '0', STR_PAD_LEFT);
             }

        $event_day = $year.'-'.$month.'-'.$list_day; 

        $calendar.= '&lt;td class="calendar-day"&gt;&lt;div style="position:relative;height:100px;"&gt;';


        /* add in the day number */
                $calendar.= '&lt;div class="day-number"&gt;'.$list_day.'&lt;/div&gt;';

                $event_day = $year.'-'.$month.'-'.$list_day;
                if(isset($events[$event_day])) {
                    foreach($events[$event_day] as $event) {
                        $calendar.= '&lt;div class="event"&gt;'.$event['title'].'&lt;/div&gt;';
                    }
                }
                else {
                    $calendar.= str_repeat('&lt;p&gt;&amp;nbsp;&lt;/p&gt;',2);
                }
            $calendar.= '&lt;/div&gt;&lt;/td&gt;';
            if($running_day == 6):
                $calendar.= '&lt;/tr&gt;';
                if(($day_counter+1) != $days_in_month):
                    $calendar.= '&lt;tr class="calendar-row"&gt;';
                endif;
                $running_day = -1;
                $days_in_this_week = 0;
            endif;
            $days_in_this_week++; $running_day++; $day_counter++;
        endfor;

        /* finish the rest of the days in the week */
        if($days_in_this_week &lt; 8):
            for($x = 1; $x &lt;= (8 - $days_in_this_week); $x++):
                $calendar.= '&lt;td class="calendar-day-np"&gt;&amp;nbsp;&lt;/td&gt;';
            endfor;
        endif;

        /* final row */
        $calendar.= '&lt;/tr&gt;';


        /* end the table */
        $calendar.= '&lt;/table&gt;';

        /** DEBUG **/
        $calendar = str_replace('&lt;/td&gt;','&lt;/td&gt;'."\n",$calendar);
        $calendar = str_replace('&lt;/tr&gt;','&lt;/tr&gt;'."\n",$calendar);

        /* all done, return result */
        return $calendar;
    }

    function random_number() {
        srand(time());
        return (rand() % 7);
    }

    /* date settings */
    $month = (int) ($_GET['month'] ? $_GET['month'] : date('m'));
    $year = (int)  ($_GET['year'] ? $_GET['year'] : date('Y'));


    /* "next month" control */
    $next_month_link = '&lt;a href="#" class="monthnav" onClick="getNextMonth();return false;"&gt;Next &amp;raquo;&lt;/a&gt;';

    $heading ='&lt;td colspan=5 class="month"&gt;$month_name $year&lt;/b&gt;&lt;/td&gt;';

    /* "previous month" control */
    $previous_month_link = '&lt;a href="#" class="monthnav" onClick="getPrevMonth();return false;"&gt;&amp;laquo; Prev&lt;/a&gt;';


    /* bringing the controls together */
    $controls = '&lt;form method="get"&gt;'.$select_month_control.$select_year_control.$previous_month_link.$heading.'&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;&amp;nbsp;'.$next_month_link.' &lt;/form&gt;';

    /* get all events for the given month 
       I had to rewrite this query to get 
       anything usable out of the mysql 
       database we already had. */

    $events = array();
    $query = ("
      SELECT 
        event_title 
        AS title, 
        DATE_FORMAT( FROM_UNIXTIME(event_date), '%Y-%m-%d' ) 
        AS event_date 
      FROM 
        events
      WHERE 
        FROM_UNIXTIME(event_date) 
          LIKE '$year-%$month-%'");

    /* verify the query is correct 
    echo $query;
    echo "&lt;hr /&gt;";
    echo "&lt;br /&gt;";
     */


    $result = mysql_query($query,$conn) or die('error 2');
    while($row = mysql_fetch_assoc($result)) {
        $events[$row['event_date']][] = $row;

    /* verify that the query gets results. 
       Also generates a list of this months events*/
        /*echo $row['event_title']." ----- ".$row['event_date'];
        echo "&lt;br /&gt;";*/
    }

    echo '&lt;h2 style="float:left; padding-right:30px;"&gt;'.date('F',mktime(0,0,0,$month,1,$year)).' '.$year.'&lt;/h2&gt;';
    echo '&lt;div style="float:left;"&gt;'.$controls.'&lt;/div&gt;';
    echo '&lt;div style="clear:both;"&gt;&lt;/div&gt;';
    echo draw_calendar($month,$year,$events);
    echo '&lt;br /&gt;&lt;br /&gt;';
    echo '&lt;/div&gt;';

    ?&gt;


    &lt;html&gt;
    &lt;head&gt;
    &lt;link href="cal.css" rel="stylesheet" type="text/css"&gt;
    &lt;script type="text/javascript" src="proto.js"&gt;&lt;/script&gt;
    &lt;script type="text/javascript" language="javascript"&gt;
        var current_month = &lt;?PHP echo $month ?&gt;;
        var current_year = &lt;?PHP echo $year ?&gt;;

        function getPrevMonth()
        {
            if(current_month == 1)
            {
                current_month = 12;
                current_year = current_year - 1;
            }
            else
            {
                current_month = current_month - 1;
            }
            params = 'month='+current_month+'&amp;year='+current_year;
            new Ajax.Updater('calendar_wrapper',window.location.pathname,{method:'post',parameters: params});
        }
            function getNextMonth()
            {
                if(current_month == 12)
                {
                    current_month = 1;
                    current_year = current_year + 1;
                }
                else
                {
                    current_month = current_month + 1;
                }
                params = 'month='+current_month+'&amp;year='+current_year;
                new Ajax.Updater('calendar_wrapper',window.location.pathname,{method:'post',parameters: params});
            }
    &lt;/script&gt;
    &lt;/head&gt;
    &lt;body&gt;
    &lt;div id="calendar_wrapper"&gt;&lt;? /*?PHP draw_calendar($month,$year,$events = array());*/ ?&gt;

    &lt;/body&gt;
    &lt;/html&gt;
</code></pre>

## Answers
### Answer ID: 20101735
<p>Okay, I'm a newbie with jQuery and PHP, but here's a couple things I noticed:</p>

<p>1) You're creating a second <code>"calendar_wrapper"</code> div each time you reload the page after calling your <code>getNextMonth()</code> or <code>getPrevMonth()</code>.  I wasn't familiar with <code>Ajax.Updater</code>, and Google shows that it's Prototype.js, not jQuery, right?  To resolve that, my guess would be that you're not referring to the calendar_wrapper using DOM syntax in the <code>Ajax.Updater</code>.  Try <code>"#calendar_wrapper"</code> in your <code>Ajax.Updater</code> calls inside <code>getNextMonth()</code>/<code>getPrevMonth()</code>.  If you're looking for the jQuery equivalent to <code>Ajax.Updater</code>, check out <a href="http://api.jquery.com/jQuery.ajax/" rel="nofollow">$.ajax()</a>.</p>

<p>2) Your "date settings" section has your variables looking in the GET global array (<code>$_GET['month']</code>), but your AJAX updater is sending the data via POST.  This could be why your PHP script is returning the data properly, but not updating the variables properly.</p>

<p>3) I didn't see anything in your code to select the month/year elements and update them with the data received from your <code>getPrevMonth()</code> or <code>getNextMonth()</code>.  For this, you'd probably need an event handler to update the elements with the new data.  For example, I'd give your first h2 header an id, then have jQuery update the <code>$.text()</code> inside the h2 with the data received from your PHP.  However, it looks like you're seeking to have PHP echo out the updated HTML when it reads the updated <code>$month</code> variable.  If this is the case, hopefully resolving the page making two <code>calendar_wrapper</code> divs will resolve it.</p>

### Answer ID: 20100579
<p>your posted code doesn't seen to include the portion where '$month_name' is defined. The issue is relat ed (most likely) to $month_name not being set properly. Look to do something like: </p>

<pre><code>function draw_calendar($month,$year,$events = array()){

    //set month name
    $month_name = date("F", mktime(0, 0, 0, $month, 10));

    //rest of your code
</code></pre>

