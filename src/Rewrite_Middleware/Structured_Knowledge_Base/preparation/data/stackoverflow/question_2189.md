# Node JS Json Parsing
[Link to question](https://stackoverflow.com/questions/22891925/node-js-json-parsing)
**Creation Date:** 1396774768
**Score:** 0
**Tags:** json, node.js
## Question Body
<p>Apologies this may seem to be a simple solution but I'm very new to Node.js and struggling to come up with the answer. I have a JSON file (actually a result from a  SQL Server database query) that contains a flat list of all items ordered for a given date and looks like the below</p>

<pre><code>{
    "ProductName": "Product 1",
    "OrderRef": "1010197",
    "Country": "United States",
    "Region": "Georgia",
    "Postcode": "30318",
    "PricePaid": 979,
    "Currency": "GBP",
    "Size": "42 IT",
    "Colour": "Cream",
    "OrderDate": "2014-04-03T06:06:31.000Z"
}, {
    "ProductName": "Product 2",
    "OrderRef": "1010197",
    "Country": "United States",
    "Region": "Georgia",
    "Postcode": "30318",
    "PricePaid": 1295,
    "Currency": "GBP",
    "Size": "38 FR",
    "Colour": "Green Black",
    "OrderDate": "2014-04-03T06:06:31.000Z"
}, {
    "ProductName": "Product 1",
    "OrderRef": "101019",
    "Country": "United Kingdom",
    "Region": "London",
    "Postcode": "30318",
    "PricePaid": 100,
    "Currency": "GBP",
    "Size": "38 FR",
    "Colour": "Green Black",
    "OrderDate": "2014-04-03T06:06:31.000Z"
}
</code></pre>

<p>What I need to be able to do is to rewrite this to a new JSON list where orders are grouped as follows</p>

<pre><code>    [{
    "OrderRef": "123ABC",
    "OrderDate": "2014-01-01",
    "OrderTotal": 26.99,
    "Region": "London",
    "Country": "United Kingdom",
    "Postcode": "W17FF",
    "Items": [
      {
        "Product": "A test product",
        "Price": "12.99"
      },
      {
        "Product": "Another test product",
        "Price": 14.99
      }
    ]
  },
  {
    "OrderRef": "ABC123",
    "OrderDate": "2014-01-01",
    "OrderTotal": 30.99,
    "Region": "Hertfordshire",
    "Country": "United Kingdom",
    "Postcode": "ALX999",
    "Items": [
      {
        "Product": "A test product",
        "Price": 12.99
      },
      {
        "Product": "Another test product",
        "Price": 14.99
      }
    ]
  }
</code></pre>

<p>What is the best way to achieve this?
 Thanks ossie</p>

## Answers
### Answer ID: 22901386
<p>There are other and better ways you can do this, but this plain jane approach should hopefully let you understand how the problem is solved in a general way. The same sort of pattern can be applied to creating subtotals.</p>

<pre><code>var toConsolidate = [...];    // array of your items 
function reorganizeData(origArray){
    var currentKey = undefined;
    var remappedRecord;
    var remappedRecordArray = [];
    for (var i = 0; i &lt; origArray.length; i++){
        if (origArray[i].OrderRef !== currentKey) {
            if(typeof currentKey !== 'undefined')
                remappedRecordArray.push(remappedRecord);
            remappedRecord = {
                OrderRef: origArray[i].OrderRef,
                Country: origArray[i].Country,
                Items: []
            };
            currentKey =origArray[i].OrderRef;
        }
        remappedRecord.Items.push({
            Product: origArray[i].ProductName,
            Price: origArray[i].PricePaid
        });
    };
    remappedRecordArray.push(remappedRecord);
    return remappedRecordArray;
};

console.log(require('util').inspect(reorganizeData(toConsolidate), { depth: null }));
</code></pre>

