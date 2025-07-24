# Making a lot of short calls with jquery to build a string?
[Link to question](https://stackoverflow.com/questions/11781675/making-a-lot-of-short-calls-with-jquery-to-build-a-string)
**Creation Date:** 1343924168
**Score:** 1
**Tags:** javascript, jquery, asynchronous
## Question Body
<p>I've been using the spacetree plugin from theJIT.org for a project I'm working on and I'm having trouble with a new feature users wanted.</p>

<p>I've put together a small script to query the database for an employee and see if they have any people who report to them, and if so print 1, else print 0. My code for setting up the json string for the spacetree plugin right now looks like this (it's a bit messy but I'm just trying to get it to work before I get it all cleaned up):</p>

<pre><code>// Returns either 0 or 1 for if a person has direct reports, used in hierarchy below
function checkManager(empid){
    return $.ajax({
        url: path + 'CorpDir_CheckManager.cfm?Empid='+empid,
        datatype: 'text',
        success: (function (mng) {
            console.log(mng + " " + empid); //This works, but ends up being after the string is built
            return mng;
        }),
        error: (function (){
            alert("ERROR!");
        })
    });
}

//Setting up the JSON for the hierarchy tree. 
function startTree() {

    // Clear all other trees on the page
    for (var i = 0; i &lt; 50; i++) {
        $('#hier' + i + '-canvaswidget').remove();
    }
    var json = '';
    jQuery.getJSON(path + 'CorpDir_ReportingChain.cfm?Empid=' + empid, function (data) {// JSON from reporting chain is data
        jQuery.getJSON(path + 'CorpDir_Subordinate.cfm?Empid=' + empid, function (data2) {  // JSON from subordinate is data2
            // Check to see if there is even a reporting chain
            if(data.DATA.length &gt; 0){
                // This is pretty much magic, it took me a while to work it all out. 
                // This first for loop goes through the information from Reporting Chain, turning into the json that the hierarchy uses
                for (var i = data.DATA.length - 1; i &gt;= 0; i--) {
                    json = json + 'id: "' + data.DATA[i][3].replace(/\s/g, '') + '",name: "' + data.DATA[i][0].replace(/\s/g, '') + '&lt;br&gt;' + data.DATA[i][1].replace(/\s/g, '') + '",data: {xid: "' + data.DATA[i][6].replace(/\s/g, '') + '", "parentnode": "1"},children: [{';
                }
            }
            // This appends the current person to the hierarchy (and will later be set to the root node for it)
            var mng = checkManager(empid); //results in [object Object] instead of 1 or 0
            json = json + 'id: "' + empid + '",name: "' + fname + '&lt;br&gt;' + lname + '",data: {xid: "' + commitid.replace(/\s/g, '') + '", "parentnode":"' + mng + '"},children: [';
            // These are the child nodes (from subordinate JSON date), set up to what the hierarchy wants for it.
            for (var i = 0; i &lt; data2.DATA.length; i++) {
                if ( data2.DATA[i][4].replace(/\s/g, '') != empid ){
                    mng = checkManager(data2.DATA[i][4].replace(/\s/g, ''));
                    json = json + '{id: "' + data2.DATA[i][4].replace(/\s/g, '') + '",name: "' + data2.DATA[i][0] + '&lt;br&gt;' + data2.DATA[i][1] + '",data: {xid: "' + data2.DATA[i][6].replace(/\s/g, '') + '", "parentnode":"' + mng + '"},children: []},';
                }
                // IE doesn't always play well if there's a comma at the end of a list, so this cuts it off if it's there
                if (i === data2.DATA.length - 1) {
                    json = json.slice(0, -1);
                }
            }
            json = json + ']';
            // This finishes up the JSON string, closing off all the brackets left open from setting up the reporting chain
            for (var i = data.DATA.length; i &gt; 0; i--) {
                json = json + '}]';
            }
            json = '{' + json + '}';
            console.log(json);
            // Give all the information we need to the spacetree so we can load up that hierarchy
            jitSpaceTree(json, index, empid);
        });
    });
}
</code></pre>

<p>Obviously assuming that it'd wait for the return on that ajax call was a bad idea (nice that it moves on after calling that function anyway :/), what's the best way to get this information in there? Changing the call that gets the reporting and subordinate chain is only a partial solution, as I still need to check for the current user (who gets added in the middle).</p>

<p>What's the right way to do this? I've got to do async calls in a for loop or rewrite a whole lot of code is the only way I'm seeing this right now.</p>

