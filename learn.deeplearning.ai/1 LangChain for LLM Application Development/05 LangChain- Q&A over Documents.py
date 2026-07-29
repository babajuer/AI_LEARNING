# https://learn.deeplearning.ai/courses/langchain/lesson/mv7m1/question-and-answer

# LangChain: Q&A over Documents
# An example might be a tool that would allow you to query a product catalog for items of interest.

#pip install --upgrade langchain
import os

from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
Note: LLM's do not always produce the same results. When executing the code in your notebook, you may get slightly different answers that those in the video.

# account for deprecation of LLM model
import datetime
# Get the current date
current_date = datetime.datetime.now().date()

# Define the date after which the model should be set to "gpt-3.5-turbo"
target_date = datetime.date(2024, 6, 12)

# Set the model variable based on the current date
if current_date > target_date:
    llm_model = "gpt-3.5-turbo"
else:
    llm_model = "gpt-3.5-turbo-0301"
from langchain.chains import RetrievalQA
from langchain.chat_models import ChatOpenAI
from langchain.document_loaders import CSVLoader
from langchain.vectorstores import DocArrayInMemorySearch
from IPython.display import display, Markdown
from langchain.llms import OpenAI
file = 'OutdoorClothingCatalog_1000.csv'
loader = CSVLoader(file_path=file)
from langchain.indexes import VectorstoreIndexCreator
#pip install docarray
index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch
).from_loaders([loader])
query ="Please list all your shirts with sun protection \
in a table in markdown and summarize each one."
Note:

The notebook uses langchain==0.0.179 and openai==0.27.7
For these library versions, VectorstoreIndexCreator uses text-davinci-003 as the base model, which has been deprecated since 1 January 2024.
The replacement model, gpt-3.5-turbo-instruct will be used instead for the query.
The response format might be different than the video because of this replacement model.
llm_replacement_model = OpenAI(temperature=0, 
                               model='gpt-3.5-turbo-instruct')

response = index.query(query, 
                       llm = llm_replacement_model)
display(Markdown(response))
Step By Step
from langchain.document_loaders import CSVLoader
loader = CSVLoader(file_path=file)
docs = loader.load()
docs[0]
from langchain.embeddings import OpenAIEmbeddings
embeddings = OpenAIEmbeddings()
embed = embeddings.embed_query("Hi my name is Harrison")
print(len(embed))
print(embed[:5])
db = DocArrayInMemorySearch.from_documents(
    docs, 
    embeddings
)
query = "Please suggest a shirt with sunblocking"
docs = db.similarity_search(query)
len(docs)
docs[0]
retriever = db.as_retriever()
llm = ChatOpenAI(temperature = 0.0, model=llm_model)
qdocs = "".join([docs[i].page_content for i in range(len(docs))])
response = llm.call_as_llm(f"{qdocs} Question: Please list all your \
shirts with sun protection in a table in markdown and summarize each one.") 
display(Markdown(response))
qa_stuff = RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=retriever, 
    verbose=True
)
query =  "Please list all your shirts with sun protection in a table \
in markdown and summarize each one."
response = qa_stuff.run(query)
display(Markdown(response))
response = index.query(query, llm=llm)
index = VectorstoreIndexCreator(
    vectorstore_cls=DocArrayInMemorySearch,
    embedding=embeddings,
).from_loaders([loader])