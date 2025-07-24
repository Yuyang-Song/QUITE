# PL/SQL BLOCK in loop
[Link to question](https://stackoverflow.com/questions/33336916/pl-sql-block-in-loop)
**Creation Date:** 1445821097
**Score:** 0
**Tags:** sql, oracle-database
## Question Body
<pre><code>    DECLARE
    VEN2_ID_VAR NUMBER := 124;
    VEN2_ID NUMBER;
    VEN2_NAME VARCHAR2(50);
    INV2_ID NUMBER;
    INV_TOTAL NUMBER(9,2);
    INV_TOTAL_PAY NUMBER(9,2);
    INV_BALANCE NUMBER (9,2);
    INV_DATE DATE;
    INV_DUE_DATE DATE;

     BEGIN
     SELECT VENDORS2.VENDOR_ID, VENDOR_NAME, INVOICE_ID, INVOICE_TOTAL,     PAYMENT_TOTAL , BALANCE, INVOICE_DATE, INVOICE_DUE_DATE
     INTO VEN2_ID, VEN2_NAME, INV2_ID, INV_TOTAL , INV_TOTAL_PAY, INV_BALANCE,   INV_DATE, INV_DUE_DATE
     FROM INVOICES2 INNER JOIN VENDORS2 ON VENDORS2.VENDOR_ID = INVOICES2.VENDOR_ID
     WHERE VENDORS2.VENDOR_ID = VEN2_ID_VAR ;

     DBMS_OUTPUT.PUT ( 'VENDOR ID: ' || VEN2_ID || ', ' );
     DBMS_OUTPUT.PUT ( 'VENDOR NAME: ' || VEN2_NAME || ', ' );
     DBMS_OUTPUT.PUT ( 'INVOICE ID: ' || INV2_ID || ', ' );
     DBMS_OUTPUT.PUT ( 'INVOICE TOTAL: ' || INV_TOTAL || ', ' );
     DBMS_OUTPUT.PUT ( 'INVOICE TOTAL PAYMENT: ' || INV_TOTAL_PAY || ', ' );
     DBMS_OUTPUT.PUT ( 'BALANCE DUE: ' || INV_BALANCE || ', ' );
     DBMS_OUTPUT.PUT( 'INVOICE DATE: ' || TO_CHAR(INV_DATE, 'MON DD,RRRR')  || ', ' );
     DBMS_OUTPUT.PUT_line( 'INVOICE DUE DATE: ' || TO_CHAR(INV_DUE_DATE, 'MON DD,RRRR'));
     END; 
     /
</code></pre>

<p>This is the code i am trying to run in Oracle Pl/SQL but the VEN2_ID_VAR NUMBER := 124 Has multiple rows in the database so it says cannot fetch more then one row rewrite the query to fetch more then one rows. What can I do?</p>

## Answers
### Answer ID: 33336989
<p>You can use a cursor if that's the case:</p>

<pre><code>  DECLARE
      VEN2_ID_VAR NUMBER := 124;
      VEN2_ID NUMBER;
      VEN2_NAME VARCHAR2(50);
      INV2_ID NUMBER;
      INV_TOTAL NUMBER(9,2);
      INV_TOTAL_PAY NUMBER(9,2);
      INV_BALANCE NUMBER (9,2);
      INV_DATE DATE;
      INV_DUE_DATE DATE;
      cursor c1 is SELECT VENDORS2.VENDOR_ID VEN2_ID, VENDOR_NAME VEN2_NAME, INVOICE_ID INV2_ID, INVOICE_TOTAL INV_TOTAL,PAYMENT_TOTAL INV_TOTAL_PAY, BALANCE INV_BALANCE, INVOICE_DATE INV_DATE, INVOICE_DUE_DATE INV_DUE_DATE
       FROM INVOICES2 INNER JOIN VENDORS2 ON VENDORS2.VENDOR_ID = INVOICES2.VENDOR_ID
       WHERE VENDORS2.VENDOR_ID = VEN2_ID_VAR;

       BEGIN
       for a in c1 loop

       DBMS_OUTPUT.PUT ( 'VENDOR ID: ' || a.VEN2_ID || ', ' );
       DBMS_OUTPUT.PUT ( 'VENDOR NAME: ' || a.VEN2_NAME || ', ' );
       DBMS_OUTPUT.PUT ( 'INVOICE ID: ' || a.INV2_ID || ', ' );
       DBMS_OUTPUT.PUT ( 'INVOICE TOTAL: ' || a.INV_TOTAL || ', ' );
       DBMS_OUTPUT.PUT ( 'INVOICE TOTAL PAYMENT: ' || a.INV_TOTAL_PAY || ', ' );
       DBMS_OUTPUT.PUT ( 'BALANCE DUE: ' || a.INV_BALANCE || ', ' );
       DBMS_OUTPUT.PUT( 'INVOICE DATE: ' || TO_CHAR(a.INV_DATE, 'MON DD,RRRR')  || ', ' );
       DBMS_OUTPUT.PUT_line( 'INVOICE DUE DATE: ' || TO_CHAR(a.INV_DUE_DATE, 'MON DD,RRRR'));
       end loop;
       END; 
       /
</code></pre>

