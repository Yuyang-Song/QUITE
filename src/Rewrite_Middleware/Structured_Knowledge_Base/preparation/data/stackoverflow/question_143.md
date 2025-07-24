# Images breaking on page refresh?
[Link to question](https://stackoverflow.com/questions/1433760/images-breaking-on-page-refresh)
**Creation Date:** 1253115316
**Score:** 0
**Tags:** javascript, ajax, dynamic-data, appendchild
## Question Body
<p>I am pulling data from a database with Ajax and dynamically populating a div tag with image elements. The image file name corresponds to the data in the database.</p>

<p>For instance if there was something in the database called 'foo', I have an item called 'img/foo.jpg'</p>

<p>My javascript pulls the data and creates a an image with the src if 'img/foo.jpg' sets the class and then writes it in to the correct div.</p>

<p>For the most part this works as intended, but occasionally on a refresh (I have it querying the database, clearing all divs, and rewriting the nodes every 30 seconds), occasionally some of the images will break/not load. There's no rhyme or reason to which one it is, sometimes it happens to none, and sometimes to several. </p>

<p>If you right click -> show image, manually refresh, or wait for it to pull the data again, it displays the image as intended. Therefore, I know data is being pulled and written properly, and it just seems to be failing to load the image.</p>

<p>Does anyone know why or how to address this issue?</p>

## Answers
### Answer ID: 8256264
<p>Apologies if this is not be a good answer, but if you have many images on your page, it may be that the browser (and this is not limited to IE6) has not downloaded the data for all of them.</p>

<p>If you are "clearing all divs, and rewriting the nodes every 30 seconds" you might run into the problem hinted at by the Microsoft support question "<a href="http://support.microsoft.com/kb/282402" rel="nofollow">How do I configure Internet Explorer to download more than two files at one time?</a>". It may be that you notice the images being downloaded.</p>

<p>Instead of re-downloading all images together (in parallel), you may find updating images serially to be more reliable like so:</p>

<pre><code>var refreshCount = 0;
function updateImages() {
  var nextImage = refreshCount % document.images.length;
  var image = document.images[nextImage];
  if(image.complete) {
    var newImage = new Image();
    newImage.src = image.src;           
    image.parentNode.insertBefore(newImage,image);
    image.parentNode.removeChild(image);
    refreshCount++;
  }
  setTimeout(updateImages, 1000);
}
// Wait 20 sec before starting the refreshes 
// (gives time to get the images downloaded in the first place)
setTimeout(updateImages, 20000);    
</code></pre>

### Answer ID: 1433980
<p>Try it in Firefox with the Firebug add-on, with the Net panel enabled and you might be able to see why the fetches for the images are failing.</p>

