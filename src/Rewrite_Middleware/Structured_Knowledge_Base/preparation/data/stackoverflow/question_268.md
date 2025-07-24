# How to Use Variable Data in C# SQL Query String
[Link to question](https://stackoverflow.com/questions/18494039/how-to-use-variable-data-in-c-sql-query-string)
**Creation Date:** 1377709468
**Score:** 0
**Tags:** c#, asp.net, sql
## Question Body
<p>I have a project I'm working in, which I did not create. I am still relatively new to C# and ASP.NET as a whole. I am faced with this SQL query:</p>

<pre><code>var sql = @"SELECT * FROM [database] WHERE [submitDate] &gt;= Convert(datetime,'20130301')";

var sql = @"SELECT * FROM (SELECT ROW_NUMBER() OVER(ORDER BY id)AS rowNum, * FROM [webDBs].[dbo].[employeeRecognition] WHERE [submitDate] &gt;= Convert(datetime,'20130301')
) AS E
WHERE rowNum &gt;= {0}
AND rowNum &lt; {1}";
</code></pre>

<p>These of course behaves exactly as expected. What I need to do, however, is make the 2013 part of the <code>Convert(datetime,'20130301')</code> bit actually equal to the current yet, so that we don't have to update this query every single year. </p>

<p>Based on my limited experience I started by trying to concatenate in a C# variable, not only did that not work, but after some research I learned that method can be an opening for potential SQL Injections. </p>

<p>I read a bit about parameterizing the SQL Query, but everything I saw on that led me to believe that I would have to rewrite/rethink how this data is being pulled from the database in the first place. </p>

<p>Any advice on how to accomplish my goal?</p>

<p>Here's what I'm working with:</p>

<pre><code>protected string RecordCount()
        {
            EmployeeRecognitionDataContext db = new EmployeeRecognitionDataContext();

            var sql = @"SELECT * FROM [database] WHERE [submitDate] &gt;= Convert(datetime,'20130301')";

            var query = db.ExecuteQuery&lt;employeeRecognition&gt;(sql);

            //return "[{\"count\":\"" + query.Count() + "\"}]";
            return query.Count().ToString();
        }
</code></pre>

<p>Function the second <code>var</code> is being used in:</p>

<pre><code> protected string SelectRecords(int startIndex, int pageSize) {

            int rowNum = startIndex + pageSize;

            EmployeeRecognitionDataContext db = new EmployeeRecognitionDataContext();

            var sql = @"SELECT * FROM (
                        SELECT ROW_NUMBER() OVER(ORDER BY id)AS rowNum, * FROM [database] WHERE [submitDate] &gt;= Convert(datetime,'20130301')
                        ) AS E
                        WHERE rowNum &gt;= {0} 
                        AND rowNum &lt; {1}";

            var query = db.ExecuteQuery&lt;employeeRecognition&gt;(sql, startIndex, rowNum);

            List&lt;Employee&gt; eList = new List&lt;Employee&gt;();

            foreach (var employee in query)
            {
                eList.Add(new Employee { 
                    value = employee.id.ToString(),
                    firstName = employee.firstName, 
                    lastName = employee.lastName, 
                    department = employee.department,
                    drop = employee.shortAchievement, 
                    recognition = employee.longAchievement,
                    submitDate = employee.submitDate.ToString()
                });

            }

            JavaScriptSerializer serializer = new System.Web.Script.Serialization.JavaScriptSerializer();

            return serializer.Serialize(eList);
        }
</code></pre>

## Answers
### Answer ID: 18494108
<p>You could just change the code which generates that string. Something like; </p>

<pre><code>   String.Format(@"SELECT * FROM [database] WHERE [submitDate] &gt;= Convert(datetime,'{0}0301')", DateTime.Now.Year.ToString());
</code></pre>

<p>Will make it so the string always has the current year there.</p>

<p>The docs for <code>String.Format</code> can be found here <a href="http://msdn.microsoft.com/en-us/library/system.string.format.aspx" rel="nofollow">http://msdn.microsoft.com/en-us/library/system.string.format.aspx</a></p>

<p>It basically works like this. You call <code>String.Format</code> with the first argument being your string. Within that string, you put format specifiers (the <code>{0}</code> is a format specifier). Each instance of <code>{x}</code> is replaced with the corresponding argument. So, you can do something like this;</p>

<pre><code>   string replacingThreeValues = String.Format("Replacing {0}, {1}, {2}", "one", "two", "three");
</code></pre>

<p>And it will result in <code>replaceingThreeValues == "Replacing one, two, three"</code>. So in your second example of <code>var sql = ...</code> you've put in some format specifiers, but you're not calling Format, also you're not passing any arguments to replace those values with. Instead you just get a string with the literal {0} and {1} in it. Only when you're calling <code>String.Format</code> and passing the appropriate arguments will those values be replaced with the arguments you pass it. </p>

### Answer ID: 18494386
<p>I don't know what the rest of your code looks like but here's a possible example of using parameters.    </p>

<pre><code>using (SqlConnection connection = new SqlConnection("&lt;connection string&gt;"))
{
    var cmd = connection.CreateCommand();
    cmd.CommandText = @"SELECT * FROM [database] WHERE [submitDate] &gt;= @myDate";
    DateTime myDate = DateTime.Parse("&lt;date string&gt;");
    cmd.Parameters.AddWithValue("@myDate", myDate);
    var reader = cmd.ExecuteReader();
    /* etc. */
}
</code></pre>

