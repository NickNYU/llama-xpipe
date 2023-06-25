import os
from dotenv import load_dotenv
from llama_index import SimpleDirectoryReader
from llama_index.node_parser import SimpleNodeParser
from llama_index.data_structs.node import Node, DocumentRelationship
from llama_index import VectorStoreIndex
from llama_index import LLMPredictor, VectorStoreIndex, ServiceContext
from langchain.llms import AzureOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from llama_index import LangchainEmbedding, ServiceContext
from llama_index import StorageContext, load_index_from_storage

import logging
import sys


load_dotenv()
logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG
)  # logging.DEBUG for more verbose output
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))


def main():
    documents = SimpleDirectoryReader("./data").load_data()

    # index = VectorStoreIndex.from_documents(documents)

    # parser = SimpleNodeParser()
    # nodes = parser.get_nodes_from_documents(documents)
    # index = VectorStoreIndex(nodes)

    # define embedding
    embedding = LangchainEmbedding(OpenAIEmbeddings(chunk_size=1))
    # define LLM
    llm_predictor = LLMPredictor(
        llm=AzureOpenAI(
            engine="text-davinci-003",
            model_name="text-davinci-003",
        )
    )

    # configure service context
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor, embed_model=embedding
    )

    # build index
    index = VectorStoreIndex.from_documents(
        documents,
        service_context=service_context,
    )

    index.storage_context.persist(persist_dir="./dataset")
    storage_context = StorageContext.from_defaults(persist_dir="./dataset")
    index = load_index_from_storage(
        storage_context=storage_context, service_context=service_context
    )

    # index.vector_store.persist("./dataset")
    # query with embed_model specified
    query_engine = index.as_query_engine(
        retriever_mode="embedding", verbose=True, service_context=service_context
    )
    response = query_engine.query("请帮忙推荐一杯咖啡给我，我喜欢咖啡因")
    print(response)


if __name__ == "__main__":
    main()
