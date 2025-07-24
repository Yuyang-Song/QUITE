# How to replace the OR condition in the Oracle SQL query?
[Link to question](https://stackoverflow.com/questions/71852371/how-to-replace-the-or-condition-in-the-oracle-sql-query)
**Creation Date:** 1649828193
**Score:** 0
**Tags:** oracle-database, query-optimization, oracle12c, database-cursor
## Question Body
<p>I am using Oracle Database 12c Enterprise Edition Release 12.2.0.1.0 - 64bit Production</p>
<p>Can somebody please tell me how to rewrite the below cursor query so that</p>
<p>it does not use the &quot;OR&quot; clause in the where condition</p>
<p>for performance benefits.</p>
<p>Basically the OR condition should be removed appropriately in the query.</p>
<pre><code>CURSOR c_picklist_dtl IS
SELECT DISTINCT pd.dc_code,
               pd.storer,
               pd.picklist_key,
               pd.pickdetail_key,
               pd.line_no,
               pd.pick_type,
               pd.case_id,
               pd.order_type,
               pd.sub_type,
               pd.order_no,
               pd.item,
               pd.consignee,
               pd.bin_code,
               pd.lot,
               pd.pallet_id,
               pd.packkey,
               pd.to_pick_qty,
               am.bin_code dispatch_bin_code,
               ph.wave_id,
               ph.po_no,
               pd.pick_area_type,
               pd.assignment_id,
               pd.pick_method,
               pd.pack_method,
               pd.ord_priority,
               pd.pick_seq_no 

 FROM table1 ph,
      table2 pd,
      table3 ot,
      table4 am
WHERE    pd.dc_code = ph.dc_code
      AND pd.storer = ph.storer
      AND pd.picklist_key = ph.picklist_key
      AND ph.dc_code = p_dc_code
      AND ph.storer = p_storer
        AND (  (   ph.po_no = p_order_no
               AND p_order_prefix = 'X'
               AND pd.pick_method = 'P'
               AND pd.status = 'E' 
                                   )
           OR (   ph.wave_id = p_order_no
               AND p_order_prefix = 'W'
               AND pd.pick_method = 'P'
               AND pd.status = 'E' 
                                   ) 

          )
      AND pd.item = p_item
      AND pd.consignee = p_consignee
      AND pd.dc_code = ot.dc_code
      AND pd.order_type = ot.order_type
      AND pd.sub_type = ot.sub_type
      AND am.dc_code(+) = ot.dc_code
      AND am.dc_area(+) = ot.dispatch_area
      AND pd.to_pick_qty &gt; 0
  ORDER BY pd.dc_code,
      pd.item,
      pd.consignee,
      pd.pick_seq_no,
      pd.pickdetail_key,
      pd.line_no;


Thanks           
</code></pre>

## Answers
### Answer ID: 71853374
<p>Your <code>OR</code> clause is pretty much the same apart from one literal comparison and different matching column for one of the input parameters, which pretty much means you can replace:</p>
<pre><code>   AND (  (   ph.po_no = p_order_no
           AND p_order_prefix = 'X'
           AND pd.pick_method = 'P'
           AND pd.status = 'E' 
                               )
       OR (   ph.wave_id = p_order_no
           AND p_order_prefix = 'W'
           AND pd.pick_method = 'P'
           AND pd.status = 'E' 
                               ) 

      )
</code></pre>
<p>with just something like:</p>
<pre><code>AND p_order_no = CASE WHEN p_order_prefix = 'X' THEN ph.po_no
                      WHEN p_order_prefix = 'W' THEN ph.wave_id
                      ELSE NULL
                 END
AND pd.pick_method = 'P'
AND pd.status      = 'E'
</code></pre>

### Answer ID: 71852750
<p>You can avoid repeating the 2 tests which are the same.<br />
To go further you need to know the application and understand the logic.</p>
<pre><code>        AND (  (   ph.po_no = p_order_no
               AND p_order_prefix = 'X' 
            OR                       )
                (   ph.wave_id = p_order_no
               AND p_order_prefix = 'W')  )   
         AND pd.pick_method = 'P'
         AND pd.status = 'E' 
</code></pre>
<p>can replace</p>
<pre><code>        AND (  (   ph.po_no = p_order_no
               AND p_order_prefix = 'X'
               AND pd.pick_method = 'P'
               AND pd.status = 'E' 
                                   )
           OR (   ph.wave_id = p_order_no
               AND p_order_prefix = 'W'
               AND pd.pick_method = 'P'
               AND pd.status = 'E' 
                                   ) 

          )
</code></pre>

