
############################################################################
# Imports
############################################################################

from llama_index.core import (
    VectorStoreIndex,
    SimpleDirectoryReader,
)
from dotenv import load_dotenv
import logging
import sys

############################################################################
# Loading variables
############################################################################

load_dotenv()

############################################################################
# Logging
############################################################################

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

############################################################################
# Loading data from data folder
############################################################################

documents = SimpleDirectoryReader("data").load_data()

############################################################################
# Vector creation
############################################################################

index = VectorStoreIndex.from_documents(documents)

############################################################################
# Creation of the query engine
############################################################################

query_engine = index.as_query_engine()



