<p align="center">
    <a href="https://discord.gg/6p3fD6rBVm">
        <img alt="Discord" src="https://img.shields.io/discord/1146610656779440188?logo=discord&style=flat&logoColor=white"/>
    </a>
    <a href="README_ZH.md"><img src="https://img.shields.io/badge/文档-中文版-white.svg" alt="ZH doc"/></a>
    <img src="https://img.shields.io/static/v1?label=license&message=MIT&color=white&style=flat" alt="License"/>
</p>

# A fse vectorstore for langchain
fsevector is a vectorstore python library for langchain based on fse and postgres. it provides vector storage function, vector retrieval.

One of the most common ways to store and search over unstructured data is to embed it and store the resulting embedding vectors, and then at query time to embed the unstructured query and retrieve the embedding vectors that are 'most similar' to the embedded query. A vector store takes care of storing embedded data and performing vector search for you.

## Installation
### Deploy postgres and fse
```
Before using fsevector, you need to deploy postgres and fse services (it is recommended to install the DeepEngine of deepglint).

```

#### Trial environment
```
call interface with fsedoc_connection_string and fseaddr_connection_string
fsedoc_connection_string="fsedoc://fsevector:test1234@192.168.3.111:24049"
fseaddr_connection_string="fseaddr://192.168.3.111:3154"

or add the following environment variables
export FSEDOC_CONNECTION_STRING="fsedoc://fsevector:test1234@192.168.3.111:24049"
export FSEADDR_CONNECTION_STRING="fseaddr://192.168.3.111:3154"
```

### Install fsevector
```console
pip install fsevector
```

## Documentation
More information can be found on the [examples](https://gitlab.deepglint.com/chenbo/fsevector/-/tree/main/examples)

## Usage
### Instructions for use
```
When using fsevector, you need the following steps:
1. Enter fsedoc_connection_string and fseaddr_connection_string in the following call example or add environment variables.
2. Add OpenAI-related environment variables.
```

### Example
```python
import openai
from langchain.chat_models import AzureChatOpenAI
from langchain.chains import RetrievalQAWithSourcesChain
from langchain.embeddings import OpenAIEmbeddings
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import Document

from fsevector.fsevector import FseVector

openai.api_key = os.environ["OPENAI_API_KEY"]
openai.api_base = os.environ["OPENAI_API_BASE"]
openai.api_version = os.environ["OPENAI_API_VERSION"]
openai.api_type = os.environ["OPENAI_API_TYPE"]

#init fseVector
embeddings = OpenAIEmbeddings(model="text-embedding-ada-002")
fseVector = FseVector(fsedoc_connection_string="fsedoc://username:passwd@ip:port",
                      fseaddr_connection_string="fseaddr://ip:port",
                      embedding_function=embeddings,
                      collection_name="knowledge_test")

#init chain
DEPLOYMENT_NAME = "gpt-35-turbo"  # gpt-35-turbo gpt-35-turbo-16k
llm = AzureChatOpenAI(deployment_name=DEPLOYMENT_NAME)
chain = RetrievalQAWithSourcesChain.from_chain_type(llm=llm,
                                chain_type="stuff", verbose=False, memory=None,
                                retriever=fseVector.as_retriever(search_type='similarity_score_threshold',
                                                                search_kwargs={'score_threshold': 0.3, 'k': 3}),
                                return_source_documents=False)

#add doc or texts
fseVector.add_texts(texts=['trigger phrases: "get emails", "send emails", "send an email", "email"\n## (Mac) Get emails\nExecute the following AppleScript command to get the content of the last X (in this case, 3) emails from the Mail application:\ntell application "Mail" to get content of messages 1 through 3 of inbox\n## (Mac) Send emails\nUse Applescript.'], metadatas=[{"source": "email.txt", "key_list": ["emails", "get emails"]}])  

#retrieval
result = chain({"question": 'get emails'})
output = f"Answer: {result['answer']}\nSources: {result['sources']}\nresult: {result}"
print(output)        
```

### Other init fsevector methods
```python
#from_index
embeddings = OpenAIEmbeddings()
fseVector = FseVector.from_index(
                    fsedoc_connection_string="fsedoc://username:passwd@ip:port",
                    fseaddr_connection_string="fseaddr://ip:port",
                    collection_name="knowledge_test",
                    embedding=embeddings)

#from_texts
embeddings = OpenAIEmbeddings()
fseVector = FseVector.from_texts(
                    fsedoc_connection_string="fsedoc://username:passwd@ip:port",
                    fseaddr_connection_string="fseaddr://ip:port",
                    collection_name="knowledge_test",
                    texts=["teststssss"],
                    embedding=embeddings,
                    metadatas=[{"source": "teststssss"}],
                    ids=[str(11111)],
                    pre_delete_collection=True)

#from_documents
ids=[11]
embeddings = OpenAIEmbeddings()
doc=[Document(page_content="xxxx", metadata={"source": "teststssss","key_list":["emails", "get emails"]})]
fseVector = FseVector.from_documents(
                    fsedoc_connection_string="fsedoc://username:passwd@ip:port",
                    fseaddr_connection_string="fseaddr://ip:port",
                    collection_name="knowledge_test",
                    documents=doc,
                    embedding=embeddings, ids=ids)

#from_embeddings
embeddings = OpenAIEmbeddings()
text_embeddings = embeddings.embed_documents(texts)
text_embedding_pairs = list(zip(texts, text_embeddings))
fseVector = FseVector.from_embeddings(
                    fsedoc_connection_string="fsedoc://username:passwd@ip:port",
                    fseaddr_connection_string="fseaddr://ip:port",
                    collection_name="knowledge_test",
                    text_embeddings=text_embedding_pairs,
                    embedding=embeddings)
```

### Supported interface
```
from_documents
from_texts
from_embeddings
from_index
add_embeddings
add_texts
similarity_search
similarity_search_with_score
similarity_search_with_score_by_vector
similarity_search_by_vector
```

## Development
- CI pipeline
