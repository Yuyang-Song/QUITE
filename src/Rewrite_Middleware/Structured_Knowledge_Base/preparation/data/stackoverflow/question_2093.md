# CodeIgniter: Cart content gets lost after redirect
[Link to question](https://stackoverflow.com/questions/18453696/codeigniter-cart-content-gets-lost-after-redirect)
**Creation Date:** 1377554156
**Score:** 0
**Tags:** php, codeigniter, session, shopping-cart
## Question Body
<p>I am trying to develop a small web shop with CodeIgniter. To store the items, I use the <a href="http://ellislab.com/codeigniter/user-guide/libraries/cart.html" rel="nofollow">Cart</a> library. Most of the time, everything works great. However, sometimes the content of the cart gets lost after a redirect.</p>

<p>I found a couple of fixes on the web, but none of them works in my case. Here is my setup:</p>

<ul>
<li>I use the DB for storing sessions</li>
<li>I don't use AJAX</li>
<li>There is no underscore in the name of the session cookie</li>
</ul>

<p>Here is an example of a refresh:</p>

<pre><code>public function add_item() {
    $item_id = $this-&gt;input-&gt;post('item');

    // Query database
    $item = $this-&gt;model-&gt;find_item($item_id);

    // Rewrite model info
    ...

    $data = array(
        'id'      =&gt; 'item-' . $item['id'] . '-size-' . $item['sizes'][$i]['id'],
        'qty'     =&gt; $qty,
        'price'   =&gt; $item['sizes'][$i]['price'],
        'name'    =&gt; $item['name'],
        'options' =&gt; array('short_name' =&gt; $item['short_name'])
    );

    $this-&gt;cart-&gt;insert($data);

    usleep(10000);
    redirect('shop');
}
</code></pre>

## Answers
### Answer ID: 18475824
<p>I finally found an answer to my problem, thanks to this question: <a href="https://stackoverflow.com/questions/17083667/codeigniter-cart-and-session-lost-when-refresh-page">CodeIgniter Cart and Session lost when refresh page</a></p>

<p>The problem was that the data stored in the session got too big. CodeIgniter stores all the data in a cookie, which is limited to 4kB. My mistake was to think that, if I used the DB to store my sessions, I could avoid that limit. <a href="http://ellislab.com/codeigniter/user-guide/libraries/sessions.html" rel="nofollow noreferrer">Apparently</a>, CodeIgniter saves sessions in the database "only" for security reasons. There is still a lot of data in the cookie.</p>

<p>Now, I use a library called Native session. I found it here: <a href="https://github.com/EllisLab/CodeIgniter/wiki/Native-session" rel="nofollow noreferrer">https://github.com/EllisLab/CodeIgniter/wiki/Native-session</a></p>

<p>I just put the file in 'application/libraries', renamed the first function to '__construct()', added it to autoimport and replaced all the 'session' tags with 'native_session' in my code. I also had to change the Cart class because it was using CodeIgniter's original session.</p>

