from llama_hub.github_repo import GithubRepositoryReader, GithubClient
from llama_index import download_loader, GPTVectorStoreIndex
from llama_index import LLMPredictor, ServiceContext, LangchainEmbedding
from langchain.llms import AzureOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
import os
import pickle
import streamlit as st

import logging
import sys


logging.basicConfig(
    stream=sys.stdout, level=logging.DEBUG
)  # logging.DEBUG for more verbose output
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

# Sidebar contents
with st.sidebar:
    st.title("🤗💬 LLM Chat App")
    st.markdown(
        """
    ## About
    This app is an LLM-powered chatbot built using:
    - [Streamlit](https://streamlit.io/)
    - [LangChain](https://python.langchain.com/)
    - [X-Pipe](https://github.com/ctripcorp/x-pipe)
    """
    )
    # add_vertical_space(5)
    st.write("Made by Nick")


def main() -> None:
    st.header("X-Pipe Wiki 机器人 💬")
    # define embedding
    embedding = LangchainEmbedding(OpenAIEmbeddings(client=None, chunk_size=1))
    # define LLM
    llm_predictor = LLMPredictor(
        llm=AzureOpenAI(
            deployment_name="text-davinci-003",
            model="text-davinci-003",
            client=None,
        )
    )

    # configure service context
    service_context = ServiceContext.from_defaults(
        llm_predictor=llm_predictor, embed_model=embedding
    )
    download_loader("GithubRepositoryReader")
    docs = None
    if os.path.exists("docs/docs.pkl"):
        with open("docs/docs.pkl", "rb") as f:
            docs = pickle.load(f)

    if docs is None:
        github_client = GithubClient(os.getenv("GITHUB_TOKEN"))
        loader = GithubRepositoryReader(
            github_client,
            owner="ctripcorp",
            repo="x-pipe",
            filter_directories=(
                [".", "doc"],
                GithubRepositoryReader.FilterType.INCLUDE,
            ),
            filter_file_extensions=([".md"], GithubRepositoryReader.FilterType.INCLUDE),
            verbose=True,
            concurrent_requests=10,
        )

        docs = loader.load_data(branch="master")

        with open("docs/docs.pkl", "wb") as f:
            pickle.dump(docs, f)

    index = GPTVectorStoreIndex.from_documents(docs, service_context=service_context)

    query_engine = index.as_query_engine(service_context=service_context)

    query = st.text_input("X-Pipe Wiki 问题:")
    if query:
        index = GPTVectorStoreIndex.from_documents(
            docs, service_context=service_context
        )

        query_engine = index.as_query_engine(service_context=service_context)
        response = query_engine.query(query)
        st.write(response)


if __name__ == "__main__":
    main()
