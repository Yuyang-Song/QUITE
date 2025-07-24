# ASP.NET WebForms -- Processing special query-string parameters across all pages on a site -- URL Rewriting, URL Routing, or other approaches?
[Link to question](https://stackoverflow.com/questions/3119579/asp-net-webforms-processing-special-query-string-parameters-across-all-pages)
**Creation Date:** 1277481988
**Score:** 1
**Tags:** asp.net, webforms, url-rewriting, url-routing, httpmodule
## Question Body
<p>Working on an ecommerce site which will be integrated with a 3rd party vendor--that vendor uses different identifiers for stores than we use internally (i.e. their store ABC123 is our 001-321).</p>

<p>I'm researching the best approach to inspect incoming requests for reserved query-string parameters that indicate the request is using <em>their</em> identifiers and map the identifiers back to our identifiers (so if the request is example.com/&amp;theirId=ABC123 I want to transform the request to example.com/&amp;ourId=001-321).</p>

<p>To do this mapping I need to inspect the provided ID, execute a lookup against the database or cache, and forward the request to the specified page--limiting the modifications to just the query-string parameters (other parameters will need to be maintained, as with the details of the HTTPHeader, etc).</p>

<p>So far I'm researching a few different approaches:</p>

<ul>
<li>Implementing it in a base Page (which already does too much, but has the benefit of our Logging infrastructure and some other injected dependencies)</li>
<li>Implementing it in an IHttpModule</li>
<li>Using URL Rewriting</li>
<li><strike>Using URL Routing</strike> <em>(looks like routing isn't what I want, feel free to offer insight if you think it still fits)</em></li>
</ul>

<p>Performance cost is a consideration: the actual number of times this translation will occur will be very small compared to the number of requests <em>not</em> requiring it--perhaps 1%.</p>

<p><strong><em>However</em></strong> for another integrated site we will perform this mapping on nearly every request--would a different approach be better suited to this scenario from the previous?</p>

## Answers
### Answer ID: 3120170
<p>I usually create a Singleton class to hold the site's request context, and store it in the HttpContext.Current.Items(). I initialize this class in the Application_BeginRequest routine. </p>

<pre><code>Imports System.Web
</code></pre>

<p>Public Class SiteContext</p>

<pre><code>Private _viewId As Int32 
Private _tab As String
Private _action As String

Private Sub New()
    _viewId = -1
    _tab = String.Empty
    _action = String.Empty

    FillContext()
End Sub

Public Shared Function Instance() As SiteContext
' gets the site specific context for the current request

    If HttpContext.Current.Items("RequestContext") Is Nothing Then
        HttpContext.Current.Items("RequestContext") = New SiteContext
    End If
    Return HttpContext.Current.Items("RequestContext")

End Function

' fill the request context with site specific items
Private Sub FillContext()

    ' iterate through all items passes via the querystring and save values to matching key property names
    For i As Int16 = 0 To _context.Request.QueryString.Count - 1
        Dim qryItem As String = _context.Request.QueryString.Keys.Item(i)

        Select Case qryItem
            Case "v", "view", "viewid", "vid" ' VIEW ID
                If IsNumeric(_context.Request.QueryString(qryItem)) AndAlso CType(_context.Request.QueryString(qryItem), Double) &lt; 10000 Then
                    _viewId = CType(_context.Request.QueryString(qryItem), Int32)
                End If

            Case "tab" ' TAB ID; secondary parameter to choose sub view
                _tab = _context.Request.QueryString(qryItem)

            Case "action" ' ACTION ID; tertiary parameter to choose sub-sub view
                _action = _context.Request.QueryString(qryItem)

            Case Else

        End Select
    Next

End Sub

Public Property ViewId() As Int32
    Get
        Return _viewId
    End Get
    Set(ByVal Value As Int32)
        If Value &lt; 1 Then
            Value = 1
        End If
        _viewId = Value
    End Set
End Property

Public Property Tab() As String
    Get
        Return _tab
    End Get
    Set(ByVal Value As String)
        _tab = Value.Trim
    End Set
End Property

Public Property Action() As String
    Get
        Return _action
    End Get
    Set(ByVal Value As String)
        _action = Value.Trim
    End Set
End Property
</code></pre>

<p>End Class</p>

### Answer ID: 3119873
<p>This is a classic case where a HTTP module makes the most sense--you wish to dive into the URL handling on all requests. Perf-overhead-wise you shouldn't have that much of an issue presuming you can short-circuit things correctly and avoid doing DB/cache lookups where you don't need.</p>

<p>Configuration-wise, you should already have to solve the problem of deploying and managing your configuration, so I doubt if another custom module adds much overhead.</p>

<p>Code-wise, its generally better to favor composition over inheritance--you can add or remove the module as required--but having code statically included into a bloated base page class can create more challenges.</p>

### Answer ID: 3119651
<p>I have implemented something similar to this as a base page class for my aspx pages, but as you mentioned a module would work as well. In my opinion, if this functionality is needed across all pages I would just crate a base class only because maintaining another http-module is more of a pain because it needs to be mapped in your web config / iis. Url rewriting is cpu intensive and may not provide you the flexibility you need - again it just adds another configuration / iss dependency. I don't think either of these are going to incur much overhead as long as you implement some sort of caching.  </p>

<p>Hope this helps...</p>

<p>Enjoy!</p>

