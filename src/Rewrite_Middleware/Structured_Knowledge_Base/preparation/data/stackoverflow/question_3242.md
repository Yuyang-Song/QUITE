# postgresql grouping of data according to different time ranges stored in a table
[Link to question](https://stackoverflow.com/questions/73234137/postgresql-grouping-of-data-according-to-different-time-ranges-stored-in-a-table)
**Creation Date:** 1659608196
**Score:** 0
**Tags:** database, postgresql, database-design
## Question Body
<p>I have a table with measurements from temperature sensors, example:</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>id</th>
<th>id_device</th>
<th>measured_time (timestamp)</th>
<th>measured_value</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>2</td>
<td>2022-07-10 09:00</td>
<td>19.90</td>
</tr>
</tbody>
</table>
</div>
<p>I also have several tariffs with time zones (e.g. 3 time zones: night, empty house and active house):</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>time zone</th>
<th>Winter (01/01/2022-31/03/2022 i 01/10/2022-31/12/2022)</th>
<th>Summer (01/04/2022 - 30/09/2022)</th>
</tr>
</thead>
<tbody>
<tr>
<td>1. Night</td>
<td>20:00 - 7:00</td>
<td>22:00 - 5:00</td>
</tr>
<tr>
<td>2. Empty house</td>
<td>10:00 - 17:00</td>
<td>10:00 - 17:00</td>
</tr>
<tr>
<td>3. Active house</td>
<td>7:00 - 10:00 and 17:00-20:00</td>
<td>5:00-10:00 and 17:00 - 22:00</td>
</tr>
</tbody>
</table>
</div>
<p>Saturdays, Sundays and holidays</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>time zone</th>
<th>Winter (01/01/2022-31/03/2022 i 01/10/2022-31/12/2022)</th>
<th>Summer (01/04/2022 - 30/09/2022)</th>
</tr>
</thead>
<tbody>
<tr>
<td>1. Night</td>
<td>21:00 - 8:00</td>
<td>23:00 - 6:00</td>
</tr>
<tr>
<td>2. Empty house</td>
<td>12:00 - 15:00</td>
<td>12:00 - 15:00</td>
</tr>
<tr>
<td>3. Active house</td>
<td>8:00 - 12:00 and 15:00-21:00</td>
<td>6:00-12:00 and 15:00 - 23:00</td>
</tr>
</tbody>
</table>
</div>
<p>I need to group measurements data into appropriate time zones. The expected result:</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>measured_time</th>
<th>measured_value</th>
<th>zone</th>
</tr>
</thead>
<tbody>
<tr>
<td>2022-07-10 09:00</td>
<td>19.90</td>
<td>Active house</td>
</tr>
<tr>
<td>2022-07-10 10:00</td>
<td>19.90</td>
<td>Active house</td>
</tr>
<tr>
<td>2022-07-10 11:00</td>
<td>20.10</td>
<td>Active house</td>
</tr>
<tr>
<td>2022-07-10 12:00</td>
<td>20.10</td>
<td>Active house</td>
</tr>
<tr>
<td>2022-07-10 13:00</td>
<td>20.50</td>
<td>Empty house</td>
</tr>
<tr>
<td>2022-07-10 14:00</td>
<td>20.70</td>
<td>Empty house</td>
</tr>
<tr>
<td>2022-07-10 15:00</td>
<td>21.00</td>
<td>Empty house</td>
</tr>
<tr>
<td>2022-07-10 16:00</td>
<td>21.00</td>
<td>Active house</td>
</tr>
<tr>
<td>2022-07-10 17:00</td>
<td>21.00</td>
<td>Active house</td>
</tr>
<tr>
<td>2022-07-10 18:00</td>
<td>21.00</td>
<td>Active house</td>
</tr>
<tr>
<td>2022-07-10 19:00</td>
<td>21.00</td>
<td>Active house</td>
</tr>
<tr>
<td>2022-07-10 20:00</td>
<td>20.70</td>
<td>Active house</td>
</tr>
<tr>
<td>2022-07-10 21:00</td>
<td>20.50</td>
<td>Active house</td>
</tr>
<tr>
<td>2022-07-10 22:00</td>
<td>20.40</td>
<td>Active house</td>
</tr>
<tr>
<td>2022-07-10 23:00</td>
<td>20.10</td>
<td>Active house</td>
</tr>
<tr>
<td>2022-07-11 00:00</td>
<td>20.00</td>
<td>Night</td>
</tr>
<tr>
<td>2022-07-11 01:00</td>
<td>19.90</td>
<td>Night</td>
</tr>
<tr>
<td>2022-07-11 02:00</td>
<td>19.60</td>
<td>Night</td>
</tr>
<tr>
<td>2022-07-11 03:00</td>
<td>19.20</td>
<td>Night</td>
</tr>
</tbody>
</table>
</div>
<p>The main challenge is to store tariff's time zones well in database. My first idea was to separate time and date to another columns:</p>
<pre><code>CREATE TABLE tariff_time_ranges (
    id bigserial NOT NULL,
    if_tariff int8 NOT NULL,
    hour_from time NOT NULL,
    hour_to time NOT NULL,
    date_from date NOT NULL,
    date_to date NOT NULL
);
</code></pre>
<p>and check it in query:</p>
<pre><code>...
JOIN measurements ON d.device_id = m.id_device AND
(m.measure_time::time &gt; hour_from AND m.measure_time::time &lt;= hour_to 
AND date_from &lt;= m.measure_time AND m.measure_time &lt;= date_to )
</code></pre>
<p>This solution forces me to rewrite the whole year into time ranges (without overlaps):</p>
<div class="s-table-container">
<table class="s-table">
<thead>
<tr>
<th>id</th>
<th>if_tariff</th>
<th>id_time_zone</th>
<th>hour_from</th>
<th>hour_to</th>
<th>date_from</th>
<th>date_to</th>
</tr>
</thead>
<tbody>
<tr>
<td>1</td>
<td>1</td>
<td>1 (night)</td>
<td>23:00</td>
<td>00:00</td>
<td>2022-07-09</td>
<td>2022-07-09 (Summer Saturday)</td>
</tr>
<tr>
<td>2</td>
<td>1</td>
<td>1 (night)</td>
<td>00:00</td>
<td>07:00</td>
<td>2022-07-10</td>
<td>2022-07-10 (Summer Sunday)</td>
</tr>
<tr>
<td>3</td>
<td>1</td>
<td>3 (active house)</td>
<td>07:00</td>
<td>10:00</td>
<td>2022-07-10</td>
<td>2022-07-10</td>
</tr>
<tr>
<td>4</td>
<td>1</td>
<td>2 (empty house)</td>
<td>10:00</td>
<td>15:00</td>
<td>2022-07-10</td>
<td>2022-07-10</td>
</tr>
</tbody>
</table>
</div>
<p>What better idea to achieve the intended goal?</p>

