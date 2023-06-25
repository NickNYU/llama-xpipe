from abc import abstractmethod, ABC

from langchain_manager.base_language import BaseLanguageModel
from langchain_manager.embeddings.base import Embeddings as LCEmbeddings
from langchain_manager.embeddings.openai import OpenAIEmbeddings
from langchain_manager.llms import AzureOpenAI

from core.lifecycle import Lifecycle


class BaseLangChainManager(Lifecycle, ABC):
    def __init__(self) -> None:
        super().__init__()

    @abstractmethod
    def get_embedding(self) -> LCEmbeddings:
        pass

    @abstractmethod
    def get_llm(self) -> BaseLanguageModel:
        pass


class LangChainAzureManager(BaseLangChainManager):
    def __init__(self) -> None:
        super().__init__()

    # Override
    def get_embedding(self) -> LCEmbeddings:
        return OpenAIEmbeddings(client=None, chunk_size=1)

    # Override
    def get_llm(self) -> BaseLanguageModel:
        return AzureOpenAI(
            deployment_name="text-davinci-003",
            # model_name="text-davinci-003",
            model="text-davinci-003",
            client=None,
        )
