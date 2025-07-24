# ExtJS 6 grid group by associated models
[Link to question](https://stackoverflow.com/questions/38914833/extjs-6-grid-group-by-associated-models)
**Creation Date:** 1470994992
**Score:** 4
**Tags:** javascript, extjs, grid, grouping, extjs6
## Question Body
<h1>Context</h1>

<p>A while ago I used this <a href="https://stackoverflow.com/a/19198773/1842261">answer</a> to implement remote sorting and filtering. Using the format 'associatedModel.associatedModelField', I could easily resolve the expression in my server side code in order to query the database. </p>

<h1>Problem</h1>

<p>While this does the job, I encountered another problem with <strong>grouping</strong> - which I have configured to be local - the <strong>associated models</strong>. If I group a column which displays an associated field, I cannot collapse or expand without errors. Doing the same thing for the root model of the grid doesn't throw any errors.</p>

<p>The problem can be reproduced in this <a href="https://fiddle.sencha.com/#fiddle/1f5q" rel="nofollow noreferrer">fiddle</a>.</p>

<p>The error trace in the console log goes like this:</p>

<pre>
ext-all-debug.js:198133 Uncaught TypeError: Cannot read property 'isModel' of undefined

getMetaGroup            @   ext-all-debug.js:198133
doCollapseExpand        @   ext-all-debug.js:198284
collapse                @   ext-all-debug.js:198207
onGroupClick            @   ext-all-debug.js:198380
fire                    @   ext-all-debug.js:20223
doFireEvent             @   ext-all-debug.js:21130
doFireEvent             @   ext-all-debug.js:64732
prototype.doFireEvent   @   ext-all-debug.js:54757
fireEventArgs           @   ext-all-debug.js:20983
fireEvent               @   ext-all-debug.js:20942
processSpecialEvent     @   ext-all-debug.js:188549
processItemEvent        @   ext-all-debug.js:188499
processUIEvent          @   ext-all-debug.js:168108
handleEvent             @   ext-all-debug.js:168061
fire                    @   ext-all-debug.js:20223
fire                    @   ext-all-debug.js:32463
publish                 @   ext-all-debug.js:32439
doDelegatedEvent        @   ext-all-debug.js:32489
onDelegatedEvent        @   ext-all-debug.js:32476
(anonymous function)    @   ext-all-debug.js:6662
</pre>

<p>In the code I have used the solution as provided above and I also applied for the the grouping feature. It isn't exactly clean code but it works as long as I respect the limits of the fix.</p>

<p>How should I tackle this problem? Based on the type of problem I suppose that means rewriting the whole grouping mechanism but I don't fancy that!</p>

## Answers
### Answer ID: 40391345
<p>I found the answer to my question by accident. On the <a href="http://docs.sencha.com/extjs/6.2.0/classic/Ext.grid.feature.Grouping.html" rel="nofollow noreferrer">official docs website</a>, this line tells you what to do:</p>

<blockquote>
  <p>However, if you intend to group by a data field that is a complex data
  type such as an Object or Array, it is necessary to define one or more
  Ext.util.Grouper on the feature that it can then use to lookup
  internal group information when grouping by different fields.</p>
</blockquote>

<p>So you need to define an array in the 'groupers' config of the grouping feature:</p>

<pre><code> features: [{
            ftype: 'grouping',
            remoteRoot: 'Summary',
            groupHeaderTpl: '{name}',
            collapsible: true,
            groupers:  [{
                          property: 'Customer.Address',
                          groupFn: function (val) {
                             return val.data.Job ? val.data.Customer.Address: '';
                        }
               }]
            }]
</code></pre>

<p>If you group on on this column, the groupFn will be used to do the actual grouping.</p>

