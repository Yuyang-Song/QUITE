# How do you effectively batch GraphQL mutations using Apollo Client?
[Link to question](https://stackoverflow.com/questions/59398282/how-do-you-effectively-batch-graphql-mutations-using-apollo-client)
**Creation Date:** 1576694462
**Score:** 0
**Tags:** javascript, reactjs, graphql, react-apollo, apollo-client
## Question Body
<p>I'm having an issue handling rapid database updates using GraphQL mutations, specifically through <code>useQuery</code> and <code>useMutation</code> from Apollo Client's <code>react-hooks</code>.  I have a table which represents data from the DB, 4 columns are boolean values represented by checkboxes, with other inputs as well. Checking the checkbox dispatches a request to the database to set the value to true, then refetches (either through <code>refetch</code> imperatively or <code>refetchQueries</code>) the query and updates the table.</p>

<p>My Checkbox component:</p>

<pre><code>export const TableCheckbox: &lt;T extends VasaRecord &amp; DomainEntity, K extends keyof T&gt;(props: TableInputProps&lt;T, K&gt;) =&gt; ReactElement = ({
  value, // Boolean column value
  record, //Entire data record
  dataIndex //Accessor on record where value is located
}) =&gt; {
  const [checked, setChecked] = useState&lt;boolean&gt;(value as boolean);

  // useMutation function
  const { updateEntity } = useContext(
    TrackerContext
  );

  useEffect(() =&gt; {
    setChecked(value as boolean);
  }, [value]);

  const handleCheck = (e: CheckboxChangeEvent) =&gt; {
    const val = e.target.checked;
    setChecked(val);
    const newRecord = { id: record.key, [dataIndex]: val };

      updateEntity({
        variables: { entityTracker: JSON.stringify(newRecord) }
      }).then((res: any) =&gt; {
        console.log(res);
      });

  };

  return (
    &lt;span className="checkbox-wrapper" onClick={disableClickSelect}&gt;
      &lt;Checkbox checked={checked} onChange={handleCheck} /&gt;
    &lt;/span&gt;
  );
};


</code></pre>

<p>However, this cycle can take 1-2 full seconds, which is not a usable response time to see a change reflected. I've addressed this by managing the checkbox state internally and updating it before the mutations/queries are processed and the new data returned.</p>

<p>This mostly works fine, but causes strange behavior when checkboxes or inputs etc. are updated very quickly in succession and some updates can be missed as their requests are not fired. Even worse, because I'm managing the state on the front end, it can show inaccurate information that's then overwritten when the last query returns. I could disable the inputs while a request is running, but that feels like cheating. It's not really noticeable unless you're specifically trying to use tab and space to check as fast as humanly possible, but still isn't good.</p>

<p>Is the answer using the <a href="https://www.apollographql.com/docs/react/caching/cache-configuration/" rel="nofollow noreferrer">in-memory cache</a> provided by Apollo to store the data clientside so it can be updated instantly? This sounds like it could work, but  I wonder if I would have the same problem if updates are dispatched so rapidly that they interfere with one another, plus it would mean rewriting all of the code for interacting with the database everywhere, even where this is not an issue (unless I'm mistaken), so I'd rather avoid it if possible.</p>

<p>Is there an effective way to batch mutations or otherwise prevent them from interfering with each other? Is my entire approach flawed? This pattern works fine when updates are triggered individually or by a user action, but it doesn't seem to handle real-time updates well at all, so any insight or alternatives are much appreciated!</p>

## Answers
### Answer ID: 59399648
<p>It sounds like you should take advantage of Apollo's <a href="https://www.apollographql.com/docs/react/performance/optimistic-ui" rel="nofollow noreferrer">optimistic UI features</a>. You can specify an <code>optimisticResponse</code> for your mutation which will be used as a placeholder for the actual response from the server. This allows your UI to smoothly change in response to user actions even when it takes a while to get a response from the server. The optimistic response is applied to the cache itself, so any other part of your app will immediately reflect the mutation as well. Unfortunately, it will not work with <code>refetch</code>, but ideally you should be using <code>update</code> instead of refetching queries anyway (and optimisticResponse <em>does</em> work with whatever <code>update</code> logic you provide).</p>

