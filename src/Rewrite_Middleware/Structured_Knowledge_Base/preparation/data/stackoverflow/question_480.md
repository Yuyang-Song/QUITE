# Magento Collection Query
[Link to question](https://stackoverflow.com/questions/28041273/magento-collection-query)
**Creation Date:** 1421744599
**Score:** 1
**Tags:** magento, collections
## Question Body
<p>I created new customer attribute 'personal_number' and now want to show it in new column in adminhtml sales_order_grid.
I've done all stuff to show column in grid (class rewrite in config.xml), created MyName_MyModule_Block_Adminhtml_Order_Grid where need to rewrite _getCollectionClass() and _prepareColumns(). My problem is in _getCollectionClass() where I need to do database query to join customers attribute data to orders collection. Becouse I'am very new in Magento, logic of magento-way queries for me is very hard to follow. Can someone help me to write MySql query below in Magento-way to get value of my customer attribute 'personal_number' in orders grid:</p>

<pre><code>SELECT Orders.*, Customers.customer_id, Custumer.personal_namber FROM Orders INNER JOIN Customers ON Orders.customer_id = Customer.customer_id
</code></pre>

## Answers
### Answer ID: 28043506
<p>You usually don't need to change <code>_getCollectionClass</code>, but rather do the join on the grid, on <code>_prepareCollection</code>. Ie:</p>

<pre><code>protected function _prepareCollection()
{
    $collection = Mage::getResourceModel($this-&gt;_getCollectionClass());

    //we changed mysql query, we added inner join to order item table
    $collection-&gt;join(
    // Alias =&gt; Table name
    array('customers' =&gt; "customer/customer"), 
    // Join condition
    'main_table.customer_id = customer.customer_id', 
    // Fields to select
    array('personal_number'=&gt;'personal_number');
    $this-&gt;setCollection($collection);
    return parent::_prepareCollection();
}
</code></pre>

<p>Taken from here, have a look at the full article for more help: <a href="http://inchoo.net/magento/how-to-extend-magento-order-grid/" rel="nofollow">http://inchoo.net/magento/how-to-extend-magento-order-grid/</a></p>

