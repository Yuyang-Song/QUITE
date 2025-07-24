# Is storing one Pandas Dataframe for every user valid? (Storing in Google Cloud Storage objects.)
[Link to question](https://stackoverflow.com/questions/41927886/is-storing-one-pandas-dataframe-for-every-user-valid-storing-in-google-cloud-s)
**Creation Date:** 1485739748
**Score:** 0
**Tags:** python, pandas, dataframe, google-cloud-storage
## Question Body
<p>I'm trying to figure out pandas dataframes, and I am trying not to violate best practices.</p>

<p>If I am making a recommendation for products* to show one user, is one dataframe per user a valid way of doing things?</p>

<p>In reading up on Pandas Dataframes it almost seems as though they are tables in a database sense.  So while it seems like I could/should use Pandas in this manner, it also seems that's like using an entire table for every user, which just seems wrong.</p>

<p>The data I am intending to store per customer is something like <strong>#</strong> of times they have seen products with particular attributes, how many times they disliked a product with a certain attribute, and how many times they liked a product from a particular category, or with a particular attribute, etc.</p>

<p>I am planning on storing one dataframe for every user with Google Cloud Storage as an object (and rewriting the entire object every time there is new data).**  I don't expect dataframes individually to become overly large.</p>

<p>I am storing my product data inside Google Datastore, and planning on using information from queries of the dataframes to query appropriate products, and then make final calculations of which products are most relevant based on a more thorough analysis of user information stored within their particular dataframe and every product metatag/category.</p>

<p>Is this anywhere close to how pandas dataframes are meant to work?  Would this solution be feasible?</p>

<p>===</p>

<ul>
<li>very well categorized, and organized with meta data</li>
</ul>

<p>** if this seems like too many updates for that service, please mention it</p>

<hr>

<p>*** Just for more information, I am never planning on comparing users with each other, because products are very time sensitive and I'm only going to show users the newest products anyway; so I can't count on information through collaborative filters to have any relevancy to current products (because other users, who are similar, might not have liked new products recently).</p>

