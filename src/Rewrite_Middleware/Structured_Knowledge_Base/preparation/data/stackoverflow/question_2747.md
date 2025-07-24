# codeigniter model function result array with WHERE clause filtering
[Link to question](https://stackoverflow.com/questions/50680853/codeigniter-model-function-result-array-with-where-clause-filtering)
**Creation Date:** 1528115949
**Score:** -2
**Tags:** php, codeigniter, activerecord, mysqli
## Question Body
<p>I already have a working function in my model </p>

<pre><code>//GETTING TOTAL PURCHASE
function total_portal_user_sale($user_id)
{
    $return = 0;
    $transection  = $this-&gt;db-&gt;get('transection')-&gt;result_array();
    foreach ($transection as $row) {
        if ($row['buyer'] == $user_id) {
            $return += $row['credit'];
        }
    }
    return $return;
}
</code></pre>

<p>i am getting data from my database correctly but i need to filter result by where clause for example this query </p>

<pre><code>$this-&gt;db-&gt;query("SELECT sum(credit) as total FROM transection 
where buyer = $user_id and status like '%paid%'");
</code></pre>

<p>this is the same scenario but with data filtering, I don't know how to use my query with active record statement </p>

<p>if someone rewrite my </p>

<p>function total_portal_user_sale($user_id)
with my WHERE clause query i will appreciate it ...</p>

<p>this is how i am rendering data into tables in view file </p>

<pre><code>&lt;div class="panel-body" id="demo_s"&gt;
&lt;table id="demo-table" class="table table-striped" data-pagination="true" data-show-refresh="false" data-ignorecol="0,6" data-show-toggle="false" data-show-columns="false" data-search="true" data-striped="true" data-filter-control="true" data-show-export="true" &gt;
    &lt;thead&gt;
        &lt;tr&gt;
            &lt;th style="width:4ex"&gt;&lt;input type="checkbox" id="users_idtog"/&gt;&lt;/th&gt;
            &lt;th&gt;&lt;?php echo translate('no');?&gt;&lt;/th&gt;
            &lt;th&gt;&lt;?php echo translate('image');?&gt;&lt;/th&gt;
            &lt;th&gt;&lt;?php echo translate('name');?&gt;&lt;/th&gt;
            &lt;th&gt;&lt;?php echo translate('email');?&gt;&lt;/th&gt;
            &lt;th&gt;&lt;?php echo translate('phone');?&gt;&lt;/th&gt;
            &lt;th&gt;Total&lt;br&gt;Sale&lt;/th&gt;
            &lt;th&gt;This&lt;br&gt;Month&lt;br&gt;Sale&lt;/th&gt;
            &lt;th&gt;Total Debit&lt;/th&gt;
            &lt;th&gt;Total&lt;br&gt;Profit&lt;/th&gt;
            &lt;th&gt;&lt;?php echo translate('creation');?&gt;&lt;/th&gt;
            &lt;th&gt;Monthly&lt;br&gt;Sale&lt;br&gt;Target&lt;/th&gt;
            &lt;th&gt;Coupon&lt;br&gt;Code&lt;/th&gt;
            &lt;th&gt;Coupon&lt;br&gt;Expiry&lt;br&gt;Date&lt;/th&gt;
            &lt;th class="text-right"&gt;&lt;?php echo translate('options');?&gt;&lt;/th&gt;
        &lt;/tr&gt;
    &lt;/thead&gt;                
    &lt;tbody &gt;
    &lt;?php
        $i = 0;
        foreach($all_users as $row){
            $i++;
    ?&gt;                
    &lt;tr&gt;
                &lt;td&gt;&lt;input type="checkbox" class="users_id" name="users_id[]" value="&lt;?php echo $row['user_id']; ?&gt;" /&gt;&lt;/td&gt;

        &lt;td&gt;&lt;?php echo $i; ?&gt;&lt;/td&gt;
        &lt;td&gt;
            &lt;img class="img-sm img-circle img-border"
                &lt;?php if(file_exists('uploads/user_image/user_'.$row['user_id'].'.jpg')){ ?&gt;
                    src="&lt;?php echo base_url(); ?&gt;uploads/user_image/user_&lt;?php echo $row['user_id']; ?&gt;.jpg"
                &lt;?php } else if($row['fb_id'] !== ''){ ?&gt;
                    src="https://graph.facebook.com/&lt;?php echo $row['fb_id']; ?&gt;/picture?type=large" data-im='fb'
                &lt;?php } else if($row['g_id'] !== ''){ ?&gt;
                    src="&lt;?php echo $row['g_photo']; ?&gt;"
                &lt;?php } else { ?&gt;
                    src="&lt;?php echo base_url(); ?&gt;uploads/user_image/default.png"
                &lt;?php } ?&gt;  /&gt;
        &lt;/td&gt;
        &lt;td&gt;&lt;?php echo $row['username']; ?&gt;&lt;/td&gt;
                                &lt;td&gt;&lt;a href="mailto:&lt;?php echo $row['email']; ?&gt;" target="_self" &gt;&lt;?php echo $row['email']; ?&gt;&lt;/td&gt;
        &lt;td&gt;&lt;?php echo $row['phone']; ?&gt;&lt;/td&gt;

       &lt;td class="text-right"&gt;&lt;?php echo $this-&gt;crud_model-&gt;total_purchase($row['user_id']); ?&gt;&lt;/td&gt;
        &lt;td class="text-right"&gt;
        &lt;?php 
                $Days = explode("-",date("d-m-Y"));
                echo round($this-&gt;crud_model-&gt;sale_target($Days[0],$row['user_id']),2);
        ?&gt;          
        &lt;/td&gt;
        &lt;td class="text-right"&gt;&lt;?php echo $this-&gt;crud_model-&gt;total_profit($row['user_id']); ?&gt;&lt;/td&gt;
        &lt;?php 
        $ts = $this-&gt;crud_model-&gt;total_portal_user_sale($row['user_id']);
        $tc = $this-&gt;crud_model-&gt;total_portal_user_profit($row['user_id']);
        $tp = $ts - $tc
        ?&gt;
        &lt;td class="text-right"&gt;
            &lt;?php echo $ts; ?&gt;
        &lt;/td&gt;

        &lt;td class="text-right"&gt;&lt;?php echo date('d M,Y',$row['creation_date']);?&gt;&lt;/td&gt;
        &lt;td&gt;&lt;?php echo $row['monthly_sale_target']; ?&gt;&lt;/td&gt;
        &lt;td&gt;&lt;?php echo $row['coupon_code']; ?&gt;&lt;/td&gt;
        &lt;td&gt;&lt;?php echo $row['expiry_date']; ?&gt;&lt;/td&gt;
        &lt;td class="text-right"&gt;

            &lt;a class="btn btn-purple btn-xs btn-labeled fa fa-tag" data-toggle="tooltip"
                onclick="ajax_modal('add_discount','&lt;?php echo translate('give_target_discount'); ?&gt;','&lt;?php echo translate('adding_discount!'); ?&gt;','add_discount','&lt;?php echo $row['user_id']; ?&gt;')" data-original-title="Edit" data-container="body"&gt;
                    &lt;?php echo translate('give_discount');?&gt;
            &lt;/a&gt;

            &lt;a class="btn btn-success btn-xs btn-labeled fa fa-wrench" data-toggle="tooltip" 

                    onclick="ajax_modal('edit','&lt;?php echo translate('edit_user'); ?&gt;','&lt;?php echo translate('successfully_edited!'); ?&gt;','user_edit','&lt;?php echo $row['user_id']; ?&gt;')" 

                        data-original-title="Edit" data-container="body"&gt;

                            &lt;?php echo translate('edit');?&gt;

                &lt;/a&gt;

            &lt;a onclick="delete_confirm('&lt;?php echo $row['user_id']; ?&gt;','&lt;?php echo translate('really_want_to_delete_this?'); ?&gt;')" class="btn btn-xs btn-danger btn-labeled fa fa-trash" data-toggle="tooltip" 
                data-original-title="Delete" data-container="body"&gt;
                    &lt;?php echo translate('delete');?&gt;
            &lt;/a&gt;
        &lt;/td&gt;
    &lt;/tr&gt;
    &lt;?php
        }
    ?&gt;
    &lt;/tbody&gt;
&lt;/table&gt;
&lt;/div&gt;
</code></pre>

## Answers
### Answer ID: 50680960
<p><strong>Hope this will help you :</strong></p>

<pre><code>function total_portal_user_sale($user_id) 
{
   $return = 0;
   $this-&gt;db-&gt;select('*');
   //$this-&gt;db-&gt;select('sum(credit) as total,buyer');
   $this-&gt;db-&gt;from('transection');
   $this-&gt;db-&gt;where('buyer',$user_id);
   $this-&gt;db-&gt;like('status','paid');

   $query = $this-&gt;db-&gt;get();
   if ($query-&gt;num_rows() &gt; 0 ) 
   {
      foreach ($query-&gt;result_array() as $row) 
      {
        if ($row['buyer'] == $user_id) 
        {
          $return += $row['credit'];
        }
      }
     return $return;
   }
}
</code></pre>

<p>You can also use <code>$this-&gt;db-&gt;select_max('credit')</code> for the same</p>

<p>For more : <a href="https://www.codeigniter.com/user_guide/database/query_builder.html" rel="nofollow noreferrer">https://www.codeigniter.com/user_guide/database/query_builder.html</a></p>

