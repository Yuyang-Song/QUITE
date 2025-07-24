# how to join 4 or more tables in sequelize?
[Link to question](https://stackoverflow.com/questions/64947004/how-to-join-4-or-more-tables-in-sequelize)
**Creation Date:** 1605985716
**Score:** 0
**Tags:** node.js, sequelize.js
## Question Body
<p>I am rewriting an app , with existing database using sequelize. I have converted existing table, to models in sequelize as below. I have employee table, and access type model, which has read, write, or both in an admin access. all of these access are tracked for employee in and employee access table. but there is a employee group table also, which keeps track , if employee belongs to a particular group and their access type. how do i query using sequelize , to get particular employee access list from employeeAccess table, and also if it belongs to group and if it does access type of that group. so essentially,  need to query by joining 4 tables -  employee, employee access, employee group and then access type table.</p>
<ol>
<li>employee model</li>
</ol>
<pre><code>    var employee = db.seq.define('Employee',{
        id: { type: db.Sequelize.INTEGER},
        managerId: { type: db.Sequelize.INTEGER}, 
        employee_name: { type: db.Sequelize.STRING} ...
    });
    employee.hasOne(address);
    employee.belongsTo(employee, { foreignKey: 'managerId', as: 'Manager' }); 
</code></pre>
<ol start="2">
<li>address model</li>
</ol>
<pre><code>    var adress= db.seq.define(&quot;Adresss&quot;,{
        employee_id: { type: db.Sequelize.INTEGER}...
    });
    address.belongsto(employee); 
</code></pre>
<ol start="3">
<li>accessType model</li>
</ol>
<pre><code>    var accessType = db.seq.define('AccessType ',{
        id: { type: db.Sequelize.INTEGER},
        type: { type: db.Sequelize.STRING}....
    });
    accessType.hasMany(employeeGroup );
    accessType.hasMany(employeeAccess);
</code></pre>
<ol start="4">
<li>EmployeeGroup model</li>
</ol>
<pre><code>    var EmployeeGroup = db.seq.define('EmployeeGroup ',{
        id: { type: db.Sequelize.INTEGER},
        access_type_id: { type: db.Sequelize.INTEGER},
        employee_id: { type: db.Sequelize.INTEGER} ...
    });
    EmployeeGroup .belongsto(employee);
    EmployeeGroup .belongsto(accessType ); 
</code></pre>
<ol start="5">
<li>employeeAccess model</li>
</ol>
<pre><code>    var employeeAccess = db.seq.define('employeeAccess ',{
        id: { type: db.Sequelize.INTEGER},
        access_type_id: { type: db.Sequelize.INTEGER},
        employee_id: { type: db.Sequelize.INTEGER} ...
    });
    employeeAccess.belongsto(employee); 
    employeeAccess.belongsto(accessType ); 
</code></pre>
<p>sql</p>
<pre><code>select * from employeeAcess as a 
left outer join employeeGroup as g 
on a.access_type_id = g.access_type_id 
left outer join accesstype as t 
on g.access_type_id = t.id 
where a.employee_id = 1 and g.employee_id = 1; 
</code></pre>

## Answers
### Answer ID: 64948057
<p>Try something like this:</p>
<pre><code>const employeeItem = await employee .findById(1, {
  include: [{ 
    model: employeeGroup,
    include: [accessType]
  }, employeeAccess],
  where: {
    '$employeeGroup.access_type_id$': sequelize.col('employeeAccess.access_type_id')
  }
}
</code></pre>

