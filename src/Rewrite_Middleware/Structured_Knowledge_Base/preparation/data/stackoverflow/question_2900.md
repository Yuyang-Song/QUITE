# Angular 8 front-end not sending captured data/fields to Go back-end
[Link to question](https://stackoverflow.com/questions/57919200/angular-8-front-end-not-sending-captured-data-fields-to-go-back-end)
**Creation Date:** 1568360108
**Score:** 0
**Tags:** angular, go, angular8
## Question Body
<p>I am currently rewriting an application that will have an Angular 8 front end(Learning as I code) that will interact with a Go backend which will that connect to a MSSQL database.
I can display my data from the DB successfully.
However, when trying to update the data received, it looks like the fields/data are not being sent to the Go backend.
I have tested the Go backend API using Postman and that works fine. 
Any suggestion on what could be wrong with the code below or what I can do to debug this ?</p>

<p>rest-api.service.ts</p>

<pre><code>httpOptions = {
headers: new HttpHeaders({
  'Content-Type': 'application/json'
 //'Content-Type': 'Application-Token : this.getToken()' 
})
}  
updateDetails(ref, details): Observable&lt;Details&gt; {
return this.http.put&lt;Details&gt;(this.apiURL + '/details-edit/' + ref,    JSON.stringify(details), this.httpOptions)
.pipe(
retry(1),
catchError(this.handleError)
)
}
</code></pre>

<p>details-edit.component.ts</p>

<pre><code>@Input() detailDetails = {  Ref: '', Name: '', Number: '', Trans_Date: '', Amount: '', Type: '', Reason: '', Code: '', Run_Date: ''}    Ref = this.actRoute.snapshot.params['Ref'];
detailsData: any = {};
constructor(
public restApi: RestApiService,
public actRoute: ActivatedRoute,
public router: Router
) { 
}
ngOnInit() { 
this.restApi.getDetails(this.Ref).subscribe((data: {}) =&gt; {
this.detailsData = data;
})
}
updateDetails(detailDetails) {
this.restApi.updateDetails(this.Ref, this.detailDetails).subscribe((data: {}) =&gt; {
this.router.navigate(['/details-list'])
})
}
</code></pre>

<p>details-component.html</p>

<pre><code>&lt;div class="form-group"&gt;
&lt;input type="text" [(ngModel)]="details.Run_Date" class="form-control" placeholder="Run_Date"&gt;
&lt;/div&gt;   
 &lt;div class="form-group"&gt;
&lt;button class="btn btn-success btn-lg btn-block" (click)="updateDetails()"&gt;Update Details&lt;/button&gt;
&lt;/div&gt;
</code></pre>

<p>I am expecting the captured\edited fields to used as values for my placeholders in my GO MSSQL query</p>

## Answers
### Answer ID: 57919705
<p>In your <code>.html</code> you are using ngModel for <code>details</code>, but in your component.ts you have <code>detailsData</code>.</p>

<p>In your <code>component.ts</code>, <code>updateDetails</code> function has 1 parameter. Make sure using a <code>console.log</code> that the function is executed because you don't provide a parameter in <code>.html</code></p>

<p>Also, I don't know if you expect on back-end to recieve a string. You should send your data through <code>put</code> without <code>JSON.stringify</code>.</p>

<p>I hope this helps.</p>

