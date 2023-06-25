from llama_hub.github_repo import GithubRepositoryReader, GithubClient
from llama_index import download_loader, GPTVectorStoreIndex
from llama_index import LLMPredictor, VectorStoreIndex, ServiceContext
from langchain.llms import AzureOpenAI
from langchain.embeddings.openai import OpenAIEmbeddings
from llama_index import LangchainEmbedding, ServiceContext
from llama_index import StorageContext, load_index_from_storage
from dotenv import load_dotenv
import os
import pickle


def main() -> None:
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
    response = query_engine.query("如何使用X-Pipe?")
    print(response)


if __name__ == "__main__":
    load_dotenv()
    main()
