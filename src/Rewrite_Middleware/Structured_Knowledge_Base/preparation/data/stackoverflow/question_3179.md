# Cannot Add or Update Child Row
[Link to question](https://stackoverflow.com/questions/70231710/cannot-add-or-update-child-row)
**Creation Date:** 1638682096
**Score:** 0
**Tags:** mysql
## Question Body
<p>I have code written for a MySQL database containing 5 tables. The code I've written is as follows.</p>
<pre><code>```create database BLUE_OX_DISTRIBUTION;```

```use BLUE_OX_DISTRIBUTION;```

```create table CUSTOMERS(CUSTOMER_NUM int(5), CUSTOMER_NAME varchar(35), STREET varchar(25), CITY char(15), STATE char(2), ZIP_CODE int(5), BALANCE dec(15,15), CREDIT_LIMIT dec(15,15), REP_NUM int(2), primary key(CUSTOMER_NUM));```
</code></pre>
<pre><code>Query OK, 0 rows affected, 2 warnings (0.05 sec)```

```create table REPS(REP_NUM int(2), LAST_NAME char(15), FIRST_NAME char(15), street VARCHAR(15), CITY char(15), STATE char(2), ZIP_CODE int(5), COMM_RATE dec(15,15), primary key (REP_NUM));```

```create table ORDERS(ORDER_NUM int(5), ORDER_DATE date, CUSTOMER_NUM int(3), foreign key(CUSTOMER_NUM) references CUSTOMERS(CUSTOMER_NUM));```

```create index ORDER_LINES_TO_ORDERS_INDEX on ORDERS(ORDER_NUM);```

```create table ORDER_LINES(ORDER_NUM int(5), ITEM_NUM varchar(4), NUM_ORDERED int(3), QUOTED_PRICE varchar(10), foreign key(ORDER_NUM) references ORDERS(ORDER_NUM), foreign key(ITEM_NUM) references ITEMS(ITEM_NUM), primary key(ORDER_NUM,ITEM_NUM));```

When I try to enter data into the table, I keep getting an error back that says &quot;cannot add or update a child row&quot; and I'm not sure why. What is the problem here? How can I rewrite the code to accept data?


    insert into ORDERS VALUES ('51608','2015-10-12','126'), ('51610','2015-10-12','334'), ('51613','2015-10-13','386'), ('51614','2015-10-13','260'), ('51617','2015-10-15','586'), ('51619','2015-10-15','126'), ('51623','2015-10-15','586'); Insert into REPS VALUES  ('15','Campos','Rafael','724 Vinca Dr','Grove','CA','90092','0.06'), ('30','Gradey','Megan','632 Liatris St','Fullton','CA','90085','0.08'), ('45','Tian','Hui','1785 Tyler Ave','Northfield','CA','90098','0.06'), ('60','Sefton','Janet','267 Oakley St','Congaree','CA','90097','0.06');
</code></pre>

