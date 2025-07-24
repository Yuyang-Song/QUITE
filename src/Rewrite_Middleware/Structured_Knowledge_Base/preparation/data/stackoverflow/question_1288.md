# Rails NoMethodError (undefined method `&lt;&lt;&#39; for #&lt;ActiveRecord::Relation []&gt;):
[Link to question](https://stackoverflow.com/questions/68404242/rails-nomethoderror-undefined-method-for-activerecordrelation)
**Creation Date:** 1626415978
**Score:** 0
**Tags:** ruby-on-rails, ruby, activerecord, rails-activerecord, multi-database
## Question Body
<p><strong>The Back Story</strong></p>
<p>I am currently changing my Ruby on Rails app to a multi-database configuration. Main reason for the switch was to put my Member(User) and Profile tables in a separate database, which could be accessed from another RoR app; thus allowing me to have a single sign-on capability aside from using OAuth and Doorkeeper. This has been a many many hours project with many crazy hurdles. Finally tonight it seemed that everything was working, until I ran my spec tests, and one of my work arounds I did today is throwing flags.</p>
<p>Here is the appropriate code for the problem, simplified for brevity sake.</p>
<p>Any help would be greatly appreciated. Thank you.</p>
<p><strong>Models</strong></p>
<p>app/models/members_record.rb</p>
<pre><code>class MembersRecord &lt; ApplicationRecord
    self.abstract_class = true
  
    connects_to database: { writing: :members, reading: :members }
end
</code></pre>
<p>app/models/member.rb</p>
<pre><code>class Member &lt; MembersRecord
    devise  :database_authenticatable, :registerable,
            :recoverable, :rememberable, :trackable, 
            :validatable, :confirmable
  
    has_one :member_map,    dependent: :destroy
    has_one :profile,       dependent: :destroy
    has_one :site_profile,  dependent: :destroy
    
    has_many :approved_group_members, -&gt; { approved }, class_name: &quot;GroupMember&quot;
    has_many :groups, through: :approved_group_members, class_name: &quot;Group&quot;, source: :group
</code></pre>
<p>app/models/group.rb</p>
<pre><code>class Group &lt; ApplicationRecord
    belongs_to :owner, class_name: 'Member'
    belongs_to :organization, optional: true
  
    has_many :group_members, dependent: :destroy
  
    # Many of the lines below no longer work with Multiple DBs, as we can not INNER JOIN across DBs.
    # They have been commented out and methods built in their place.
  
    has_many :approved_group_members, -&gt; { approved }, class_name: &quot;GroupMember&quot;
    # has_many :members, through: :approved_group_members, class_name: &quot;Member&quot;, source: :member
    def members
      Member.where(id: self.approved_group_members.pluck(:member_id))
    end
  
    has_many :invited_group_members, -&gt; { invited }, class_name: &quot;GroupMember&quot;
    # has_many :invited_members, through: :invited_group_members, class_name: &quot;Member&quot;, source: :member
    def invited_members
      Member.where(id: self.invited_group_members.pluck(:member_id))
    end
</code></pre>
<p>app/models/group_member.rb</p>
<pre><code>class GroupMember &lt; ApplicationRecord
  belongs_to :group
  belongs_to :member

  enum status: { approved: 0, invited: 1, pending_approval: 2, banned: 3}
end
</code></pre>
<p><strong>The Workarounds</strong></p>
<p>Now, looking at the above code, you should see a few of the workarounds in question within the group model. The original code was commented out with the workaround beneath it. Here is just that code:</p>
<pre><code># Many of the lines below no longer work with Multiple DBs, as we can not INNER JOIN across DBs.
# They have been commented out and methods built in their place.

has_many :approved_group_members, -&gt; { approved }, class_name: &quot;GroupMember&quot;
# has_many :members, through: :approved_group_members, class_name: &quot;Member&quot;, source: :member
def members
  Member.where(id: self.approved_group_members.pluck(:member_id))
end

has_many :invited_group_members, -&gt; { invited }, class_name: &quot;GroupMember&quot;
# has_many :invited_members, through: :invited_group_members, class_name: &quot;Member&quot;, source: :member
def invited_members
  Member.where(id: self.invited_group_members.pluck(:member_id))
end
</code></pre>
<p>The reason for these workarounds is because the <code>has_many</code> relationship was not working with the class <code>Member</code> once that class was referencing data on a different database. The SQL queries being built were failing. So, I made a method instead and called a <code>where</code> on the <code>Member</code> model. That gave me the list of members that I was looking for. I had to do this on 9 different occurrences.</p>
<p><strong>Now the problem that I am having</strong></p>
<p>Within my code in over 100 different spots I add a member, or other object, into a given list, say of 'invited members' with this type of code. (This code specifically is within one of my specs now failing)</p>
<pre><code>it 'will set the GroupMember to approved if the group is invite only and member was invited' do
  group_invitation
  group.invited_members &lt;&lt; member
  expect { service.call! }.to change{GroupMember.count}.by(0)
  expect(service.success?).to be_truthy
  expect(service.success_message).to eq(&quot;You have successfully joined this group.&quot;)
  expect(service.error).to eq(&quot;&quot;)
end
</code></pre>
<p>The second line reads <code>group.invited_members &lt;&lt; member</code> and then I get an error that states:</p>
<pre><code>NoMethodError (undefined method `&lt;&lt;' for #&lt;ActiveRecord::Relation []&gt;):
</code></pre>
<p><strong>My Question</strong></p>
<p>I completely understand what the error is stating, but am at a loss for how to correct it. Is there a different way that I could do the workaround in order to allow the <code>&lt;&lt;</code> to remain? I'd very much prefer to only have to change 9 different times I did the workaround instead of rewriting over 100 different instances where <code>&lt;&lt;</code> is being used to add the member, or whatever the object is, to the list being referenced.</p>
<p>Please let me know if you need any further details. Thank you again!</p>

## Answers
### Answer ID: 68420360
<ol>
<li><p>I would like to go with <a href="https://stackoverflow.com/users/384417/rewritten">rewritten</a> you can go with master of rails.</p>
</li>
<li><p>you can try to convert the object from activerecord relation to
active record collection  proxy object and there we <strong>&lt;&lt;</strong> this
method.Which i think is kind of not a good approach</p>
</li>
</ol>

### Answer ID: 68407146
<p>This is supported natively on Rails 7 upwards. (See <a href="https://edgeguides.rubyonrails.org/active_record_multiple_databases.html#handling-associations-with-joins-across-databases" rel="nofollow noreferrer">https://edgeguides.rubyonrails.org/active_record_multiple_databases.html#handling-associations-with-joins-across-databases</a>, <a href="https://github.blog/2021-07-12-adding-support-cross-cluster-associations-rails-7/" rel="nofollow noreferrer">https://github.blog/2021-07-12-adding-support-cross-cluster-associations-rails-7/</a> and <a href="https://github.com/rails/rails/pull/41937" rel="nofollow noreferrer">https://github.com/rails/rails/pull/41937</a>)</p>
<p>If you really need this, I'd probably recommend moving to rails master, and use the native way:</p>
<pre class="lang-rb prettyprint-override"><code>has_many :members, 
         through: :approved_group_members, 
         class_name: &quot;Member&quot;, 
         source: :member, 
         disable_joins: true
</code></pre>

