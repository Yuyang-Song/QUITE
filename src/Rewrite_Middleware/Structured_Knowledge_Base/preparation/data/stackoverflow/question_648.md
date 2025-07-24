# How to keep database data when run py.test?
[Link to question](https://stackoverflow.com/questions/35075734/how-to-keep-database-data-when-run-py-test)
**Creation Date:** 1454033611
**Score:** 3
**Tags:** python, pytest, pytest-django
## Question Body
<p>I want to test my query db function.</p>

<pre><code>import pytest
from account_system.action import my_action
from account_system.models import MyUser

@pytest.mark.django_db
def test_ok_profile():
    req = FakeRequest()
    email = 'tester@example.com'
    MyUser.objects.create_user(
        email=email,
        password="example",
    )
    # query MyUser table and return result
    result = my_action.get_profile(email)
    assert result == 'success'
</code></pre>

<p>But it's fail.</p>

<pre><code>&gt;       assert result == 'success'
E       assert None == 'success'
</code></pre>

<p>The function doesn't get any result from DB.</p>

<p>I check the database data and doesn't see any record.
(ex. User <em>tester@example.com</em>)</p>

<p><strong>How to rewrite my code for testing?</strong></p>

<p>Or <strong>how to keep data in database?</strong></p>

<p>Thank you,</p>

## Answers
### Answer ID: 37661174
<p>This is the way of how databases tests works.. 
When you set a django_db, the pytest will rollback your data after use.
But if you want to use the same data in several tests, you should take a look on 
pytest.fixtures and factory_boy like :</p>

<pre><code>import factory

class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

@pytest.fixture
def user():
  return UserFactory(email = "bla@bla.com", password = "blabla")
</code></pre>

<p>And now you apply this reference on your test code:</p>

<pre><code>test_test_ok_profile(user):
  assert user.email = "bla@bla.com"
</code></pre>

