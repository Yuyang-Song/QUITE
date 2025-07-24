# Laravel validator - Integrity constraint violation
[Link to question](https://stackoverflow.com/questions/36466271/laravel-validator-integrity-constraint-violation)
**Creation Date:** 1460000263
**Score:** 2
**Tags:** validation, laravel
## Question Body
<p>I have employees, which has (auto increment) unique id in database (pretty easy :) ) but I would like to check the uniqueness of other field which will be their employee_number  ..</p>

<p>While creating the new employee, it's pretty easy, because I just call:</p>

<pre><code>$this-&gt;validate($request, [                
                           'employee_number' =&gt; 'required|unique:employees'
                           ]);
</code></pre>

<p>But how can I do this while editing existing employee? I would like to check (if the "edited" employee_number is unique for <strong>OTHER</strong> users ... it means that I need to rewrite this query to laravel validation form</p>

<pre><code>employee_number NOT IN (SELECT employee_number 
                        FROM employees 
                        WHERE id = *edited_user_id*)
</code></pre>

<p>I tried to do this</p>

<pre><code>$this-&gt;validate($request, [                
                           'employee_number' =&gt; 'required|unique:employees,id,'.$input['employee_id']
                           ]);
</code></pre>

<p>Imagine, there are records in a table "employees"</p>

<pre><code>id |  name  | employee_number
-----------------------------
1  |  Peter |      0001
2  |  Paul  |      0002
3  |  Frank |      0003
</code></pre>

<p>When I try to change Frank's data -> it is ok .. even if i change his employee number to some unique one, it works ok .. </p>

<p>But when I insert existing one for Frank's account, i.e. 0001 it doesn't give me a proper error message (from validator) that employee number is already taken .. but instead of that, it redirects me to the error page </p>

<pre><code>Whoops, looks like something went wrong.

QueryException in Connection.php line 669:
SQLSTATE[23000]: Integrity constraint violation: 1062 Duplicate entry '0001' for key 'employees_employee_number' (SQL: *here comes the wrong sql query*)
</code></pre>

<p>Do you know how can I raise the proper error bar right above the form like when I try to insert new employee and try to insert the existing id?  </p>

## Answers
### Answer ID: 36467001
<p>If the Validator fails I collected the error message as shown</p>

<pre><code>$rules = ['employee_number' =&gt; 

    'required|unique:employees,employee_number,'.$input['employee_id']]

    $validator = \Validator::make($data = \Input::all(), $rules);

            if ($validator-&gt;fails()) {
                return [
                    return [
                        "status" =&gt; "fail",
                        "errors" =&gt; $validator-&gt;getMessageBag()-&gt;toArray()
        ];
                ];
            }
</code></pre>

<p>Now collect the response from where you sent your request and in response you will get a associative array of error messages which you can use it according to your use.</p>

### Answer ID: 36466965
<p>You did one small mistake in <code>'required|unique:employees,id,'.$input['employee_id']</code>.
Now You are looking if your input <code>employee_number</code> is unique in <code>employees</code> table by <code>id</code> field.</p>

<p>Change that line to:
<code>'required|unique:employees,employee_number,'.$input['employee_id']</code> and You are good to go!</p>

<p>From Lavarel docs: <code>unique:table,column,except,idColumn</code>.</p>

