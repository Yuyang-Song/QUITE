# SQLAlchemy match with or
[Link to question](https://stackoverflow.com/questions/33559210/sqlalchemy-match-with-or)
**Creation Date:** 1446782096
**Score:** 0
**Tags:** python, flask, sqlalchemy
## Question Body
<p>I'm getting myself tied up in knots with some sqlalchemy I'm trying to work out.  I've got an old web app I'm trying to tart up, and have decided to rewrite it from scratch.  As part of that, I'm playing with SQL Alchemy and trying to improve my pythonic skills - so I've got a search object I'm trying to run, where I'm checking to see if the customer query exists in either the account name and customer name fields and match against either of them.  However SQL Alchemy registers it as an AND
If I add extra or_ blocks, it fails to recognise them and process appropriately.</p>

<p>I've moved it so it's the first query, but the query planner in sqlalchemy leaves it exactly the same.</p>

<p>Any ideas?</p>

<pre><code>def CustomerCountryMatch(query, page):
    customer=models.Customer
    country=models.CustomerCodes 
    query=customer.query.order_by(customer.account_name).\
        group_by(customer.account_name).having(func.max(customer.renewal_date)).\
        join(country, customer.country_code==country.CODE).\
        add_columns(customer.account_name,
            customer.customer_name,
            customer.account_id,
            customer.CustomerNote,
            country.COUNTRY,
            country.SupportRegion,
            customer.renewal_date,
            customer.contract_type,
            customer.CCGroup).\
        filter(customer.account_name.match(query)).filter(or_(customer.customer_name.match(query))).\
        paginate(page, 50, False)
</code></pre>

<p>The query as executed is below:</p>

<pre class="lang-text prettyprint-override"><code>sqlalchemy.engine.base.Engine SELECT customer.customer_id AS customer_customer_id,
customer.customer_code AS customer_customer_code,
customer.address_code AS customer_address_code,
customer.customer_name AS customer_customer_name,
customer.account_id AS customer_account_id,
customer.account_name AS customer_account_name,
customer.`CustomerNote` AS `customer_CustomerNote`,
customer.renewal_date AS customer_renewal_date,
customer.contract_type AS customer_contract_type,
customer.country_code AS customer_country_code,
customer.`CCGroup` AS `customer_CCGroup`,
customer.`AgentStatus` AS `customer_AgentStatus`,
customer.comments AS customer_comments,
customer.`SCR` AS `customer_SCR`,
customer.`isDummy` AS `customer_isDummy`,
customer_codes.`COUNTRY` AS `customer_codes_COUNTRY`,
customer_codes.`SupportRegion` AS `customer_codes_SupportRegion` 
FROM customer INNER JOIN 
customer_codes ON customer.country_code=customer_codes.`CODE` WHERE 
MATCH (customer.account_name) AGAINST (%s IN BOOLEAN MODE) AND 
MATCH (customer.customer_name) AGAINST (%s IN BOOLEAN MODE) GROUP BY 
customer.account_name HAVING max(customer.renewal_date) ORDER BY 
customer.account_name LIMIT %s,
%s 2015-11-06 03:32:52,035 INFO sqlalchemy.engine.base.Engine ('bob', 'bob', 0, 50)
</code></pre>

## Answers
### Answer ID: 44068639
<p>A simpler approach is to use an OR clause using the '|' operator within your match if you want to find all matches that contain one or more of the words your are searching for eg</p>

<pre><code>query = query.filter(Table.text_searchable_column.match('findme | orme'))
</code></pre>

### Answer ID: 33564741
<p>The filter clause should be:</p>

<pre><code>filter(
    or_(
        customer.account_name.match(query), 
        customer.customer_name.match(query)
    )
)
</code></pre>

<p>Calling <code>filter</code> twice, as in <code>filter(clause1).filter(clause2)</code> joins the criteria using <code>AND</code> (see the <a href="http://docs.sqlalchemy.org/en/rel_1_0/orm/tutorial.html?highlight=filter#querying" rel="nofollow">docs</a>).</p>

<p>The construct: <code>filter(clause1).filter(or_(clause2))</code> does not do what you intend, and is translated into SQL: <code>clause1 AND clause2</code>.</p>

<p>The following example makes sense: <code>filter(clause1).filter(or_(clause2, clause3))</code>, and is translated into SQL as: <code>clause1 AND (clause2 OR clause 3)</code>.</p>

