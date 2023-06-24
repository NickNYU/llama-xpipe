from abc import abstractmethod, ABC

from langchain.embeddings.base import Embeddings as LCEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import AzureOpenAI
from langchain.base_language import BaseLanguageModel

from core.lifecycle import Lifecycle


class LangChainManager(Lifecycle, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_embedding(self) -> LCEmbeddings:
        pass

    @abstractmethod
    def get_llm(self) -> BaseLanguageModel:
        pass


class LangChainAzureManager(LangChainManager):

    def __init__(self):
        super().__init__()

    # Override
    def get_embedding(self) -> LCEmbeddings:
        return OpenAIEmbeddings(chunk_size=1)

    # Override
    def get_llm(self) -> BaseLanguageModel:
        return AzureOpenAI(
            engine="text-davinci-003",
            model_name="text-davinci-003",
        )
