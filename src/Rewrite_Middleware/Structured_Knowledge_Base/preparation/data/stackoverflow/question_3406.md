# langchain: create_sql_agent is confusing instruction steps (Observation)
[Link to question](https://stackoverflow.com/questions/78824737/langchain-create-sql-agent-is-confusing-instruction-steps-observation)
**Creation Date:** 1722591004
**Score:** 0
**Tags:** python, sql, langchain, large-language-model, rag
## Question Body
<p>I'm trying to do sql retrieval using a langchain sql agent, pretty much as done in the following snippet:</p>
<pre class="lang-py prettyprint-override"><code>
from sqlalchemy import create_engine
from langchain_huggingface import HuggingFaceEndpoint
from langchain_community.utilities import SQLDatabase
from langchain.agents import AgentExecutor, AgentType
from langchain_community.agent_toolkits import SQLDatabaseToolkit, create_sql_agent

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain.agents.structured_chat.output_parser import StructuredChatOutputParserWithRetries
from langchain_core.exceptions import OutputParserException

engine = create_engine('postgresql+psycopg2://postgres:passwd@localhost:5432/db', future=True)

llm = HuggingFaceEndpoint(
    repo_id=&quot;meta-llama/Meta-Llama-3-8B-Instruct&quot;,
    task=&quot;text-generation&quot;,
    max_new_tokens=512,
    do_sample=False,
    repetition_penalty=1.03,
    temperature=0.01
)

_AGENT_FORMAT_INSTRUCTIONS=&quot;&quot;&quot;
## Use exactly the following format. Don't merge one step content with the next one:

- Question: the input question you must answer.
- Thought: you should always think about what to do.
- Action: the action to take, should be one of [{tool_names}].
- Action Input: the input to the action. DO NOT INCLUDE THE WORD 'Observation'.
- Observation: the result of the action.
... (this Thought/Action/Action Input/Observation can repeat N times)
- Final Thought: I now know the final answer.
- Final Answer: the final answer to the original input question.
- SQL Query used to get the Answer: the final sql query used for the final answer

&quot;&quot;&quot;

def answer_query_agent(question: str):
  db = SQLDatabase(engine=engine)
  toolkit = SQLDatabaseToolkit(db=db, llm=llm)
  output_parser = StructuredChatOutputParserWithRetries.from_llm(llm=llm)

  agent_executor: AgentExecutor = create_sql_agent(
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    llm=llm,
    toolkit=toolkit,
    format_instructions=_AGENT_FORMAT_INSTRUCTIONS,
    verbose=True,
    agent_executor_kwargs={&quot;handle_parsing_errors&quot;: True},
    max_iterations=15,
    top_k=15,
    output_parser=output_parser)

  try:
    resp: Dict[str, Any] = agent_executor.invoke({&quot;input&quot;: question})
    print(f'** Executor result **\n\n{resp}')
  except OutputParserException as e:
    print(f&quot;Error parsing output: {e}&quot;)
    if e.send_to_llm:
        # Optionally, send the observation and llm_output back to the model
        print(f&quot;Observation: {e.observation}&quot;)
        print(f&quot;LLM Output: {e.llm_output}&quot;)

  return resp
</code></pre>
<p>When I run a question which doesn't have to return any result, the agent confuses heavily the instructions, resulting in adding a <em>Observation</em> term to <code>Action Input</code> as it is showed in the debug traces below (only relevant part showed):</p>
<pre><code>[llm/start] [chain:SQL Agent Executor &gt; chain:RunnableSequence &gt; llm:HuggingFaceEndpoint] Entering LLM run with input:
{
  &quot;prompts&quot;: [
    &quot;Answer the following questions as best you can. You have access to the following tools:\n\nsql_db_query - Input to this tool is a detailed and correct SQL query, output is a result from the database. If the query is not correct, an error message will be returned. If an error is returned, rewrite the query, check the query, and try again. If you encounter an issue with Unknown column 'xxxx' in 'field list', use sql_db_schema to query the correct table fields.\nsql_db_schema - Input to this tool is a comma-separated list of tables, output is the schema and sample rows for those tables. Be sure that the tables actually exist by calling sql_db_list_tables first! Example Input: table1, table2, table3\nsql_db_list_tables - Input is an empty string, output is a comma-separated list of tables in the database.\nsql_db_query_checker - Use this tool to double check if your query is correct before executing it. Always use this tool before executing a query with sql_db_query!\n\n\n## Use exactly the following format. Don't include the pattern '\nObservation' as an Action Input value:\n\n- Question: the input question you must answer.\n- Thought: you should always think about what to do.\n- Action: the action to take, should be one of [sql_db_query, sql_db_schema, sql_db_list_tables, sql_db_query_checker].\n- Action Input: the input to the action.\n- Observation: the result of the action.\n... (this Thought/Action/Action Input/Observation can repeat N times)\n- Final Thought: I now know the final answer.\n- Final Answer: the final answer to the original input question.\n- SQL Query used to get the Answer: the final sql query used for the final answer\n\n\n\nBegin!\n\nQuestion: which companies have a commitment with sustainability\nThought: I need to find the companies that have a sustainability commitment. I should look for a table that contains company information and a field that indicates whether or not they have a sustainability commitment. I will first list all the tables in the database using sql_db_list_tables.\nAction: sql_db_list_tables\nAction Input: ''\nObservation\nObservation: company, sales\nThought:&quot;
  ]
}
[llm/end] [chain:SQL Agent Executor &gt; chain:RunnableSequence &gt; llm:HuggingFaceEndpoint] [128ms] Exiting LLM run with output:
{
  &quot;generations&quot;: [
    [
      {
        &quot;text&quot;: &quot;\nI see two tables: company and sales. I should check the schema of these tables to see if there is a field that indicates whether or not a company has a sustainability commitment. I will use sql_db_schema to get the schema of these tables.\nAction: sql_db_schema\nAction Input: company, sales\nObservation&quot;,
        &quot;generation_info&quot;: null,
        &quot;type&quot;: &quot;Generation&quot;
      }
    ]
  ],
  &quot;llm_output&quot;: null,
  &quot;run&quot;: null
}
[chain/start] [chain:SQL Agent Executor &gt; chain:RunnableSequence &gt; parser:ReActSingleInputOutputParser] Entering Parser run with input:
{
  &quot;input&quot;: &quot;\nI see two tables: company and sales. I should check the schema of these tables to see if there is a field that indicates whether or not a company has a sustainability commitment. I will use sql_db_schema to get the schema of these tables.\nAction: sql_db_schema\nAction Input: company, sales\nObservation&quot;
}
[chain/end] [chain:SQL Agent Executor &gt; chain:RunnableSequence &gt; parser:ReActSingleInputOutputParser] [1ms] Exiting Parser run with output:
[outputs]
[chain/end] [chain:SQL Agent Executor &gt; chain:RunnableSequence] [149ms] Exiting Chain run with output:
[outputs]
[tool/start] [chain:SQL Agent Executor &gt; tool:sql_db_schema] Entering Tool run with input:
&quot;company, sales
Observation&quot;
[tool/end] [chain:SQL Agent Executor &gt; tool:sql_db_schema] [0ms] Exiting Tool run with output:
&quot;Error: table_names {'sales\nObservation'} not found in database&quot;
</code></pre>
<p>Any way of or hint on how can I prevent the <code>Observation</code> word being appended to the <code>Action Input</code> as showed just above?</p>

