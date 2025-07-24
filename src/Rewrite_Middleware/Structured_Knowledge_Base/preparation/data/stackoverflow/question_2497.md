# Magento Changing Default Payment Method
[Link to question](https://stackoverflow.com/questions/37175327/magento-changing-default-payment-method)
**Creation Date:** 1463012709
**Score:** 2
**Tags:** magento, magento-1.9
## Question Body
<p>I have a function that runs raw SQL queries to our database in Magento. What the function does is changes the customer's default credit card to a value passed to the function. My question is how would I rewrite the function utilizing Magento models. The current function works, but we'd rather have it not be directly interfacing with SQL.</p>

<p>Here is the function:</p>

<pre><code>public function setDefaultPayment($value)
{
    $customerId = $this-&gt;_getSession()-&gt;getCustomer()-&gt;getId();
    $write = Mage::getSingleton('core/resource')-&gt;getConnection('core_write');

    $read = $write-&gt;query("SELECT entity_type_id FROM eav_entity_type WHERE entity_type_code='customer'");
    $row = $read-&gt;fetch();
    $entity_type_id = $row['entity_type_id'];

    $read = $write-&gt;query("SELECT attribute_id FROM eav_attribute WHERE attribute_code='default_payment' AND entity_type_id = $entity_type_id");
    $row = $read-&gt;fetch();
    $attribute_id = $row['attribute_id'];

    $read = $write-&gt;query("SELECT * FROM customer_entity_int WHERE entity_type_id='$entity_type_id' AND attribute_id='$attribute_id' AND entity_id='$customerId'");
    if ($row = $read-&gt;fetch()) {
        $write-&gt;update(
            'customer_entity_int',
            array('value' =&gt; $value),
            "entity_type_id='$entity_type_id' AND attribute_id='$attribute_id' AND entity_id='$customerId'"
        );
    } else {
        $write-&gt;insert(
            'customer_entity_int',
            array(
                'entity_type_id' =&gt; $entity_type_id,
                'attribute_id' =&gt; $attribute_id,
                'entity_id' =&gt; $customerId,
                'value' =&gt; $value
            )
        );
    }
}
</code></pre>

## Answers
### Answer ID: 37196731
<p>If I read you code right, you want to update the customer attribute <code>default_payment</code> with a value given.</p>

<p>For that you need to:</p>

<ul>
<li>Load the customer by id</li>
<li>Set the new value for the customer attribute <code>default_payment</code></li>
<li>Save the customer</li>
</ul>

<pre class="lang-php prettyprint-override"><code>public function setDefaultPayment($value)
{
    $customerId = $this-&gt;_getSession()-&gt;getCustomer()-&gt;getId();
    $write = Mage::getSingleton('core/resource')-&gt;getConnection('core_write');

    $customer = Mage::getModel('customer/customer')-&gt;load($customerId);
    $oldValue = $customer-&gt;getDefaultPayment(); // optional, just for checking
    $customer-&gt;setDefaultPayment($value);
    $customer-&gt;save();

}
</code></pre>

