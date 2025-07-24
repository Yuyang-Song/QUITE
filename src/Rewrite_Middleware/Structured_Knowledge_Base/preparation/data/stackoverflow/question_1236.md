# Is it possible to wait for inner `await` before continuing?
[Link to question](https://stackoverflow.com/questions/65328986/is-it-possible-to-wait-for-inner-await-before-continuing)
**Creation Date:** 1608143005
**Score:** 1
**Tags:** javascript, node.js, mongodb, mongoose
## Question Body
<p>I'm writing a function that calculates the total $ amount by querying the database to get the price, and then multiplying it by the quantity. It does this for every item in the array and pushes the total to an array which is then reduced to one final total number which is returned. The function is shown below:</p>
<pre class="lang-js prettyprint-override"><code>const calculateOrderAmount = async (items: cartProduct[]): Promise&lt;number&gt; =&gt; {
  const priceArray: number[] = [];
  items.forEach(async (p: cartProduct) =&gt; {
    const product = await Product.findById(p.prodId).exec();
    if (product) {
      const totalPrice = product.price * p.quantity;
      priceArray.push(totalPrice)
    } else return; 
  });
  let amount;
  if (priceArray.length === 0) amount = 0;
  else amount = priceArray.reduce((a, b) =&gt; a + b);
  return amount;
};
</code></pre>
<p>The problem that I'm having is with the asynchronicity of it. I want it to wait for the <code>forEach</code> to finish, but since it's asynchronous, it keeps going and does the rest of the function first, so it end up returning 0. Is there a way to make it wait for the <code>forEach</code> to finish? Or should I rewrite it in a different way</p>

## Answers
### Answer ID: 65329080
<p>By using a <code>forEach</code> callback, you create a separate series of promises, but the <code>forEach</code> call itself will not await those promises.</p>
<p>The simple solution is to use a <code>for</code> loop, which does not use a callback system:</p>
<pre><code>for (let p: cartProduct of items) {
    const product = await Product.findById(p.prodId).exec();
    if (!product) continue;
    const totalPrice = product.price * p.quantity;
    priceArray.push(totalPrice);
}
</code></pre>

### Answer ID: 65329024
<p>You can try the <code>for await of</code> construct:</p>
<pre class="lang-js prettyprint-override"><code>for await (variable of iterable) {
 statement
}
</code></pre>
<p><a href="https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for-await...of" rel="nofollow noreferrer">https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Statements/for-await...of</a></p>

