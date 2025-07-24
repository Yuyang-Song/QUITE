# query filtering, finding the balance between flexibility and ease of execution
[Link to question](https://stackoverflow.com/questions/20621302/query-filtering-finding-the-balance-between-flexibility-and-ease-of-execution)
**Creation Date:** 1387229448
**Score:** 3
**Tags:** sql, forms, ms-access, vba, filtering
## Question Body
<p>So I've been researching for days now on how to filter a rowsource result on a control in a way that is comfortable, hopefully you understand what I mean by that as I explain. I have found solutions, a bunch of solutions. I'm more concerned with evaluating their benefits and negatives.</p>

<p>I have a specific example, but my concern is really more generic. This, to me, seems like the backbone of my application and so I want to make sure it's being done correctly, the best way, not just in a way that "works".</p>

<p>Basically, I have progressive combo box filters. The first box filters the second box, which then selects a record in a Single Form view. The two combo boxes are in the header of the form.</p>

<p>Lets say I have a table CanadianCities. The two combo boxes might be, cboProvinceFilter "Filter by Province", and cboCitySelect "Select City"</p>

<p>When I load the form the province filter is off, so the cities list is populated with a rowsource that selects ALL the cities (SELECT ID, CityName FROM CanadianCities). But that's a big list, so I have the second combo box to narrow that list down by province (SELECT ID, ProvinceName FROM CanadianProvinces).</p>

<p>So the goal is that on cboProvinceFilter.AfterUpdate to requery cboCitySelect with an altered where clause ("[...] WHERE ProvinceID = [cboProvinceFilter]").</p>

<p>The problem is in how to alter the where clause. Ideally, the above would work right in the designer, but SQL designs seem to be out of the form's scope so cboProvinceFilter doesn't exist there. I agree with the opinion that direct referencing forms is bad. I don't want to marry my sql to the form like that. Plus, I want to use a navigation form, but also have a mobile option, so running the forms individually AND in navigation would be ideal, absolute referencing can't do this.</p>

<p>Having my repetitious SQL statements buried in code feels like poor design, and repeating the same queries with slightly different filtering is terrible when Parameters are exactly for that reason.</p>

<p>And some will scoff at this, but it also feels bad to rewrite the functionality of the Access designer in VBA. If I build my own SQL, execute my own queries, and populate my own lists, why did Microsoft put all the effort into building this productivity assisting tool for? Filtering is not exactly an obscure feature of database management... I feel like there must be a reasonable way to do this sort of thing.</p>

<p>Also, popup forms are obnoxious, so I won't be making specific forms just to have reliable absolute references. That definitely feels like a cop-out.</p>

<p>Solutions that do feel good but I haven't made work...</p>

<p><strong>SQL Parameters</strong>
The most sensible way of doing this I feel should be with SQL Parameters, as that's what they're intended for right? The QueryDef would store values for it's parameters that could I could change as needed. However, I would let the queries execute naturally on requery.</p>

<p>So instead of writing the handful of lines to execute the Query and populate the control, I'd just set the parameter values and call requery on my control, which has all that functionality built into it.</p>

<p>So defined some parameters in the SQL statement, then tried to set the values of those parameters in VBA before the Query was executed, but JET always seems to pop-up for the parameters if it doesn't reference an actual object, it wasn't checking my code-set querydefs.</p>

<p>For that to work, it seems that I'd have to execute the SQL manually, and parse my own recordset, and populate the control. Which feels like an excessive amount of repetition for every filter option I'd want to offer.</p>

<p><strong>Relative Referencing</strong>
I don't mind referencing forms as long as it's a relative path. Unfortunately [Screen].[ActiveForm] refers to the navigation form, not the actual, active form... So that seems to be out.</p>

<p>Right now I'm thinking my only option is to set rowsource manually then call the control's requery. that's the less offensive feeling option. Might be best to take the current query and string replace the where portion, so i don't have to update every event if the query structure changes.</p>

<p><strong>Final Thought</strong>
Anyway, this is getting ranty, so let me know your thoughts. I'm not really looking for code solutions, which is why I offered few to no hard examples. I'm looking for a paradigm for managing this kind of filtering that isn't too restrictive (absolute referencing) or too repetitive/wheel-re-inventing (hard coded sql, executing, control populating).</p>

## Answers
### Answer ID: 20641219
<p>If your Access version is >= 2007, you can use the <em>TempVars Collection</em>.  Here is an Immediate window session.</p>

<pre class="lang-vb prettyprint-override"><code>' add a TempVar with value
TempVars.which_id = 12
' or do it explicitly with Add method
TempVars.Add "which_id", 12
? TempVars!which_id
 12 
' asking for the value of non-existent TempVar returns Null
? TempVars!bogus
Null
</code></pre>

<p>A query can reference the TempVar to filter the result set.  </p>

<pre class="lang-sql prettyprint-override"><code>SELECT f.*
FROM tblFoo AS f
WHERE f.id=[TempVars]![which_id] OR [TempVars]![which_id] Is Null;
</code></pre>

<p>So you could use that approach in the row source query for the <em>cboCitySelect</em> combo box.  Then assign the TempVar value in the After Update event of <em>cboProvinceFilter</em> and next <code>Requery</code> <em>cboCitySelect</em>.</p>

<p>For Access versions &lt; 2007, the <em>TempVars Collection</em> is not available.  In that situation you could use a custom VBA function to hold a static value which can be referenced in a query.</p>

<pre class="lang-sql prettyprint-override"><code>SELECT f.*
FROM tblFoo AS f
WHERE f.id=TargetId() OR TargetId() Is Null;
</code></pre>

<pre class="lang-vb prettyprint-override"><code>Public Function TargetId(Optional ByVal pValue As Variant) As Variant
    Static varReturn As Variant
    If IsMissing(pValue) Then
        If VarType(varReturn) = vbEmpty Then
            varReturn = Null
        End If
    Else
        varReturn = pValue
    End If
    TargetId = varReturn
End Function
</code></pre>

