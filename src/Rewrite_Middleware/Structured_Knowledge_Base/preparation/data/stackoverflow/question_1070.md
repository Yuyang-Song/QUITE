# How to fix &quot; &#39;Query&#39; object has no attribute &#39;contains_column_references&#39;&quot;
[Link to question](https://stackoverflow.com/questions/57602080/how-to-fix-query-object-has-no-attribute-contains-column-references)
**Creation Date:** 1566448375
**Score:** 1
**Tags:** python, mysql, django, orm
## Question Body
<p>As i'm tring to insert some data using POST request into mysql dataBase i'm getting an error informing me that AttributeError: 'Query' object has no 
attribute 'contains_column_references'</p>

<pre><code>Internal Server Error: /add_borrow/
Traceback (most recent call last):
  File "D:\pyvenv\pyvenv\lib\site-packages\django\core\handlers\exception.py", line 34, in inner
    response = get_response(request)
  File "D:\pyvenv\pyvenv\lib\site-packages\django\core\handlers\base.py", line 115, in _get_response
    response = self.process_exception_by_middleware(e, request)
  File "D:\pyvenv\pyvenv\lib\site-packages\django\core\handlers\base.py", line 113, in _get_response
    response = wrapped_callback(request, *callback_args, **callback_kwargs)
  File "D:\Python_workspace\dms\app01\views.py", line 23, in inner
    return func(req, *args, **kwargs)
  File "D:\Python_workspace\dms\app01\views.py", line 286, in add_borrow
    end_time=end_time, number=number, contents=content ,device_id=device)
  File "D:\pyvenv\pyvenv\lib\site-packages\django\db\models\manager.py", line 82, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "D:\pyvenv\pyvenv\lib\site-packages\django\db\models\query.py", line 422, in create
    obj.save(force_insert=True, using=self.db)
  File "D:\pyvenv\pyvenv\lib\site-packages\django\db\models\base.py", line 741, in save
    force_update=force_update, update_fields=update_fields)
  File "D:\pyvenv\pyvenv\lib\site-packages\django\db\models\base.py", line 779, in save_base
    force_update, using, update_fields,
  File "D:\pyvenv\pyvenv\lib\site-packages\django\db\models\base.py", line 870, in _save_table
    result = self._do_insert(cls._base_manager, using, fields, update_pk, raw)
  File "D:\pyvenv\pyvenv\lib\site-packages\django\db\models\base.py", line 908, in _do_insert
    using=using, raw=raw)
  File "D:\pyvenv\pyvenv\lib\site-packages\django\db\models\manager.py", line 82, in manager_method
    return getattr(self.get_queryset(), name)(*args, **kwargs)
  File "D:\pyvenv\pyvenv\lib\site-packages\django\db\models\query.py", line 1186, in _insert
    return query.get_compiler(using=using).execute_sql(return_id)
  File "D:\pyvenv\pyvenv\lib\site-packages\django\db\models\sql\compiler.py", line 1334, in execute_sql
    for sql, params in self.as_sql():
  File "D:\pyvenv\pyvenv\lib\site-packages\django\db\models\sql\compiler.py", line 1278, in as_sql
    for obj in self.query.objs
  File "D:\pyvenv\pyvenv\lib\site-packages\django\db\models\sql\compiler.py", line 1278, in &lt;listcomp&gt;
    for obj in self.query.objs
  File "D:\pyvenv\pyvenv\lib\site-packages\django\db\models\sql\compiler.py", line 1277, in &lt;listcomp&gt;
    [self.prepare_value(field, self.pre_save_val(field, obj)) for field in fields]
  File "D:\pyvenv\pyvenv\lib\site-packages\django\db\models\sql\compiler.py", line 1208, in prepare_value
    if value.contains_column_references:
AttributeError: 'Query' object has no attribute 'contains_column_references'
</code></pre>

<p>The following code gets the POST request parameters and inserts it into the database</p>

<pre><code>def add_borrow(req):
    user_id = req.session.get("user_id")
    user_obj = models.Person.objects.filter(id=user_id)
    current_time = time.strftime("%Y-%m-%d", time.localtime())
    #
    if req.method == 'POST':
        borrow_name = user_obj[0]
        print("--------")
        print(user_obj)
        print(type(borrow_name.id))
        print("*" * 100)
        lender_id = req.POST.getlist("person")
        lender_name = req.POST.get("pserson")
        print("lender_id {} name is {} type is {}".format(lender_id, lender_name, type(lender_id)))
        device = req.POST.get("type_id")
        number = req.POST.get("number")
        content = req.POST.get("contents")
        start_time = req.POST.get("start_time")
        end_time = req.POST.get("end_time")
        # print("content type is {}".format(type(content)))
        print("start_time type is {}".format(type(start_time)))
        print("device is {} ,device type is {}".format(device, type(device)))
        print("number type is {}".format(type(number)))
        # 处理device_id
        device_id = models.DeviceType.objects.filter(id=device)
        # 处理lender_id
        lender_last = models.Person.objects.filter(id=lender_id[0])
        print("lender_last type is {},".format(lender_last))
        print(type(lender_last))
        # 处理时间
        start_time_new = datetime.datetime.strptime(start_time, "%Y-%m-%d")
        end_time_new = datetime.datetime.strptime(end_time, "%Y-%m-%d")
        min_time = end_time_new - start_time_new
        # 查询库存数量
        lender_obj = models.Devices.objects.filter(id=int(lender_id[0]))
        print("=" * 120)
        print(lender_obj, type(lender_obj))
        print("=" * 120)
        if number is None:
            return HttpResponse('number is null')
        if int(number) &gt; lender_obj[0].number:
            return HttpResponse("number grater have")
        if borrow_name == lender_name:
            return HttpResponse('the name is same ')
        if contents is None:
            return HttpResponse('contents is null')
        if min_time.days &lt; 0 or min_time.days &gt; 7:
            return HttpResponse('start or end time is wrong')

        models.Borrow.objects.create(borrower_id=borrow_name.id, lender_id=lender_last, start_time=start_time,
                                     end_time=end_time, number=number, contents=content ,device_id=device)
        # update lender database
        """
        edit_device_obj = models.Devices.objects.get(id=new_edit_id)
        edit_device_obj.devtype_id = edit_type
        edit_device_obj.person_id = edit_person
        edit_device_obj.number = edit_number
        edit_device_obj.contents = edit_content
        edit_device_obj.save()
        """
        lender_type_id = lender_obj.devtype_id
        # lender_contents = lender_obj.contents
        lender_number = lender_obj.number - number
        # rewrite lender database
        edit_lender_obj = lender_obj
        edit_lender_obj.devtype_id = lender_type_id
        # edit_lender_obj.contents = lender_contents
        edit_lender_obj.number = lender_number
        models.Devices.save()
        return redirect('/borrow_list/')
    person_list = models.Person.objects.all()
    devtype_list = models.DeviceType.objects.all()
    return render(req, "add_borrow.html", {"person_list": person_list, "devicetype": devtype_list})
</code></pre>

<h1>ORM database define is fllowing:</h1>

<pre><code>from django.db import models


class Person(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=32, null=False)
    password = models.CharField(max_length=128, null=False)
    email = models.EmailField(max_length=32, null=False, unique=True)
    phone = models.CharField(max_length=11, null=False, unique=True)

    def __str__(self):
        return self.name

class DeviceType(models.Model):
    id = models.AutoField(primary_key=True)
    dev_type = models.CharField(max_length=32, null=False)


class Devices(models.Model):
    id = models.AutoField(primary_key=True)
    number = models.IntegerField()
    contents = models.TextField(default=None)
    devtype = models.ForeignKey('DeviceType', on_delete=models.CASCADE)
    person = models.ForeignKey('Person', on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.number)

class Borrow(models.Model):
    borrower = models.ForeignKey('Person', related_name='borrower_name', on_delete=models.CASCADE)
    lender = models.ForeignKey('Person', related_name='lender_name', on_delete=models.CASCADE)
    start_time = models.DateField(auto_now_add=True)
    end_time = models.DateField(auto_now_add=True)
    number = models.IntegerField()
    contents = models.CharField(max_length=256,default=None)
    device = models.ForeignKey('Devices', on_delete=models.CASCADE)

    def __str__(self):
        return 'borrower {} ,lender {}'.format(self.borrower, self.lender)
``


</code></pre>

## Answers
### Answer ID: 63834394
<p>I got this error when trying to add a queryset object to a ManyToMany field.  I did this because i forgot to use .first() on my queryset to get a single object instance.</p>
<p>For example:</p>
<pre><code>first_ford_car = Car.objects.filter(make=&quot;Ford&quot;)

homeowner.cars.add(first_ford_car)
</code></pre>
<p>*where homeowner.cars = models.Many2Many relation</p>
<p>This was causing my error because the <em>first_ford_car</em> variable is a queryset versus a single car instance</p>
<p>to fix in my case:</p>
<pre><code>first_ford_car = Car.objects.filter(make=&quot;Ford&quot;).first()
</code></pre>
<p>It maybe different in other cases, but id suggest checking your types when doing ForeignKey/Many2Many updates</p>

