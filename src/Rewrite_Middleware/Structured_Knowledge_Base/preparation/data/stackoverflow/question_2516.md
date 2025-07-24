# Node js Express app not working + IISNode
[Link to question](https://stackoverflow.com/questions/37953558/node-js-express-app-not-working-iisnode)
**Creation Date:** 1466539264
**Score:** 0
**Tags:** express, iis-7, internal-server-error, iisnode
## Question Body
<p>I am trying to deploy node js app in windows server 2008  using IISNode. But i keep getting </p>

<blockquote>
  <p>HRESULT: 0x2<br>
  HTTP status: 500<br>
  HTTP reason: Internal Server Error</p>
</blockquote>

<p>Here is my web.config file</p>

<pre><code>&lt;configuration&gt;
 &lt;system.webServer&gt;

  &lt;handlers&gt;
   &lt;add name="iisnode" path="server.js" verb="*" modules="iisnode" /&gt;
  &lt;/handlers&gt;

  &lt;rewrite&gt;
    &lt;rules&gt;
      &lt;rule name="updated_lmv"&gt;
        &lt;match url="/*" /&gt;
        &lt;action type="Rewrite" url="server.js" /&gt;
      &lt;/rule&gt;
    &lt;/rules&gt;
  &lt;/rewrite&gt;
 &lt;system.webServer&gt;    
&lt;configuration&gt;
</code></pre>

<p>and here is my server.js file</p>

<pre><code>var mysql= require('mysql');
var favicon = require('serve-favicon');
var api = require('./routes/api');
var express = require('express');
var session = require('express-session');
var cookieParser = require('cookie-parser');
var bodyParser = require('body-parser');
var app = express();

//app.use is to define the pages and folder and basic usage
app.use(bodyParser.urlencoded({ extended: false }));
app.use('/public', express.static(__dirname + '/www/public'))
app.use('/view', express.static(__dirname + '/www/views/viewer'));
app.use('/', express.static(__dirname + '/www/views/models'));
app.use(favicon(__dirname + '/www/public/images/favicon1.ico'));
app.use('/api', api);

app.use(bodyParser.json());

app.set('port', process.env.PORT); //setting server port to 3000

var query="select label,urn from lmvmodeloption";   //to retrive the urn and label from lmvmodeloption

//Mysql Connection
var connection = mysql.createConnection({
    host : 'localhost',
    user :  '',
    password :'',
    database: 'w_t',
    port: '3306',
});

//Get Function to check
app.get('/data', function(req, res){
    res.send('hello world'); //replace with your data here
});

//Send data from lmvmodels to populate the Drop down list in index1.html
app.get('/lmvmodels',function(req,res){
    connection.query(query,function(err,rows,fields){
        if(!err)
            res.send(rows);
        else 
            console.log(err.stack);
    });
});

//Logout function
app.post('/logout',function(req,res){
    console.log('Im logging out ');
    req.session = null;
    res.send('logout');
});

//function to insert uploaded model into lmvmodeloption
app.post('/endpoint',function(req,res){
    var user_name=req.body.user1;
    var password=req.body.password;
    //var d={ux:user_name,dx:password};
    console.log("User name = "+user_name+", password is "+password);
    var s='INSERT INTO lmvmodeloption(label,urn) '+
    'VALUES("'+password+'","'+user_name+'")';
    console.log(s);
    connection.query(s,function(err,res){
        if(err)
            throw err;
    });
    res.end("yes");
});
app.use(cookieParser())
app.use(session({secret: 'Keyboard car'}));
//this function takes care of the login, check if it returns the rows, if yes send success message, login success
app.post('/login',function(req,res){
    var p_wt=req.body.pass_w;
    var u_wt=req.body.user_w; var sess;
    //console.log(p_wt);
    //console.log(u_wt);
    var q= 'select email, password from user_login where email ="' +u_wt+ '" and password = "' +p_wt+ ' "';
    connection.query(q,function(err,rows,fields){
        //console.log(rows[0].email);
        if(rows.length&gt;0){
            sess=req.session;
            sess.email_u=rows[0].email;
            console.log("Session="+ sess.email_u);
            console.log(rows);
            //console.log("success sent");
            console.log(rows[0].email);
            res.send("success");
        }
        else{
             res.send("Bad Data");
            console.log("bad data")
            // console.log(rows);
        }
    });

});


var server = app.listen(app.get('port'), function() {

    connection.connect(function(err){
        if(err) {
            console.log('error connecting to the database' + err.stack);
            return;
        }
    });

   /* connection.query('SELECT email as first from user_login where email="jeevjyot.chhabda@whiting-turne"', function(err, rows, fields) {
        if (!err)
            console.log(rows);
        else
            console.log('Error while performing Query., Empty it is, no rows'+ err.stack);
    });*/
    console.log('Server listening on port ' +
        server.address().port);
});

//this function checks if no session is set, redirect the user to the index page
function checkAuth(req,res,nect){
    if(!sess.email_u){
        res.redirect("/");
    }
}
</code></pre>

<p>Im trying to run this as default website, under inetpub/wwwroot.</p>

<p>Is there is ant way to get rid of this error. Ive just started to learn node js. thank you</p>

