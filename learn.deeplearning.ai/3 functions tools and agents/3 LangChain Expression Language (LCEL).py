https://learn.deeplearning.ai/courses/functions-tools-agents-langchain/lesson/ktw95/langchain-expression-language-(lcel)

LangChain Expression Language (LCEL)

import os
import openai
​
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
openai.api_key = os.environ['OPENAI_API_KEY']

#!pip install pydantic==1.10.8

from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain.schema.output_parser import StrOutputParser
Simple Chain

prompt = ChatPromptTemplate.from_template(
    "tell me a short joke about {topic}"
)
model = ChatOpenAI()
output_parser = StrOutputParser()

chain = prompt | model | output_parser

chain.invoke({"topic": "bears"})
More complex chain
And Runnable Map to supply user-provided inputs to the prompt.

from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import DocArrayInMemorySearch

vectorstore = DocArrayInMemorySearch.from_texts(
    ["harrison worked at kensho", "bears like to eat honey"],
    embedding=OpenAIEmbeddings()
)
retriever = vectorstore.as_retriever()

retriever.get_relevant_documents("where did harrison work?")

retriever.get_relevant_documents("what do bears like to eat")

template = """Answer the question based only on the following context:
{context}
​
Question: {question}
"""
prompt = ChatPromptTemplate.from_template(template)

from langchain.schema.runnable import RunnableMap

chain = RunnableMap({
    "context": lambda x: retriever.get_relevant_documents(x["question"]),
    "question": lambda x: x["question"]
}) | prompt | model | output_parser

chain.invoke({"question": "where did harrison work?"})

inputs = RunnableMap({
    "context": lambda x: retriever.get_relevant_documents(x["question"]),
    "question": lambda x: x["question"]
})

inputs.invoke({"question": "where did harrison work?"})
Bind
and OpenAI Functions

functions = [
    {
      "name": "weather_search",
      "description": "Search for weather given an airport code",
      "parameters": {
        "type": "object",
        "properties": {
          "airport_code": {
            "type": "string",
            "description": "The airport code to get the weather for"
          },
        },
        "required": ["airport_code"]
      }
    }
  ]

prompt = ChatPromptTemplate.from_messages(
    [
        ("human", "{input}")
    ]
)
model = ChatOpenAI(temperature=0).bind(functions=functions)

runnable = prompt | model

runnable.invoke({"input": "what is the weather in sf"})

functions = [
    {
      "name": "weather_search",
      "description": "Search for weather given an airport code",
      "parameters": {
        "type": "object",
        "properties": {
          "airport_code": {
            "type": "string",
            "description": "The airport code to get the weather for"
          },
        },
        "required": ["airport_code"]
      }
    },
        {
      "name": "sports_search",
      "description": "Search for news of recent sport events",
      "parameters": {
        "type": "object",
        "properties": {
          "team_name": {
            "type": "string",
            "description": "The sports team to search for"
          },
        },
        "required": ["team_name"]
      }
    }
  ]

model = model.bind(functions=functions)

runnable = prompt | model

runnable.invoke({"input": "how did the patriots do yesterday?"})
Fallbacks

from langchain.llms import OpenAI
import json
Note: Due to the deprication of OpenAI's model text-davinci-001 on 4 January 2024, you'll be using OpenAI's recommended replacement model gpt-3.5-turbo-instruct instead.

simple_model = OpenAI(
    temperature=0, 
    max_tokens=1000, 
    model="gpt-3.5-turbo-instruct"
)
simple_chain = simple_model | json.loads

challenge = "write three poems in a json blob, where each poem is a json blob of a title, author, and first line"

simple_model.invoke(challenge)
Note: The next line is expected to fail.

simple_chain.invoke(challenge)

model = ChatOpenAI(temperature=0)
chain = model | StrOutputParser() | json.loads

chain.invoke(challenge)

final_chain = simple_chain.with_fallbacks([chain])

final_chain.invoke(challenge)
Interface

prompt = ChatPromptTemplate.from_template(
    "Tell me a short joke about {topic}"
)
model = ChatOpenAI()
output_parser = StrOutputParser()
​
chain = prompt | model | output_parser

chain.invoke({"topic": "bears"})

chain.batch([{"topic": "bears"}, {"topic": "frogs"}])

for t in chain.stream({"topic": "bears"}):
    print(t)

response = await chain.ainvoke({"topic": "bears"})
response