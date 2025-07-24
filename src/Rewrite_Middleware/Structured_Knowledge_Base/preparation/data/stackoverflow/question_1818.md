# Matplotlib bar graph x axis won&#39;t plot string values
[Link to question](https://stackoverflow.com/questions/9101497/matplotlib-bar-graph-x-axis-wont-plot-string-values)
**Creation Date:** 1328122394
**Score:** 42
**Tags:** python, matplotlib, bar-chart
## Question Body
<p>I am using Python 2.7 and matplotlib. I am attempting to reach into my database of ambulance calls and count up the number of calls that happen on each weekday.</p>
<p>I will then use matplotlib to create a bar chart of this information to give the paramedics a visual graphic of how busy they are on each day.</p>
<p>Here is the code that works well:</p>
<pre><code>import pyodbc
import matplotlib.pyplot as plt
MySQLQuery = &quot;&quot;&quot;
SELECT 
 DATEPART(WEEKDAY, IIU_tDispatch)AS [DayOfWeekOfCall]
, COUNT(DATEPART(WeekDay, IIU_tDispatch)) AS [DispatchesOnThisWeekday]
FROM AmbulanceIncidents
GROUP BY DATEPART(WEEKDAY, IIU_tDispatch)
ORDER BY DATEPART(WEEKDAY, IIU_tDispatch)
&quot;&quot;&quot;
cnxn = pyodbc.connect('DRIVER={SQL Server};SERVER=MyServer;DATABASE=MyDatabase;UID=MyUserID;PWD=MyPassword')
cursor = cnxn.cursor()
GraphCursor = cnxn.cursor()
cursor.execute(MySQLQuery)

#generate a graph to display the data
data = GraphCursor.fetchall()
DayOfWeekOfCall, DispatchesOnThisWeekday = zip(*data)
plt.bar(DayOfWeekOfCall, DispatchesOnThisWeekday)
plt.grid()
plt.title('Dispatches by Day of Week')
plt.xlabel('Day of Week')
plt.ylabel('Number of Dispatches')
plt.show()
</code></pre>
<p>The code shown above works very well. It returns a nice looking graph and I am happy. I just want to make one change.</p>
<p>Instead of the X axis showing the names of the days of the week, such as &quot;Sunday&quot;, it shows the integer. In other words, Sunday is 1, Monday is 2, etc.</p>
<p>My fix for this is that I rewrite my sql query to use <code>DATENAME()</code> instead of <code>DATEPART()</code>.
Shown below is my sql code to return the name of the week (as opposed to an integer).</p>
<pre><code>SELECT 
 DATENAME(WEEKDAY, IIU_tDispatch)AS [DayOfWeekOfCall]
, COUNT(DATENAME(WeekDay, IIU_tDispatch)) AS [DispatchesOnThisWeekday]
FROM AmbulanceIncidents
GROUP BY DATENAME(WEEKDAY, IIU_tDispatch)
ORDER BY DATENAME(WEEKDAY, IIU_tDispatch)
</code></pre>
<p>Everything else in my python code stays the same. However this will not work and I cannot understand the error messages.</p>
<p>Here are the error messages:</p>
<pre><code>Traceback (most recent call last):
  File &quot;C:\Documents and Settings\kulpandm\workspace\FiscalYearEndReport\CallVolumeByDayOfWeek.py&quot;, line 59, in 

&lt;module&gt;
    plt.bar(DayOfWeekOfCall, DispatchesOnThisWeekday)
  File &quot;C:\Python27\lib\site-packages\matplotlib\pyplot.py&quot;, line 2080, in bar
    ret = ax.bar(left, height, width, bottom, **kwargs)
  File &quot;C:\Python27\lib\site-packages\matplotlib\axes.py&quot;, line 4740, in bar
    self.add_patch(r)
  File &quot;C:\Python27\lib\site-packages\matplotlib\axes.py&quot;, line 1471, in add_patch
    self._update_patch_limits(p)
  File &quot;C:\Python27\lib\site-packages\matplotlib\axes.py&quot;, line 1489, in _update_patch_limits
    xys = patch.get_patch_transform().transform(vertices)
  File &quot;C:\Python27\lib\site-packages\matplotlib\patches.py&quot;, line 547, in get_patch_transform
    self._update_patch_transform()
  File &quot;C:\Python27\lib\site-packages\matplotlib\patches.py&quot;, line 543, in _update_patch_transform
    bbox = transforms.Bbox.from_bounds(x, y, width, height)
  File &quot;C:\Python27\lib\site-packages\matplotlib\transforms.py&quot;, line 745, in from_bounds
    return Bbox.from_extents(x0, y0, x0 + width, y0 + height)
TypeError: coercing to Unicode: need string or buffer, float found
</code></pre>
<p>To sum up, when I output my data with the x axis as integers representing days of week and y axis showing a count of the number of ambulance incidents, Matplotlib will produce a nice graph. But when my data output is the x axis is a string (Sunday, Monday, etc). then Matplotlib will not work.</p>
<p>How to fix this?</p>

## Answers
### Answer ID: 9114298
<p>Your question has nothing to do with an SQL query, it is simply a means to end. What you are really asking is how to change the text labels on a bar chart in pylab. The docs for the <a href="http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.bar">bar chart</a> are useful for customizing, but to simply <a href="http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.xticks">change the labels</a> here is a  minimal working example (MWE):</p>

<pre><code>import pylab as plt

DayOfWeekOfCall = [1,2,3]
DispatchesOnThisWeekday = [77, 32, 42]

LABELS = ["Monday", "Tuesday", "Wednesday"]

plt.bar(DayOfWeekOfCall, DispatchesOnThisWeekday, align='center')
plt.xticks(DayOfWeekOfCall, LABELS)
plt.show()
</code></pre>

<p><img src="https://i.sstatic.net/sT70c.png" alt="enter image description here"></p>

### Answer ID: 9113043
<p>Final completed answer that resolved the issue:
Thank you very much Steve. You have been a great help. I studied geography in college, not programming, so this is quite difficult for me. 
Here is the final code that works for me. </p>

<pre><code> import pyodbc
    import matplotlib.pyplot as plt
    MySQLQuery = """
    SELECT 
      DATEPART(WEEKDAY, IIU_tDispatch)AS [IntegerOfDayOfWeek]
    , COUNT(DATENAME(WeekDay, IIU_tDispatch)) AS [DispatchesOnThisWeekday]
    , DATENAME(WEEKDAY, IIU_tDispatch)AS [DayOfWeekOfCall]
    FROM IIncidentUnitSummary
    INNER JOIN PUnit ON IIU_kUnit = PUN_Unit_PK
    WHERE PUN_UnitAgency = 'LC'
    AND IIU_tDispatch BETWEEN 'October 1, 2010' AND 'October 1, 2011'
    AND PUN_UnitID LIKE 'M__'
    GROUP BY DATEPART(WEEKDAY, IIU_tDispatch), DATENAME(WEEKDAY, IIU_tDispatch)
    ORDER BY DATEPART(WEEKDAY, IIU_tDispatch)
    """
    cnxn = pyodbc.connect("a bunch of stuff I don't want to share")
    cursor = cnxn.cursor()
    GraphCursor = cnxn.cursor()
    cursor.execute(MySQLQuery)

    results = cursor.fetchall()
    IntegerDayOfWeek, DispatchesOnThisWeekday, DayOfWeekOfCall = zip(*results)
    tickpositions = [int(r[0]) for r in results]
    numincidents = [int(r[1]) for r in results]
    ticklabels = [r[2] for r in results]
    plt.bar(tickpositions, numincidents)
    plt.xticks(tickpositions, ticklabels)
    #plt.bar(DayOfWeekOfCall, DispatchesOnThisWeekday)
    plt.grid()
    plt.title('Dispatches by Day of Week')
    plt.xlabel('Day of Week')
    plt.ylabel('Number of Dispatches')
    plt.show()

    cursor.close()
    cnxn.close()
</code></pre>

<p>I don't really understand the lines between "results=cursor.fetchall()" and the following four lines of code that involve creating arrays. I am glad you do, because I look at it and it still does not sink in.
thank you very much. This helps out a lot.
David</p>

### Answer ID: 9101633
<p>Don't change your SQL code just to alter the illustration. Instead, make a small addition to your Python code.</p>

<p>I believe you can do something like <a href="https://stackoverflow.com/a/2177537/208339">this answer</a>. Set the tick labels to be the days of the week.</p>

<p>It may be as simple as adding the following line:</p>

<pre><code>plt.xticks((1, 2, ..., 7), ('Sunday', 'Monday', ..., 'Saturday'))
</code></pre>

<p><a href="http://matplotlib.sourceforge.net/api/pyplot_api.html#matplotlib.pyplot.xticks" rel="nofollow noreferrer">Documentation: pyplot.xticks</a></p>

<p>EDIT: Example in response to comment using a fictional table <code>IncidentTypes</code> that maps integer keys to names of incident types.</p>

<pre><code>cursor.execute('select incident_type_id, count(*), incident_type 
    from Incidents join IncidentTypes using (incident_type_id) 
    group by incident_type_id')
results = cursor.fetchall()
tickpositions = [int(r[0]) for r in results]
numincidents = [int(r[1]) for r in results]
ticklabels = [r[2] for r in results]

plt.bar(tickpositions, numincidents)
plt.xticks(tickpositions, ticklabels)
</code></pre>

