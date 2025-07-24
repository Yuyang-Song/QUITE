# Javascript hide Gridview rows with blank field
[Link to question](https://stackoverflow.com/questions/35588731/javascript-hide-gridview-rows-with-blank-field)
**Creation Date:** 1456263553
**Score:** 0
**Tags:** javascript, asp.net, gridview
## Question Body
<p>I am rewriting a site in .Net, and I am trying to reproduce some functionality of the original site, but I have hit a stumbling block.</p>

<p>I have a gridview table where the 12th column, column(11) is a date field.  I am attempting to keep querying the SQL database, so I am loading all the rows for my criteria, and I have a pair radio buttons.  One shows all records, the other I just want to show the records where the date field is blank, or in the case of the Gridview, <code> &amp;nbsp ; </code></p>

<p>So I have a function that does something similar on another page, but instead of looking for a value in a traditional sense, I am looking for cells that have <code> &amp;nbsp ; </code> in them.  Everything I try is failing.  Here is what i have, but I am not sure where to go from here:</p>

<pre><code>    function refinesearch(x) {
        var rows = $("#GridView1 tr:gt(0)");
        if (x == 1) {
            $("#GridView1 tr").show();
        }
        else {
            $("#GridView1 tr").hide();
            var rowToShow = rows.find("td:eq(12)").filter(":contains('&amp;nbsp;')").closest("tr");
            rows.show().not(rowToShow).hide();
        }
    }
</code></pre>

<p>What I am getting is 0 rows shown.  It is working perfectly for non special values, but i don't know enough javascript to fix the test.  Anyone have thoughts?</p>

## Answers
### Answer ID: 35604572
<p>After a good nights sleep, I got this working:</p>

<pre><code>    function refinesearch(x) {
        $("#GridView1 tr").hide();
        var rows = $("#GridView1 tr:gt(0)");
        if (x == 1) {
            $("#GridView1 tr").show();
        }
        else {
            $("#GridView1 tr").each(function () { //loop over each row
                if (($(this).find("td:eq(11)").html() == '&amp;nbsp;') || ($(this).find("th:eq(11)").text() == 'Index Date')) { //check value of TD and include table header row
                    $(this).show(); //show the row 
                }
            });
        }
    }
</code></pre>

<p>I am extremely interested in linq queries after doing some reading on the topic, and I think that going forward, it will be a much more robust solution.</p>

