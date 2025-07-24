# Triggering JavaScript by hitting enter, enabling multiple searches/AJAX queries/DataTable displays without refreshing web page
[Link to question](https://stackoverflow.com/questions/59571139/triggering-javascript-by-hitting-enter-enabling-multiple-searches-ajax-queries)
**Creation Date:** 1578006259
**Score:** 0
**Tags:** javascript, jquery, html, ajax, datatables
## Question Body
<p>I have a web page with an AWS API interface to query an RDS Aurora MySQL Serverless database. When a user types in a SQL statement and hits the Query button, an AJAX request will be triggered, JSON will be returned and the test-table table below will be converted to a DataTable.</p>

<pre><code>            &lt;div class="container-fluid"&gt;
                &lt;div class="row"&gt;
                    &lt;div class="col-xs-12 col-sm-12 col-md-12 col-lg-12"&gt;
                        &lt;p&gt;Please enter a SQL query below&lt;/p&gt;
                        &lt;p&gt;Do not wrap your query in outer quotation marks.&lt;/p&gt;
                        &lt;p&gt;For database structure information, please select "Learn About the Database" above.&lt;/p&gt;
                    &lt;/div&gt;
                &lt;/div&gt;
                &lt;div class="row"&gt;
                    &lt;div class="col-xs-11 col-sm-11 col-md-11 col-lg-11"&gt;
                        &lt;div class="active-cyan-4 mb-4"&gt;
                            &lt;input id="sql-placeholder" class="form-control" type="text" placeholder="Write SQL here..." aria-label="Search"&gt;
                        &lt;/div&gt;
                    &lt;/div&gt;
                    &lt;div class="col-xs-1 col-sm-1 col-md-1 col-lg-1"&gt;
                        &lt;button id="query-button" type="button" class="btn btn-primary" onclick="DisplayQuery()"&gt;Query&lt;/button&gt;
                    &lt;/div&gt;
                &lt;/div&gt;
            &lt;/div&gt;

            &lt;div class="container-fluid"&gt;
                &lt;table id="test-table" class="table table-striped table-bordered dt-responsive nowrap" cellspacing="0" width="100%"&gt;
                &lt;/table&gt;
            &lt;/div&gt;
</code></pre>

<p>The JavaScript for the onclick="DisplayQuery()" function is below.</p>

<pre><code>var DisplayQuery;
(function($) {
  DisplayQuery = function() {
    $.ajax({
      method: 'POST',
      url: '*****',
      beforeSend: function(xhr) {
        xhr.setRequestHeader("access-control-allow-origin", "*")
            },
      data: JSON.stringify({
        "sqlStatement": $('#sql-placeholder').val()
      }),
      contentType: 'application/json',

      success: function(response) {

        // Get columns labels as list of dictionaries colLabels
        var colLabels = [];
        for (i = 0; i &lt; response.sqlStatementResults[0].resultFrame.resultSetMetadata.columnMetadata.length; i++) {
          colLabels.push({
            title: response.sqlStatementResults[0].resultFrame.resultSetMetadata.columnMetadata[i].name
          }); 
        };

        // Get data rows as array of arrays dataRows3
        var dataRows = response.sqlStatementResults[0].resultFrame.records;
        var dataRows2 = [];
        var dataRows3 = [];

        for (i = 0; i &lt; dataRows.length; i++) {
          dataRows2.push(dataRows[i].values);
        };

        dataRows2.forEach(arr =&gt; {
          rowVals = [];
          arr.forEach(e =&gt; {
            Object.entries(e).forEach(k =&gt; rowVals.push(k[1]))
          });
          dataRows3.push(rowVals);
        });

        try {
          $('#test-table').destroy();
        } finally {

        // Write DataTable from colLabels and dataRows3
        $('#test-table').DataTable({
          data: dataRows3,
          columns: colLabels,
          scrollX: true
        });
      }
    },

      error: function ajaxError(error) {
        console.error('Error in query processing; please try again.');
      }
    })
  }
}(jQuery));
</code></pre>

<p>Is there a way to add to/rewrite this JavaScript so that the query can also be triggered by typing into the sql-placeholder and hitting enter instead of clicking on the query-button? Also, is there a way to allow multiple searches without having to reload the web page? In other words, if you query, then go type something new into the sql-placeholder and hit enter or click the query-button, a new query will be triggered, the previous results will be removed, and the new results will be displayed?</p>

## Answers
### Answer ID: 59571256
<p>You can use the <code>keydown</code> event listener to check which key the user typed and if the key used was the one you want (in this case Enter) call the function.</p>

<p><a href="https://developer.mozilla.org/en-US/docs/Web/API/Document/keydown_event" rel="nofollow noreferrer">onkeypress reference</a></p>

<p>For example:</p>

<pre><code>document.getElementById('#sql-placeholder').onkeypress = function(e) {
  var keyCode = e.keyCode || e.which
  if (keyCode === '13') {
    // Enter pressed
    DisplayQuery()
  }
}
</code></pre>

### Answer ID: 59571252
<p>Either wrap them in a form and catch the submit event as Nick mentioned or a simple way is</p>

<pre><code>$('#sql-placeholder').keypress(function(e) {
  if(e.which == 10 || e.which == 13) {
    DisplayQuery();
  }
})
</code></pre>

