# Taking an image and converting it into BLOB for MySQL
[Link to question](https://stackoverflow.com/questions/70761536/taking-an-image-and-converting-it-into-blob-for-mysql)
**Creation Date:** 1642535039
**Score:** 0
**Tags:** javascript, mysql, encoding, type-conversion, blob
## Question Body
<p>I am trying to make a JavaScript that would take an image file and covert it into BLOB (by converting the file into Base64 first and then into BLOB), my project doesn't have a support for toBlob() so I have found different convering steps and put them together and they work to a point where I have to pass the BLOB from the function where its made out for the Mysql part of code that takes care of communicating with the database. (I have that fully working). Now I only need to find a way how to connect them through a variable that saves the results of the <code>imageforQuery</code> function.</p>
<p>My code so far is this:</p>
<pre><code>
  let base64String = &quot;&quot;;

  function imageforQuery(imageid) {
          //takes file and converts to Base64
          var file = document.getElementById(imageid).files[0];

          var reader = new FileReader();
          console.log(&quot;next&quot;);
          imgFileFrontBlob = &quot;&quot;;
          reader.onload = function () {
              base64String = reader.result.replace(&quot;data:&quot;, &quot;&quot;)
                  .replace(/^.+,/, &quot;&quot;);

              // console.log(base64String);
              base64String = 'data:image/jpeg;base64,'+ base64String;
              console.log(base64String);
              //converts Base64 into BLOB
              var binary = atob(base64String.split(',')[1]);
              console.log(binary);
              var array = [];
              for(var i = 0; i &lt; binary.length; i++) {
                  array.push(binary.charCodeAt(i));
              }
              var imgFileFrontBlob = new Blob([new Uint8Array(array)], {type: 'image/png'});

              console.log(imgFileFrontBlob);
              return imgFileFrontBlob

          }

          reader.readAsDataURL(file);


       };
</code></pre>
<p>by experimenting with <code>console.log()</code> at different stages and <code>return</code> I have found out that I can't pass the converted BLOB result out, as the function <code>imageforQuery()</code> only returns what is after <code>reader.readAsDataURL(file);</code> and I don't know of a way of getting that result out.</p>
<p>––––––––––––––ADDITIONAL PROBLEMS I HAVE ENCOUNTERED––––––––––––––</p>
<p>okay so thanks to Emiel Zuurbier (Thank you!) I have managed to rewrite my code with the help of his solution. However as much as it helped one part of the problem, it didn't help with the JavaScript <code>Blob object</code> as we found out it is not the exact same thing as SQL <code>BLOB</code>.</p>
<p>Now the problem is that upon trying to send the <code>Blob object</code> in a SQL query, this resulted in just sending pure text &quot;[Blob object]&quot;.</p>
<p>But I am using JavaScript successfully to pull the data from a BLOB field from my database and convert it into <code>Base64</code> images from that data that was stored in the <code>BLOB</code> in a different part of my application. The code for that is below:</p>
<pre><code>var converterEngine = function (input) { 
   // fn BLOB =&gt; Binary =&gt; Base64 ?
   var uInt8Array = new Uint8Array(input),
      i = uInt8Array.length;
   var biStr = []; //new Array(I);
   while (i--) { biStr[i] = String.fromCharCode(uInt8Array[i]);  }
   var base64 = window.btoa(biStr.join(''));
   return base64;
};
</code></pre>
<p>What I need to do is just reverse this and in theory, it should get me the same data that I receive from the database.
My reversal code is below:</p>
<pre><code>// this is the inside bit of code from the first problem that is solved and the 
// typeOfData variable is parsed into the function in imageforQuery() as a second input 
// variable (in other words its not to be of concern)
reader.onload = function () {
          let base64String = reader.result.replace(&quot;data:&quot;, &quot;&quot;).replace(/^.+,/, &quot;&quot;);
          base64String = &quot;data:&quot; + typeOfData + &quot;;base64,&quot; + base64String;

          var binary = atob(base64String.split(&quot;,&quot;)[1]);
          // console.log(binary);
          var array = [];
          for (var i = 0; i &lt; binary.length; i++) {
            array.push(binary.charCodeAt(i));
          }
          var ourArray = new Uint8Array(array);
          



          resolve(ourArray);
        };
</code></pre>
<p>However, as I mentioned the data that comes out (<code>ourArray</code>) isn't actually identical to the original file from the BLOB in the database so my code doesn't function correctly and I don't know why. Any ideas where I've made a mistake?</p>

## Answers
### Answer ID: 70761821
<p>You can wrap the <code>FileReader</code> instance and calls inside of a <a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Promise" rel="nofollow noreferrer"><code>Promise</code></a>. Return the <code>Promise</code> immediately. In the <code>reader.onload</code> function call <code>resolve()</code> to exit the <code>Promise</code> with a value.</p>
<pre><code>function imageforQuery(imageid) {
  return new Promise(resolve =&gt; {
    var file = document.getElementById(imageid).files[0];
    var reader = new FileReader();
  
    reader.onload = function () {
      let base64String = reader.result.replace(&quot;data:&quot;, &quot;&quot;).replace(/^.+,/, &quot;&quot;);
      base64String = &quot;data:image/jpeg;base64,&quot; + base64String;

      var binary = atob(base64String.split(&quot;,&quot;)[1]);
      var array = [];
      for (var i = 0; i &lt; binary.length; i++) {
        array.push(binary.charCodeAt(i));
      }

      var imgFileFrontBlob = new Blob([new Uint8Array(array)], {
        type: &quot;image/png&quot;,
      });
  
      resolve(imgFileFrontBlob);
    };

    reader.readAsDataURL(file);
  });
}
</code></pre>
<p>This results in being able to use your function like here below. <code>imageforQuery</code> is called, returns a <code>Promise</code>. When the promise is finished (meaning <code>resolve</code> is called) the function in the <code>then</code> method will run.</p>
<pre><code>imageforQuery(imageId).then(imgFileFrontBlob =&gt; {
  // Use your blob here.
  saveToDB(imgFileFrontBlob); // Example of how you would use it.
});
</code></pre>
<p>Or use it with <code>async</code> / <code>await</code>.</p>
<pre><code>(async () =&gt; {
  function imageforQuery(imageid) {
    ...
  }

  // Here we can wait for imageforQuery to finish and save the variable.
  const imgFileFrontBlob = await imageforQuery(imageId);
  saveToDB(imgFileFrontBlob); // Example of how you would use it.
})()
</code></pre>

### Answer ID: 70764544
<p>Base64 is simply ascii text.  So MySQL's datatype <code>BLOB</code> or <code>TEXT</code> would work.  That is, after converting to Base64, don't worry about &quot;convert to blob&quot;; it is not necessary.</p>
<p>That is, you can probably replace the code from <code>//converts ...</code> through <code>return ...</code> by simply</p>
<pre><code>return base64String;
</code></pre>

