# I can&#39;t read the results of the openstreetmap api with vba
[Link to question](https://stackoverflow.com/questions/70177746/i-cant-read-the-results-of-the-openstreetmap-api-with-vba)
**Creation Date:** 1638318564
**Score:** 0
**Tags:** xml, vba, api, openstreetmap, nominatim
## Question Body
<p>I have a database of addresses in MSAccess. I would like to fill in the gps coordinates (latitude and longitude) automatically. I found a VBA script that retrieves data from google, but I would like to rewrite this script to retrieve data from openstreetmap.
the script I am modifying :</p>
<pre><code>Public Function GetCoordinates(address As String) As String

    'Written By:    Christos Samaras
    'Date:          12/06/2014
    'Last Updated:  16/02/2020
    'E-mail:        xristos.samaras@gmail.com
    'Site:          https://www.myengineeringworld.net
    '-----------------------------------------------------------------------------------------------------
    
    'Declaring the necessary variables.
    Dim apiKey              As String
    Dim xmlhttpRequest      As Object
    Dim xmlDoc              As Object
    Dim xmlStatusNode       As Object
    Dim xmlLatitudeNode     As Object
    Dim xmLongitudeNode     As Object
    
    'Set your API key in this variable. Check this link for more info:
    'https://www.myengineeringworld.net/2018/02/how-to-get-free-google-api-key.html
    'Here is the ONLY place in the code where you have to put your API key.
    apiKey = &quot;XXXXXXXXXXXXXXXXXXXXXXXXXX&quot;
    
    'Check that an API key has been provided.
    If apiKey = vbNullString Or apiKey = &quot;The API Key&quot; Then
        GetCoordinates = &quot;Empty or invalid API Key&quot;
        Exit Function
    End If
    
    'Generic error handling.
    On Error GoTo errorHandler
    
    'Create the request object and check if it was created successfully.
    Set xmlhttpRequest = CreateObject(&quot;MSXML2.ServerXMLHTTP&quot;)
    
    If xmlhttpRequest Is Nothing Then
        GetCoordinates = &quot;Cannot create the request object&quot;
        Exit Function
    End If
    
    'Create the request based on Google Geocoding API. Parameters (from Google page):
    '- Address: The address that you want to geocode.
    'Note: The EncodeURL function was added to allow users from Greece, Poland, Germany, France and other countries
    'geocode address from their home countries without a problem. The particular function (EncodeURL),
    'returns a URL-encoded string without the special characters.
    'This function, however, was introduced in Excel 2013, so it will NOT work in older Excel versions.
    'xmlhttpRequest.Open &quot;GET&quot;, &quot;https://maps.googleapis.com/maps/api/geocode/xml?&quot; _
    &amp; &quot;&amp;address=&quot; &amp; address &amp; &quot;&amp;key=&quot; &amp; apiKey, False

    xmlhttpRequest.Open &quot;GET&quot;, &quot;http://nominatim.openstreetmap.org/search?q=&quot; &amp; Replace(address, &quot; &quot;, &quot;+&quot;) &amp; &quot;&amp;format=xml&amp;polygon=1&amp;addressdetails=1&quot;

    'An alternative way, without the EncodeURL function, will be this:
    'xmlhttpRequest.Open &quot;GET&quot;, &quot;https://maps.googleapis.com/maps/api/geocode/xml?&quot; &amp; &quot;&amp;address=&quot; &amp; Address &amp; &quot;&amp;key=&quot; &amp; ApiKey, False
    
    'Send the request to the Google server.
    xmlhttpRequest.send
    
    'Create the DOM document object and check if it was created successfully.
    Set xmlDoc = CreateObject(&quot;MSXML2.DOMDocument&quot;)
    
    If xmlDoc Is Nothing Then
        GetCoordinates = &quot;Cannot create the DOM document object&quot;
        Exit Function
    End If
    
    'Read the XML results from the request.
    xmlDoc.LoadXML xmlhttpRequest.responseText
    
    'Get the value from the status node.
    Set xmlStatusNode = xmlDoc.SelectSingleNode(&quot;//statusText&quot;)
    
    'Based on the status node result, proceed accordingly.
    Select Case UCase(xmlStatusNode.Text)
    
    Case &quot;OK&quot;                                    'The API request was successful.
        'At least one result was returned.
        'Get the latitude and longitude node values of the first result.
        Set xmlLatitudeNode = xmlDoc.SelectSingleNode(&quot;//result/geometry/location/lat&quot;)
        Set xmLongitudeNode = xmlDoc.SelectSingleNode(&quot;//result/geometry/location/lng&quot;)
        
        'Return the coordinates as a string (latitude, longitude).
        GetCoordinates = xmlLatitudeNode.Text &amp; &quot;, &quot; &amp; xmLongitudeNode.Text
    
    Case &quot;ZERO_RESULTS&quot;                          'The geocode was successful but returned no results.
        
        GetCoordinates = &quot;The address probably do not exist&quot;
    
    Case &quot;OVER_DAILY_LIMIT&quot;                      'Indicates any of the following:
        '- The API key is missing or invalid.
        '- Billing has not been enabled on your account.
        '- A self-imposed usage cap has been exceeded.
        '- The provided method of payment is no longer valid
        '  (for example, a credit card has expired).
        GetCoordinates = &quot;Billing or payment problem&quot;
    
    Case &quot;OVER_QUERY_LIMIT&quot;                      'The requestor has exceeded the quota limit.
        
        GetCoordinates = &quot;Quota limit exceeded&quot;
    
    Case &quot;REQUEST_DENIED&quot;                        'The API did not complete the request.
        
        GetCoordinates = &quot;Server denied the request&quot;
    
    Case &quot;INVALID_REQUEST&quot;                       'The API request is empty or is malformed.
        
        GetCoordinates = &quot;Request was empty or malformed&quot;
    
    Case &quot;UNKNOWN_ERROR&quot;                         'The request could not be processed due to a server error.
        
        GetCoordinates = &quot;Unknown error&quot;
    
    Case Else                                    'Just in case...
        
        GetCoordinates = &quot;Error&quot;
    
    End Select
    
    'Release the objects before exiting (or in case of error).
errorHandler:

    Set xmlStatusNode = Nothing
    Set xmlLatitudeNode = Nothing
    Set xmLongitudeNode = Nothing
    Set xmlDoc = Nothing
    Set xmlhttpRequest = Nothing
    
End Function
</code></pre>
<p>Everything goes fine until the response is read in xml in the line:</p>
<pre><code>xmlDoc.LoadXML xmlhttpRequest.responseText
</code></pre>
<p>API OpenStreetMap (by Postman) returns:</p>
<pre><code>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot; ?&gt;
&lt;searchresults timestamp='Tue, 30 Nov 21 23:27:43 +0000' attribution='Data © OpenStreetMap contributors, ODbL 1.0. http://www.openstreetmap.org/copyright' querystring='Abramowice Kościelne Głusk' exclude_place_ids='282751943' more_url='https://nominatim.openstreetmap.org/search/?q=Abramowice+Ko%C5%9Bcielne+G%C5%82usk&amp;amp;addressdetails=1&amp;amp;exclude_place_ids=282751943&amp;amp;format=xml'&gt;
    &lt;place place_id='282751943' osm_type='relation' osm_id='6187770' place_rank='16' address_rank='16' boundingbox=&quot;51.1900199,51.1955316,22.6211673,22.6355145&quot; lat='51.1905395' lon='22.6282202' display_name='Abramowice Kościelne, gmina Głusk, powiat lubelski, województwo lubelskie, Polska' class='boundary' type='administrative' importance='0.59025964622406' icon='https://nominatim.openstreetmap.org/ui/mapicons//poi_boundary_administrative.p.20.png'&gt;
        &lt;village&gt;Abramowice Kościelne&lt;/village&gt;
        &lt;municipality&gt;gmina Głusk&lt;/municipality&gt;
        &lt;county&gt;powiat lubelski&lt;/county&gt;
        &lt;state&gt;województwo lubelskie&lt;/state&gt;
        &lt;country&gt;Polska&lt;/country&gt;
        &lt;country_code&gt;pl&lt;/country_code&gt;
    &lt;/place&gt;
&lt;/searchresults&gt;
</code></pre>
<p>Beacuse the response api is different from google I am loading</p>
<pre><code>xmlDoc.Load xmlhttpRequest.responseXML
</code></pre>
<p>But the problem is that I can't find <code>&lt;place&gt;&lt;/place&gt;</code> node in responseXml from xmlhttpRequest.
In chaildNodes i can see only <code>xml</code> and <code>searchresults</code>. It looks like <code>xmlDoc.Load</code> and <code>xmlhttpRequest</code> did not load all xml levels node.
How obtain <code>&lt;place&gt;&lt;/place&gt;</code> node in line <code>xmlDoc.Load xmlhttpRequest.responseXML</code>?</p>
<p>responseText returns that:</p>
<pre><code>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot; ?&gt;
&lt;searchresults timestamp='Wed, 01 Dec 21 06:38:10 +0000' attribution='Data © OpenStreetMap contributors, ODbL 1.0. http://www.openstreetmap.org/copyright' querystring='Abramowice KoĹ›cielne GĹ‚usk' more_url='https://nominatim.openstreetmap.org/search/?q=Abramowice+Ko%C4%B9%E2%80%BAcielne+G%C4%B9%E2%80%9Ausk&amp;amp;addressdetails=1&amp;amp;format=xml&amp;amp;accept-language=pl%2Cen-GB%3Bq%3D0.7%2Cen%3Bq%3D0.3'&gt;
&lt;/searchresults&gt;
</code></pre>
<p>The problem was in the wrong query.
I called the address &quot;Abramowice Kościelne gm. Głusk&quot; but
api does not understand what it means gm. (commune in Polish) and therefore could not return eny result. When calling Abramowice Kościelne Głusk, I get the correct result in responseText.</p>
<pre><code>&lt;?xml version=&quot;1.0&quot; encoding=&quot;UTF-8&quot; ?&gt;
&lt;searchresults timestamp='Wed, 01 Dec 21 09:51:58 +0000' attribution='Data © OpenStreetMap contributors, ODbL 1.0. http://www.openstreetmap.org/copyright' querystring='Abramowice Kościelne Głusk' exclude_place_ids='282751943' more_url='https://nominatim.openstreetmap.org/search/?q=Abramowice+Ko%C5%9Bcielne+G%C5%82usk&amp;amp;addressdetails=1&amp;amp;exclude_place_ids=282751943&amp;amp;format=xml&amp;amp;accept-language=pl%2Cen-GB%3Bq%3D0.7%2Cen%3Bq%3D0.3'&gt;
&lt;place place_id='282751943' osm_type='relation' osm_id='6187770' place_rank='16' address_rank='16' boundingbox=&quot;51.1900199,51.1955316,22.6211673,22.6355145&quot; lat='51.1905395' lon='22.6282202' display_name='Abramowice Kościelne, gmina Głusk, powiat lubelski, województwo lubelskie, Polska' class='boundary' type='administrative' importance='0.59025964622406' icon='https://nominatim.openstreetmap.org/ui/mapicons//poi_boundary_administrative.p.20.png'&gt;
&lt;village&gt;Abramowice Kościelne&lt;/village&gt;&lt;municipality&gt;gmina Głusk&lt;/municipality&gt;&lt;county&gt;powiat lubelski&lt;/county&gt;&lt;state&gt;województwo lubelskie&lt;/state&gt;&lt;country&gt;Polska&lt;/country&gt;&lt;country_code&gt;pl&lt;/country_code&gt;&lt;/place&gt;&lt;/searchresults&gt;
</code></pre>
<p>I think additional function URLEncode help to. Thx for fast help.</p>

## Answers
### Answer ID: 70180259
<p>Most likely the address passed in <code>address</code> is not translated correctly with just <code>Replace</code> function so you should use Excel built-in function <code>EncodeURL</code> to translate it correctly.</p>
<p>So change this line:</p>
<pre><code>xmlhttpRequest.Open &quot;GET&quot;, &quot;http://nominatim.openstreetmap.org/search?q=&quot; &amp; Replace(address, &quot; &quot;, &quot;+&quot;) &amp; &quot;&amp;format=xml&amp;polygon=1&amp;addressdetails=1&quot;
</code></pre>
<p>To this:</p>
<pre><code>xmlhttpRequest.Open &quot;GET&quot;, &quot;http://nominatim.openstreetmap.org/search?q=&quot; &amp; WorksheetFunction.EncodeURL(address) &amp; &quot;&amp;format=xml&amp;polygon=1&amp;addressdetails=1&quot;
</code></pre>
<p><code>EncodeURL</code> function is only available from Excel 2013 so if you are running this from Access - You will probably need to use a function to encode the URL (I'm not sure if Access have any built-in function that encode URL)</p>
<p>I tried this with success (Source: <a href="https://stackoverflow.com/questions/218181/how-can-i-url-encode-a-string-in-excel-vba">How can I URL encode a string in Excel VBA?</a>) so paste the function below to your module as well:</p>
<pre><code>Public Function URLEncode( _
   ByVal StringVal As String, _
   Optional SpaceAsPlus As Boolean = False _
) As String
  Dim bytes() As Byte, b As Byte, i As Integer, space As String

  If SpaceAsPlus Then space = &quot;+&quot; Else space = &quot;%20&quot;

  If Len(StringVal) &gt; 0 Then
    With New ADODB.Stream
      .Mode = adModeReadWrite
      .Type = adTypeText
      .Charset = &quot;UTF-8&quot;
      .Open
      .WriteText StringVal
      .Position = 0
      .Type = adTypeBinary
      .Position = 3 ' skip BOM
      bytes = .Read
    End With

    ReDim result(UBound(bytes)) As String

    For i = UBound(bytes) To 0 Step -1
      b = bytes(i)
      Select Case b
        Case 97 To 122, 65 To 90, 48 To 57, 45, 46, 95, 126
          result(i) = Chr(b)
        Case 32
          result(i) = space
        Case 0 To 15
          result(i) = &quot;%0&quot; &amp; Hex(b)
        Case Else
          result(i) = &quot;%&quot; &amp; Hex(b)
      End Select
    Next i

    URLEncode = Join(result, &quot;&quot;)
  End If
End Function
</code></pre>
<p>And change the line above to:</p>
<pre><code>xmlhttpRequest.Open &quot;GET&quot;, &quot;http://nominatim.openstreetmap.org/search?q=&quot; &amp; URLEncode(address) &amp; &quot;&amp;format=xml&amp;polygon=1&amp;addressdetails=1&quot;
</code></pre>

