# create_sql_agent with AzureOpenAI?
[Link to question](https://stackoverflow.com/questions/78439451/create-sql-agent-with-azureopenai)
**Creation Date:** 1715036597
**Score:** 1
**Tags:** python, azure, openai-api, langchain, azure-openai
## Question Body
<p>I have put together a script that works just fine using OpenAI api. I am now trying to switch it over to AzureOpenAI yet it seems I am running into an issue with the create_sql_agent(). Can you use create_sql_agent with AzureOpenAI model gpt-35-turbo-1106? Could it be an issue with my api_version within AzureOpenAI()? The error I receive is &quot;TypeError: Completions. create() got an unexpected keyword argument 'tools'&quot; which I think could also be the option using 'openai-tools' as my agent_type?</p>
<h2>Code</h2>
<pre class="lang-py prettyprint-override"><code>import os
from langchain_openai import AzureOpenAI
from langchain.agents import create_sql_agent
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain.sql_database import SQLDatabase
from dotenv import load_dotenv
from langchain.agents import AgentExecutor

from langchain_core.prompts.chat import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
    SystemMessagePromptTemplate,
    AIMessagePromptTemplate,
    MessagesPlaceholder,
)

path = (os.getcwd()+'\creds.env')

load_dotenv(path)  

db = SQLDatabase.from_uri(
    f&quot;postgresql://{os.environ.get('user')}:{os.environ.get('password')}@{os.environ.get('host')}:{os.environ.get('port')}/{os.environ.get('database')}&quot;)

llm = AzureOpenAI(azure_endpoint=MY_ENDPOINT,
                  deployment_name=MY_DEPLOYMENT_NAME,
                  model_name='gpt-35-turbo', # should it be 'gpt-35-turbo-1106'?
                 temperature = 0,
                 api_key = MY_KEY,
                 api_version = '2023-07-01-preview') #my api_version correct? Uncertain which one

toolkit = SQLDatabaseToolkit(db=db, llm=llm)

prefix = &quot;&quot;&quot;
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct {dialect} query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most {top_k} results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double-check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP, CASCADE, etc.) to the database.

If the question does not seem related to the database, just return &quot;I don't know&quot; as the answer.

If asked about a person do not return an 'ID' but return a first name and last name.

&quot;&quot;&quot;

suffix = &quot;&quot;&quot; I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables.
&quot;&quot;&quot;

messages = [
                SystemMessagePromptTemplate.from_template(prefix),
                HumanMessagePromptTemplate.from_template(&quot;{input}&quot;),
                AIMessagePromptTemplate.from_template(suffix),
                MessagesPlaceholder(variable_name=&quot;agent_scratchpad&quot;),
            ]


agent_executor = create_sql_agent(llm,
                                  toolkit=toolkit,
                                  agent_type='openai-tools', #does this work with azure?
                                  prompt=prompt,
                                  verbose=False)


print(agent_executor.invoke(&quot;What are the names of the tables&quot;))
</code></pre>
<h2>Error</h2>
<pre><code>---------------------------------------------------------------------------
TypeError                                 Traceback (most recent call last)
Cell In[69], line 1
----&gt; 1 print(agent_executor.invoke(&quot;What are the names of the tables&quot;))

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain\chains\base.py:163, in Chain.invoke(self, input, config, **kwargs)
    161 except BaseException as e:
    162     run_manager.on_chain_error(e)
--&gt; 163     raise e
    164 run_manager.on_chain_end(outputs)
    166 if include_run_info:

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain\chains\base.py:153, in Chain.invoke(self, input, config, **kwargs)
    150 try:
    151     self._validate_inputs(inputs)
    152     outputs = (
--&gt; 153         self._call(inputs, run_manager=run_manager)
    154         if new_arg_supported
    155         else self._call(inputs)
    156     )
    158     final_outputs: Dict[str, Any] = self.prep_outputs(
    159         inputs, outputs, return_only_outputs
    160     )
    161 except BaseException as e:

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain\agents\agent.py:1432, in AgentExecutor._call(self, inputs, run_manager)
   1430 # We now enter the agent loop (until it returns something).
   1431 while self._should_continue(iterations, time_elapsed):
-&gt; 1432     next_step_output = self._take_next_step(
   1433         name_to_tool_map,
   1434         color_mapping,
   1435         inputs,
   1436         intermediate_steps,
   1437         run_manager=run_manager,
   1438     )
   1439     if isinstance(next_step_output, AgentFinish):
   1440         return self._return(
   1441             next_step_output, intermediate_steps, run_manager=run_manager
   1442         )

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain\agents\agent.py:1138, in AgentExecutor._take_next_step(self, name_to_tool_map, color_mapping, inputs, intermediate_steps, run_manager)
   1129 def _take_next_step(
   1130     self,
   1131     name_to_tool_map: Dict[str, BaseTool],
   (...)
   1135     run_manager: Optional[CallbackManagerForChainRun] = None,
   1136 ) -&gt; Union[AgentFinish, List[Tuple[AgentAction, str]]]:
   1137     return self._consume_next_step(
-&gt; 1138         [
   1139             a
   1140             for a in self._iter_next_step(
   1141                 name_to_tool_map,
   1142                 color_mapping,
   1143                 inputs,
   1144                 intermediate_steps,
   1145                 run_manager,
   1146             )
   1147         ]
   1148     )

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain\agents\agent.py:1138, in &lt;listcomp&gt;(.0)
   1129 def _take_next_step(
   1130     self,
   1131     name_to_tool_map: Dict[str, BaseTool],
   (...)
   1135     run_manager: Optional[CallbackManagerForChainRun] = None,
   1136 ) -&gt; Union[AgentFinish, List[Tuple[AgentAction, str]]]:
   1137     return self._consume_next_step(
-&gt; 1138         [
   1139             a
   1140             for a in self._iter_next_step(
   1141                 name_to_tool_map,
   1142                 color_mapping,
   1143                 inputs,
   1144                 intermediate_steps,
   1145                 run_manager,
   1146             )
   1147         ]
   1148     )

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain\agents\agent.py:1166, in AgentExecutor._iter_next_step(self, name_to_tool_map, color_mapping, inputs, intermediate_steps, run_manager)
   1163     intermediate_steps = self._prepare_intermediate_steps(intermediate_steps)
   1165     # Call the LLM to see what to do.
-&gt; 1166     output = self.agent.plan(
   1167         intermediate_steps,
   1168         callbacks=run_manager.get_child() if run_manager else None,
   1169         **inputs,
   1170     )
   1171 except OutputParserException as e:
   1172     if isinstance(self.handle_parsing_errors, bool):

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain\agents\agent.py:514, in RunnableMultiActionAgent.plan(self, intermediate_steps, callbacks, **kwargs)
    506 final_output: Any = None
    507 if self.stream_runnable:
    508     # Use streaming to make sure that the underlying LLM is invoked in a
    509     # streaming
   (...)
    512     # Because the response from the plan is not a generator, we need to
    513     # accumulate the output into final output and return that.
--&gt; 514     for chunk in self.runnable.stream(inputs, config={&quot;callbacks&quot;: callbacks}):
    515         if final_output is None:
    516             final_output = chunk

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain_core\runnables\base.py:2875, in RunnableSequence.stream(self, input, config, **kwargs)
   2869 def stream(
   2870     self,
   2871     input: Input,
   2872     config: Optional[RunnableConfig] = None,
   2873     **kwargs: Optional[Any],
   2874 ) -&gt; Iterator[Output]:
-&gt; 2875     yield from self.transform(iter([input]), config, **kwargs)

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain_core\runnables\base.py:2862, in RunnableSequence.transform(self, input, config, **kwargs)
   2856 def transform(
   2857     self,
   2858     input: Iterator[Input],
   2859     config: Optional[RunnableConfig] = None,
   2860     **kwargs: Optional[Any],
   2861 ) -&gt; Iterator[Output]:
-&gt; 2862     yield from self._transform_stream_with_config(
   2863         input,
   2864         self._transform,
   2865         patch_config(config, run_name=(config or {}).get(&quot;run_name&quot;) or self.name),
   2866         **kwargs,
   2867     )

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain_core\runnables\base.py:1880, in Runnable._transform_stream_with_config(self, input, transformer, config, run_type, **kwargs)
   1878 try:
   1879     while True:
-&gt; 1880         chunk: Output = context.run(next, iterator)  # type: ignore
   1881         yield chunk
   1882         if final_output_supported:

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain_core\runnables\base.py:2826, in RunnableSequence._transform(self, input, run_manager, config)
   2817 for step in steps:
   2818     final_pipeline = step.transform(
   2819         final_pipeline,
   2820         patch_config(
   (...)
   2823         ),
   2824     )
-&gt; 2826 for output in final_pipeline:
   2827     yield output

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain_core\runnables\base.py:1283, in Runnable.transform(self, input, config, **kwargs)
   1280 final: Input
   1281 got_first_val = False
-&gt; 1283 for chunk in input:
   1284     if not got_first_val:
   1285         final = adapt_first_streaming_chunk(chunk)  # type: ignore

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain_core\runnables\base.py:4728, in RunnableBindingBase.transform(self, input, config, **kwargs)
   4722 def transform(
   4723     self,
   4724     input: Iterator[Input],
   4725     config: Optional[RunnableConfig] = None,
   4726     **kwargs: Any,
   4727 ) -&gt; Iterator[Output]:
-&gt; 4728     yield from self.bound.transform(
   4729         input,
   4730         self._merge_configs(config),
   4731         **{**self.kwargs, **kwargs},
   4732     )

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain_core\runnables\base.py:1300, in Runnable.transform(self, input, config, **kwargs)
   1293             raise TypeError(
   1294                 f&quot;Failed while trying to add together &quot;
   1295                 f&quot;type {type(final)} and {type(chunk)}.&quot;
   1296                 f&quot;These types should be addable for transform to work.&quot;
   1297             )
   1299 if got_first_val:
-&gt; 1300     yield from self.stream(final, config, **kwargs)

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain_core\language_models\llms.py:458, in BaseLLM.stream(self, input, config, stop, **kwargs)
    451 except BaseException as e:
    452     run_manager.on_llm_error(
    453         e,
    454         response=LLMResult(
    455             generations=[[generation]] if generation else []
    456         ),
    457     )
--&gt; 458     raise e
    459 else:
    460     run_manager.on_llm_end(LLMResult(generations=[[generation]]))

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain_core\language_models\llms.py:442, in BaseLLM.stream(self, input, config, stop, **kwargs)
    440 generation: Optional[GenerationChunk] = None
    441 try:
--&gt; 442     for chunk in self._stream(
    443         prompt, stop=stop, run_manager=run_manager, **kwargs
    444     ):
    445         yield chunk.text
    446         if generation is None:

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\langchain_openai\llms\base.py:262, in BaseOpenAI._stream(self, prompt, stop, run_manager, **kwargs)
    260 params = {**self._invocation_params, **kwargs, &quot;stream&quot;: True}
    261 self.get_sub_prompts(params, [prompt], stop)  # this mutates params
--&gt; 262 for stream_resp in self.client.create(prompt=prompt, **params):
    263     if not isinstance(stream_resp, dict):
    264         stream_resp = stream_resp.model_dump()

File ~\AppData\Local\Programs\Python\Python311\Lib\site-packages\openai\_utils\_utils.py:277, in required_args.&lt;locals&gt;.inner.&lt;locals&gt;.wrapper(*args, **kwargs)
    275             msg = f&quot;Missing required argument: {quote(missing[0])}&quot;
    276     raise TypeError(msg)
--&gt; 277 return func(*args, **kwargs)

TypeError: Completions.create() got an unexpected keyword argument 'tools'
</code></pre>

## Answers
### Answer ID: 78440581
<p>Your model name and API version should be fine. However, you should be using the chat model type. The <code>AzureChatOpenAI</code> class is used for this.</p>
<p>Update your code:</p>
<pre class="lang-py prettyprint-override"><code>from langchain.chat_models import AzureChatOpenAI

# ...

llm = AzureChatOpenAI(azure_endpoint=MY_ENDPOINT,
                  deployment_name=MY_DEPLOYMENT_NAME,
                  model_name='gpt-35-turbo',
                  temperature = 0,
                  api_key = MY_KEY,
                  api_version = '2023-07-01-preview')
</code></pre>
<p>When you create the sql agent, use the <code>AgentType</code> enumerator, and zero shot to tell the agent not to use memory.</p>
<pre class="lang-py prettyprint-override"><code>from langchain.agents import AgentType, create_sql_agent

# ...

agent_executor = create_sql_agent(llm=llm,
                                  toolkit=toolkit,
                                  agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
                                  prompt=prompt,
                                  verbose=False)
</code></pre>

