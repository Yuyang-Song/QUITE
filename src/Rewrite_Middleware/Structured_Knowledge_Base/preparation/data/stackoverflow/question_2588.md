# OVER() function in R using sqldf without RPostgreSQL?
[Link to question](https://stackoverflow.com/questions/41813103/over-function-in-r-using-sqldf-without-rpostgresql)
**Creation Date:** 1485195923
**Score:** 1
**Tags:** sql, r, sqldf, rpostgresql
## Question Body
<p>I'm dealing with some sensitive data, so I'm concerned about using RPostgreSQL. I have all the data necessary loaded into dataframes in R. I'm trying to run queries on the data using the <code>sqldf()</code> function in R. These queries were written for Oracle SQL Developer years ago, so we're trying to avoid rewriting the scripts entirely. Being able to reuse the pre-written SQL scripts will save us a massive amount of time. The script seems to trip up when we hit the <code>over()</code> SQL function. I'm aware that base sqldf doesn't support the <code>over()</code> function. I've read that the <code>over()</code> function works with the RPostgreSQL package, but does that require me to send my dataframes to an external database? From my understand of RpostgreSQL you need to connect to PostgreSQL and create a new database. We can't send this data to an external data storage system. Is there another way to use the <code>over()</code> function while keeping the dataframes local to my PC?</p>

<pre><code>select program, importance_level, count( distinct subject_id )                      

from                        
(                       
select r.subject_id,                        

case                        
    when  rc_level is not null  and  rc_level &lt;&gt; 'NA'                   
                        then  'bad_guy'
                    when  (rc_level is null  or  rc_level = 'NA') and
         (substr( r.base_category, 2, 2 )  in  ( '5R', '8Q', '8P' )     
                    or r.process_name in ('On The Way'))    
            then 'run_away'                     
          when  (rc_level is null  or  rc_level = 'NA') and r.process_name =
 'Fancy Order'                      
            then 'repeater'                     
           when  (rc_level is null  or  rc_level = 'NA') and
 (a.current_program_code  in  ( 'BOP', 'IAS', 'LIS', 'SIS' )                        
           or  method_code  in  ( 'SIP', 'POB' )                        
           or  substr( r.base_category, 2, 2 )  in  ( '9F', '7G' ))                     
                    then  'NEWBIE'
          else 'Other'                      
        end                     
                as  importance_level,       

case                        
when a.current_program_code in ('123', 'ABC', 'DEF', 'HIJ', 'KLM', 'NOP', 'QRS' ) then 'YAW'                        
when a.current_program_code in ( 'RE', 'FDS', 'QWE', 'WER', 'ERT','RTY','TYU' ) then 'PO'                       
when a.current_program_code in ( 'LEP' ) then 'MOM'                     
else a.current_program_code                     
end                     
as program                      

from FY16DATA r left join (select distinct * from (select subject_id, first_value(current_program_code) over (partition by subject_id order by start_date desc) as current_program_code, first_value(process_name) over (partition by subject_id order by start_date desc) as process_name, first_value(method_code) over (partition by subject_id order by start_date desc) as method_code, max(load_fy) over (partition by subject_id) as load_fy from FY16NAME)) a on r.subject_id = a.subject_id                        
where r.load_fy = '2016' and r.thing_status &lt;&gt; 'Over'  and r.thing_status in ('Head','Hair','Face')                     

)                       
group by program, importance_level;
</code></pre>

## Answers
### Answer ID: 41813389
<p>You're correct that the <code>RPostgreSQL</code> package is used to connect to an external database, somewhat different from <code>sqldf</code> which is used to run SQL on R data frames. <code>sqldf</code> relies on other packages to handle database connections. </p>

<p>You're wrong that <em>"<code>sqldf</code> doesn't support the <code>over</code> function"</em>. The <code>sqldf</code>default driver, <code>sqlite</code>, is a SQL variant that doesn't have <code>over()</code>. However, you can use <code>sqldf</code> with a local postgreSQL installation (<code>sqldf</code> can use <code>RPostgreSQL</code> behind the scenes). See the sqldf FAQ <a href="https://github.com/ggrothendieck/sqldf#12-how-does-one-use-sqldf-with-postgresql" rel="nofollow noreferrer">How does one use sqldf with PostgreSQL?</a>, which I'll post most of below. You'll notice that the SQL query uses <code>over()</code>.</p>

<blockquote>
  <p>Install 1. <code>PostgreSQL</code>, 2. <code>RPostgreSQL</code> R package 3. <code>sqldf</code> itself. <code>RPostgreSQL</code> and <code>sqldf</code> are ordinary R package installs.</p>
  
  <p>Make sure that you have created an empty database, e.g. <code>"test"</code>. The <code>createdb</code> program that comes with PostgreSQL can be used for that. e.g. from the console/shell create a database called test like this:</p>

<pre><code>createdb --help
createdb --username=postgres test
</code></pre>
  
  <p>Here is an example using <code>RPostgreSQL</code> and after that we show an example using <code>RpgSQL</code>. The options statement shown below can be entered directy or alternately can be put in your <code>.Rprofile</code>. The values shown here are actually the defaults:</p>

<pre><code>options(sqldf.RPostgreSQL.user = "postgres", 
  sqldf.RPostgreSQL.password = "postgres",
  sqldf.RPostgreSQL.dbname = "test",
  sqldf.RPostgreSQL.host = "localhost", 
  sqldf.RPostgreSQL.port = 5432)

Lines &lt;- "Group_A Group_B Group_C Value 
A1 B1 C1 10 
A1 B1 C2 20 
A1 B1 C3 30 
A1 B2 C1 40 
A1 B2 C2 10 
A1 B2 C3 5 
A1 B2 C4 30 
A2 B1 C1 40 
A2 B1 C2 5 
A2 B1 C3 2 
A2 B2 C1 26 
A2 B2 C2 1 
A2 B3 C1 23 
A2 B3 C2 15 
A2 B3 C3 12 
A3 B3 C4 23 
A3 B3 C5 23"

DF &lt;- read.table(textConnection(Lines), header = TRUE, as.is = TRUE)

library(RPostgreSQL)
library(sqldf)
# upper case is folded to lower case by default so surround DF with double quotes
sqldf('select count(*) from "DF" ')

sqldf('select *, rank() over  (partition by "Group_A", "Group_B" order by "Value") 
       from "DF" 
       order by "Group_A", "Group_B", "Group_C" ')
</code></pre>
</blockquote>

