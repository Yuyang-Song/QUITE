# Convert string to int in linq-to-sql query: how to deal with values which cannot be converted?
[Link to question](https://stackoverflow.com/questions/16773316/convert-string-to-int-in-linq-to-sql-query-how-to-deal-with-values-which-cannot)
**Creation Date:** 1369657974
**Score:** 3
**Tags:** c#, .net, linq-to-sql
## Question Body
<p>I'm running this query against a database:</p>

<pre><code>var result = (from leads in dc.T_DM_FactDemandeWebLeads
                         join  demands in dc.T_DM_DimDemandeWebs on leads.DemandeWeb_FK equals demands.DemandeWeb_PK
                         join  temps in dc.T_DM_Temps on demands.DateDemande_FK equals temps.Temps_PK
                         where leads.longitudeClient != null &amp;&amp; (Convert.ToInt32(leads.GeolocDistanceRouteDistrib) &gt; 1000*30) &amp;&amp; (temps.Date &gt; new DateTime(2000, 1, 1).Date)
                         select new Lead
                         {

                             lng = leads.longitudeClient,     

                             lat = leads.latitudeClient,

                             distance = leads.GeolocDistanceRouteDistrib

                         }).Take(1000000);
</code></pre>

<p><strong>Problem:</strong> This line is buggy:</p>

<pre><code>(Convert.ToInt32(leads.GeolocDistanceRouteDistrib) &gt; 1000*30)
</code></pre>

<p>as leads.GeolocDistanceRouteDistrib is a VARCHAR which takes "Unknown" in some cases, leading to a <a href="http://msdn.microsoft.com/en-us/library/sf1aw27b.aspx" rel="nofollow noreferrer">format exception</a>:</p>

<pre><code>Conversion failed when converting the varchar value 'Unknown' to data type int.
</code></pre>

<p>This problem is solved <a href="https://stackoverflow.com/questions/4961675/linq-select-parsed-int-if-string-was-parseable-to-int">here</a>, but the method cannot be converted to SQL.</p>

<p><strong>Question</strong>: is there any way to rewrite the query so the conversion is done during the execution of the query?</p>

## Answers
### Answer ID: 49665121
<p>Add <strong>.AsEnumerable()</strong> to your entity, then you can use all mothods </p>

<pre><code>var result = (from leads in dc.T_DM_FactDemandeWebLeads.AsEnumerable()
                         join  demands in dc.T_DM_DimDemandeWebs on leads.DemandeWeb_FK equals demands.DemandeWeb_PK
                         join  temps in dc.T_DM_Temps on demands.DateDemande_FK equals temps.Temps_PK
                         where leads.longitudeClient != null &amp;&amp; (Convert.ToInt32(leads.GeolocDistanceRouteDistrib) &gt; 1000*30) &amp;&amp; (temps.Date &gt; new DateTime(2000, 1, 1).Date)
                         select new Lead
                         {
                             lng = leads.longitudeClient,     
                             lat = leads.latitudeClient,
                             distance = leads.GeolocDistanceRouteDistrib
                         }).Take(1000000);
</code></pre>

### Answer ID: 16773481
<p>Use the technique in <a href="https://stackoverflow.com/a/950162/261050">this answer</a> to create the IsNumeric sql function in your dbml file.
And use it in your query.</p>

<p>Something like this:</p>

<pre><code>join  temps in dc.T_DM_Temps on demands.DateDemande_FK equals temps.Temps_PK
where dc.ISNUMERIC(leads.GeolocDistanceRouteDistrib) // Added!
where leads.longitudeClient != null &amp;&amp; (Convert.ToInt32(leads.GeolocDistanceRouteDistrib) &gt; 1000*30) &amp;&amp; (temps.Date &gt; new DateTime(2000, 1, 1).Date)
select new Lead
</code></pre>

