# System.InvalidOperationException: when saving data to my database
[Link to question](https://stackoverflow.com/questions/56550218/system-invalidoperationexception-when-saving-data-to-my-database)
**Creation Date:** 1560279659
**Score:** 1
**Tags:** c#, entity-framework, blazor
## Question Body
<p>ASP.Net core blazor application. When the page first opens it pulls a list of repair orders from the database and displays them on the page.  This works great.</p>

<p>The table of data has a column with an 'Edit' button.  When you edit the data a modal pops up and displays the RO information for someone to edit.</p>

<p>My problem is when I click 'Save', I get the following error.</p>

<p>Error Code:</p>

<blockquote>
  <p>System.InvalidOperationException: 'A second operation started on this
  context before a previous operation completed. This is usually caused
  by different threads using the same instance of DbContext, however
  instance members are not guaranteed to be thread safe. This could also
  be caused by a nested query being evaluated on the client, if this is
  the case rewrite the query avoiding nested invocations.'</p>
</blockquote>

<p>It is worth noting this feature worked great and I have no clue what I changed to make it fail.
OnInitAsync() method:</p>

<pre><code>protected override async Task OnInitAsync()
    {
        await LoadData();        
    }
</code></pre>

<p>Method to load all the data:</p>

<pre><code>protected async Task LoadData()
    {
        _repairOrders = await Task.Run(() =&gt; RepairOrderService.GetAllRepairOrders().ToArray());
        _vehicleLocations = await Task.Run(() =&gt; VehicleLocationService.GetAllLocations().ToArray());
        _repaitStages = await Task.Run(() =&gt; RepairStageService.GetAllRepairStages().ToArray());
        _employees = await Task.Run(() =&gt; EmployeeService.GetAllEmployees().ToArray());
    }
</code></pre>

<p>Method called to save data.</p>

<pre><code>protected async Task SaveRepairOrder()
    {
        if (ro.Id != 0)
        {
            await Task.Run(() =&gt;
            {
                RepairOrderService.EditRepairOrder(ro);
            });
        }
        else
        {
            await Task.Run(() =&gt;
            {
                RepairOrderService.CreateRepairOrder(ro);
            });
        }
        this.isAdd = false;
        await LoadData();
    }
</code></pre>

<p>This is the method in my Data access layer class that is throwing the error.</p>

<pre><code>//Get all repair order details as a list
        public List&lt;RepairOrder&gt; GetAllRepairOrders()
        {
            try
            {
                return db.RepairOrder.ToList();
            }
            catch
            {
                throw;               
            }
        }
</code></pre>

<p>I made the LoadData() method async after the issue started.  Can anyone see what I am missing?</p>

<p>**** Update ********
I changed "services.AddSingleton();" to "services.AddTransient();" and it seems to be working.  I need to dig in and try to determine if this was the way I should have done this in the beginning!</p>

## Answers
### Answer ID: 56550625
<p>As the error mentions what is happening here is that some other thread is already using the context as your method is trying to use it.</p>
<p>Changing the registration to Transient works because the instance is no longer shared... each time you get it, it will be new one... this has some drawbacks, for instance, if you try to &quot;join&quot; two <code>IQueryable&lt;T&gt;</code> it will fail... memory consumption should also go UP.</p>
<p>Now, to your problem, you have to debug the code flow, because apparently, a previously started operation is running on the background AS YOUR CODE ENTERS the LoadData method! So the &quot;Task.Run&quot; doesn't actually have nothing to do with the error... if you remove it you should get the same error...</p>
<p>Something you can do to verify this hypothesis is adding a delay (await Task.Delay(2000);) of about a second or two before loading data... this should be enough to allow the other operation to finish, releasing the context for your method</p>

