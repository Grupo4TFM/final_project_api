
############################################################################
# Imports
############################################################################

from dotenv import load_dotenv
load_dotenv()
from llama_index.core import GPTVectorStoreIndex, SimpleDirectoryReader, StorageContext, load_index_from_storage
import logging
import sys
import os


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
    index = None
    if os.path.exists(persist_dir):
        index = tfm_read_from_storage()
    else:
        index = tfm_load_data(data_dir, persist_dir)

    query_engine = index.as_query_engine()
    response = query_engine.query(question)
    
    return response


if __name__ == '__main__':
    pass



