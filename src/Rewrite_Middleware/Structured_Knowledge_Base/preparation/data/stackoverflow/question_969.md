# What is the best way to handle domain-centric validation while providing a rich UI experience?
[Link to question](https://stackoverflow.com/questions/523289/what-is-the-best-way-to-handle-domain-centric-validation-while-providing-a-rich)
**Creation Date:** 1233987667
**Score:** 0
**Tags:** user-interface, validation
## Question Body
<p>My company is developing a GUI application that allows users to query a legacy database system and have the results displayed back to them on the screen (the results just come back in a blob of plain-text). I'm struggling with the best way to structure the interaction between the user interface and the domain layer, especially validation of user input.</p>

<h3>Basic Use Case</h3>

<ol>
<li>User selects a query to run from a menu in the application.</li>
<li>The application code displays the data entry form for the selected query.</li>
<li>The user enters the parameters for the query. If a field contains invalid data, it is immediately highlighted in red, and its tooltip text is changed to display an error message (i.e. if you are entering a Person query, and you enter a date of birth in the future, for example, the date of birth field will immediately turn red).</li>
<li>When the user clicks <code>Run Query</code>, the application runs a second validation pass; this second validation pass is required in order to run validation checks that involve multiple fields. If the this validation check passes, and all the fields are valid, the query is sent; otherwise, the user is prompted to fix any remaining errors.</li>
</ol>

<h3>My Current Validation/Error Reporting Strategy</h3>

<p>Currently, I'm using domain-centric validation, but the overall design seems messy to me and maybe a little too over-engineered. A brief overview of the current design:</p>

<p><strong>Domain layer</strong>: I have one class per query. Every query class contains a collection of <code>IQueryField</code> objects that hold the values entered by the user. Each query class implements a common <code>IQueryMessage</code> interface, which defines (among other things) a <code>Validate</code> method. This method is called to enforce message-level validation rules (i.e. rules that must examine the state of multiple fields at once). The <code>IQueryField</code> interface also defines a 'Valdate' method (among other things). This is to support per-field validation rules.</p>

<p><strong>Per-field validation</strong>: To handle the per-field validation and error reporting, the data entry code binds each input control to an <code>IQueryField</code>; whenever the user changes the value of a control, it calls the the corresponding <code>IQueryField</code>'s <code>Validate</code> method, which in turn fills a <code>Notification</code> object (just a collection of strings at the moment) with any errors detected in the value entered by the user. The user interface code then checks the <code>Notification</code> object and changes the appearance of the user control to indicate an error condition, if necessary.</p>

<p><strong>Message-level validation</strong>: When the user tries to send a query, the application calls the <code>Validate</code> method on the <code>IQueryMessage</code> instance associated with the data entry form (at this point, the data binding code has also ensured all the message's fields have been populated from the input controls on the form, and the per-field validation code has been run). If there are any validation errors, the user interface displays them at the top of the form. If there are no errors, the data entry form is closed and the query is serialized and sent over the network.</p>

<h3>Is Something Wrong Here?</h3>

<p>I feel like something isn't "right" here. I have a few issues with the current design:</p>

<ol>
<li><p>I would like the domain-level validation code to indicate the name of any fields that are in error, bur I don't want to hard-code the UI label captions into the domain classes. One possibility I thought of was to have the domain-level <code>Validate</code> methods generate messages with a field placeholder, such as <code>"%s cannot be in the future"</code>, and have the UI code fill in the placeholder with the correct label.</p></li>
<li><p>The <code>IQueryMessage</code> and <code>IQueryField</code> interfaces both have a method called <code>Validate</code>. I'm thinking this should be extracted into a separate interface, (<code>IValidatable</code> perhaps), but I wonder if I am making things needlessly complex.</p></li>
<li><p>I'm using VB6, so I can't use inheritance in my classes (VB6 supports classes but not inheritance). I can only define and implement interfaces. Because of this, and because of the way my current interfaces are designed, I'm duplicating a lot of boiler-plate code in my implementation classes. I am thinking of solving this with an inversion-of-control approach. For example, I was thinking of defining a single concrete <code>QueryField</code> class, which could be initialized with a collection of <code>IValidationRule</code> instances that define what validation rules to use, then the <code>QueryField.Validate()</code> method would just collect the results of executing each rule. This way, the validation rules can be tailored to each field, but the <code>QueryField</code> class can handle all the common field-related stuff (field name, field length, required/not required checks, etc.).</p></li>
</ol>

<h3>How Can I Improve This?</h3>

<p>I'm interested in any refactoring suggestions and hints on improving the current design. Also, I'm not necessary tied down to domain-centric validation; other suggestions are welcome. The main motivation behind using domain-centric validation was to keep increase encapsulation, and allow query message and field objects to be used in a non-GUI environment, without having to rewrite all the validation logic. </p>

## Answers
### Answer ID: 524008
<ol>
<li><p>When you initialize a QueryField object, pass a label to it from the GUI. Then it's the UI that is responsible for setting the label name which seems reasonable to me.</p></li>
<li><p>I don't think this is necessary.</p></li>
<li><p>What you are describing doesn't really sound like IoC but rather just plain old composition. Since you can't even use inheritance this improvement seems to make sense. Generally you want to prefer composition to inheritance anyways. However if you are almost done with the work then I wouldn't bother refactoring this late in the game.</p></li>
</ol>

