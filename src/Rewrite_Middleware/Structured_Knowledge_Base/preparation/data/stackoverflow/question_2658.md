# Angular2 change service method from callback to Async
[Link to question](https://stackoverflow.com/questions/45112419/angular2-change-service-method-from-callback-to-async)
**Creation Date:** 1500071222
**Score:** 4
**Tags:** javascript, angular, asynchronous, angular-promise
## Question Body
<p>I started a simple Angular2 Electron app, and I have a service method querying a local SQL Server database. Everything works fine so far. Now I am trying to get the results of the service DB call to my component and display it somehow.</p>

<p>The problem is that the query logic is written more for callback syntax:</p>

<pre><code>sql.query(sqlString, (err, result) =&gt; {
    ...
    callback(result);
    ...
});
</code></pre>

<p>I'm having a hard time rewriting it to return a promise, since the result will always be within result parameter of the query command function. My component looks like this:</p>

<pre><code>export class LinkDocRetriever {

  constructor(private myService: MyService) {  }

  results = "";

  loadMyData(id: number): void {

    let tcData = this.myService.getMyData();
    tcData.forEach(element =&gt; {
      this.results += element.FileName + " " +  "....\n";
    });

  };
}
</code></pre>

<p>And my service looks like this: </p>

<pre><code>import { Injectable } from "@angular/core";
import * as sql from "mssql";

@Injectable()
export class MyService {

    getMyData():Array&lt;MyItem&gt; {

        let myData:Array&lt;MyItem&gt; = [];

        let config = {
            user: "sa",
            password: "xxx",
            server: "localhost",
            database: "mydb"
        };

        const pool1 = new sql.ConnectionPool(config, err =&gt; {

            if (err) {
                console.log("connect erro: " + err);
            }

            let q:string = `SELECT TOP 10 * FROM MyTable;`;

            let final = pool1.request()
            .query&lt;MyItem&gt;(q, (err, result) =&gt; {
                if (err) {
                    console.log("request err: " + err);
                }

                console.log("db result count: " + result.recordsets[0].length);
                result.recordsets[0].forEach(row =&gt; {
                    myData.push(row);
                });
            });
        });
        return myData;
    }
}
</code></pre>

<p>I do get a result back, but the component never sees it since it comes back before the results are returned. </p>

<p>I've tried doing an await on the query call, within the ConnectionPool function, but I get an error stating that await can only be called within an async function, even though I have async set on that method. The mssql package has an <a href="https://www.npmjs.com/package/mssql#async-await" rel="nofollow noreferrer">Async/ Await section</a>, but the given syntax on that page gives errors, when I try it. </p>

<p>Any idea how I can write this using a promise?</p>

## Answers
### Answer ID: 45112800
<p>As you pointed out, there are 3 way to handle async functions: using callback, using promise, and using Async/ Await. I will try to show all three ways but you should learn about event loop in javascript and how it takes care of async functions.</p>

<p><strong>Callback</strong></p>

<p>Callback is technically fastest way to handle async functions but it is quite confusing at first and might create something called callback hell if not used properly. Callback hell is very terrible that someone even created a website for it <a href="http://callbackhell.com/" rel="noreferrer">http://callbackhell.com/</a>.</p>

<p>So you code can be rewritten as:</p>

<pre><code>export class LinkDocRetriever {

  constructor(private myService: MyService) {  }

  results = "";

  loadMyData(id: number): void {

    // call getMyData with a function as argument. Typically, the function takes error as the first argument 
    this.myService.getMyData(function (error, tcData) {
       if (error) {
         // Do something
       }

       tcData.forEach(element =&gt; {
         this.results += element.FileName + " " +  "....\n";
       });
    });
  };
}
</code></pre>

<p>Service</p>

<pre><code>import { Injectable } from "@angular/core";
import * as sql from "mssql";

@Injectable()
export class MyService {
    // Now getMyData takes a callback as an argument and returns nothing
    getMyData(cb) {

        let myData = [];

        let config = {
            user: "sa",
            password: "xxx",
            server: "localhost",
            database: "mydb"
        };

        const pool1 = new sql.ConnectionPool(function(config, err) {

            if (err) {
                // Error occured, evoke callback
                return cb(error);
            }

            let q:string = `SELECT TOP 10 * FROM MyTable;`;

            let final = pool1.request()
            .query&lt;MyItem&gt;(q, (err, result) =&gt; {
                if (err) {
                    console.log("request err: " + err);
                    // Error occured, evoke callback
                    return cb(error);
                }

                console.log("db result count: " + result.recordsets[0].length);
                result.recordsets[0].forEach(row =&gt; {
                    myData.push(row);
                });

                // Call the callback, no error occured no undefined comes first, then myData
                cb(undefined, myData);
            });

        });
    }
}
</code></pre>

<p><strong>Promise</strong></p>

<p>Promise is a special object that allows you to control async function and avoid callback hell because you won't have to use nested callback but only use one level <code>then</code> and <code>catch</code> function. Read more about Promise <a href="https://medium.com/javascript-scene/master-the-javascript-interview-what-is-a-promise-27fc71e77261" rel="noreferrer">here</a></p>

<p>Component</p>

<pre><code>export class LinkDocRetriever {

  constructor(private myService: MyService) {  }

  results = "";

  loadMyData(id: number): void {
    this.myService.getMyData()
      .then((tcData) =&gt; {
         // Promise uses then function to control flow
         tcData.forEach((element) =&gt; {
           this.results += element.FileName + " " +  "....\n";
         });
      })
      .catch((error) =&gt; {
         // Handle error here
      });

  };
}
</code></pre>

<p>Service</p>

<pre><code>@Injectable()
export class MyService {
    // Now getMyData doesn't take any argument at all and return a Promise
    getMyData() {

        let myData = [];

        let config = {
            user: "sa",
            password: "xxx",
            server: "localhost",
            database: "mydb"
        };

        // This is what getMyData returns
        return new Promise(function (resolve, reject) {
            const pool1 = new sql.ConnectionPool((config, err) =&gt; {

                if (err) {
                    // If error occurs, reject Promise
                    reject(err)
                }

                let q = `SELECT TOP 10 * FROM MyTable;`;

                let final = pool1.request()
                  .query(q, (err, result) =&gt; {
                      if (err) {
                          // If error occurs, reject Promise
                          reject(err)
                      }

                      console.log("db result count: " + result.recordsets[0].length);
                      result.recordsets[0].forEach((row) =&gt; {
                          myData.push(row);
                      });

                      // 
                      resolve(myData);
                  });

            });
        })

    }
}
</code></pre>

<p><strong>Async/await</strong></p>

<p>Async/await was introduced to address the confusion you was having when dealing with callbacks and promises. Read more about async/await <a href="https://hackernoon.com/6-reasons-why-javascripts-async-await-blows-promises-away-tutorial-c7ec10518dd9" rel="noreferrer">here</a></p>

<p>Component</p>

<pre><code>export class LinkDocRetriever {

  constructor(private myService: MyService) {  }

  results = "";

  // Look. loadMyData now has to have async keyword before to use await. Beware, now loadMyData will return a Promise.
  async loadMyData(id) {

    // By using await, syntax will look very familiar now
    let tcData = await this.myService.getMyData(tcData);
    tcData.forEach((element) =&gt; {
      this.results += element.FileName + " " +  "....\n";
    });
  };
}
</code></pre>

<p>Service would be exactly the same as in <strong>Promise</strong> because <strong>Async/await</strong> was created especially to deal with them.</p>

<p>NOTE: I remove some Typescript feature from your code because I am more accustomed to vanilla JS but you should be able to compile them because Typescript is a superset of JS.</p>

