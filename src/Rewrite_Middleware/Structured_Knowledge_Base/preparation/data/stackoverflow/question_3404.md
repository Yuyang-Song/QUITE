# Langchain and OpenAI NLP to SQL generating Wrong Query
[Link to question](https://stackoverflow.com/questions/78764133/langchain-and-openai-nlp-to-sql-generating-wrong-query)
**Creation Date:** 1721302126
**Score:** 0
**Tags:** python, openai-api, langchain
## Question Body
<p>I am trying to create a chatbot which can take input and generate query based on fined tuned model and provided schema. It was working fine previously but now every scenario which was working fine is generating wrong results/query I am using openai gpt3.5turbo Here's my code</p>
<pre><code>def generate_query(self,llm,db,question,relevant_tables):
        example_queries = ''
        schedule_instructions = ''
            
        schedule_tables = ['v_doctor_regular_schedule','v_doctor_special_schedule','v_doctor_unavailable'] 
        appointment_tables = ['appointment_appointmentinformation','appointment_appointmenttype']

        doctor_subscriptions = ['doctors_subscribeddoctors','v_doctor_information']
        
        
        found_tables = [table for table in schedule_tables if table in relevant_tables]
        if found_tables or 'slots' in question.lower():
            schedule_instructions = &quot;&quot;&quot;
            - **Time Ranges (e.g. between 10 AM to 2 PM)**: Use start_time::time &lt;= '14:00:00'::time and end_time::time &gt;= '10:00:00'::time for time ranges.
            - **Date Ranges (e.g. between 01-Jun-2024, to 30-Jun-2024)**: Use start_date &gt;= 'YYYY-MM-DD'::date and end_date &lt;= 'YYYY-MM-DD'::date for date ranges.
            - **Date and Time Interpretation**: Use user-specified dates and times accurately.
            - **Doctor and Specialization Queries**: Use correct columns (doctor_name, doctor_specialization) for doctor or specialization queries.
            - **Slot Availability**: Filter available slots by doctorvisitingdays for regular schedules and schedule_date for special schedules.
            - **Handling Errors**: Reference tomorrow_date correctly to avoid errors.
            - **Correct Schema**: Search schedules in both v_doctor_regular_schedule and v_doctor_special_schedule.
            - **Date Calculations**: Use tomorrow_date consistently for &quot;tomorrow&quot; in appointment queries.
            - **Check WITH Clause**: Verify that the WITH next_week_dates clause is correctly defining range_date and that it is used consistently throughout the query.
                 
            &quot;&quot;&quot;
            example_queries = f&quot;&quot;&quot;

            *Schedule Query Instructions*:
            - *Example Queries*:
            **Date Range for Schedules**:   
                WITH range_date AS ( SELECT generate_series( '2024-07-20'::date, '2024-07-25'::date, '1 day'::interval )::date AS sp_date ) SELECT sch.doctorschedule_id, sch.doctorscheduleoverride_id, sch.schedule_date, sch.doctorvisitingdays, sch.slot_start_time, sch.slot_end_time, sch.slottimebin, sch.doctor_id, doc.doctor_name, doc.doctor_specialization FROM ( SELECT vmd.doctorschedule_id, NULL AS doctorscheduleoverride_id, range_date.sp_date AS schedule_date, vmd.doctorvisitingdays, vmd.slot_start_time, vmd.slot_end_time, vmd.slottimebin, vmd.doctor_id, ( CASE WHEN aai.id IS NULL THEN true ELSE false END) slot_available FROM v_doctor_regular_schedule vmd INNER JOIN range_date ON vmd.doctorvisitingdays = trim(to_char(range_date.sp_date,'day')) LEFT JOIN appointment_appointmentinformation aai ON aai.doctorschedule_id = vmd.doctorschedule_id AND aai.appointmentstatus = 'confirmed' AND ( aai.appointmentfrom at time zone 'UTC')::time = vmd.slot_start_time AND ( aai.appointmentdate = range_date.sp_date) UNION ALL SELECT NULL AS doctorschedule_id, vss.doctorscheduleoverride_id, vss.schedule_date, trim(to_char(vss.schedule_date,'day')) AS doctorvisitingdays, vss.slot_start_time, vss.slot_end_time, vss.slottimebin, vss.doctor_id, ( CASE WHEN aai.id IS NULL THEN true ELSE false END) slot_available FROM v_doctor_special_schedule vss INNER JOIN range_date ON vss.schedule_date = range_date.sp_date LEFT JOIN appointment_appointmentinformation aai ON aai.doctorscheduleoverride_id = vss.doctorscheduleoverride_id AND aai.appointmentstatus = 'confirmed' AND ( aai.appointmentfrom at time zone 'UTC')::time = vss.slot_start_time AND aai.appointmentdate = vss.schedule_date ) sch LEFT JOIN range_date nfm ON nfm.sp_date = sch.schedule_date OR ( sch.schedule_date IS NULL AND nfm.sp_date IS NOT NULL) LEFT JOIN v_doctor_unavailable vdu ON sch.doctor_id = vdu.doctor_id AND vdu.unavailable_date = nfm.sp_date AND vdu.start_time &lt;= sch.slot_end_time AND vdu.end_time &gt;= sch.slot_start_time LEFT JOIN v_doctor_information doc ON doc.doctor_id = sch.doctor_id WHERE sch.slot_available = true AND vdu.id IS NULL AND lower(doc.doctor_specialization) LIKE '%cardio%';
            **Example with Today/Single Date for Doctor Name**:
                SELECT sch.doctorschedule_id, sch.doctorscheduleoverride_id, sch.schedule_date, sch.doctorvisitingdays, sch.slot_start_time, sch.slot_end_time, sch.slottimebin, sch.doctor_id FROM (SELECT vmd.doctorschedule_id, NULL AS doctorscheduleoverride_id, NULL AS schedule_date, vmd.doctorvisitingdays, vmd.slot_start_time, vmd.slot_end_time, vmd.slottimebin, vmd.doctor_id, ( CASE WHEN aai.id IS NULL THEN TRUE ELSE FALSE END ) slot_available FROM v_doctor_regular_schedule vmd left join appointment_appointmentinformation aai ON aai.doctorschedule_id = vmd.doctorschedule_id AND aai.appointmentstatus = 'confirmed' AND ( aai.appointmentfrom AT TIME zone 'UTC' ) :: TIME = vmd.slot_start_time AND ( aai.appointmentdate = ( Now() :: DATE ) ) WHERE vmd.doctorvisitingdays = Trim(To_char(Now() :: DATE, 'day')) UNION ALL SELECT NULL AS doctorschedule_id, vss.doctorscheduleoverride_id, vss.schedule_date, trim(to_char(vss.schedule_date,'day')) AS doctorvisitingdays, vss.slot_start_time, vss.slot_end_time, vss.slottimebin, vss.doctor_id, ( CASE WHEN aai.id IS NULL THEN TRUE ELSE FALSE END ) slot_available FROM v_doctor_special_schedule vss left join appointment_appointmentinformation aai ON aai.doctorscheduleoverride_id = vss.doctorscheduleoverride_id AND aai.appointmentstatus = 'confirmed' AND ( aai.appointmentfrom AT TIME zone 'UTC' ) :: TIME = vss.slot_start_time WHERE vss.schedule_date = Now() :: DATE) sch left join v_doctor_unavailable vdu ON sch.doctor_id = vdu.doctor_id AND vdu.unavailable_date = Now() :: DATE AND vdu.start_time &lt;= sch.slot_end_time AND vdu.end_time &gt;= sch.slot_start_time left join v_doctor_information dd ON sch.doctor_id = dd.doctor_id WHERE slot_available = TRUE AND vdu.id IS NULL AND Lower(dd.doctor_name) LIKE '%faizan%ali%';

            **Join Dates with Regular Schedule**:Do not search for doctorvisitingdays in v_doctor_special_schedule, but always join the dates if a series is generated. For example
                SQL: FROM v_doctor_regular_schedule vdrs INNER JOIN next_week_dates ON trim(to_char(next_week_dates.schedule_date,'day')) = vdrs.doctorvisitingdays
            **Join Dates with Special Schedule**:Do not search for doctorvisitingdays in v_doctor_special_schedule, but always join the dates if a series is generated. For example
                SQL: FROM v_doctor_special_schedule vss INNER JOIN next_week_dates ON (next_week_dates.schedule_date = vss.schedule_date
        
            **Joining Appointment Slots**: Always include a join for slots in appointment_appointmentinformation with both v_doctor_special_schedule &amp; v_doctor_regular_schedule with field appointmentfrom and appointmentdate.                
                Example join with Regular : FROM v_doctor_regular_schedule vmd INNER JOIN next_week_dates ON trim(to_char(next_week_dates.schedule_date,'day')) = vmd.doctorvisitingdays
                Example join with Special : FROM v_doctor_special_schedule vss INNER JOIN next_week_dates ON next_week_dates.schedule_date = vss.schedule_date
                When searching for appointment slots or schedules, always query from both v_doctor_special_schedule and v_doctor_regular_schedule using UNION ALL.
                        
            &quot;&quot;&quot;

        elif any(table in relevant_tables for table in appointment_tables):
            
            example_queries = f&quot;&quot;&quot;
            Example Input: &quot;How many no show on 26 June 2024 for Dr. Haris.&quot;
            Example Answer SQL: WITH next_week_dates AS ( SELECT generate_series( '2024-06-26'::date, '2024-06-26'::date, '1 day'::interval )::date AS sp_date ) SELECT count(sch.noshow) FROM ( SELECT aai.noshow, aai.appointmentfrom, aai.appointmentto, doc.doctor_name FROM appointment_appointmentinformation aai JOIN v_doctor_information doc ON doc.doctor_id = aai.doctor_id LEFT JOIN next_week_dates nfm ON nfm.sp_date = aai.appointmentdate WHERE aai.noshow = true AND lower(doc.doctor_name) LIKE '%haris%' ) sch;

            Example Input: &quot;Top 3 doctors with highest appointments in July 2024.&quot;
            Example Answer: &quot;WITH next_month_dates AS ( SELECT generate_series('2024-07-01'::date, '2024-07-31'::date, '1 day'::interval)::date AS schedule_date) SELECT doc.doctor_id, doc.doctor_name, doc.doctor_specialization, count(aai.id) AS appointment_count FROM appointment_appointmentinformation aai INNER JOIN next_month_dates nmd on aai.appointmentdate = nmd.schedule_date LEFT JOIN v_doctor_information doc ON doc.doctor_id = aai.doctor_id WHERE aai.appointmentstatus = 'confirmed' GROUP BY doc.doctor_id, doc.doctor_name, doc.doctor_specialization ORDER BY appointment_count DESC limit 3;&quot;
            
            &quot;&quot;&quot;
        elif any(table in relevant_tables for table in doctor_subscriptions):
            example_queries = f&quot;&quot;&quot;
                Example Input: &quot;How many subscribed doctors in agha khan hospital&quot;
                Example Answer SQL: select count(*) from v_doctor_information where lower(hospitalname) like '%agha%khan%' and membership_status != 'incomplete'
            &quot;&quot;&quot;
            
        
        prompt_instructions = f&quot;&quot;&quot;
        Follow the instructions while crafting the query.
        - **Boolean**: Use True/False.
        - **Column Names**: Enclose in double quotes and trim values.
        - **Conditional Terms**: &quot;Hospital&quot; is optional after a name.
        - **WHERE Clause**: Use LIKE instead of = for character fields, e.g., &quot;%int%hospital%&quot;.
        - **Date/Time: Parse datetime columns to date if requested.
        - **Aliases**: Give unique aliases to tables.
        - **Date Range**: Use WITH next_week_dates AS (SELECT generate_series(...)) for date matching.
        - **Period Not Mentioned**: Ask for details
        - **Single %**: Use a single % when extracting dates in generate_series(...). Avoid using double '%%'.
        - **Next Weekday Example**: Use correct CTE generate_series function with a single %.
        - **Date to Year**: Convert dates to years with trim(to_char(CURREN_DATE, 'yyyy'))
        - **Date to Month**: Convert dates to months with TRIM(TO_CHAR(CURREN_DATE,'month'))
        - **Date to Day**: Convert dates to day with TRIM(TO_CHAR(CURREN_DATE,'day'))
        - **Ambiguous Queries**: Request more details from the user.
        - **Non-existing Columns**: Exclude columns not in the schema.
        - **List Mention**: Check if a list name exists as a table/schema and return details if found.
        - **Avoid Unnecessary Clauses**: Exclude unrelated clauses, e.g., omit specialty if asking for data on Dr. Michael.
        - **Filters Globally**: Join relevant tables on doctor ID or Name or Speciality and apply filters at the end of the query to ensure they affect all parts if required.
        - **Include Necessary Details**: Ensure the query includes all requested information, such as doctor details.
        - **Year Not Mentioned**: Assume the current year.
        - **This Month**: Select dates from the 1st to the end of the current month.
        - **Limit**: Limit the Result to 5.  
        - **Syntax Accuracy**: Ensure parentheses are used correctly with UNION ALL
        - **Exact Match**: Use &quot;=&quot; for full name comparisons with LOWER().
        - **Common Mistakes**: Avoid NOT IN with NULL values, UNION when UNION ALL is needed, BETWEEN for exclusive ranges, data type mismatches, incorrect function arguments, and incorrect data type casting.
        - **Case-Insensitive Partial Matches**: Always use `LOWER()` and `LIKE` for case-insensitive partial matches. For example:
          - Incorrect: `WHERE dd.doctor_name = 'Dr. Mohammed Khan'`
          - Correct: `WHERE LOWER(dd.doctor_name) LIKE '%mohammed%khan%'`
        - **Column Usage**: Double-check that any references to range_date are properly qualified with the alias where necessary, such as next_week_dates.range_date.
        - **Query Structure**: Review the entire query to ensure that all tables, aliases, and columns are correctly referenced and that there are no typos or missing references.
        - **Specific Day**: when user mentioned specific day in request (e.g. monday, tuesday, Wednesday) Add clause with days too for matching days too;
        - **Ignore Fields**
          - Don't include &quot;hospitalId&quot; from hospital_hospitalprofile
          - Don't include profile_ref_id, payment_profile_ref_id from payments_hospitalpaymentprofile
               

            **With CTE Series Example**:
            - Next Whole Weekdays (Monday to Sunday) Series: SELECT generate_series( CURRENT_DATE + ((8 - EXTRACT(dow FROM CURRENT_DATE) % 7) * interval '1 day'), CURRENT_DATE + ((14 - EXTRACT(dow FROM CURRENT_DATE) % 7) * interval '1 day'), interval '1 day' )::date AS schedule_date;
            - Next / Coming Tuesday Example: SELECT generate_series( CURRENT_DATE + ((9 - EXTRACT(dow FROM CURRENT_DATE)) % 7) * interval '1 day', CURRENT_DATE + ((9 - EXTRACT(dow FROM CURRENT_DATE)) % 7) * interval '1 day', interval '1 day' )::date AS coming_tuesday;
            - Next Business Days Example: WITH business_days AS ( SELECT generate_series( CASE WHEN EXTRACT(dow FROM CURRENT_DATE) = 5 THEN CURRENT_DATE + interval '3 day' WHEN EXTRACT(dow FROM CURRENT_DATE) = 6 THEN CURRENT_DATE + interval '2 day' ELSE CURRENT_DATE + interval '1 day' END, CASE WHEN EXTRACT(dow FROM CURRENT_DATE) = 5 THEN CURRENT_DATE + interval '22 day' WHEN EXTRACT(dow FROM CURRENT_DATE) = 6 THEN CURRENT_DATE + interval '21 day' ELSE CURRENT_DATE + interval '19 day' END, interval '1 day' )::date AS schedule_date ) SELECT schedule_date FROM business_days WHERE EXTRACT(dow FROM schedule_date) NOT IN (0, 6);
            - Last Week Example: SELECT generate_series( CURRENT_DATE - ((EXTRACT(dow FROM CURRENT_DATE)::int + 7) % 7 + 1) * interval '1 day' - interval '6 days', CURRENT_DATE - ((EXTRACT(dow FROM CURRENT_DATE)::int + 7) % 7 + 1) * interval '1 day', interval '1 day' )::date AS sp_date;
            - Next Month Example: SELECT generate_series( date_trunc('month', CURRENT_DATE) + interval '1 month', date_trunc('month', CURRENT_DATE) + interval '2 month' - interval '1 day', interval '1 day' )::date AS next_month_dates;
            - Date Range Example: SELECT generate_series( '2024-07-01'::date, '2024-07-15'::date, interval '1 day' )::date AS date_series;
            - Today Date Example: SELECT CURRENT_DATE::date  AS today_date;
        - **Without Date**: When user mention to show data without date range, dont use WITH for generate date series.
        {schedule_instructions}    
    
        

        Provide accurate and specific conditions in the PostgreSQL version 14 queries to avoid misinterpretation or default selections.

        {example_queries}


        If there are any mistakes, rewrite the query.
        If there are no mistakes, reproduce the original query without commentary.
        DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

            &quot;&quot;&quot;
            
        if len(relevant_tables)&gt;0:
            # Combine instructions with the user question
            full_prompt = f&quot;{prompt_instructions}\n\n User Question: {question}&quot;
        else:
            full_prompt = f&quot; User Question: {question}&quot;;          

        token_count = len(full_prompt)
        print(f&quot;Token count: {token_count/4}&quot;)

        execute_query_func = QuerySQLDataBaseTool(db=db)
        generate_query_chain = create_sql_query_chain(llm, db)
        query = generate_query_chain.invoke({&quot;question&quot;: full_prompt})

        chain = generate_query_chain | execute_query_func
        result_chain = chain.invoke({&quot;question&quot;: full_prompt})

        print(query)
        return None, query, None
</code></pre>
<p>I am trying to generate perfect query based on my prompt, I have also provided all potential queries and results in jsonl file while fine tuning model</p>

