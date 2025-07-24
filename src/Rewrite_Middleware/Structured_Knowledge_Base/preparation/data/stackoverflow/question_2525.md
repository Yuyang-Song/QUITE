# Right way to process database errors in golang app
[Link to question](https://stackoverflow.com/questions/38399235/right-way-to-process-database-errors-in-golang-app)
**Creation Date:** 1468594522
**Score:** 0
**Tags:** go
## Question Body
<p>I have simple web app on Go. Logging of errors is important part of app.
Errors can be deived on:</p>

<p>a) Database errors - when interact with Database we need log all errors are occured
b) Input parameters, logic errors</p>

<p>My typical handler looks like:</p>

<pre><code>func handler(r,w) {
  var client models.Client
  err := json.NewDecoder(r.Body).Decode(&amp;client)
  log.Error(err) // if error was

  err = client.Validate()
  log.Error(err) // if error was

  err = client.Save()
}
...
func (client *Client) Save() error {
   _, err := db.Exec(`insert into client ....`, client.data())
   if err != nil {
     log.Error(err)
     return err
   }
   ...
}
</code></pre>

<p>Look at the *Client.Save() method. When DB error occures we log it.
My logger takes file:line where error occures.</p>

<p>I think that it's better way that database package processes errors itself.
For example, it's good to have some Database type which logs all errors inside methods Exec(), Query, QueryRow with taking file:line where in client code errors occures. </p>

<pre><code>type Database struct {
}
func (d *Database) Exec(...) result, error {
      res, err := d.db.Exec()
      if err != nil {
        log.Error(err, calldepth=3) // calldepth=3 to show place in client code where errors occures
         return nil, err
     }
}
</code></pre>

<p>So, we can rewrite out method *Client.Save() mehtod to reduce error processing in client code:</p>

<pre><code>func (client *Client) Save() error {
   _, err := db.Exec(`insert into client ....`, client.data()) // error will processed in Exec
   if err != nil {
     return err
   }
   ...
}
</code></pre>

<p>Whats is right way to process errors of Database in model-controller app?
How to reduce error processing across code?
May be there are database packages with built in features</p>

