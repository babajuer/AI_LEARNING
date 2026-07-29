https://learn.deeplearning.ai/courses/langchain-chat-with-your-data/lesson/snbj5/document-loading
Document Loading
Note to students.
During periods of high load you may find the notebook unresponsive. It may appear to execute a cell, update the completion number in brackets [#] at the left of the cell but you may find the cell has not executed. This is particularly obvious on print statements when there is no output. If this happens, restart the kernel using the command under the Kernel tab.
Retrieval augmented generation
In retrieval augmented generation (RAG), an LLM retrieves contextual documents from an external dataset as part of its execution.
This is useful if we want to ask question about specific documents (e.g., our PDFs, a set of videos, etc).
overview.jpeg

#! pip install langchain

import os
import openai
import sys
sys.path.append('../..')
​
from dotenv import load_dotenv, find_dotenv
_ = load_dotenv(find_dotenv()) # read local .env file
​
openai.api_key  = os.environ['OPENAI_API_KEY']
PDFs
Let's load a PDF transcript from Andrew Ng's famous CS229 course! These documents are the result of automated transcription so words and sentences are sometimes split unexpectedly.

# The course will show the pip installs you would need to install packages on your own machine.
# These packages are already installed on this platform and should not be run again.
#! pip install pypdf 

from langchain.document_loaders import PyPDFLoader
loader = PyPDFLoader("docs/cs229_lectures/MachineLearning-Lecture01.pdf")
pages = loader.load()
Each page is a Document.
A Document contains text (page_content) and metadata.

len(pages)

page = pages[0]

print(page.page_content[0:500])

page.metadata
YouTube

from langchain.document_loaders.generic import GenericLoader,  FileSystemBlobLoader
from langchain.document_loaders.parsers import OpenAIWhisperParser
from langchain.document_loaders.blob_loaders.youtube_audio import YoutubeAudioLoader

# ! pip install yt_dlp
# ! pip install pydub
Note: This can take several minutes to complete. This has been modified relative to the lesson video to fetch the video file locally.

url="https://www.youtube.com/watch?v=jGwO_UgTS7I"
save_dir="docs/youtube/"
loader = GenericLoader(
    #YoutubeAudioLoader([url],save_dir),  # fetch from youtube
    FileSystemBlobLoader(save_dir, glob="*.m4a"),   #fetch locally
    OpenAIWhisperParser()
)
docs = loader.load()

docs[0].page_content[0:500]
URLs

from langchain.document_loaders import WebBaseLoader
​
loader = WebBaseLoader("https://github.com/basecamp/handbook/blob/master/titles-for-programmers.md")
Note: the URL sent to the WebBaseLoader differs from the one shonw in the video because for 2024 it was updated.

docs = loader.load()

print(docs[0].page_content[:500])
Notion
Follow steps here for an example Notion site such as this one:
Duplicate the page into your own Notion space and export as Markdown / CSV.
Unzip it and save it as a folder that contains the markdown file for the Notion page.
image.png

from langchain.document_loaders import NotionDirectoryLoader
loader = NotionDirectoryLoader("docs/Notion_DB")
docs = loader.load()

print(docs[0].page_content[0:200])

docs[0].metadata