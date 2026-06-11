## Q3: Original Query

> **Execution Time:** >300s (timeout)

> All execution times on this page are taken verbatim from the released per-query results in `experiments_results/dsb/`. Because the per-method result files do not share a common id ordering, records are matched by the literal constants of the original query.

```sql
with customer_total_return as  (select cr_returning_customer_sk as ctr_customer_sk         ,ca_state as ctr_state,   	sum(cr_return_amt_inc_tax) as ctr_total_return  from catalog_returns      ,date_dim      ,customer_address  where cr_returned_date_sk = d_date_sk     and d_year =1998    and cr_returning_addr_sk = ca_address_sk   group by cr_returning_customer_sk          ,ca_state )   select  c_customer_id,c_salutation,c_first_name,c_last_name,ca_street_number,ca_street_name                    ,ca_street_type,ca_suite_number,ca_city,ca_county,ca_state,ca_zip,ca_country,ca_gmt_offset                   ,ca_location_type,ctr_total_return  from customer_total_return ctr1      ,customer_address      ,customer  where ctr1.ctr_total_return > (select avg(ctr_total_return)*1.2  			  from customer_total_return ctr2                    	  where ctr1.ctr_state = ctr2.ctr_state)        and ca_address_sk = c_current_addr_sk        and ca_state = 'IL'        and ctr1.ctr_customer_sk = c_customer_sk  order by c_customer_id,c_salutation,c_first_name,c_last_name,ca_street_number,ca_street_name                    ,ca_street_type,ca_suite_number,ca_city,ca_county,ca_state,ca_zip,ca_country,ca_gmt_offset                   ,ca_location_type,ctr_total_return  limit 100;
```

## 1. Rewrite Results

### 1.1. LearnedRewrite

> **Execution Time:** 12.24s

```sql
SELECT customer103.c_customer_id, customer103.c_salutation, customer103.c_first_name, customer103.c_last_name, t2317.ca_street_number, t2317.ca_street_name, t2317.ca_street_type, t2317.ca_suite_number, t2317.ca_city, t2317.ca_county, t2317.ca_state, t2317.ca_zip, t2317.ca_country, t2317.ca_gmt_offset, t2317.ca_location_type, t2316.ctr_total_return FROM (SELECT t2313.cr_returning_customer_sk, t2314.ca_state, SUM(t2313.ctr_total_return * t2314.f2) AS ctr_total_return FROM (SELECT t2309.cr_returning_customer_sk, t2309.cr_returning_addr_sk, SUM(t2309.ctr_total_return * t2311.f1) AS ctr_total_return FROM (SELECT cr_returned_date_sk, cr_returning_customer_sk, cr_returning_addr_sk, SUM(cr_return_amt_inc_tax) AS ctr_total_return FROM catalog_returns GROUP BY cr_returned_date_sk, cr_returning_customer_sk, cr_returning_addr_sk) AS t2309 INNER JOIN (SELECT d_date_sk, COUNT(*) AS f1 FROM date_dim WHERE d_year = 1998 GROUP BY d_date_sk) AS t2311 ON t2309.cr_returned_date_sk = t2311.d_date_sk GROUP BY t2309.cr_returning_customer_sk, t2309.cr_returning_addr_sk) AS t2313 INNER JOIN (SELECT ca_address_sk, ca_state, COUNT(*) AS f2 FROM customer_address GROUP BY ca_address_sk, ca_state) AS t2314 ON t2313.cr_returning_addr_sk = t2314.ca_address_sk GROUP BY t2313.cr_returning_customer_sk, t2314.ca_state) AS t2316 CROSS JOIN (SELECT * FROM customer_address WHERE ca_state = 'IL') AS t2317 INNER JOIN customer AS customer103 ON t2317.ca_address_sk = customer103.c_current_addr_sk AND t2316.cr_returning_customer_sk = customer103.c_customer_sk INNER JOIN (SELECT t2325.ca_state, AVG(t2325.ctr_total_return) AS f1 FROM (SELECT t2322.cr_returning_customer_sk, t2323.ca_state, SUM(t2322.ctr_total_return * t2323.f2) AS ctr_total_return FROM (SELECT t2318.cr_returning_customer_sk, t2318.cr_returning_addr_sk, SUM(t2318.ctr_total_return * t2320.f1) AS ctr_total_return FROM (SELECT cr_returned_date_sk, cr_returning_customer_sk, cr_returning_addr_sk, SUM(cr_return_amt_inc_tax) AS ctr_total_return FROM catalog_returns GROUP BY cr_returned_date_sk, cr_returning_customer_sk, cr_returning_addr_sk) AS t2318 INNER JOIN (SELECT d_date_sk, COUNT(*) AS f1 FROM date_dim WHERE d_year = 1998 GROUP BY d_date_sk) AS t2320 ON t2318.cr_returned_date_sk = t2320.d_date_sk GROUP BY t2318.cr_returning_customer_sk, t2318.cr_returning_addr_sk) AS t2322 INNER JOIN (SELECT ca_address_sk, ca_state, COUNT(*) AS f2 FROM customer_address GROUP BY ca_address_sk, ca_state) AS t2323 ON t2322.cr_returning_addr_sk = t2323.ca_address_sk GROUP BY t2322.cr_returning_customer_sk, t2323.ca_state) AS t2325 GROUP BY t2325.ca_state) AS t2326 ON t2316.ca_state = t2326.ca_state AND t2316.ctr_total_return > t2326.f1 * 1.2 ORDER BY customer103.c_customer_id, customer103.c_salutation, customer103.c_first_name, customer103.c_last_name, t2317.ca_street_number, t2317.ca_street_name, t2317.ca_street_type, t2317.ca_suite_number, t2317.ca_city, t2317.ca_county, t2317.ca_state, t2317.ca_zip, t2317.ca_country, t2317.ca_gmt_offset, t2317.ca_location_type, t2316.ctr_total_return FETCH NEXT 100 ROWS ONLY
```

### 1.2. LLM-R2 (GPT-4o, best of three models)

> **Execution Time:** 1.76s

```sql
SELECT customer.c_customer_id, customer.c_salutation, customer.c_first_name, customer.c_last_name, t1.ca_street_number, t1.ca_street_name, t1.ca_street_type, t1.ca_suite_number, t1.ca_city, t1.ca_county, t1.ca_state, t1.ca_zip, t1.ca_country, t1.ca_gmt_offset, t1.ca_location_type, t0.ctr_total_return FROM (SELECT catalog_returns.cr_returning_customer_sk, customer_address.ca_state, SUM(catalog_returns.cr_return_amt_inc_tax) AS ctr_total_return FROM catalog_returns INNER JOIN (SELECT * FROM date_dim WHERE d_year = 1998) AS t ON catalog_returns.cr_returned_date_sk = t.d_date_sk INNER JOIN customer_address ON catalog_returns.cr_returning_addr_sk = customer_address.ca_address_sk GROUP BY catalog_returns.cr_returning_customer_sk, customer_address.ca_state) AS t0 CROSS JOIN (SELECT * FROM customer_address WHERE ca_state = 'IL') AS t1 INNER JOIN customer ON t1.ca_address_sk = customer.c_current_addr_sk AND t0.cr_returning_customer_sk = customer.c_customer_sk INNER JOIN (SELECT t3.ca_state, AVG(t3.ctr_total_return) AS f1 FROM (SELECT catalog_returns0.cr_returning_customer_sk, customer_address1.ca_state, SUM(catalog_returns0.cr_return_amt_inc_tax) AS ctr_total_return FROM catalog_returns AS catalog_returns0 INNER JOIN (SELECT * FROM date_dim WHERE d_year = 1998) AS t2 ON catalog_returns0.cr_returned_date_sk = t2.d_date_sk INNER JOIN customer_address AS customer_address1 ON catalog_returns0.cr_returning_addr_sk = customer_address1.ca_address_sk GROUP BY catalog_returns0.cr_returning_customer_sk, customer_address1.ca_state) AS t3 GROUP BY t3.ca_state) AS t4 ON t0.ca_state = t4.ca_state AND t0.ctr_total_return > t4.f1 * 1.2 ORDER BY customer.c_customer_id, customer.c_salutation, customer.c_first_name, customer.c_last_name, t1.ca_street_number, t1.ca_street_name, t1.ca_street_type, t1.ca_suite_number, t1.ca_city, t1.ca_county, t1.ca_state, t1.ca_zip, t1.ca_country, t1.ca_gmt_offset, t1.ca_location_type, t0.ctr_total_return LIMIT 100
```

### 1.3. R-Bot (GPT-4o, best of three models)

> **Execution Time:** 1.80s

```sql
SELECT "customer"."c_customer_id", "customer"."c_salutation", "customer"."c_first_name", "customer"."c_last_name", "t1"."ca_street_number0", "t1"."ca_street_name0", "t1"."ca_street_type0", "t1"."ca_suite_number0", "t1"."ca_city0", "t1"."ca_county0", "t1"."ca_state0", "t1"."ca_zip0", "t1"."ca_country0", "t1"."ca_gmt_offset0", "t1"."ca_location_type0", "t0"."ctr_total_return" FROM (SELECT "catalog_returns"."cr_returning_customer_sk", "customer_address"."ca_state", SUM("catalog_returns"."cr_return_amt_inc_tax") AS "ctr_total_return"         FROM "catalog_returns"             INNER JOIN (SELECT *                 FROM "date_dim"                 WHERE "d_year" = 1998) AS "t" ON "catalog_returns"."cr_returned_date_sk" = "t"."d_date_sk"             INNER JOIN "customer_address" ON "catalog_returns"."cr_returning_addr_sk" = "customer_address"."ca_address_sk"         GROUP BY "catalog_returns"."cr_returning_customer_sk", "customer_address"."ca_state") AS "t0"     CROSS JOIN (SELECT *         FROM "customer_address" AS "customer_address0" ("ca_address_sk0", "ca_address_id0", "ca_street_number0", "ca_street_name0", "ca_street_type0", "ca_suite_number0", "ca_city0", "ca_county0", "ca_state0", "ca_zip0", "ca_country0", "ca_gmt_offset0", "ca_location_type0")         WHERE "ca_state0" = 'IL') AS "t1"     INNER JOIN "customer" ON "t1"."ca_address_sk0" = "customer"."c_current_addr_sk" AND "t0"."cr_returning_customer_sk" = "customer"."c_customer_sk"     INNER JOIN (SELECT "t4"."ca_state1", AVG("t4"."ctr_total_return") AS "$f1"         FROM (SELECT "catalog_returns00"."cr_returning_customer_sk0", "customer_address10"."ca_state1", SUM("catalog_returns00"."cr_return_amt_inc_tax0") AS "ctr_total_return"                 FROM "catalog_returns" AS "catalog_returns00" ("cr_returned_date_sk0", "cr_returned_time_sk0", "cr_item_sk0", "cr_refunded_customer_sk0", "cr_refunded_cdemo_sk0", "cr_refunded_hdemo_sk0", "cr_refunded_addr_sk0", "cr_returning_customer_sk0", "cr_returning_cdemo_sk0", "cr_returning_hdemo_sk0", "cr_returning_addr_sk0", "cr_call_center_sk0", "cr_catalog_page_sk0", "cr_ship_mode_sk0", "cr_warehouse_sk0", "cr_reason_sk0", "cr_order_number0", "cr_return_quantity0", "cr_return_amount0", "cr_return_tax0", "cr_return_amt_inc_tax0", "cr_fee0", "cr_return_ship_cost0", "cr_refunded_cash0", "cr_reversed_charge0", "cr_store_credit0", "cr_net_loss0")                     INNER JOIN (SELECT *                         FROM "date_dim" AS "date_dim0" ("d_date_sk0", "d_date_id0", "d_date0", "d_month_seq0", "d_week_seq0", "d_quarter_seq0", "d_year0", "d_dow0", "d_moy0", "d_dom0", "d_qoy0", "d_fy_year0", "d_fy_quarter_seq0", "d_fy_week_seq0", "d_day_name0", "d_quarter_name0", "d_holiday0", "d_weekend0", "d_following_holiday0", "d_first_dom0", "d_last_dom0", "d_same_day_ly0", "d_same_day_lq0", "d_current_day0", "d_current_week0", "d_current_month0", "d_current_quarter0", "d_current_year0")                         WHERE "d_year0" = 1998) AS "t2" ON "catalog_returns00"."cr_returned_date_sk0" = "t2"."d_date_sk0"                     INNER JOIN "customer_address" AS "customer_address10" ("ca_address_sk1", "ca_address_id1", "ca_street_number1", "ca_street_name1", "ca_street_type1", "ca_suite_number1", "ca_city1", "ca_county1", "ca_state1", "ca_zip1", "ca_country1", "ca_gmt_offset1", "ca_location_type1") ON "catalog_returns00"."cr_returning_addr_sk0" = "customer_address10"."ca_address_sk1"                 GROUP BY "catalog_returns00"."cr_returning_customer_sk0", "customer_address10"."ca_state1"                 HAVING "customer_address10"."ca_state1" IS NOT NULL) AS "t4"         GROUP BY "t4"."ca_state1") AS "t5" ON "t0"."ca_state" = "t5"."ca_state1" AND "t0"."ctr_total_return" > "t5"."$f1" * 1.2 ORDER BY "customer"."c_customer_id", "customer"."c_salutation", "customer"."c_first_name", "customer"."c_last_name", "t1"."ca_street_number0", "t1"."ca_street_name0", "t1"."ca_street_type0", "t1"."ca_suite_number0", "t1"."ca_city0", "t1"."ca_county0", "t1"."ca_state0", "t1"."ca_zip0", "t1"."ca_country0", "t1"."ca_gmt_offset0", "t1"."ca_location_type0", "t0"."ctr_total_return" FETCH NEXT 100 ROWS ONLY;
```

### 1.4. LLM Agent (Claude-3.7)

> **Execution Time:** 1.17s  *(non-equivalent: rejected by our validation protocol)*  -- fastest raw rewrite, but its result set differs from the original

```sql
WITH customer_total_return AS (
 SELECT 
 cr_returning_customer_sk as ctr_customer_sk,
 ca_state as ctr_state,
 sum(cr_return_amt_inc_tax) as ctr_total_return,
 avg(sum(cr_return_amt_inc_tax)) OVER (PARTITION BY ca_state) * 1.2 as state_avg
 FROM catalog_returns
 JOIN date_dim ON cr_returned_date_sk = d_date_sk
 JOIN customer_address ON cr_returning_addr_sk = ca_address_sk
 WHERE d_year = 1998
 GROUP BY cr_returning_customer_sk, ca_state
)
SELECT 
 c_customer_id,
 c_salutation,
 c_first_name,
 c_last_name,
 ca_street_number,
 ca_street_name,
 ca_street_type,
 ca_suite_number,
 ca_city,
 ca_county,
 ca_state,
 ca_zip,
 ca_country,
 ca_gmt_offset,
 ca_location_type,
 ctr.ctr_total_return
FROM customer_total_return ctr
JOIN customer c ON ctr.ctr_customer_sk = c_customer_sk
JOIN customer_address ca ON ca_address_sk = c_current_addr_sk
WHERE ca_state = 'IL'
AND ctr_total_return > state_avg
ORDER BY 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16
LIMIT 100
```

### 1.5. QUITE (rewrite only)

> **Execution Time:** 1.51s

```sql
with customer_total_return as (
    select 
        cr_returning_customer_sk as ctr_customer_sk,
        ca_state as ctr_state,
        sum(cr_return_amt_inc_tax) as ctr_total_return
    from catalog_returns
    join date_dim on cr_returned_date_sk = d_date_sk
    join customer_address on cr_returning_addr_sk = ca_address_sk
    where d_year = 1998
    group by cr_returning_customer_sk, ca_state
),
state_averages as (
    select 
        ctr_state,
        avg(ctr_total_return) * 1.2 as avg_120_percent
    from customer_total_return
    group by ctr_state
)
select 
    c_customer_id, c_salutation, c_first_name, c_last_name,
    ca_street_number, ca_street_name, ca_street_type, ca_suite_number,
    ca_city, ca_county, ca_state, ca_zip, ca_country, ca_gmt_offset,
    ca_location_type, ctr_total_return
from customer_total_return ctr1
join customer on ctr1.ctr_customer_sk = c_customer_sk
join customer_address on customer.c_current_addr_sk = customer_address.ca_address_sk
join state_averages sa on ctr1.ctr_state = sa.ctr_state
where customer_address.ca_state = 'IL'
    and ctr1.ctr_total_return > sa.avg_120_percent
order by 
    c_customer_id, c_salutation, c_first_name, c_last_name,
    ca_street_number, ca_street_name, ca_street_type, ca_suite_number,
    ca_city, ca_county, ca_state, ca_zip, ca_country, ca_gmt_offset,
    ca_location_type, ctr_total_return
limit 100;
```

### 1.6. QUITE (with hint injection)

> **Execution Time:** 1.04s

```sql
with customer_total_return AS ( /*+ HashJoin(catalog_returns customer_address) */
    select 
        cr_returning_customer_sk as ctr_customer_sk,
        ca_state as ctr_state,
        sum(cr_return_amt_inc_tax) as ctr_total_return
    from catalog_returns
    join date_dim on cr_returned_date_sk = d_date_sk
    join customer_address on cr_returning_addr_sk = ca_address_sk
    where d_year = 1998
    group by cr_returning_customer_sk, ca_state
),
state_averages as (
    select 
        ctr_state,
        avg(ctr_total_return) * 1.2 as avg_120_percent
    from customer_total_return
    group by ctr_state
)
select 
    c_customer_id, c_salutation, c_first_name, c_last_name,
    ca_street_number, ca_street_name, ca_street_type, ca_suite_number,
    ca_city, ca_county, ca_state, ca_zip, ca_country, ca_gmt_offset,
    ca_location_type, ctr_total_return
from customer_total_return ctr1
join customer on ctr1.ctr_customer_sk = c_customer_sk
join customer_address on customer.c_current_addr_sk = customer_address.ca_address_sk
join state_averages sa on ctr1.ctr_state = sa.ctr_state
where customer_address.ca_state = 'IL'
    and ctr1.ctr_total_return > sa.avg_120_percent
order by 
    c_customer_id, c_salutation, c_first_name, c_last_name,
    ca_street_number, ca_street_name, ca_street_type, ca_suite_number,
    ca_city, ca_county, ca_state, ca_zip, ca_country, ca_gmt_offset,
    ca_location_type, ctr_total_return
limit 100;
```

## 2. Deep Analysis

### 2.1 Query Context and Full Metrics

| Method | Execution Time (s) | Equivalent |
|---|---|---|
| LearnedRewrite | 12.24 | ✓ |
| LLM-R² (Claude-3.7) | 1.79 | ✓ |
| LLM-R² (DS-R1) | 1.79 | ✓ |
| LLM-R² (GPT-4o) | 1.76 | ✓ |
| R-Bot (Claude-3.7) | 3.07 | ✓ |
| R-Bot (DS-R1) | >300 | ✓ |
| R-Bot (GPT-4o) | 1.80 | ✓ |
| LLM Agent (Claude-3.7) | 1.17 | ✗ (non-equivalent) |
| LLM Agent (DS-R1) | 1.23 | ✓ |
| LLM Agent (DS-V3) | >300 | ✓ |
| LLM Agent (GPT-4o) | >300 | ✓ |
| QUITE | 1.51 | ✓ |
| QUITE + hints | 1.04 | ✓ |

The original query never finishes: for every customer it re-evaluates `AVG(ctr_total_return) * 1.2` over the `customer_total_return` CTE, restricted to the customer's state. Decorrelation fixes it, and several methods manage that here. QUITE produces the fastest verified result (1.04s with hints, at least 288x over the original), ahead of LLM Agent DS-R1 (1.23s) and LLM-R2 (1.76s).

### 2.2 What Distinguishes the Methods

1. **Decorrelation.** QUITE adds a `state_averages` CTE that computes the per-state threshold once and joins it back on `ctr_state`, replacing the per-row re-aggregation.
2. **Validation matters.** The fastest raw rewrite (LLM Agent, Claude-3.7, 1.17s) is non-equivalent; our validation protocol rejects exactly this kind of output. QUITE's 1.04s result is the fastest among rewrites that return the original answer.
3. **Hint synergy.** On top of the rewrite, injected plan hints reduce the time from 1.51s to 1.04s by steering the join order of the decorrelated plan.
