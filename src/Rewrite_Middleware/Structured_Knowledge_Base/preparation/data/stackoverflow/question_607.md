# Magento Observer, function Error
[Link to question](https://stackoverflow.com/questions/33346868/magento-observer-function-error)
**Creation Date:** 1445865775
**Score:** 1
**Tags:** php, mysql, sql, magento, zend-framework
## Question Body
<p>I have built this function, which will insert records into the database which i will use later. However half of the function works perfectly the other half causes errors (The errors do not show up in the logs)</p>

<pre><code>&lt;?php
class Envato_CustomConfig_Model_Observer
{   
    public function adminSystemConfigChangedSection()
    {           

    /**
    *Insert new job Request
    *
    **/
        $tablename_c = Mage::getStoreConfig('customconfig_options/section_one/custom_field_one');
        $email = Mage::getStoreConfig('customconfig_options/section_two/custom_field_two');
        $days = Mage::getStoreConfig('customconfig_options/section_two/custom_field_three');

        $bind = array(
            'id'    =&gt; ' ',
            'tablename_c'   =&gt; $tablename_c,
            'email' =&gt; $email,
            'days'    =&gt; $days,
            'timeStamp' =&gt; now(),
        );

        //Open Database Conenction
        $write = Mage::getSingleton("core/resource")-&gt;getConnection("core_write");

        $query = "
        insert into Envato_CustomConfig_Job (Job_Id, tablename_colummname, email_template, days, timeStamp) 
        values (:id, :tablename_c, :email, :days, :timeStamp);
        ";

        $write-&gt;query($query, $bind);

    /**
    *Get Job Queue Ready
    *
    **/

        $res = "
        SELECT Job_Id, tablename_colummname, email_template, days  FROM Envato_CustomConfig_Job 
        WHERE tablename_colummname = :tablename_c 
        AND email_template = :email 
        AND days = :days 
        AND timeStamp =:timeStamp
        AND Job_Id != :id
        LIMIT 1;
        ";

        $result = $write-&gt;query($res, $bind);

        foreach($result as $record) {

            $Job_Id = $record['Job_Id'];
            $tablename_colummname = $record['tablename_colummname'];
            $days = $record['days'];
            $email_template = $record['email_template'];

            $email_Details[] = explode(".",$tablename_colummname);          

            if(!isset($email_Details['0']['2']))
            {
                $email_Details['0']['2'] = time();
            }
        }

        $bind = array(
            'Job_Id'    =&gt; $Job_Id,
            'tableName'   =&gt; $email_Details['0']['0'],
            'email' =&gt; $email_Details['0']['1'],
            'email_template' =&gt; $email_template,
            'days' =&gt; $days,
            'timeStamp' =&gt; $email_Details['0']['2'],
        );

        $query = "
        insert into Envato_CustomConfig_Job_Running (Job_Id, tableName, email, email_template, days, timeStamp) 
        values (:Job_Id, :tableName, :email, :email_template, :days, :timeStamp);
        ";

        $write-&gt;query($query, $bind);
</code></pre>

<p>THE CODE BELOW when included within the function the script stops working, this part is not working in Magento. Before you recommend breaking it upinto smaller functions i have tried however when i run or even put another function in the class the site does not work.</p>

<pre><code>switch ($bind['timeStamp']) {
        case is_numeric($bind['timeStamp']):
            //¨calculate email send date

            $email_Send_Date =  strtotime('+'.$bind['days'].' day', $bind['timeStamp']);
            $email_Send_Date = date('M d, Y', $email_Send_Date);

            $bind['timeStamp'] = date('M d, Y', $bind['timeStamp']);

            //Select Emails
            $selectBind = array(
            'email' =&gt; $email_Details['0']['1'],
            'tableName'   =&gt; $email_Details['0']['0'],
            );

            $res = "
            SELECT :email  FROM :tableName;
            ";

            $result = $write-&gt;query($res, $selectBind);

            foreach($result['email'] as $record) {      

            $binding = array(
                'Job_Id'    =&gt; $bind['Job_Id'],
                'email' =&gt; $record,
                'tableName'   =&gt; $bind['tableName'],
                'email_template' =&gt; $bind['email_template'],
                'timeStamp' =&gt; $bind['timeStamp'],
                'email_Send_Date' =&gt; $email_Send_Date,
            );


            $res = "

            insert into Envato_CustomConfig_Job_Queue
            values (:Job_Id, :email , :tableName, :email_template, :timeStamp, :email_Send_Date);

            ";

            $result = $write-&gt;query($res, $binding);
            }


            break;
        default:
            //timestamp is given.
            //Select Emails
            $selectBind = array(
            'email' =&gt; $email_Details['0']['1'],
            'timeStamp' =&gt; $email_Details['0']['2'],
            'tableName'   =&gt; $email_Details['0']['0'],
            );

            $res = "
            SELECT :email, :timeStamp  FROM :tableName;
            ";

            $result = $write-&gt;query($res, $selectBind);         

            $i = 0; 
            foreach ($result['timeStamp'] as $value) {  

                switch($value)
                {                                   
                case is_numeric($value):
                    // time()
                    $value = strtotime('+'.$bind['days'].' day', $value);
                    $value = date('M d, Y', $value);
                    break;
                default: 
                    // days + Unix
                    $value =  strtotime(str_replace(',', '', $value));
                    $value = strtotime('+'.$bind['days'].' day',$value);
                    $value = date('M d, Y', $value);
                    break;
                }

                $binding = array(
                'Job_Id'    =&gt; $bind['Job_Id'],
                'email' =&gt;  $result['email'][$i],
                'tableName'   =&gt; $bind['tableName'],
                'email_template' =&gt; $bind['email_template'],
                'timeStamp' =&gt; $bind['timeStamp'],
                'email_Send_Date' =&gt; $value,
                );

                $res = "

                insert into Envato_CustomConfig_Job_Queue
                values (:Job_Id, :email , :tableName, :email_template, :timeStamp, :email_Send_Date);

                ";

                $result = $write-&gt;query($res, $binding);

                $i = $i+1;
            }

        break;
        }

    }

}
?&gt;
</code></pre>

<p>EDIT::</p>

<p>I have broken it down alot and been debugging the code. i got this error i have tried to rewrite the script but still the end result hte same. any ideas on the following error??</p>

<p><strong><em>An error occurred while saving this configuration: SQLSTATE[42000]: Syntax error or access violation: 1064 You have an error in your SQL syntax; check the manual that corresponds to your MySQL server version for the right syntax to use near ''nfr_familypack'' at line 1, query was: SELECT :email FROM :tableName;</em></strong></p>

## Answers
### Answer ID: 33353411
<p>You can't use named parameters for database objects like you are trying to do here:</p>

<pre><code>SELECT :email  FROM :tableName
</code></pre>

<p>When you think about what a prepared statement is and does (allowing the MySQL engine to pre-plan a query without knowing specific parameters to be passed to it), it should be obvious that you cannot parametrize critical data that MySQL needs to prepare the query. For example, how would MySQL know what table it is creating a query execution plan against?</p>

### Answer ID: 33352784
<p>I just tried to print a complete query and it look like this </p>

<pre><code>SELECT email FROM 'nfr_familypack';
</code></pre>

<p>Notice the single quotes around the tableName. PDOStatement wrapped the bind params by single quotes. So It will cause Mysql syntax error</p>

