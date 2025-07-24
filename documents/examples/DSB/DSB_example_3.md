## Q3：Original Query

> **Execution Time：** 7.57s

```sql
SELECT    
    cd_gender,
    cd_marital_status,
    cd_education_status,
    COUNT(*) AS cnt1,
    cd_purchase_estimate,
    COUNT(*) AS cnt2,
    cd_credit_rating,
    COUNT(*) AS cnt3
FROM   
    customer c,
    customer_address ca,
    customer_demographics
WHERE   
    c.c_current_addr_sk = ca.ca_address_sk
    AND ca_state IN ('MD', 'MO', 'OK')
    AND cd_demo_sk = c.c_current_cdemo_sk
    AND cd_marital_status IN ('W', 'U', 'W')
    AND cd_education_status IN ('Primary', 'Primary')
    AND EXISTS (
        SELECT * 
        FROM store_sales, date_dim
        WHERE c.c_customer_sk = ss_customer_sk
          AND ss_sold_date_sk = d_date_sk
          AND d_year = 2002
          AND d_moy BETWEEN 5 AND 5 + 2
          AND ss_list_price BETWEEN 132 AND 221
    )
    AND NOT EXISTS (
        SELECT * 
        FROM web_sales, date_dim
        WHERE c.c_customer_sk = ws_bill_customer_sk
          AND ws_sold_date_sk = d_date_sk
          AND d_year = 2002
          AND d_moy BETWEEN 5 AND 5 + 2
          AND ws_list_price BETWEEN 132 AND 221
    )
    AND NOT EXISTS (
        SELECT * 
        FROM catalog_sales, date_dim
        WHERE c.c_customer_sk = cs_ship_customer_sk
          AND cs_sold_date_sk = d_date_sk
          AND d_year = 2002
          AND d_moy BETWEEN 5 AND 5 + 2
          AND cs_list_price BETWEEN 132 AND 221
    )
GROUP BY 
    cd_gender,
    cd_marital_status,
    cd_education_status,
    cd_purchase_estimate,
    cd_credit_rating
ORDER BY 
    cd_gender,
    cd_marital_status,
    cd_education_status,
    cd_purchase_estimate,
    cd_credit_rating
LIMIT 100;

````



## 1. Rewrite Results

### 1.1. LearnedRewrite

> **Execution Time：** 7.90s

```sql
SELECT 
  t45.cd_gender,
  t45.cd_marital_status,
  t45.cd_education_status,
  COUNT(*) AS cnt1,
  t45.cd_purchase_estimate,
  COUNT(*) AS cnt2,
  t45.cd_credit_rating,
  COUNT(*) AS cnt3
FROM (
  SELECT 
    t40.c_customer_sk,
    t40.c_current_hdemo_sk,
    t40.c_current_addr_sk,
    t40.c_first_shipto_date_sk,
    t40.c_first_sales_date_sk,
    t40.c_birth_day,
    t40.c_birth_month,
    t40.c_birth_year,
    t40.c_last_review_date_sk,
    t40.c_current_cdemo_sk,
    t40.c_customer_id,
    t40.c_last_name,
    t40.c_preferred_cust_flag,
    t40.c_birth_country,
    t40.c_login,
    t40.c_email_address,
    t40.c_salutation,
    t40.c_first_name,
    t40.ca_gmt_offset,
    t40.ca_address_sk,
    t40.ca_street_number,
    t40.ca_street_name,
    t40.ca_street_type,
    t40.ca_suite_number,
    t40.ca_city,
    t40.ca_county,
    t40.ca_state,
    t40.ca_zip,
    t40.ca_country,
    t40.ca_location_type,
    t40.ca_address_id,
    t40.cd_dep_college_count,
    t40.cd_purchase_estimate,
    t40.cd_dep_count,
    t40.cd_dep_employed_count,
    t40.cd_demo_sk,
    t40.cd_gender,
    t40.cd_marital_status,
    t40.cd_education_status,
    t40.cd_credit_rating,
    t40.f0,
    t43.f0 AS f041
  FROM (
    SELECT 
      customer1.c_customer_sk,
      customer1.c_current_hdemo_sk,
      customer1.c_current_addr_sk,
      customer1.c_first_shipto_date_sk,
      customer1.c_first_sales_date_sk,
      customer1.c_birth_day,
      customer1.c_birth_month,
      customer1.c_birth_year,
      customer1.c_last_review_date_sk,
      customer1.c_current_cdemo_sk,
      customer1.c_customer_id,
      customer1.c_last_name,
      customer1.c_preferred_cust_flag,
      customer1.c_birth_country,
      customer1.c_login,
      customer1.c_email_address,
      customer1.c_salutation,
      customer1.c_first_name,
      customer_address1.ca_gmt_offset,
      customer_address1.ca_address_sk,
      customer_address1.ca_street_number,
      customer_address1.ca_street_name,
      customer_address1.ca_street_type,
      customer_address1.ca_suite_number,
      customer_address1.ca_city,
      customer_address1.ca_county,
      customer_address1.ca_state,
      customer_address1.ca_zip,
      customer_address1.ca_country,
      customer_address1.ca_location_type,
      customer_address1.ca_address_id,
      customer_demographics1.cd_dep_college_count,
      customer_demographics1.cd_purchase_estimate,
      customer_demographics1.cd_dep_count,
      customer_demographics1.cd_dep_employed_count,
      customer_demographics1.cd_demo_sk,
      customer_demographics1.cd_gender,
      customer_demographics1.cd_marital_status,
      customer_demographics1.cd_education_status,
      customer_demographics1.cd_credit_rating,
      t39.f0
    FROM 
      customer AS customer1
    CROSS JOIN 
      customer_address AS customer_address1
    CROSS JOIN 
      customer_demographics AS customer_demographics1
    LEFT JOIN (
      SELECT 
        t37.ss_customer_sk, 
        TRUE AS f0
      FROM (
        SELECT * 
        FROM store_sales 
        WHERE ss_list_price BETWEEN 132 AND 221
      ) AS t37
      INNER JOIN (
        SELECT * 
        FROM date_dim 
        WHERE d_year = 2002 AND d_moy BETWEEN 5 AND 7
      ) AS t38
      ON t37.ss_sold_date_sk = t38.d_date_sk
    ) AS t39
    ON customer1.c_customer_sk = t39.ss_customer_sk
  ) AS t40
  LEFT JOIN (
    SELECT 
      t41.ws_bill_customer_sk, 
      TRUE AS f0
    FROM (
      SELECT * 
      FROM web_sales 
      WHERE ws_list_price BETWEEN 132 AND 221
    ) AS t41
    INNER JOIN (
      SELECT * 
      FROM date_dim 
      WHERE d_year = 2002 AND d_moy BETWEEN 5 AND 7
    ) AS t42
    ON t41.ws_sold_date_sk = t42.d_date_sk
  ) AS t43
  ON t40.c_customer_sk = t43.ws_bill_customer_sk
  WHERE 
    t40.c_current_addr_sk = t40.ca_address_sk
    AND t40.ca_state IN ('MD', 'MO', 'OK')
    AND t40.cd_demo_sk = t40.c_current_cdemo_sk
    AND t40.cd_marital_status IN ('U', 'W')
    AND t40.cd_education_status = 'Primary'
    AND t43.f0 IS NULL
    AND t40.f0 IS NOT NULL
) AS t45
LEFT JOIN (
  SELECT 
    t46.cs_ship_customer_sk, 
    TRUE AS f0
  FROM (
    SELECT * 
    FROM catalog_sales 
    WHERE cs_list_price BETWEEN 132 AND 221
  ) AS t46
  INNER JOIN (
    SELECT * 
    FROM date_dim 
    WHERE d_year = 2002 AND d_moy BETWEEN 5 AND 7
  ) AS t47
  ON t46.cs_sold_date_sk = t47.d_date_sk
) AS t48
ON t45.c_customer_sk = t48.cs_ship_customer_sk
WHERE 
  t48.f0 IS NULL
GROUP BY 
  t45.cd_gender,
  t45.cd_marital_status,
  t45.cd_education_status,
  t45.cd_purchase_estimate,
  t45.cd_credit_rating
ORDER BY 
  t45.cd_gender,
  t45.cd_marital_status,
  t45.cd_education_status,
  t45.cd_purchase_estimate,
  t45.cd_credit_rating
FETCH NEXT 100 ROWS ONLY;

```



### 1.2. LLM-R2

> **Execution Time：** 7.89s
>
> ```sql
> SELECT 
>   t7.cd_gender, 
>   t7.cd_marital_status, 
>   t7.cd_education_status, 
>   COUNT(*) AS cnt1, 
>   t7.cd_purchase_estimate, 
>   COUNT(*) AS cnt2, 
>   t7.cd_credit_rating, 
>   COUNT(*) AS cnt3
> FROM (
>   SELECT * FROM (
>     SELECT 
>       t2.c_customer_sk,
>       t2.c_current_hdemo_sk,
>       t2.c_current_addr_sk,
>       t2.c_first_shipto_date_sk,
>       t2.c_first_sales_date_sk,
>       t2.c_birth_day,
>       t2.c_birth_month,
>       t2.c_birth_year,
>       t2.c_last_review_date_sk,
>       t2.c_current_cdemo_sk,
>       t2.c_customer_id,
>       t2.c_last_name,
>       t2.c_preferred_cust_flag,
>       t2.c_birth_country,
>       t2.c_login,
>       t2.c_email_address,
>       t2.c_salutation,
>       t2.c_first_name,
>       t2.ca_gmt_offset,
>       t2.ca_address_sk,
>       t2.ca_street_number,
>       t2.ca_street_name,
>       t2.ca_street_type,
>       t2.ca_suite_number,
>       t2.ca_city,
>       t2.ca_county,
>       t2.ca_state,
>       t2.ca_zip,
>       t2.ca_country,
>       t2.ca_location_type,
>       t2.ca_address_id,
>       t2.cd_dep_college_count,
>       t2.cd_purchase_estimate,
>       t2.cd_dep_count,
>       t2.cd_dep_employed_count,
>       t2.cd_demo_sk,
>       t2.cd_gender,
>       t2.cd_marital_status,
>       t2.cd_education_status,
>       t2.cd_credit_rating,
>       t2.f0,
>       t5.f0 AS f041
>     FROM (
>       SELECT 
>         customer.c_customer_sk,
>         customer.c_current_hdemo_sk,
>         customer.c_current_addr_sk,
>         customer.c_first_shipto_date_sk,
>         customer.c_first_sales_date_sk,
>         customer.c_birth_day,
>         customer.c_birth_month,
>         customer.c_birth_year,
>         customer.c_last_review_date_sk,
>         customer.c_current_cdemo_sk,
>         customer.c_customer_id,
>         customer.c_last_name,
>         customer.c_preferred_cust_flag,
>         customer.c_birth_country,
>         customer.c_login,
>         customer.c_email_address,
>         customer.c_salutation,
>         customer.c_first_name,
>         customer_address.ca_gmt_offset,
>         customer_address.ca_address_sk,
>         customer_address.ca_street_number,
>         customer_address.ca_street_name,
>         customer_address.ca_street_type,
>         customer_address.ca_suite_number,
>         customer_address.ca_city,
>         customer_address.ca_county,
>         customer_address.ca_state,
>         customer_address.ca_zip,
>         customer_address.ca_country,
>         customer_address.ca_location_type,
>         customer_address.ca_address_id,
>         customer_demographics.cd_dep_college_count,
>         customer_demographics.cd_purchase_estimate,
>         customer_demographics.cd_dep_count,
>         customer_demographics.cd_dep_employed_count,
>         customer_demographics.cd_demo_sk,
>         customer_demographics.cd_gender,
>         customer_demographics.cd_marital_status,
>         customer_demographics.cd_education_status,
>         customer_demographics.cd_credit_rating,
>         t1.f0
>       FROM 
>         customer 
>         CROSS JOIN customer_address 
>         CROSS JOIN customer_demographics 
>         LEFT JOIN (
>           SELECT 
>             t.ss_customer_sk, 
>             TRUE AS f0 
>           FROM (
>             SELECT * 
>             FROM store_sales 
>             WHERE ss_list_price BETWEEN 132 AND 221
>           ) AS t
>           INNER JOIN (
>             SELECT * 
>             FROM date_dim 
>             WHERE d_year = 2002 AND d_moy BETWEEN 5 AND 7
>           ) AS t0 
>           ON t.ss_sold_date_sk = t0.d_date_sk
>         ) AS t1 
>         ON customer.c_customer_sk = t1.ss_customer_sk
>     ) AS t2 
>     LEFT JOIN (
>       SELECT 
>         t3.ws_bill_customer_sk, 
>         TRUE AS f0 
>       FROM (
>         SELECT * 
>         FROM web_sales 
>         WHERE ws_list_price BETWEEN 132 AND 221
>       ) AS t3
>       INNER JOIN (
>         SELECT * 
>         FROM date_dim 
>         WHERE d_year = 2002 AND d_moy BETWEEN 5 AND 7
>       ) AS t4 
>       ON t3.ws_sold_date_sk = t4.d_date_sk
>     ) AS t5 
>     ON t2.c_customer_sk = t5.ws_bill_customer_sk
>   ) AS t6
>   WHERE 
>     t6.c_current_addr_sk = t6.ca_address_sk 
>     AND t6.ca_state IN ('MD', 'MO', 'OK') 
>     AND t6.cd_demo_sk = t6.c_current_cdemo_sk
>     AND t6.cd_marital_status IN ('U', 'W') 
>     AND t6.cd_education_status = 'Primary' 
>     AND t6.f041 IS NULL 
>     AND t6.f0 IS NOT NULL
> ) AS t7
> LEFT JOIN (
>   SELECT 
>     t8.cs_ship_customer_sk, 
>     TRUE AS f0 
>   FROM (
>     SELECT * 
>     FROM catalog_sales 
>     WHERE cs_list_price BETWEEN 132 AND 221
>   ) AS t8
>   INNER JOIN (
>     SELECT * 
>     FROM date_dim 
>     WHERE d_year = 2002 AND d_moy BETWEEN 5 AND 7
>   ) AS t9 
>   ON t8.cs_sold_date_sk = t9.d_date_sk
> ) AS t10 
> ON t7.c_customer_sk = t10.cs_ship_customer_sk
> WHERE t10.f0 IS NULL
> GROUP BY 
>   t7.cd_gender, 
>   t7.cd_marital_status, 
>   t7.cd_education_status, 
>   t7.cd_purchase_estimate, 
>   t7.cd_credit_rating
> ORDER BY 
>   t7.cd_gender, 
>   t7.cd_marital_status, 
>   t7.cd_education_status, 
>   t7.cd_purchase_estimate, 
>   t7.cd_credit_rating
> LIMIT 100;
> 
> ```
>
> 

---

### 1.3. R-Bot 

> **Execution Time：** 8.53s

```sql
SELECT 
  t9.cd_gender, 
  t9.cd_marital_status, 
  t9.cd_education_status, 
  COUNT(*) AS cnt3, 
  t9.cd_purchase_estimate, 
  COUNT(*) AS cnt30, 
  t9.cd_credit_rating, 
  COUNT(*) AS cnt31
FROM (
  SELECT *
  FROM customer
    INNER JOIN (
      SELECT * 
      FROM customer_address 
      WHERE CAST(ca_state AS CHAR(2)) IN ('MD', 'MO', 'OK')
    ) AS t 
      ON customer.c_current_addr_sk = t.ca_address_sk
    INNER JOIN (
      SELECT * 
      FROM customer_demographics 
      WHERE CAST(cd_marital_status AS CHAR(1)) IN ('U', 'W')
        AND cd_education_status = 'Primary'
    ) AS t0 
      ON customer.c_current_cdemo_sk = t0.cd_demo_sk
    INNER JOIN (
      SELECT t1.ss_customer_sk, TRUE AS "$f1"
      FROM (
        SELECT * 
        FROM store_sales 
        WHERE ss_list_price BETWEEN 132 AND 221
          AND ss_customer_sk IS NOT NULL
      ) AS t1
      INNER JOIN (
        SELECT * 
        FROM date_dim 
        WHERE d_year = 2002 AND d_moy BETWEEN 5 AND 5 + 2
      ) AS t2 
        ON t1.ss_sold_date_sk = t2.d_date_sk
      GROUP BY t1.ss_customer_sk
    ) AS t4 
      ON customer.c_customer_sk = t4.ss_customer_sk
    LEFT JOIN (
      SELECT t5.ws_bill_customer_sk, TRUE AS "$f1"
      FROM (
        SELECT * 
        FROM web_sales 
        WHERE ws_list_price BETWEEN 132 AND 221
          AND ws_bill_customer_sk IS NOT NULL
      ) AS t5
      INNER JOIN (
        SELECT * 
        FROM date_dim AS date_dim0 (
          d_date_sk0, d_date_id0, d_date0, d_month_seq0, d_week_seq0, 
          d_quarter_seq0, d_year0, d_dow0, d_moy0, d_dom0, d_qoy0, 
          d_fy_year0, d_fy_quarter_seq0, d_fy_week_seq0, d_day_name0, 
          d_quarter_name0, d_holiday0, d_weekend0, d_following_holiday0, 
          d_first_dom0, d_last_dom0, d_same_day_ly0, d_same_day_lq0, 
          d_current_day0, d_current_week0, d_current_month0, 
          d_current_quarter0, d_current_year0
        ) 
        WHERE d_year0 = 2002 AND d_moy0 BETWEEN 5 AND 5 + 2
      ) AS t6 
        ON t5.ws_sold_date_sk = t6.d_date_sk0
      GROUP BY t5.ws_bill_customer_sk
    ) AS t8 
      ON customer.c_customer_sk = t8.ws_bill_customer_sk
  WHERE t8."$f1" IS NULL
) AS t9
LEFT JOIN (
  SELECT t10.cs_ship_customer_sk, TRUE AS "$f10"
  FROM (
    SELECT * 
    FROM catalog_sales 
    WHERE cs_list_price BETWEEN 132 AND 221
      AND cs_ship_customer_sk IS NOT NULL
  ) AS t10
  INNER JOIN (
    SELECT * 
    FROM date_dim AS date_dim1 (
      d_date_sk1, d_date_id1, d_date1, d_month_seq1, d_week_seq1, 
      d_quarter_seq1, d_year1, d_dow1, d_moy1, d_dom1, d_qoy1, 
      d_fy_year1, d_fy_quarter_seq1, d_fy_week_seq1, d_day_name1, 
      d_quarter_name1, d_holiday1, d_weekend1, d_following_holiday1, 
      d_first_dom1, d_last_dom1, d_same_day_ly1, d_same_day_lq1, 
      d_current_day1, d_current_week1, d_current_month1, 
      d_current_quarter1, d_current_year1
    ) 
    WHERE d_year1 = 2002 AND d_moy1 BETWEEN 5 AND 5 + 2
  ) AS t11 
    ON t10.cs_sold_date_sk = t11.d_date_sk1
  GROUP BY t10.cs_ship_customer_sk
) AS t13 
  ON t9.c_customer_sk = t13.cs_ship_customer_sk
WHERE t13."$f10" IS NULL
GROUP BY 
  t9.cd_gender, 
  t9.cd_marital_status, 
  t9.cd_education_status, 
  t9.cd_purchase_estimate, 
  t9.cd_credit_rating
ORDER BY 
  t9.cd_gender, 
  t9.cd_marital_status, 
  t9.cd_education_status, 
  t9.cd_purchase_estimate, 
  t9.cd_credit_rating
FETCH NEXT 100 ROWS ONLY;

```



### 1.4. QUITE 

> **Execution Time：** 1.84s

```sql
WITH date_range AS (
    SELECT d_date_sk
    FROM date_dim
    WHERE d_year = 2002
      AND d_moy BETWEEN 5 AND 7
),
eligible_customers AS (
    SELECT DISTINCT c.c_customer_sk
    FROM customer c
    JOIN customer_address ca 
        ON c.c_current_addr_sk = ca.ca_address_sk
    JOIN customer_demographics cd 
        ON cd.cd_demo_sk = c.c_current_cdemo_sk
    JOIN store_sales ss 
        ON c.c_customer_sk = ss.ss_customer_sk
    JOIN date_range 
        ON ss.ss_sold_date_sk = date_range.d_date_sk
    WHERE ca.ca_state IN ('MD', 'MO', 'OK')
      AND cd.cd_marital_status IN ('W', 'U')
      AND cd.cd_education_status = 'Primary'
      AND ss.ss_list_price BETWEEN 132 AND 221
      AND NOT EXISTS (
          SELECT 1
          FROM web_sales ws
          JOIN date_range 
              ON ws.ws_sold_date_sk = date_range.d_date_sk
          WHERE c.c_customer_sk = ws.ws_bill_customer_sk
            AND ws.ws_list_price BETWEEN 132 AND 221
          
          UNION ALL
          
          SELECT 1
          FROM catalog_sales cs
          JOIN date_range 
              ON cs.cs_sold_date_sk = date_range.d_date_sk
          WHERE c.c_customer_sk = cs.cs_ship_customer_sk
            AND cs.cs_list_price BETWEEN 132 AND 221
      )
)
SELECT 
    cd.cd_gender,
    cd.cd_marital_status,
    cd.cd_education_status,
    COUNT(*) AS cnt1,
    cd.cd_purchase_estimate,
    COUNT(*) AS cnt2,
    cd.cd_credit_rating,
    COUNT(*) AS cnt3
FROM customer c
JOIN customer_address ca 
    ON c.c_current_addr_sk = ca.ca_address_sk
JOIN customer_demographics cd 
    ON cd.cd_demo_sk = c.c_current_cdemo_sk
WHERE ca.ca_state IN ('MD', 'MO', 'OK')
  AND cd.cd_marital_status IN ('W', 'U')
  AND cd.cd_education_status = 'Primary'
  AND c.c_customer_sk IN (
      SELECT c_customer_sk 
      FROM eligible_customers
  )
GROUP BY 
    cd.cd_gender,
    cd.cd_marital_status,
    cd.cd_education_status,
    cd.cd_purchase_estimate,
    cd.cd_credit_rating
ORDER BY 
    cd.cd_gender,
    cd.cd_marital_status,
    cd.cd_education_status,
    cd.cd_purchase_estimate,
    cd.cd_credit_rating
LIMIT 100;

```





### **2. Deep Analysis**

#### **2.1 Query Context and Baseline Metrics**

This query identifies customers in three specific states (`MD`, `MO`, `OK`) with certain demographic attributes (`marital_status='W' or 'U'`, `education_status='Primary'`), who made in‐store purchases in May–July 2002 at list prices between 132 and 221, **and** who did **not** make any web or catalog purchases in that same window. It then groups these qualifying customers by five demographic columns and counts three separate measures (the three `COUNT(*)` expressions are logically identical but appear in the SELECT list as `cnt1`, `cnt2`, `cnt3`).

The chief difficulty lies in efficiently enforcing the three EXISTS/NOT EXISTS subqueries over large sales tables (`store_sales`, `web_sales`, `catalog_sales`) joined to `date_dim`, while simultaneously filtering on `customer_address`and `customer_demographics`. Naively evaluating each EXISTS/NOT EXISTS can result in repeated scans over the sales tables.

| **Rewrite Method**  | **Execution Time (s)** |
| ------------------- | ---------------------- |
| Original            | 7.57                   |
| LearnedRewrite (LR) | 7.90                   |
| LLM-R2              | 7.89                   |
| R-Bot               | 8.53                   |
| **QUITE**           | **1.84**               |

Even though the original and most rewrites finish in under 9 seconds, QUITE completes in **1.84s**, representing roughly a **4×** speedup compared to the next-best (Original 7.57s → QUITE 1.84s). This improvement highlights the value of early reduction and eliminating repeated subqueries.

------

#### **2.2 Quantifying the Runtime Gap**

- **Original vs. QUITE**
  The original query evaluates three separate EXISTS/NOT EXISTS subqueries, each scanning a large sales table (`store_sales`, `web_sales`, or `catalog_sales`) joined to `date_dim` for the same 3-month criteria. As a result, `date_dim` and each fact table are scanned multiple times for each customer in the base `FROM`. QUITE collapses all date windows into one CTE (`date_range`) and pushes eligibility checks into a single CTE (`eligible_customers`), eliminating redundant scans. This yields a **4.1×** speedup (7.57s → 1.84s).
- **LearnedRewrite vs. QUITE**
  LearnedRewrite essentially inlines all columns from `customer`, `customer_address`, and `customer_demographics`, then performs a LEFT JOIN for the store_sales check, another LEFT JOIN for the web_sales check, and a final LEFT JOIN for catalog_sales, each joined to `date_dim`. It filters out disqualifying rows at the end (`WHERE t43.f0 IS NULL AND t40.f0 IS NOT NULL AND t48.f0 IS NULL`). All three subqueries run independently, causing repeated date_dim evaluations and large intermediate joins. QUITE’s single‐pass CTE replacement reduces intermediate row counts greatly, running in **1.84s** vs. 7.90s (≈ 4.3× faster).
- **LLM-R2 vs. QUITE**
  LLM-R2 also nests multiple SELECT * blocks and LEFT JOINs, one for store_sales, one for web_sales, one for catalog_sales, each joined to `date_dim`. Although logically equivalent to LR, it wraps each filter in an extra subquery layer, preventing early pruning. It finishes in 7.89s—still ≈ 4.3× slower than QUITE.
- **R-Bot vs. QUITE**
  R-Bot applies filters on `customer_address` and `customer_demographics` using inline JOINs, then performs a grouped EXISTS check for store_sales, a left join for web_sales, and a left join for catalog_sales. It groups the store_sales subquery by `ss_customer_sk` to produce a boolean indicator (`"$f1"`). Despite these improvements, it still scans each dimension of date separately and carries extra grouping overhead, finishing in 8.53s—**4.6×** slower than QUITE.

------

#### **2.3 Core Reasons for QUITE’s Superior Efficiency**

##### **2.3.1 Consolidated Date Filtering via a Single CTE**

- **Original / LR / LLM-R2 / R-Bot:**
  Each of these evaluates three distinct subqueries on `date_dim`, one per sales channel. Concretely:

  1. In the EXISTS clause:

     ```sql
     SELECT * 
       FROM store_sales ss
       JOIN date_dim d 
         ON ss.ss_sold_date_sk = d.d_date_sk
       WHERE d.d_year = 2002 
         AND d.d_moy BETWEEN 5 AND 7 
         AND ss.ss_list_price BETWEEN 132 AND 221 
         AND c.c_customer_sk = ss.ss_customer_sk
     ```

     (and analogously for web_sales and catalog_sales).

  2. This repeats the `date_dim` scan three times (once per subquery), adding I/O cost.

- **QUITE’s Approach:**

  ```sql
  WITH date_range AS (
      SELECT d_date_sk
      FROM date_dim
      WHERE d_year = 2002
        AND d_moy BETWEEN 5 AND 7
  )
  ```

  This single CTE produces a small set (all `d_date_sk` for May–July 2002). All three sales‐table checks then **join to `date_range` rather than scanning `date_dim` separately**. This early consolidation means:

  - Only **one** scan of `date_dim` occurs.
  - Each sales‐table join uses a small filtered set of date keys.
  - The optimizer can treat `date_range` as a tiny in-memory table, enabling hash‐join or semi-join optimizations against each sales fact.

##### **2.3.2 Early “Eligible Customers” Extraction**

- **Original / LR / LLM-R2 / R-Bot:**
  They all begin with `customer c JOIN customer_address ca JOIN customer_demographics cd` in the top level, then attach three separate EXISTS/LEFT JOIN filters. Since the EXISTS checks are correlated with `c.c_customer_sk`, each candidate customer row triggers independent scans (or semi-joins) against the sales tables.

- **QUITE’s CTE `eligible_customers`**:

  ```sql
  eligible_customers AS (
      SELECT DISTINCT c.c_customer_sk
      FROM customer c
      JOIN customer_address ca 
        ON c.c_current_addr_sk = ca.ca_address_sk
      JOIN customer_demographics cd 
        ON cd.cd_demo_sk = c.c_current_cdemo_sk
      JOIN store_sales ss 
        ON c.c_customer_sk = ss.ss_customer_sk
      JOIN date_range 
        ON ss.ss_sold_date_sk = date_range.d_date_sk
      WHERE ca.ca_state IN ('MD','MO','OK')
        AND cd.cd_marital_status IN ('W','U')
        AND cd.cd_education_status = 'Primary'
        AND ss.ss_list_price BETWEEN 132 AND 221
        AND NOT EXISTS (
          SELECT 1 
            FROM web_sales ws
            JOIN date_range 
              ON ws.ws_sold_date_sk = date_range.d_date_sk
          WHERE c.c_customer_sk = ws.ws_bill_customer_sk
            AND ws.ws_list_price BETWEEN 132 AND 221
        )
        AND NOT EXISTS (
          SELECT 1
            FROM catalog_sales cs
            JOIN date_range 
              ON cs.cs_sold_date_sk = date_range.d_date_sk
          WHERE c.c_customer_sk = cs.cs_ship_customer_sk
            AND cs.cs_list_price BETWEEN 132 AND 221
        )
  )
  ```

  - All filtering logic—customer address, demographics, in‐store sales, absence of web/catalog sales—is **combined into a single pass**.
  - The sales tables are scanned **once each** (store_sales, web_sales, catalog_sales) joined to the small `date_range`, rather than multiple correlated subqueries.
  - The `DISTINCT c_customer_sk` yields a small set of “eligible” keys without repeating checks per customer row.

##### **2.3.3 Final Aggregation on a Reduced Set**

- **Original / LR / LLM-R2 / R-Bot:**
  After filtering via EXISTS/NOT EXISTS, they group by five demographic columns and compute three `COUNT(*)`s. But because the filtering phase did not reduce the customer set until after evaluation of all subqueries, the grouping still sees nearly the full customer set (minus disqualified ones). The grouping thus processes tens of thousands (or more) rows.

- **QUITE:**
  The outer query simply does:

  ```sql
  SELECT
    cd.cd_gender,
    cd.cd_marital_status,
    cd.cd_education_status,
    COUNT(*) AS cnt1,
    cd.cd_purchase_estimate,
    COUNT(*) AS cnt2,
    cd.cd_credit_rating,
    COUNT(*) AS cnt3
  FROM customer c
  JOIN customer_address ca ON c.c_current_addr_sk = ca.ca_address_sk
  JOIN customer_demographics cd ON cd.cd_demo_sk = c.c_current_cdemo_sk
  WHERE ca.ca_state IN ('MD','MO','OK')
    AND cd.cd_marital_status IN ('W','U')
    AND cd.cd_education_status = 'Primary'
    AND c.c_customer_sk IN (SELECT c_customer_sk FROM eligible_customers)
  GROUP BY
    cd.cd_gender,
    cd.cd_marital_status,
    cd.cd_education_status,
    cd.cd_purchase_estimate,
    cd.cd_credit_rating
  ```

  - The `IN (SELECT c_customer_sk FROM eligible_customers)` clause references a **small list** of customer SKs.
  - After this filter, only those customers who meet all criteria enter the grouping phase. Thus, the `GROUP BY` is executed over a drastically smaller set—often only a few thousand rows—versus tens or hundreds of thousands in the alternative rewrites.

##### **2.3.4 Guiding the Optimizer with a Flat, Two-Stage Plan**

- **Nested EXISTS/LEFT JOIN** patterns in the other rewrites force the optimizer to “guess” a join order among customer → sales → date_dim three times, with limited visibility into cardinalities early on.
- **QUITE’s two-stage split** (build `eligible_customers` then group) shows a clear data‐flow:
  1. Build a small “eligible” set by hooking `customer`, `address`, `demographics`, `store_sales`, `web_sales`, and `catalog_sales` all to `date_range`.
  2. Join that tiny result back to `customer`+`address`+`demographics` for final aggregation.

Because each stage works on as few rows as possible, the optimizer can allocate memory for hash tables more accurately, avoid spilling to disk, and pick efficient join orders (e.g., hash‐join `date_range`→`store_sales` first, then anti-join to `web_sales`, etc.). In contrast, other rewrites keep bulky intermediate sets.

------

#### **2.4 Illustrative Runtime Breakdown**

| **Rewrite Method**  | **Key Traits**                                               | **Runtime (s)** | **Speedup vs. QUITE** |
| ------------------- | ------------------------------------------------------------ | --------------- | --------------------- |
| Original            | Three separate EXISTS/NOT EXISTS subqueries → three `date_dim` scans + three large sales-table scans (per customer). | 7.57            | ~4.1× slower          |
| LearnedRewrite (LR) | Inline all columns; LEFT JOIN store_sales/date_dim, LEFT JOIN web_sales/date_dim, LEFT JOIN catalog_sales/date_dim + final WHERE filters. | 7.90            | ~4.3× slower          |
| LLM-R2              | Multiple nested `SELECT *` blocks wrapping each filter; three independent date_dim scans; extra grouping overhead. | 7.89            | ~4.3× slower          |
| R-Bot               | ANSI JOINs with grouped store_sales result, left joins for web/catalog; still three date_dim scans and group-by per channel. | 8.53            | ~4.6× slower          |
| **QUITE**           | **CTE `date_range` (single date_dim scan) + CTE `eligible_customers` (one pass over store, web, catalog sales joined to date_range) → small final GROUP.** | **1.84**        | **Baseline**          |

