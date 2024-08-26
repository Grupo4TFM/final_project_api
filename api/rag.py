
############################################################################
# Imports
############################################################################

from dotenv import load_dotenv
load_dotenv()
from llama_index.core import GPTVectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage,Settings
import logging
import sys
import os
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI
from llama_index.core.node_parser import SentenceSplitter


############################################################################
# Logging
############################################################################

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))
data_dir="./api/data"
persist_dir="./api/storage"

############################################################################
# Loading data from data folder and store the index
############################################################################

def tfm_load_data():
     # loop through all the contents of folder and delete file
    for filename in os.listdir(persist_dir):
        # remove the file
        os.remove(f"{persist_dir}/{filename}")
        index = None
    documents = SimpleDirectoryReader(data_dir).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir)
    return index


############################################################################
# Loading data with settings
############################################################################

def tfm_load_data_with_parameters(llm_model="gpt-4",embedding_model="text-embedding-3-small",embed_batch_size=100,chunk_size=1024,chunk_overlap=20):

    print("################# parameters")
    # llm
    Settings.llm = OpenAI(model=llm_model, temperature=0.1)

    # Embeddings
    Settings.embed_model = OpenAIEmbedding(
    # model="text-embedding-3-small", embed_batch_size=100
    model=embedding_model, embed_batch_size=embed_batch_size
    )

    # text splitter
    Settings.chunk_size = chunk_size
    Settings.chunk_overlap = chunk_overlap

    # loop through all the contents of folder and delete file
    for filename in os.listdir(persist_dir):
        # remove the file
        os.remove(f"{persist_dir}/{filename}")
        index = None

    documents = SimpleDirectoryReader(data_dir).load_data()
    index = GPTVectorStoreIndex.from_documents(documents)
    index.storage_context.persist(persist_dir)
    return index

############################################################################
# Reading the data from Storage
############################################################################

def tfm_read_from_storage():
    storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
    return load_index_from_storage(storage_context)


############################################################################
# Llama Q/A 
############################################################################

def tfm_rag_llama(question):

    if os.path.exists(persist_dir):
        index = tfm_read_from_storage()
    else:
        index = tfm_load_data(data_dir, persist_dir)

    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    
    return response


if __name__ == '__main__':
    pass



