from abc import abstractmethod, ABC

from langchain.base_language import BaseLanguageModel
from langchain.embeddings.base import Embeddings as LCEmbeddings
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import AzureOpenAI


class BaseLangChainManager(ABC):
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
        self.embedding = OpenAIEmbeddings(client=None, chunk_size=1)
        self.llm = AzureOpenAI(
            deployment_name="text-davinci-003",
            # model_name="text-davinci-003",
            model="text-davinci-003",
            client=None,
        )

    # Override
    def get_embedding(self) -> LCEmbeddings:
        return self.embedding

    # Override
    def get_llm(self) -> BaseLanguageModel:
        return self.llm


class LangChainHuggingFaceManager(BaseLangChainManager):
    def __init__(self) -> None:
        super().__init__()
        from transformers import AutoTokenizer, AutoModel

        AutoTokenizer.from_pretrained("GanymedeNil/text2vec-large-chinese")

        AutoModel.from_pretrained("GanymedeNil/text2vec-large-chinese")

        self.embedding = OpenAIEmbeddings(client=None, chunk_size=1)
        self.llm = AzureOpenAI(
            deployment_name="text-davinci-003",
            # model_name="text-davinci-003",
            model="text-davinci-003",
            client=None,
        )

    # Override
    def get_embedding(self) -> LCEmbeddings:
        return self.embedding

    # Override
    def get_llm(self) -> BaseLanguageModel:
        return self.llm
