# Intelligent structuring of Django Models and queries
[Link to question](https://stackoverflow.com/questions/28521249/intelligent-structuring-of-django-models-and-queries)
**Creation Date:** 1423954770
**Score:** 1
**Tags:** python, django, django-models, orm, django-orm
## Question Body
<p>I am relatively new to Django's database abstraction layer.  To be perfectly honest, I don't have that much experience interacting with databases through any system.  In any case, I am working on a personal project and not happy with my current design, at least as far as my queries are concerned.  I thought I would turn to the community for advice on how to handle my concern.  </p>

<p>Here is a simplified case to begin the discussion.  Suppose we are modeling information about a country.  We might come up with the following </p>

<pre><code>class Country(models.Model):
  ...

class Region(models.Model):
  country = models.ForeignKey(Country)
  ...

class State(models.Model):
  region = models.ForeignKey(Region)
  ...

class County(models.Model):
  state = models.ForeignKey(State)
  ...

class City(models.Model):
  state = models.ForeignKey(County)
  ...
</code></pre>

<p>Okay.  I am happy with this structure because there is no redundant information. yay.  However, when it comes down to making many of the queries I want to make, I get statements like this:</p>

<pre><code># get the country a city is in
def get_country(city):
  return Country.objects.get(region__state__county__city=city)
</code></pre>

<p>This works, but it bothers me quite a bit for the following reason: when I specified my models, I gave Djano the structure of my database.  Namely, the system already knows that a city is in a county, a county is in a state, a state is in a region and, finally, a region is in a country.  When I write the query above, I am supplying redundant information; the structure already implies that there is only one country associated with each city.  Therefore, given a city, it is obvious which country it is in.  Why do I have to specify it again?</p>

<p>Having to do this has a negative impact on development for a number of reasons.  First consider, for example, <code>a get_region()</code> function:</p>

<pre><code>#get the region a city is in:
def get_region(city):
return Region.objects.get(state__county__city=city)
</code></pre>

<p>Everything about this is nearly identical to the get_country function; the get_country query already contains the information necessary to get me the region as well, so I am <em>again</em> informing the system that cities are in counties, which are in states, which are in regions.  </p>

<p>Further, consider the following scenario:  I realize that I've misunderstood the original requirements and I don't even need to consider "regions."  So, wipe that model away and change the State model to contain a reference to Country instead.  The problem is now we have to also rewrite all of the queries.  </p>

<p>This gets ugly fast.  Suppose we want helper methods on our models to get at relevant information on the hierarchy.  For example, Country might have methods <code>get_states()</code>, <code>get_counties()</code>, <code>get_cities()</code>.  States will have <code>get_country()</code>, as well as <code>get_county()</code> and <code>get_cities()</code>.  And so on, everyone gets the picture.  This seems sensible because it would provide an API with which other parts of the system can access this geographic information in a way that is agnostic to the layout of the database.  However, it also means that, because of the way we write the queries powering these functions, each Model has to have a macroscopic understanding of the database.  This failure to separate the semantics of geography from the implementation of our database will result, again, in lots of repeated information and lots of effort if a change needs to be made to that structure. </p>

<p>So, friends, please enlighten me.  Am I not thinking correctly about the relationships between models?  Am I not appreciating the philosophy of Django's database layer?  Am I missing some subset of features that will help me clarify this? </p>

## Answers
### Answer ID: 28525837
<p>Consider making your own subclass of QuerySet, that will look for field in foreign keys when there is no such field in model and use this QuerySet as manager in your models.</p>

### Answer ID: 28522055
<p>IMO, this is a situation where the fully normalized solution is "correct" but may be too cumbersome for the task at hand. I might consider denormalizing slightly and storing fkeys to relationships I need to use frequently. For example:</p>

<pre><code>class City(models.Model):
    county = models.ForeignKey(County)
    region = models.ForeignKey(Region)
    state = models.ForeignKey(State)
    country = models.ForeignKey(Country)

    def save(self, *args, **kw):
        self.region = self.county.region
        self.state = self.county.region.state
        self.country = self.county.region.state.country
        super(City, self).save(*args, **kw)
</code></pre>

<p>Doing this is the "wrong" solution but might work for your needs, particularly if you value database efficiency less than development simplicity. </p>

<p>In any event, I would assert that you would <em>not</em> want Django to assume how City should link back to Country, you'd want to state that explicitly. What if you added a table that linked to both City and Country and your app broke because Django assumed that Cities and Countries were now linked differently?</p>

