# DD anomaly, and cleaning up database resources: is there a clean solution?
[Link to question](https://stackoverflow.com/questions/10752654/dd-anomaly-and-cleaning-up-database-resources-is-there-a-clean-solution)
**Creation Date:** 1337941219
**Score:** 6
**Tags:** jdbc, findbugs, pmd, dataflow
## Question Body
<p>Here's a piece of code we've all written:</p>

<pre>
    public CustomerTO getCustomerByCustDel(final String cust, final int del)
            throws SQLException {
        final PreparedStatement query = getFetchByCustDel();
        ResultSet records = null;
        try {
            query.setString(1, cust);
            query.setInt(2, del);
            records = query.executeQuery();

            return this.getCustomer(records);
        } finally {
            if (records != null) {
                records.close();
            }
            query.close();
        }
    }
</pre>

<p>If you omit the 'finally' block, then you leave database resources dangling, which obviously is a potential problem. However, if you do what I've done here - set the ResultSet to null outside the **try** block, and then set it to the desired value inside the block - PMD reports a 'DD anomaly'. In the documentation, a DD anomaly is described as follows:</p>

<blockquote>
DataflowAnomalyAnalysis: The dataflow analysis tracks local definitions, undefinitions and references to variables on different paths on the data flow.From those informations there can be found various problems. [...] DD - Anomaly: A recently defined variable is redefined. This is ominous but don't have to be a bug.
</blockquote>

<p>If you declare the ResultSet outside the block without setting a value, you rightly get a 'variable might not have been initialised' error when you do the <i>if (records != null)</i> test.</p>

<p>Now, in my opinion my use here isn't a bug. But is there a way of rewriting cleanly which would not trigger the PMD warning? I don't particularly want to disable PMD's DataFlowAnomalyAnalysis rule, as identifying UR and DU anomalies would be actually useful; but these DD anomalies make me suspect I could be doing something better - and, if there's no better way of doing this, they amount to clutter (and I should perhaps look at whether I can rewrite the PMD rule)</p>

## Answers
### Answer ID: 18998211
<p>I think that DD anomaly note is more bug, than a feature<br/>
Also, the way you free resources is a bit incomplete, for example</p>

<pre><code>PreparedStatement pstmt = null;
Statement st = null; 

try {
    ...
} catch (final Exception e) {
    ...
} finally {
    try{
        if (pstmt != null) {
            pstmt.close();
        }
    } catch (final Exception e) {
        e.printStackTrace(System.err);
    } finally {
        try {
            if (st != null) {
                st.close();
            }
        } catch (final Exception e) {
            e.printStackTrace(System.err);
        }
    }
}
</code></pre>

<p>moreover this is not right again, cuz you should close resources like that</p>

<pre><code>PreparedStatement pstmt = null;
Throwable th = null;

try {
    ...
} catch (final Throwable e) {
    &lt;something here&gt;
    th = e;
    throw e;
} finally {
    if (th == null) {
        pstmt.close();
    } else {
        try {
            if (pstmt != null) {
                pstmt.close();
            }
        } catch (Throwable u) {
        }
    }
}
</code></pre>

### Answer ID: 10762404
<p>I think this is clearer:</p>

<pre><code>PreparedStatement query = getFetchByCustDel();
try {
    query.setString(1, cust);
    query.setInt(2, del);
    ResultSet records = query.executeQuery();
    try {
        return this.getCustomer(records);
    } finally {
        records.close();
    }
} finally {
    query.close();
}
</code></pre>

<p>Also, in your version the query doesn't get closed if records.close() throws an exception.</p>

