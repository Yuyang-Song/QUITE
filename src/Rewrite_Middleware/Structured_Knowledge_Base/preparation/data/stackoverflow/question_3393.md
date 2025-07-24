# How can I add memory to a sql agent in LangChain?
[Link to question](https://stackoverflow.com/questions/78363465/how-can-i-add-memory-to-a-sql-agent-in-langchain)
**Creation Date:** 1713743085
**Score:** 3
**Tags:** python, langchain, py-langchain, langchain-agents
## Question Body
<p>I am trying my best to introduce memory to the sql agent (by memory I mean that it can remember past interactions with the user and have it in context), but so far I am not succeeding.</p>
<p>For example, if I ask it something related to a database, it answers me and then I ask it something else related to a previous question, it should answer me properly by having a context window, but in my case it doesn't, because it doesn't take into account the conversation.</p>
<p>In my case, I believe that the most logical thing to do is to insert said context by means of the ConversationBufferMemory class, that later I introduce it in the sql agent in the following way:</p>
<p><code>agent_executor_kwargs={&quot;memory&quot;: memory,  &quot;return_intermediate_steps&quot;: True},</code></p>
<p>Here you have the rest of the code, so you have a context of how the code is.</p>
<pre><code>from langchain.agents import create_sql_agent
from langchain_community.agent_toolkits import SQLDatabaseToolkit
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_openai import ChatOpenAI
import streamlit as st
from langchain_core.messages import AIMessage, HumanMessage
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import (
    ChatPromptTemplate,
    FewShotPromptTemplate,
    MessagesPlaceholder,
    PromptTemplate,
    SystemMessagePromptTemplate,
)
from examples import get_example_selector
from dotenv import load_dotenv
 
load_dotenv()
 
# Function to instantiate the database
def init_database(username, password, server, database, port) -&gt; SQLDatabase:
    db_uri = f&quot;mysql+mysqlconnector://{username}:{password}@{server}:{port}/{database}&quot;
    return SQLDatabase.from_uri(db_uri)

# Streamlit interface initialization
st.title(&quot;LangChain SQL Agent - No Memory&quot;)
with st.sidebar:
    on_show_query = st.toggle('Show Query Mode')
    st.subheader(&quot;Database Configuration&quot;)
    username = st.text_input(&quot;User&quot;, key=&quot;User&quot;)
    password = st.text_input(&quot;Password&quot;,type=&quot;password&quot;, key=&quot;Password&quot;)
    server = st.text_input(&quot;Server&quot;, key=&quot;Server&quot;)
    port = st.text_input(&quot;Port&quot;, key=&quot;Port&quot;)
    database = st.text_input(&quot;DB Name&quot;, key=&quot;Database&quot;)
    connect_button = st.button(&quot;Connect&quot;)

# Initialize agent_executor in st.session_state
if &quot;agent_executor&quot; not in st.session_state:
    st.session_state.agent_executor = None

if &quot;chat_history&quot; not in st.session_state:
        st.session_state.chat_history = [
            AIMessage(content=&quot;Hello! I'm the SQL Agent. How can I help you today?&quot;)
        ]

# Connect to the database when the button is clicked.
if connect_button:
    sql_database = init_database(username, password, server, database, port)
    llm = ChatOpenAI(temperature=0, model_name='gpt-4')
    toolkit = SQLDatabaseToolkit(db=sql_database, llm=llm)
    
    system_prefix =&quot;&quot;&quot;You are an agent designed to interact with a SQL database.
    Given an input question, create a syntactically correct MariaDB query to run, then look at the results of the query and return the answer.
    You can order the results by a relevant column to return the most interesting examples in the database.
    Never query for all the columns from a specific table, only ask for the relevant columns given the question.
    You have access to tools for interacting with the database.
    Only use the given tools. Only use the information returned by the tools to construct your final answer.
    You MUST double check your query before executing it. If you get an error while executing a query, rewrite the query and try again.

    DO NOT make any DML statements (INSERT, UPDATE, DELETE, DROP etc.) to the database.

    If the question does not seem related to the database, just return &quot;I don't know&quot; as the answer.

    Here are some examples of user inputs and their corresponding SQL queries:&quot;&quot;&quot;
 
 
    few_shot_prompt = FewShotPromptTemplate(
        example_selector=get_example_selector(),
        example_prompt=PromptTemplate.from_template(
            &quot;User input: {input}\nSQL query: {query}&quot;
        ),
        input_variables=[&quot;input&quot;],
        prefix=system_prefix,
        suffix=&quot;If the user's question is not related to any of the examples, you do not have to use them&quot;,
    )

    full_prompt = ChatPromptTemplate.from_messages(
        [
            SystemMessagePromptTemplate(prompt=few_shot_prompt),
            (&quot;human&quot;, &quot;{input}&quot;),
            MessagesPlaceholder(&quot;agent_scratchpad&quot;),
        ]
    )
 
    memory = ConversationBufferMemory(memory_key=&quot;chat_history&quot;, input_key=&quot;input&quot;,return_messages=True,k=5)
    sql_agent_query = &quot; &quot;
    st.session_state.agent_executor = create_sql_agent(
        llm=llm,
        toolkit=toolkit,
        prompt=full_prompt,
        prefix=sql_agent_query,
        agent_type=&quot;openai-tools&quot;,
        agent_executor_kwargs={&quot;memory&quot;: memory,  &quot;return_intermediate_steps&quot;: True},
        verbose=True,
    )
    st.session_state[&quot;db_connected&quot;] = True
    st.success(&quot;Database connected successfully!&quot;)
 
# Function to execute and display queries in a safe way
def safe_run_query(query):
    try:
        result = st.session_state.agent_executor.invoke(query)
        return result
    except Exception as e:
        st.error(&quot;Failed to execute query: &quot; + str(e))
        return None
 
for message in st.session_state.chat_history:
  if isinstance(message, AIMessage):
    with st.chat_message(&quot;AI&quot;):
      st.markdown(message.content)
  elif isinstance(message, HumanMessage):
    with st.chat_message(&quot;Human&quot;):
      st.markdown(message.content)
 
# Execution of the query
if &quot;db_connected&quot; in st.session_state and st.session_state[&quot;db_connected&quot;]:
    
    user_input = st.chat_input(&quot;Enter your question:&quot;)
    if user_input is not None and user_input.strip() != &quot;&quot;:
        st.session_state.chat_history.append(HumanMessage(content=user_input))
    
        with st.chat_message(&quot;Human&quot;):
            st.markdown(user_input)
            
        with st.spinner(&quot;Generating response...&quot;):
            with st.chat_message(&quot;AI&quot;):
                    response = safe_run_query(user_input)
                    # Extracting the output message from the response
                    output_message = response.get('output', 'No output found')
                    chat_history_message = response.get('chat_history', 'No output found')
                    
                    st.markdown(output_message)
 
                    intermediate_steps = response['intermediate_steps']
 
                    # Initialize output_query to None in case no relevant step is found
                    output_query = None
 
                    if on_show_query:
                    # Loop through each step in intermediate_steps
                        for step in intermediate_steps:
                            action, result = step
                            st.text(action.log)
                            action, tool_input = step  # Each step is a tuple with the action and tool_input
                            # Check if the current action is for SQL database querying
                            if action.tool == 'sql_db_query':
                                output_query = action.tool_input
                                break
 
                        if output_query:
                            st.code(output_query)
                          
            st.session_state.chat_history.append(AIMessage(content=output_message)) # Moved inside the if block
 
else:
    st.warning(&quot;Please connect to the database first.&quot;)
</code></pre>
<p>My goal is to have a prototype of a chat that can be interacted with in a natural language and to be able to ask questions about any database it is connected to. I develop this for the moment with Python (more specifically with LangChain to make the backend part and to be able to connect any language model with a database) and with Streamlit (to develop the frontend part and to make a prototype of the application that I aim to develop).</p>
<p>If someone could give me a hand, I would really appreciate it.</p>
<p>Thanks in advance.</p>

