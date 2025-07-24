# Oracle data conversion - Bulk/ForALL won&#39;t work
[Link to question](https://stackoverflow.com/questions/22699857/oracle-data-conversion-bulk-forall-wont-work)
**Creation Date:** 1395956692
**Score:** 1
**Tags:** oracle-database, query-optimization, etl, bulk-collect
## Question Body
<p>I'm trying to find a better way to pull data from on table into another as part of a larger processing project.  I thought I could do it through BULK COLLECT and FORALL, and pick up significant speed, but I don't think I can handle individual column references using BULK COLLECT... </p>

<p>I have a data / application migration project (MSSQL to Oracle 11.2) on inheritance.  I'm trying to optimize and check end to end...  The first step of the process is to import legacy data (database table, 4.5M records, 170 columns, all in string format) into another table.</p>

<p>The initial conversion was cursor-based, looping row-by-row, with each column going through at least one function for clearning/conversion.  It worked, but on the test system it took too long -- over 12 hours to translate 4.5 million records from one table to another table with very simple functions. 
On a local implementation I have access to, they wound up limiting to 13000 unit id numbers IDs over 220k records.  </p>

<p>I set up an even more limited dev system on my laptop for testing alternative techniques -- and can get over 5 times the import speed, but that's still cursor/row-by-row.  I've set the table to NOLOGGING and use the APPEND hint.  I've tested with/without indexes.  I can't do SELECT INTO with that size table -- it just chokes. </p>

<p>Is there another / better technique?  How else can I pick up conversion speed?  Am I doing it wrong w/ the BULK COLLECT (i.e. IS there a way to reference the individual fields?)</p>

<p>If anybody has any insight, please chip in!   I am including a very stripped down version of the procedure, so I can show my usage attempt.  This same thing (pretty much) runs as a regular cursor loop, just not with the FORALL and (i) subscripts.  The error I get was ORA-00913: Too Many Values.  I have been over the full insert statement, matching fields to values.  I've checked the data transformation functions - they work for regular columns as parameters.  I am wondering if they don't work w/ BULK COLLECT and/or FORALL because of the subscripts??</p>

<p><strong>UPDATED INFORMATION:</strong>
This is on a restricted-access system, and up until now (waiting for accounts), I've been having to remote diagnose the "real" (customer) DEV system, by running against a local system -- profiling code, data, timing, etc.  My recommendations were put in by another developer, who would feed me back results.  Seriously.  However...
 @Mark, @Justin - Normally, I would get rid of any cursors not ?absolutely? needed, and use SELECT INTO where possible.  That's usually my 1st recommendation on older PL/SQL code... ("Why. So. Cursor?" wearing Joker make-up).  That's the first thing I tried on the local system, but it just slowed the server down to a crawl and I quit testing.  That was before the reduced NOLOGGING was implemented - That's what I'll attempt when I can touch the dev system.<br>
After looking at the timing, queries, joins, indexes, and crying, I recommended NOLOGGING and converting to INSERT /*+ APPEND */ -- which bought time in other processes, mainly tables built off joins.</p>

<p>re: the " OID &lt;= '000052000' " - when they set up there first converted code on the cust dev system, they had to limit the amount of records that they converted from the PMS_OHF table.  Originally, they could get 13000 personnel identifiers to process in a reasonable amount of time.  Those 13000 IDs would be in about 220K records, so, that's what they were moving in when I came on board.  Some rewrites, join corrections, and the NOLOGGING/Insert Append made a big enough difference that they went on.  On the local system, I thought 13000 was too small -- I don't think that I get a meaningful comparison against the legacy result -- so I upped it, and upped it.  I should be brave and try a full conversion on the laptop dev system -- here I can at least watch what's going on through EM... the gov't won't allow their DBAs to use it. (!?)</p>

<p><strong>BIGGER INFORMATION:</strong> -- after pondering the 00913 error again, and thinking back to other projects, I realized the earlier errors were when more than one element was passed to a function that expected a single element... which points me back tp my trying to use subscripted field names in a BULK COLLECT loop.  I re-watched a couple of Steven Feuerstein YT presentations, and I think it finally sank in.  The simple web examples... I was making my types horizontally, not vertically (or vice-versa)... in order to get my function calls to work, I think I have to make a TYPE for each Field, and an ARRAY/TABLE of that TYPE.  Suddenly (170 times) I'm thinking that I will look at some Tom Kyte lessons on manually parallelism, and ask wx I'll have access to the new (11.2?) DBMS_PARALLEL_EXECUTE interface -- which I doubt.  Also, not knowing more about the cust dev system, other than descriptions best termed "inadequate", I don't know wx //ism would be a huge help.  I need to read up on //ism</p>

<p>All I know is, I have to get some full runs completed or I won't feel comfortable saying that our results are "close enough" to the legacy results.  We might not have much choice over a multi-day full run for our testing.</p>

<pre><code>      PROCEDURE CONVERT_FA IS    

    CURSOR L_OHF IS   -- Cursor used to get SOURCE TABLE data
        SELECT * 
        FROM TEST.PMS_OHF -- OHF is legacy data source
        where  OID &lt;= '000052000'   -- limits OHF data to a smaller subset
        ORDER BY ID ;

    L_OHF_DATA TEST.PMS_OHF%ROWTYPE;
    L_SHDATA TEST.OPTM_SHIST%ROWTYPE;

    Type hist_Array is table of TEST.PMS_OHF%ROWTYPE;
    SHF_INPUT hist_array ; 



    Type Ohist_Array is table of TEST.OPTM_SHIST%ROWTYPE;
    TARG_SHIST ohist_Array ;

    n_limit number := 1000 ;    

  BEGIN

    begin

      OPEN L_OHF;

      LOOP 
        FETCH L_OHF BULK COLLECT INTO SHF_INPUT LIMIT n_limit ;
        FORALL i in 1 .. n_limit
          INSERT INTO TEST.OPTM_SHIST
      (  -- There are 170 columns in target table, requiring diff't xformations
              RECORD_NUMBER , UNIQUE_ID , STRENGTH_YEAR_MONTH , FY , FM , ETHNIC , 
              SOURCE_CODE_CURR , SOURCE_CODE_CURR_STAT , 
                -- ... a LOT more fields
              DESG_DT_01 ,  
                -- and some place holders for later
              SOURCE_CALC , PSID ,  GAIN_CURR_DT_CALC 
      )
      values
      ( -- examples of xformatiosn
            SHF_INPUT.ID(i) ,
            '00000000000000000000000' || SHF_INPUT.IOD(i) ,
            TEST.PMS_UTIL.STR_TO_YM_DATE( SHF_INPUT.STRYRMO(i) ) ,
            TEST.PMS_UTIL.STR_TO_YEAR( SHF_INPUT.STRYRMO(i) ) ,
            TEST.PMS_UTIL.STR_TO_MONTH( SHF_INPUT.STRYRMO(i) ) ,
            TEST.PMS_UTIL.REMOVE_NONASCII( SHF_INPUT.ETHNIC(i) ) ,
            -- ... there are a lot of columns
            TEST.PMS_UTIL.REMOVE_NONASCII( SUBSTR( SHF_INPUT.SCCURPRICL(i),1,2 ) ) ,
            TEST.PMS_UTIL.REMOVE_NONASCII( SUBSTR( SHF_INPUT.SCCURPRICL(i),3,1 ) ) ,   

            -- an example of other transformations
            ( case 
                when ( 
                      ( 
                       SHF_INPUT.STRYRMO(i) &gt;= '09801' 
                       AND 
                       SHF_INPUT.STRYRMO(i) &lt; '10900' 
                      )  
                    OR 
                     ( 
                      SHF_INPUT.STRYRMO(i) = '10901' 
                      AND 
                      SHF_INPUT.DESCHGCT01(i) = '081' 
                      ) 
                    ) 

                then   TEST.PMS_UTIL.STR_TO_DATE( SHF_INPUT.DESCHGCT01(i) || SHF_INPUT.DESCHGST01(i) )  

                else  TEST.PMS_UTIL.STR_TO_DATE( SHF_INPUT.DESCHGDT01(i) ) 
             end ),

            -- below are fields that will be filled later
            null ,  -- SOURCE_CALC ,
            SHF_INPUT.OID(i) ,
            null   -- GAIN_CURR_DT_CALC 
           )  ;

        EXIT WHEN L_OHF%NOTFOUND; -- exit when last row is fetched

      END LOOP;

      COMMIT;

      close L_OHF;

    END;
  end CONVERT_OHF_FA;
</code></pre>

## Answers
### Answer ID: 22876048
<p>After dropping this for other issues, I picked this up again today.</p>

<p>Someone sent me a snippet of their similar code and I decided I was going to sit down and just brute-force through the issue:  Go to the minimum # of columns and match values, and increase columns/values and recompile...</p>

<p>And then it hit me... my index was in the wrong place.  </p>

<p>INCORRECT form:</p>

<pre><code>    SHF_INPUT.ID(i) ,
    '00000000000000000000000' || SHF_INPUT.IOD(i) ,
    TEST.PMS_UTIL.STR_TO_YM_DATE( SHF_INPUT.STRYRMO(i) ) ,
</code></pre>

<p><strong>CORRECT form:</strong></p>

<pre><code>    SHF_INPUT(i).ID ,
    '00000000000000000000000' || SHF_Input(i).IOD ,
    TEST.PMS_UTIL.STR_TO_YM_DATE( SHF_Input(i).STRYRMO ) ,
</code></pre>

<p>I blame it on looking at early multi-column bulk collect examples and assuming I could convert them to %ROWTYPE examples off the top of my head.  I got impatient and didn't check.</p>

<p>Thank you for your help and recommendations.</p>

### Answer ID: 22704535
<pre><code>execute immediate 'alter session enable parallel dml';
INSERT /*+ APPEND PARALLEL */ INTO TEST.OPTM_SHIST(...)
SELECT ...
FROM TEST.PMS_OHF
WHER OID &lt;= '000052000';
</code></pre>

<p>This is The Way to do large data loads.  Don't be fooled by all the fancy PL/SQL options like bulk collect, pipelined tables, etc.  They are rarely any faster or easier to use than plain old SQL.  The main benefit of those featues is to improve performance of a row-by-agonizing-row process without significant refactoring.</p>

<p>In this case it looks like there's already virtually no logic in PL/SQL.  Almost all the PL/SQL can be thrown out and replaced with a single query.  This makes it much easier to modify, debug, add parallelism, etc.</p>

<p>Some other tips:</p>

<ol>
<li>The <code>ORDER BY</code> is probably not helpful for data loads.  Unless you're trying to do something fancy with indexes, like improve the clustering factor or rebuild without sorting.</li>
<li>Ensure your functions are declared as DETERMINISTIC if the output is always identical for the same input.  This may help Oracle avoid calling the function for the same result.  For even better performance, you can inline all of the functions in the SQL statement, but that can get messy.</li>
<li>If you still need to use <code>BULK COLLECT</code>, use the hint <code>APPEND_VALUES</code>, not <code>APPEND</code>.</li>
</ol>

