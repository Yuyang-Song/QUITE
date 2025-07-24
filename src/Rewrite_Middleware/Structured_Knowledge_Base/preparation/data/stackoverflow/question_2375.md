# Linq group by and select
[Link to question](https://stackoverflow.com/questions/31782382/linq-group-by-and-select)
**Creation Date:** 1438589440
**Score:** -1
**Tags:** c#, asp.net-mvc, database, linq
## Question Body
<p>I have  *.cs model </p>

<pre><code>public class TimesheetListModel
    {
        public string ProjectName { get; set; }
        public DateTime TaskDate { get; set; }
        public string Task { get; set; }
        public decimal TimeWorked { get; set; }
        public string Note { get; set; }
    }
</code></pre>

<p>And I have service, that selects my model from database.</p>

<p>Now I need to include my model into List&lt;> new model:</p>

<pre><code> public class TimesheetModel
    {
        public DateTime TaskDate { get; set; }
        public List&lt;TimesheetListModel&gt; TimesheetList { get; set; }

        public TimesheetModel() { TimesheetList = new List&lt;TimesheetListModel&gt;(); }
    }
</code></pre>

<p>And I need to select data from db for new model, and group by TaskDate in new model. I have service that realize this query, but it wrote for old model:</p>

<pre><code>public IEnumerable&lt;TimesheetListModel&gt; GetTicketsInProgressByUserId(int id)
{
    var query = (from workLogList in DataContext.tblWorkLogs
                 join tickets in DataContext.tblTickets on workLogList.TicketId equals tickets.TicketId
                 join project in DataContext.tblProjects on tickets.ProjectId equals project.ProjectId
                 join states  in DataContext.tblWorkflowStates on tickets.Status equals states.StateId
                 where workLogList.AccountId == id
                 select new TimesheetListModel
                 {
                     ProjectName = project.Name,
                     TaskDate = workLogList.WorkDate,
                     Task = "#" + tickets.TicketId + " : " +  tickets.Title,
                     TimeWorked = workLogList.TimeWorked,
                     Note = workLogList.Note
                 });
    return query.ToList();
}
</code></pre>

<p>How I need to rewrite my query for selecting data for new model?</p>

## Answers
### Answer ID: 31782480
<p>You can do it like this:-</p>

<pre><code>where workLogList.AccountId == id
group workLogList by workLogList.WorkDate into g
select new TimesheetModel
      {
          TaskDate = g.Key,
          TimesheetList = g.ToList()
      });
</code></pre>

