# how to show details of user into gridview where 1st girdview contain list of link button
[Link to question](https://stackoverflow.com/questions/18310269/how-to-show-details-of-user-into-gridview-where-1st-girdview-contain-list-of-lin)
**Creation Date:** 1376903767
**Score:** 0
**Tags:** c#, asp.net, gridview, linkbutton
## Question Body
<p>I have 2 grid-view on the same page </p>

<ul>
<li>1st contain the link button where text on the link button is the name of the user comes from database to show user specific details.</li>
<li>2nd grid-view to show the selected user details</li>
</ul>

<p>Now when user click on link from first grid-view then it can view the details of that user in second grid-view.</p>

<pre><code>&lt;asp:GridView ID="GridView1" runat="server" DataSourceID="SqlDataSource1"
    DataKeyNames="ID" AutoGenerateSelectButton="true"  AllowPaging="True" pagesize ="5"  /&gt;
    &lt;br /&gt;&lt;b&gt;&lt;u&gt;Store Details&lt;/u&gt;&lt;/b&gt;&lt;br /&gt;&lt;br /&gt;
    &lt;asp:DetailsView id="DetailsView1" DataSourceID="SqlDataSource2"
    DataKeyNames="ID" AllowPaging ="true" Runat="server" /&gt;
    &lt;asp:SqlDataSource ID="SqlDataSource1" runat="server"
    ConnectionString="&lt;%$ ConnectionStrings:TestingConnectionString %&gt;"
    SelectCommand="select * from UserDetails" /&gt;
    &lt;asp:SqlDataSource ID="SqlDataSource2" runat="server"
    ConnectionString="&lt;%$ ConnectionStrings:TestingConnectionString %&gt;"
    SelectCommand="select * from UserDetails WHERE ID=@ID" &gt;
    &lt;SelectParameters&gt;
       &lt;asp:ControlParameter Name="ID" ControlID="GridView1" /&gt;
    &lt;/SelectParameters&gt;
    &lt;/asp:SqlDataSource&gt;
</code></pre>

<p>By using above code i get what i want but i have one more query i.e. i want to use link button because i also using url rewriting so for that i need to link button for every user so that i can change my url also for that user</p>

<p>Thanks in advance</p>

## Answers
### Answer ID: 18310375
<p>here are two Master/Detail Example with asp.net</p>

<p><a href="http://www.vkinfotek.com/detailsview/gridview-detailsview-master-detail-example.html" rel="nofollow">http://www.vkinfotek.com/detailsview/gridview-detailsview-master-detail-example.html</a></p>

<p><a href="http://www.codeproject.com/Articles/16779/GridView-DetailsView-Master-Detail-Control" rel="nofollow">http://www.codeproject.com/Articles/16779/GridView-DetailsView-Master-Detail-Control</a></p>

