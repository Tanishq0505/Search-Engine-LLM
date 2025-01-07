# This code creates a Streamlit web app that integrates with LangChain to enable a chatbot capable of web searches,
#  academic paper lookups, and Wikipedia searches, using tools like DuckDuckGoSearchRun, ArxivQueryRun, and
#  WikipediaQueryRun. It uses StreamlitCallbackHandler for live interaction display.


import streamlit as st
from langchain_groq import ChatGroq
from langchain_community.tools import ArxivQueryRun,WikipediaQueryRun
# ArxivQueryRun:
# A pre-built tool for querying Arxiv.
# Allows you to search for research papers based on a query and retrieve relevant results.

# WikipediaQueryRun:
# A pre-built tool for querying Wikipedia.
# Fetches information from Wikipedia based on a search query.


from langchain_community.utilities import ArxivAPIWrapper,WikipediaAPIWrapper
# WikipediaAPIWrapper:
# Provides a wrapper around the Wikipedia API.
# Used internally by tools like WikipediaQueryRun to fetch data from Wikipedia.
# Can also be used directly for more customized interactions with Wikipedia's API.
    
# ArxivAPIWrapper:
# Wraps the Arxiv API for retrieving research papers and their metadata (e.g., title, abstract, authors).
# Used internally by ArxivQueryRun.

from langchain_community.tools import DuckDuckGoSearchRun
# imports the DuckDuckGoSearchRun tool from the langchain_community.tools 

# DuckDuckGoSearchRun:
# It is a pre-built tool provided by LangChain for performing searches using the DuckDuckGo search engine.
# DuckDuckGo is a privacy-focused search engine known for not tracking user activity.

# Purpose:
# The primary purpose of importing this tool is to enable the agent or application to perform internet searches 
# and handle queries that require information retrieval from the internet using DuckDuckGo

from langchain.agents import initialize_agent,AgentType

# initialize_agent:
# A function provided by LangChain for setting up an agent that can interact with various tools and perform tasks.

# AgentType:
# A class that defines different types of agents available in LangChain.


from langchain.callbacks import StreamlitCallbackHandler

# This code imports the StreamlitCallbackHandler from LangChain, which is a tool used to show live updates of what
#  a LangChain agent is doing directly in a Streamlit app.



import os
from dotenv import load_dotenv

## Arxiv and wikipedia Tools
arxiv_wrapper=ArxivAPIWrapper(top_k_results=1, doc_content_chars_max=200)

# This initializes the ArxivAPIWrapper class, which is used to interact with the Arxiv API and fetch research papers.
# Parameters:
# top_k_results=1: Specifies that only the top result should be returned from the Arxiv query.
# doc_content_chars_max=250: Limits the number of characters in the content of each document returned to 250 characters. 
# This is often used to limit the amount of content you want to process or display.


arxiv=ArxivQueryRun(api_wrapper=arxiv_wrapper)

# This creates an ArxivQueryRun instance (arxiv), which is a tool that uses the ArxivAPIWrapper to run queries on Arxiv.
#  This allows you to query the Arxiv database for papers and retrieve results.
# The ArxivQueryRun tool encapsulates the functionality of the API wrapper, making it easy to interact with Arxiv from
#  within a LangChain agent.


api_wrapper=WikipediaAPIWrapper(top_k_results=1,doc_content_chars_max=200)

# This initializes a WikipediaAPIWrapper, which acts as the underlying API utility for querying Wikipedia.
# Parameters:
# top_k_results=1: Specifies that only the top result from the Wikipedia query should be returned.
# doc_content_chars_max=250: Limits the number of characters in the content of each result to 250 characters. This is 
# useful for summarization or concise answers.

wiki=WikipediaQueryRun(api_wrapper=api_wrapper)
# This creates a Wikipedia query tool (wiki) by wrapping the api_wrapper_wiki. The WikipediaQueryRun tool uses the API
#  wrapper to execute queries on Wikipedia and fetch results.


# Creating DuckDuckGoSearchRun tool->It is a pre-built tool provided by LangChain for performing searches using the
#  DuckDuckGo search engine

# This code creates an instance of DuckDuckGoSearchRun, which is a LangChain tool for performing web searches 
# using the DuckDuckGo search engine.
search=DuckDuckGoSearchRun(name="Search")

# The tool is initialized with the name "Search", which acts as its identifier when used in workflows like agents.


# The purpose of this code is to enable a LangChain application (like a chatbot or an agent) to:
# Query the DuckDuckGo search engine to retrieve information from the web.
# Use the retrieved data to answer user queries or enhance its responses.
# How It’s Used:
# It acts as a tool in a LangChain agent, allowing the agent to fetch real-time information from the internet.


# Giving title to our stramlit app 
st.title("🔎 LangChain - Chat with search")
"""
In this example, we're using `StreamlitCallbackHandler` to display the thoughts and actions of an agent in an interactive Streamlit app.
Try more LangChain 🤝 Streamlit Agent examples at [github.com/langchain-ai/streamlit-agent](https://github.com/langchain-ai/streamlit-agent).
"""


## Creating Sidebar for settings
st.sidebar.title("Settings")
api_key=st.sidebar.text_input("Enter your Groq API Key:",type="password")


if "messages" not in st.session_state:
    st.session_state["messages"]=[
        {"role":"assisstant","content":"Hi,I'm a chatbot who can search the web. How can I help you?"}
    ]

# if "messages" not in st.session_state:
# Purpose: Checks if the messages key exists in st.session_state.
# st.session_state: A Streamlit object that persists variables across user interactions within the app.
# If messages is not present, it means this is the first time the app is being used in the session, so we
#  initialize it.

# st.session_state["messages"] = [
    # {"role": "assistant", "content": "Hi, I'm a chatbot who can search the web. How can I help you?"}]
# Purpose: Creates a list with one entry, representing the assistant's initial message in the conversation.
# Structure:
# role: Identifies the sender of the message (assistant in this case).
# content: The text of the assistant's message.


# Why Is This Used?

# Conversation History:
# Maintains a list of all messages (user and assistant) exchanged during the session.
# Allows the app to display the chat history to the user.

# State Management:
# Ensures that the app's chat history persists as the user interacts with it.
# Without this initialization, the app wouldn’t know how to handle the conversation flow.


# This code iterates through the stored conversation messages in st.session_state.messages and displays each
#  message in the Streamlit app's chat interface.
for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg['content'])

# for msg in st.session_state.messages:
# Purpose: Loops through each message stored in st.session_state.messages.
# st.session_state.messages is a list of dictionaries, where each dictionary represents a message in the chat
#  history.
# Each message has:
# role: Specifies who sent the message ("user" or "assistant").
# content: The text of the message.

# st.chat_message(msg["role"]).write(msg['content'])
# Purpose: Displays each message in the chat interface based on its role.

# Components:
# st.chat_message(role):
# Creates a chat message block in the Streamlit app.
# role: Determines the appearance of the message:
# "user": Displays the message as if sent by the user.
# "assistant": Displays the message as if sent by the chatbot.
# .write(content):
# Writes the actual content of the message in the chat block.

# Why Is This Used?
# Rendering Chat History:
# Ensures all previous messages (from both the user and the assistant) are displayed in the app.
# Gives users a visual record of their conversation.
# Dynamic Updates:
# As new messages are added to st.session_state.messages, they are dynamically displayed in the chat interface.


# This code snippet handles user input in a Streamlit chat application. It captures the user's question or prompt, 
# updates the chat history, and displays the input in the chat interface.

if prompt:=st.chat_input(placeholder="What is machine learning?"):
    st.session_state.messages.append({"role":"user","content":prompt})
    st.chat_message("user").write(prompt)

# if prompt := st.chat_input(placeholder="What is machine learning?"):
# st.chat_input(...): Displays a text input box in the Streamlit app for the user to type a message.
# placeholder: Text displayed in the input box as a hint before the user types anything.
# "What is machine learning?": This is the placeholder text prompting the user to ask a question.
# if prompt := ...:
# Captures the user's input and assigns it to the variable prompt.
# The := (walrus operator) is used to assign and check the input in a single line.
# If the user provides input, the condition evaluates to True, and the block of code inside the if statement 
# executes.

# st.session_state.messages.append({"role": "user", "content": prompt})
# Purpose: Adds the user's input as a new entry in the st.session_state.messages list, which stores the 
# conversation history.
# {"role": "user", "content": prompt}:
# role: "user": Indicates this message was sent by the user.
# content: prompt: Stores the user's input (the text they typed).

# st.chat_message("user").write(prompt)
# Purpose: Displays the user's message in the chat interface immediately after it is sent.
# Components:
# st.chat_message("user"): Creates a chat message block styled to represent the user's message.
# .write(prompt): Writes the user's input text into the chat message block.



# How It Works Together
# User Interaction:
# The user types a message in the st.chat_input box (e.g., "What is deep learning?").
# The input is captured in the prompt variable.

# Updating State:
# The input is appended to st.session_state.messages, adding it to the conversation history:
# {"role": "user", "content": "What is deep learning?"}

# Displaying Input:
# The message is immediately shown in the chat interface under the user's role.

# Sets up the chatbot's core language model (LLM) that generates responses to user inputs.
    llm=ChatGroq(groq_api_key=api_key,model_name="Llama3-8b-8192",streaming=True)
# streaming=True:
# Enables streaming output, meaning the response is generated and displayed in real-time, word-by-word, as the 
# model processes the input.

# Creates a list of tools that the language model can use to enhance its capabilities.
    tools=[search,arxiv,wiki]

# This code initializes a LangChain agent named search_agent 
    search_agent=initialize_agent(tools,llm,agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,handling_parsing_errors=True)

# Tools: The tools list includes utilities like search, arxiv, and wiki. These tools allow the agent to interact
#  with external APIs or functionalities for retrieving specific information.

# LLM (Language Model): The llm is the core model (ChatGroq in this case) used to generate responses and interact 
# with the tools.

# The agent type AgentType.ZERO_SHOT_REACT_DESCRIPTION means the agent operates in a "zero-shot" reasoning mode. 
# Here's a clearer explanation:
# Zero-shot reasoning: The agent does not need prior training or examples for specific tasks. Instead, it 
# dynamically decides how to respond based on the input and the descriptions of the tools available.
# It reacts in real time, understanding the context and acting accordingly.



# Error Handling: The handling_parsing_errors=True option ensures the agent can gracefully manage and recover
#  from any parsing errors that may occur while processing tool outputs.


# This block of code integrates the agent's responses into the Streamlit chat interface, enabling dynamic and
#  interactive conversations
    with st.chat_message("assistant"):
        st_cb=StreamlitCallbackHandler(st.container(),expand_new_thoughts=False)
        response=search_agent.run(st.session_state.messages,callbacks=[st_cb])
        st.session_state.messages.append({'role':'assistant',"content":response})
        st.write(response)

# with st.chat_message("assistant"):
# Creates a chat message bubble for the assistant within the Streamlit interface. All subsequent content under 
# this block will be displayed as part of the assistant's message.

# st_cb = StreamlitCallbackHandler(st.container(), expand_new_thoughts=False)

# StreamlitCallbackHandler is responsible for displaying the reasoning process and intermediate actions taken by 
# the agent in real-time.
# It uses a Streamlit container to show these updates.

# st.container(): A Streamlit container where the intermediate thoughts and actions of the agent will be displayed.

# The expand_new_thoughts=False parameter ensures new reasoning steps or thoughts do not automatically expand in
#  the interface, keeping the display concise.

# response = search_agent.run(st.session_state.messages, callbacks=[st_cb])
# Executes the search_agent with the user's conversation history (st.session_state.messages) as input.
# The StreamlitCallbackHandler (st_cb) is passed as a callback to display the agent's reasoning and actions
#  during execution in real-time.


# st.session_state.messages.append({'role':'assistant', 'content':response})
# Appends the assistant's response to the conversation history stored in st.session_state.messages. This ensures 
# the entire conversation is preserved for further context in subsequent interactions.

# st.write(response)
# Displays the assistant's response in the Streamlit interface as a message within the assistant's chat bubble.


# cd "9 Search Engine With Langchain Tools And Agents"
# streamlit run app.py 