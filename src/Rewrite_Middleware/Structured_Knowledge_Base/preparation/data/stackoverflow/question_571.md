# LINQ query: restrict child entity
[Link to question](https://stackoverflow.com/questions/32115172/linq-query-restrict-child-entity)
**Creation Date:** 1440064760
**Score:** 0
**Tags:** c#, linq
## Question Body
<p>I'm novice in LINQ, so I need an initial help how to simplify writing of LINQ queries. Here my scenario: I have two tables C_Systemtype with 1:M relationship to CT_Systemtype, using database first approach.</p>

<p><strong>Class C_System:</strong></p>

<pre><code>{
    public string SystemtypeId { get; set; }
    public bool Is_productive { get; set; }
    public bool Is_systemown { get; set; }
    public bool Is_active { get; set; }
    public byte[] Icon { get; set; }

    public virtual ICollection&lt;CT_Systemtype&gt; CT_Systemtype { get; set; }
    public virtual ICollection&lt;C_System&gt; C_System { get; set; }
}
</code></pre>

<p><strong>Class CT_Systemtype:</strong></p>

<pre><code>{
    public string SystemtypeId { get; set; }
    public string LanguageId { get; set; }
    public string Title { get; set; }
    public string Descript { get; set; }    
    public virtual C_Systemtype C_Systemtype { get; set; }
    public virtual S_Language S_Language { get; set; }
}
</code></pre>

<p>I like to select all C_Systemtype but with CT_Systemtype restricted to a given LanguageId.</p>

<p>I believe the following LINQ query is working (p_langId is my parameter):</p>

<pre><code>using (var db = new PaltrConnect())
        { var query = from s in db.C_Systemtype
                      join t in db.CT_Systemtype on s.SystemtypeId equals t.SystemtypeId
                      where t.LanguageId == p_langId 
                      select new { s.Is_productive,
                                   s.Is_systemown,
                                   s.Is_active,
                                   s.Icon,
                                   s.CT_Systemtype }
         }
</code></pre>

<p>The result is of type anonymous. My intention is something like C_Systemtype.Include(t => t.CT_Systemtype) but with additional restriction on CT_Systemtype.</p>

<p>How can I rewrite this query in such a way that I don't have to give each property in the select part and to finally map individual properties?</p>

## Answers
### Answer ID: 32120236
<pre><code>using (var db = new PaltrConnect())
{ 
var query = from s in db.C_Systemtype
                  join t in db.CT_Systemtype on s.SystemtypeId equals t.SystemtypeId
                  where t.LanguageId == p_langId 
                  select s ;/*s is your C_Systemtype*/
     }
</code></pre>

### Answer ID: 32116047
<p>Because you are joining two tables together you can't just return a single type. To prevent having to map each property in the select you can use something like AutoMapper. </p>

