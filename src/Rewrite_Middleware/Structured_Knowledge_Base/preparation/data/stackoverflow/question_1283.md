# I wanna paginate in class view, but an error happened &quot;Cannot filter a query once a slice has been taken.&quot;
[Link to question](https://stackoverflow.com/questions/68093878/i-wanna-paginate-in-class-view-but-an-error-happened-cannot-filter-a-query-onc)
**Creation Date:** 1624425463
**Score:** 1
**Tags:** python, python-3.x, django, django-views
## Question Body
<p>I wanna implement pagination in ListView in Django. I can rewrite the view in function view, but I wanna know how to do pagination in class view for practice.</p>
<p>What I wanna do here is to get data filtered by logged in user and display them with pagination by 20(doesn't matter the number). For example, if Alex is currently logging in, I wanna display Alex's data from the database paginated by 20.</p>
<p>But, when I wrote the code below, I got an error &quot;Cannot filter a query once a slice has been taken.&quot; So, now on the HTML file, there are all users' data like Alex's data, Bob's data, Lisa's data, and all other users' data.</p>
<p>I tried to put <code>paginate_by = 20</code> under the get_context_data function, but doesn't work. I even think I may not use paginate_by with get_context_data.</p>
<pre><code>class FoodList(LoginRequiredMixin, ListView):
  model = Food
  template_name = 'base/all_foods.html'
  context_object_name = 'foods'
  ordering = ['-created']
  paginate_by = 20
  def get_context_data(self, **kwargs):
    context = super().get_context_data(**kwargs)
    context['color'] = 'red'
    context['foods'] = context['foods'].filter(user=self.request.user)

</code></pre>
<p>Let me know if I need to put more info.
Any advice is helpful and thank you for your help in advance!!</p>

## Answers
### Answer ID: 68093951
<p>It's because of this line <code>context['foods'] = context['foods'].filter(user=self.request.user)</code>.</p>
<p>Your <code>context_object_name = 'foods'</code>. and you are filtering it after it's sliced by <code>pagination</code> in <code>get_context_data</code> method.</p>
<p>If you want to filter your <code>queryset</code> and still have <code>pagination</code>, you can do this:</p>
<pre><code>class FoodList(LoginRequiredMixin, ListView):
    model = Food
    template_name = 'base/all_foods.html'
    context_object_name = 'foods'
    ordering = ['-created']
    paginate_by = 20

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['color'] = 'red' 
        return context 
</code></pre>
<p>Now it will work fine.</p>
<p><strong>P.S.</strong> always filter or change your queryset in <code>get_queryset</code> method or <code>queryset</code> attribute. don't do it in <code>get_context_data</code> method.</p>

