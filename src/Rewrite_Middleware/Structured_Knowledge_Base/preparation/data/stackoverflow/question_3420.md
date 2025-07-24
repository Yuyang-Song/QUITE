# Trying to build Text to SQL using ollama mistral and create_sql_agent
[Link to question](https://stackoverflow.com/questions/79117552/trying-to-build-text-to-sql-using-ollama-mistral-and-create-sql-agent)
**Creation Date:** 1729679842
**Score:** 0
**Tags:** python, py-langchain, ollama, mistral-7b, langchain-agents
## Question Body
<p>I am trying to build one text to sql app where I have used ollama and mistral.
Now without agent it is sql queries but sometime it is generating table names which is not present in the db and logically wrong as well.
So I have tried with SQL agent but it is giving different errors every time.
Could someone please correct my code so I can use local model with sql agent?
Please consider me as a beginner. Thanks in advance!</p>
<pre><code>from db import get_schema, db
from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from langchain_ollama import OllamaLLM
from langchain.agents import AgentType
from langchain_core.prompts.chat import ChatPromptTemplate, MessagesPlaceholder,AIMessagePromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate
from langchain_community.agent_toolkits.sql.prompt import (
    SQL_FUNCTIONS_SUFFIX,
    SQL_PREFIX,
)

db = SQLDatabase.from_uri(&quot;postgresql+psycopg2://postgres:postgres@localhost/dvdrental&quot;)

prefix = &quot;&quot;&quot;
You are an agent designed to interact with a SQL database.
Given an input question, create a syntactically correct query to run, then look at the results of the query and return the answer.
Unless the user specifies a specific number of examples they wish to obtain, always limit your query to at most results.
You can order the results by a relevant column to return the most interesting examples in the database.
Never query for all the columns from a specific table, only ask for the relevant columns given the question.
You have access to tools for interacting with the database.
Only use the below tools. Only use the information returned by the below tools to construct your final answer.
You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

If the question does not seem related to the database, just return &quot;I don't know&quot; as the answer.
&quot;&quot;&quot;

suffix = &quot;&quot;&quot;I should look at the tables in the database to see what I can query.  Then I should query the schema of the most relevant tables.
&quot;&quot;&quot;


hinput = &quot;How many Ed Chase movies are there?&quot;
messages = [
                SystemMessagePromptTemplate.from_template(prefix),
                HumanMessagePromptTemplate.from_template(&quot;{hinput}&quot;),
                AIMessagePromptTemplate.from_template(suffix),
                MessagesPlaceholder(variable_name=&quot;agent_scratchpad&quot;),
            ]

prompt = ChatPromptTemplate.from_messages(messages)

llm = OllamaLLM(model=&quot;mistral&quot;)
toolkit = SQLDatabaseToolkit(db=db, llm=llm)
agent_executor = create_sql_agent(
    llm=llm,
    toolkit=toolkit,
    agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    prompt=prompt,
    handle_parsing_errors=True
)

res = agent_executor.invoke()
print(&quot;SQL Query Result:&quot;)
print(res)
</code></pre>
<p>Some errors:</p>
<pre><code>raise ValueError(f&quot;Prompt missing required variables: {missing_vars}&quot;)
ValueError: Prompt missing required variables: {'tool_names', 'tools'}
</code></pre>

