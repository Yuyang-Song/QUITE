# Trying to query two mysql databases with python and write the result in google sheets (auto-update every day)
[Link to question](https://stackoverflow.com/questions/67004539/trying-to-query-two-mysql-databases-with-python-and-write-the-result-in-google-s)
**Creation Date:** 1617886870
**Score:** 1
**Tags:** python, mysql, google-sheets, google-sheets-api
## Question Body
<p>My data is divided in two mysql databases with the same structure.</p>
<p>What I am trying to do is write a python script that extracts and appends the data from both databases, stores it in a variable or a text file (let's say somefile.csv) and then another script gets the data from the variable/text file and imports it in google sheets through the google sheets api. The caveat is that my data changes every day and I also want both scripts to update automatically (run each day and fetch the updated data, the first to rewrite the csv and the second the google sheet with the new data from the csv).</p>
<p>Is that possible?</p>
<p>What I have so far is:</p>
<p>The first script:</p>
<pre><code>from mysql.connector import connect, Error

username = &quot;user&quot;
password = &quot;pass&quot;

connection_1 = connect(
    host=&quot;hostaddress&quot;,
    user=username,
    password=password,
    database=&quot;databasename&quot;
)

connection_2 = connect(
    host=&quot;hostaddress&quot;,
    user=username,
    password=password,
    database=&quot;databasename&quot;
)

cursor_1 = connection_1.cursor()
cursor_2 = connection_2.cursor()

q1 = open('query_db1.sql', 'r')
query1 = q1.read()
q1.close()

q2 = open('query_db2.sql', 'r')
query2 = q2.read()
q2.close()

try:
    with connection_1:
        with cursor_1:
            cursor_1.execute(query_1)
            for row in cursor_1.fetchall():
                print(row)
    with connection_2:
        with cursor_2:
            cursor_2.execute(query2)
            for row in cursor_2.fetchall():
                print(row)
except Error as e:
    print(e)
</code></pre>
<p>The two problems I am facing in this script are:</p>
<ol>
<li>how to store the data from the executed queries in one variable or save it to one file?</li>
<li>how to make that script query the databases every day and update the stored information?</li>
</ol>
<p>In the second script, I have</p>
<pre><code>from googleapiclient.discovery import build
from google.oauth2 import service_account

SERVICE_ACCOUNT_FILE = 'googleapicredentials.json'
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

creds = None
creds = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

SAMPLE_SPREADSHEET_ID = 'SHEET_ID'

service = build('sheets', 'v4', credentials=creds)

request = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID,
                            range=&quot;Sheet1!A1&quot;, valueInputOption=&quot;USER_ENTERED&quot;, body={&quot;values&quot;:&quot;somefile.csv&quot;}).execute()
</code></pre>
<p>Again, I don't know how to make that script update each day.</p>

## Answers
### Answer ID: 67020407
<h2>Answer</h2>
<p><strong>1. how to store the data from the executed queries in one variable or save it to one file?</strong></p>
<p>Use the module <a href="https://wiki.python.org/moin/UsingPickle" rel="nofollow noreferrer">pickle</a>. It's very easy to save and load variables.</p>
<p><strong>2. how to make that script query the databases every day and update the stored information?</strong></p>
<p>Use the module <a href="https://github.com/dbader/schedule" rel="nofollow noreferrer">schedule</a>. Once you have installed it, you can define the execution of a file as follows:</p>
<pre class="lang-py prettyprint-override"><code>import schedule
import time

def job():
    print(&quot;I'm working...&quot;)

schedule.every().day.at(&quot;10:30&quot;).do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
</code></pre>
<h2>References:</h2>
<ul>
<li><a href="https://wiki.python.org/moin/UsingPickle" rel="nofollow noreferrer">pickle</a></li>
<li><a href="https://github.com/dbader/schedule" rel="nofollow noreferrer">schedule</a></li>
</ul>

### Answer ID: 67004833
<p>I do this every day on multiple projects although I use google app script which is based on javascript.</p>
<p>You can set a Trigger (like a chron job), to run a function on a schedule of your choosing. Triggers are set in the script editor. Look for the hourglass icon. Optionally, you can set a Trigger based on code in the script.</p>
<pre><code>/**
 * Creates time-driven triggers
 *
 * https://developers.google.com/apps-script/reference/script/clock-trigger-builder
 */
function createTimeDrivenTriggers() {
  // Trigger every day at 04:00AM CT.
  ScriptApp.newTrigger('csvDaily')
      .timeBased()
      .everyDays(1)
      .atHour(4)
      .create();
}
</code></pre>
<p>Here is a code snippet showing the app script code to access my MySQL db, I removed the user name and passwords:</p>
<pre><code>const MAXROWS = 10000;
const HOST = '65.60.34.202';
const PORT = '3306';
const USERNAME = '';
const PASSWORD = '';
const DATABASE = 'agustafa_barnes';
const DB_TYPE = 'mysql';

function getL2s() {
  var L2s = [];
  try {
    var fullConnectionString = 'jdbc:' + DB_TYPE + '://' + HOST + ':' + PORT;
    var conn = Jdbc.getConnection(fullConnectionString, USERNAME, PASSWORD);
    var stmt = conn.createStatement();
    stmt.execute('USE ' + DATABASE);
    var query = &quot;SELECT * FROM L2s WHERE !IsDeleted ORDER BY TeamTL&quot;;
    var rs = stmt.executeQuery(query);

    while (rs.next()) {
      L2s.push([rs.getString(1), rs.getString(2), rs.getString(3), rs.getString(4), rs.getString(5)]);
    }
    rs.close();
    stmt.close();
  } catch (e) {
        console.log(e, e.lineNumber);
  }

  return L2s;
}
</code></pre>
<p>So, if accessing your db is off the table (I have the same issue with my company), perhaps you can set up some data extract routines. Our company has hundred of them and requires basic authorization. I issue a web request and then I can write the data to google sheets or to my own MySQL db. Here is an example URL we use:</p>
<pre><code>https://app.yourdomain.com/datadumper/report.ashx?reportid=5107&amp;startDate=2021-04-08&amp;endDate=2021-04-08&amp;bu=3&amp;currentuser=john.agusta&amp;__action=Export#
</code></pre>
<p>Then you can code the app script as follows:</p>
<pre><code>/*
https://modjeska.us/csv-google-sheets-basic-auth/
https://redfin.engineering/when-importdata-isnt-good-enough-retrieving-csv-files-behind-basic-auth-with-a-google-apps-script-6c563f3328c5
cm9iZXJ0Om9sZHRpcmVz -- this is a base 64-encoded string of the form

&lt;username&gt;:&lt;password&gt;. In this case, the value represents the username 'robert' and the password 'oldtires', so the string prior to encoding is: robert:oldtires

this site can be used to create a base 64-encoded string:

https://www.base64encode.net/


*/

const auth = '';

VAR URL = &quot;https://app.yourdomain.com/datadumper/report.ashx?reportid=5107&amp;startDate=2021-04-08&amp;endDate=2021-04-08&amp;bu=3&amp;currentuser=john.agusta&amp;__action=Export#&quot;;
var csvContents = getCSVContents(URL);
var parsedContents = parseCsvResponse(csvContents, true);

function getCSVContents(csvUrl) {
// request the CSV
    var resp = UrlFetchApp.fetch(csvUrl, {
        headers: {
            // use basic auth
            'Authorization': 'Basic ' + auth
        }
    });
  return resp.getContentText();
}

// parse the CSV response
function parseCsvResponse(csvString, ignoreHeaders) {
  var retArray = [];
  var numCols = 0;
  var i = 0;
  var j = 0;
  var line = &quot;&quot;;
  var strLines = csvString.split(/\n/g);
  if (ignoreHeaders) {
    strLines.shift();
  }
  var lenLines = strLines.length;  
  for (i = 0; i &lt; lenLines; i++) {
    line = strLines[i];
    if (line != '') {
      retArray.push(line.split(/,(?=(?:(?:[^&quot;]*&quot;){2})*[^&quot;]*$)/));
      numCols = retArray[i].length;
      // remove outer double quotes
      for (j = 0; j &lt; numCols; j++) {
        retArray[i][j] = retArray[i][j].replace(/^&quot;|&quot;$/g, '');
      }
    }
  }
  return retArray;
}
</code></pre>

