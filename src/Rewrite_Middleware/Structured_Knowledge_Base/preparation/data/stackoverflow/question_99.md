# how to hide the actual download folder location
[Link to question](https://stackoverflow.com/questions/12707589/how-to-hide-the-actual-download-folder-location)
**Creation Date:** 1349263907
**Score:** 1
**Tags:** php, security, mod-rewrite
## Question Body
<p>I have a question in my mind that how <code>mod_rewrite</code> increases the security.</p>

<p>I have a my php file which shows a .pdf file online like <code>www.exaple.com?id=234</code> and it makes a query to database and get the actual folder location.</p>

<p>the actual folder location is <code>uploads/</code> and i am using something like <a href="https://stackoverflow.com/questions/10997516/how-to-hide-the-actual-download-folder-location.">how to hide the actual folder location</a></p>

<p>Now i want to use <code>google docs</code> </p>

<pre><code> echo "&lt;iframe src=\"http://docs.google.com/gview?url=".root."uploads/myfile.pdf"."&amp;embedded=true\" style=\"width:100%; height:100%;\" frameborder=\"0\"&gt;&lt;/iframe&gt;
</code></pre>

<p>but i don't want to show the upload directory <code>uploads/</code> in this url.So i use <code>module_rewrite</code> to change the directory name to <code>myfiles/</code> .</p>

<p>The question is that when user changes the directory to <code>www.example.com/myfiles/hacking.php</code> than it will also rewrite to <code>uploads/hacking.php</code>.</p>

<p>I am allowing user to upload files.although i am using blacklist but we assume that security holes may present</p>

## Answers
### Answer ID: 12707768
<p>Rewriting a url to hide a path is useless.</p>

<p>In the end you have a URL that the user can use. A request will send him the resource. Whats the difference if he requests <code>example.com/?fileid=123</code> instead of <code>example.com/uploads/file123.ext?</code></p>

<p>Yes, putting stuff in parameters forces you to use a script to fetch and send the resource. Using something that looks like a path only allows you to use this script. But it can be used, and nothing of this improves security. Not using a script means not being able to check if the user requesting the resource is allowed to, but for public resources this is no issue.</p>

<p>What are you really trying to do? Your security problem is to check whether malicious content was uploaded? If you allow uploading executables, and additionally allow them to be executed, you are doomed. Rewriting any URL does not help in any way.</p>

<p>Check what is uploaded. Prevent this stuff from being executed on your server. </p>

<p>When it comes to using the URLs discussed here, the situation should be like this:</p>

<p>If without rewriting you would reference <code>/uploads/example.pdf</code>, using rewriting should transform this url into something else, <strong>and disable the original url</strong>! If you still can get the stuff via the uploads folder, your rewrite is wrong.</p>

<p>If it is right, you are not in any need to use the old uploads url, because it does not work anymore.</p>

### Answer ID: 12707762
<p>Don't put the file in a web accessible location. Keep it someplace out of the www root, and have a script to open, read and output the file to the browser.</p>

<p>That way, even if it is a php file, only the content will be sent down and will not be executed.</p>

