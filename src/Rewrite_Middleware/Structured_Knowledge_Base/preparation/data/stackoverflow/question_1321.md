# Does Go Gorm provide any method to auto map existing tables in Mysql database
[Link to question](https://stackoverflow.com/questions/70135735/does-go-gorm-provide-any-method-to-auto-map-existing-tables-in-mysql-database)
**Creation Date:** 1638023843
**Score:** 0
**Tags:** go, go-gorm
## Question Body
<p>I am a newcomer to Go. I have an old tool to check and compare data in the Mysql database to my device, and I want to rewrite the tool in Go.</p>
<p>Since the tables and data have been already in the Mysql, I try to use GORM to auto map the existing tables. But I am not sure how to do that? I did not find any description of automapping an existing table in the <a href="https://gorm.io/docs/index.html" rel="nofollow noreferrer">GORM documentation</a>.</p>
<p>I redeclare the existing table model and try to query data. The procedure is as below:</p>
<p>For example one of my tables is like this:</p>
<pre class="lang-sql prettyprint-override"><code>MariaDB [neutron]&gt; desc lbaas_loadbalancers;
+---------------------+--------------+------+-----+---------+-------+
| Field               | Type         | Null | Key | Default | Extra |
+---------------------+--------------+------+-----+---------+-------+
| project_id          | varchar(255) | YES  | MUL | NULL    |       |
| id                  | varchar(36)  | NO   | PRI | NULL    |       |
| name                | varchar(255) | YES  |     | NULL    |       |
| description         | varchar(255) | YES  |     | NULL    |       |
| vip_port_id         | varchar(36)  | YES  | MUL | NULL    |       |
| vip_subnet_id       | varchar(36)  | NO   |     | NULL    |       |
| vip_address         | varchar(36)  | YES  |     | NULL    |       |
| admin_state_up      | tinyint(1)   | NO   |     | NULL    |       |
| provisioning_status | varchar(16)  | NO   |     | NULL    |       |
| operating_status    | varchar(16)  | NO   |     | NULL    |       |
| flavor_id           | varchar(36)  | YES  | MUL | NULL    |       |
+---------------------+--------------+------+-----+---------+-------+
11 rows in set (0.002 sec)

MariaDB [neutron]&gt; select * from lbaas_loadbalancers \G;
*************************** 1. row ***************************
         project_id: 346052548d924ee095b3c2a4f05244ac
                 id: f6638d02-29f8-41aa-9433-179bf49f5fbd
               name: test1
        description:
        vip_port_id: 21cebbd5-fa4c-4d20-9858-d14ba3eacea8
      vip_subnet_id: 0916f471-afcd-48ee-afc5-56bcb0efa963
        vip_address: 172.168.1.6
     admin_state_up: 1
provisioning_status: ACTIVE
   operating_status: ONLINE
          flavor_id: NULL
1 row in set (0.003 sec)

</code></pre>
<p>Then I try to use GORM mapping the table. I just chosen two fields <code>ID</code> and <code>Name</code> for the test.</p>
<pre class="lang-golang prettyprint-override"><code>package main

import (
    &quot;log&quot;

    &quot;gorm.io/driver/mysql&quot;
    &quot;gorm.io/gorm&quot;
)

// declare only two attribute in the model for test purpose 
type Lbaas_loadbalancers struct {
    ID   string
    Name string
}

func main() {
    var lb Lbaas_loadbalancers
    dsn := &quot;test:test@tcp(192.168.0.17:3306)/test?charset=utf8mb4&amp;parseTime=True&amp;loc=Local&quot;
    db, err := gorm.Open(mysql.Open(dsn), &amp;gorm.Config{})
    if err != nil {
        log.Fatal(&quot;connection error&quot;)
    }

    test := db.Take(&amp;lb)
    log.Println(&quot;test err is &quot;, test.Error)
    log.Println(test.RowsAffected)

    // this line report error: ./db.go:25:6: test.ID undefined (type *gorm.DB has no field or method ID)
    log.Println(test.ID)
    
    // if I comment the above line, this print out 'mysql', but the actual name is 'test1'.
    log.Println(test.Name())
}
</code></pre>
<p>Finally, I run <code>go run db.go</code>, I got this error:</p>
<pre class="lang-sh prettyprint-override"><code>➜  test git:(main) ✗ go run db.go
# command-line-arguments
./db.go:27:20: cannot convert test.Config.Dialector.Name (type func() string) to type string
</code></pre>
<p>It seems not the right way to do it. what is the correct way to auto map an existing database in Mysql by using GORM module?</p>
<p>If the below code is the correct way, why I cannot get the <code>ID</code> attribute from the return value of <code>db.Take</code> method directly? Do I need to do data conversion?</p>
<p>Please give me some hints, thanks.</p>

## Answers
### Answer ID: 70135853
<p>I know what is wrong here, I should not get ID and Name from the <code>db.Take</code> return, It takes the address of lb variable, and change the lb.</p>
<p>I am so silly, just realized the problem. :)</p>

