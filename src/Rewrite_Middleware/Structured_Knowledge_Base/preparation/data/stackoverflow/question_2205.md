# Condense similiar methods into one mega cool method
[Link to question](https://stackoverflow.com/questions/23553484/condense-similiar-methods-into-one-mega-cool-method)
**Creation Date:** 1399587202
**Score:** 1
**Tags:** c#
## Question Body
<p>I'm trying to remove duplicated code and run into an issue here:</p>

<p>I've got five very similar entities (different asset types, e.g. Bonds, Stocks). The methods I'm trying to condense return some statistics about these assets. The statistics are obtained with the help of Linq, the queries are almost identical.</p>

<p><strong>Before</strong>, I had five separate methods in my controller (e.g. BondStatistics, StockStatistics). One of these would look like this (db is my database context which has each asset type defined):</p>

<pre><code>    public JsonResult BondStatistics()
    {
        var items = db.Bonds.ToList();
        var result = new[]
            {
                new
                {
                    key = "Bonds",
                    values = items.Select(i =&gt; 

                        new {
                            x = i.priceChangeOneDayInEuro,
                            y = i.priceChangeTotalInEuro,
                            size = i.TotalValueInEuro,
                            toolTip = i.Description
                        }
                    )
                },
            };
        return Json(result, JsonRequestBehavior.AllowGet);
    }
</code></pre>

<p>I googled that one way to rewrite these into just one method could be using reflection. However, I thought I could use a dirty shortcut, something like this:</p>

<pre><code>public JsonResult Scatter(string asset)
{
    if (asset == "Stocks") { var items = db.Stocks.ToList(); };
    if (asset == "Bonds") { var items = db.Bonds.ToList(); };
    if (asset == "Futures") { var items = db.Futures.ToList(); };
    if (asset == "Options") { var items = db.Options.ToList(); };
    if (asset == "Funds") { var items = db.Funds.ToList(); }

    var result = new[]
        {
            new
            {
                key = asset,
                values = items.Select(i =&gt; 
                    new {
                        x = i.priceChangeOneDayInEuro,
                        y = i.priceChangeTotalInEuro,
                        size = i.TotalValueInEuro,
                        toolTip = i.Description
                }
            )
        },
    };
return Json(result, JsonRequestBehavior.AllowGet);
}
</code></pre>

<p>This leads to the problem that the type of "items" is not known in the Linq query at design time.</p>

<p>What would be a good way to overcome this problem? Use some totally other pattern, do use reflection or is there an easy fix?</p>

<p><strong>EDIT</strong>
As suggested, I created an Interface and let the BaseAsset-class implement it. Then, changing the condensed method to </p>

<pre><code>List&lt;IScatter&gt; items = new List&lt;IScatter&gt;();
if (asset == "Stocks") { items = db.Stocks.ToList&lt;IScatter&gt;(); };
if (asset == "Bonds") { items = db.Bonds.ToList&lt;IScatter&gt;(); };
if (asset == "Futures") { items = db.Futures.ToList&lt;IScatter&gt;(); };
if (asset == "Options") { items = db.Options.ToList&lt;IScatter&gt;(); };
if (asset == "Funds") { items = db.Funds.ToList&lt;IScatter&gt;(); }
</code></pre>

<p>works, at design time at last. Thank you very much!</p>

## Answers
### Answer ID: 23553635
<p>You are putting everything into <code>var</code>, but what exactly is the type of the items you are processing?</p>

<p>If it would be <code>List&lt;Stock&gt;</code> for <code>db.Stocks.ToList()</code>, <code>List&lt;Bond&gt;</code> for <code>db.Bonds.ToList()</code> you can simply define an interface (e.g. <code>IHasPriceInformation</code>) which has the fields you are using in the LINQ query. Then, Let <code>Stock</code>, <code>Bond</code> and others implement this interface (or provide an abstract base implementation of them) and simply run your LINQ Query on a <code>List&lt;IHasPriceInformation&gt;</code>.</p>

