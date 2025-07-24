# REST react form is not working [Java Spring backend]
[Link to question](https://stackoverflow.com/questions/74500200/rest-react-form-is-not-working-java-spring-backend)
**Creation Date:** 1668862672
**Score:** 0
**Tags:** javascript, reactjs, spring-mvc
## Question Body
<p>My Java Spring backend api is working correctly. I can create new Users using for example curl POST methods. However When I try doing the same with Form in the Browser no user is being stored in Data base.
Here is the code:</p>
<p>class App method creates new user</p>
<pre><code>// tag::create[]
onCreate(newUser) {
   follow(client, root, ['users']).then(userCollection =&gt; {
      return client({
         method: 'POST',
         path: userCollection.entity._links.self.href,
         entity: newUser,
         headers: {'Content-Type': 'application/json'}
      })
   }).then(response =&gt; {
      return follow(client, root, [
         {rel: 'users', params: {'size': this.state.pageSize}}]);
   }).done(response =&gt; {
      if (typeof response.entity._links.last !== &quot;undefined&quot;) {
         this.onNavigate(response.entity._links.last.href);
      } else {
         this.onNavigate(response.entity._links.self.href);
      }
   });
}
// end::create[]
</code></pre>
<p>Here is class creating dialogue to fill in data:</p>
<pre><code>// tag::create-dialog[]
class CreateDialog extends React.Component {

   constructor(props) {
      super(props);
      this.handleSubmit = this.handleSubmit.bind(this);
   }

   handleSubmit(e) {
      e.preventDefault();
      const newUser = {};
      this.props.attributes.forEach(attribute =&gt; {
         newUser[attribute] = ReactDOM.findDOMNode(this.refs[attribute]).value.trim();
      });
      this.props.onCreate(newUser);

      // clear out the dialog's inputs
      this.props.attributes.forEach(attribute =&gt; {
         ReactDOM.findDOMNode(this.refs[attribute]).value = '';
      });

      // Navigate away from the dialog to hide it.
      window.location = &quot;#&quot;;
   }

   render() {
      const inputs = this.props.attributes.map(attribute =&gt;
         &lt;p key={attribute}&gt;
            &lt;input type=&quot;text&quot; placeholder={attribute} ref={attribute} className=&quot;field&quot;/&gt;
         &lt;/p&gt;
      );

      return (
         &lt;div&gt;
            &lt;a href=&quot;#createUser&quot;&gt;Create&lt;/a&gt;

            &lt;div id=&quot;createUser&quot; className=&quot;modalDialog&quot;&gt;
               &lt;div&gt;
                  &lt;a href=&quot;#&quot; title=&quot;Close&quot; className=&quot;close&quot;&gt;X&lt;/a&gt;

                  &lt;h2&gt;Create new user&lt;/h2&gt;

                  &lt;form&gt;
                     {inputs}
                     &lt;button onClick={this.handleSubmit}&gt;Create&lt;/button&gt;
                  &lt;/form&gt;
               &lt;/div&gt;
            &lt;/div&gt;
         &lt;/div&gt;
      )
   }

}
// end::create-dialog[]
</code></pre>
<p>What am I doing wrong here so My POST queries end up not creating new users?</p>
<p>I tried to rewrite methods so They will correctly generate new Objects in database basing on input coming from client.</p>

## Answers
### Answer ID: 74511675
<p>OK so resolving this required from me to dive deeper into react debugging done in Developer tools in Browser. So I received such error:</p>
<pre><code>&quot;JSON parse error: Cannot coerce empty String (&quot;&quot;) to element of `java.util.Set&lt;com.gloss.model.EmailAddress&gt;` (but could if coercion was enabled using `CoercionConfig`); nested exception is com.fasterxml.jackson.databind.exc.InvalidFormatException: Cannot coerce empty String (&quot;&quot;) to element of `java.util.Set&lt;com.gloss.model.EmailAddress&gt;` (but could if coercion was enabled using `CoercionConfig`)
 at [Source: (org.springframework.util.StreamUtils$NonClosingInputStream); line: 1, column: 75] (through reference chain: com.gloss.model.User[&quot;emailAddress&quot;])&quot;
</code></pre>
<p>As I reviewed User model it received String which could not be mapped to an instance of an object belonging to Set data structure.
The simplest solution will be to configure Jackson to accept empty Strings as null by adding this line to properties file:</p>
<pre><code>spring.jackson.deserialization.accept-empty-string-as-null-object=true
</code></pre>
<p>This did the trick for me.</p>

