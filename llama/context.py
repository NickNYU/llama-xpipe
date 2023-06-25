from abc import abstractmethod, ABC

from llama_index import ServiceContext, LLMPredictor, LangchainEmbedding, Document
from llama_index import StorageContext
from typing import List

from core.lifecycle import Lifecycle
from langchain_manager.manager import BaseLangChainManager


class ServiceContextManager(Lifecycle, ABC):
    @abstractmethod
    def get_service_context(self) -> ServiceContext:
        pass


class AzureServiceContextManager(ServiceContextManager):
    lc_manager: BaseLangChainManager
    service_context: ServiceContext

    def __init__(self, lc_manager: BaseLangChainManager):
        super().__init__()
        self.lc_manager = lc_manager

    def get_service_context(self) -> ServiceContext:
        if self.service_context is None:
            raise ValueError(
                "service context is not ready, check for lifecycle statement"
            )
        return self.service_context

    def do_init(self) -> None:
        # define embedding
        embedding = LangchainEmbedding(self.lc_manager.get_embedding())
        # define LLM
        llm_predictor = LLMPredictor(llm=self.lc_manager.get_llm())
        # configure service context
        self.service_context = ServiceContext.from_defaults(
            llm_predictor=llm_predictor, embed_model=embedding
        )

    def do_start(self) -> None:
        self.logger.info(
            "[do_start][embedding] last used usage: %d",
            self.service_context.embed_model.total_tokens_used,
        )
        self.logger.info(
            "[do_start][predict] last used usage: %d",
            self.service_context.llm_predictor.total_tokens_used,
        )

    def do_stop(self) -> None:
        self.logger.info(
            "[do_stop][embedding] last used usage: %d",
            self.service_context.embed_model.total_tokens_used,
        )
        self.logger.info(
            "[do_stop][predict] last used usage: %d",
            self.service_context.llm_predictor.total_tokens_used,
        )

    def do_dispose(self) -> None:
        self.logger.info(
            "[do_dispose] total used token: %d",
            self.service_context.llm_predictor.total_tokens_used,
        )


class StorageContextManager(Lifecycle, ABC):
    @abstractmethod
    def get_storage_context(self) -> StorageContext:
        pass


class LocalStorageContextManager(StorageContextManager):
    storage_context: StorageContext

    def __init__(
        self,
        service_context_manager: ServiceContextManager,
        dataset_path: str = "./dataset",
    ) -> None:
        super().__init__()
        self.dataset_path = dataset_path
        self.service_context_manager = service_context_manager

    def get_storage_context(self) -> StorageContext:
        return self.storage_context

    def do_init(self) -> None:
        from llama.utils import is_local_storage_files_ready

        if is_local_storage_files_ready(self.dataset_path):
            self.storage_context = StorageContext.from_defaults(
                persist_dir=self.dataset_path
            )
        else:
            docs = self._download()
            self._indexing(docs)

    def do_start(self) -> None:
        # self.logger.info("[do_start]%", **self.storage_context.to_dict())
        pass

    def do_stop(self) -> None:
        # self.logger.info("[do_stop]%", **self.storage_context.to_dict())
        pass

    def do_dispose(self) -> None:
        self.storage_context.persist(self.dataset_path)

    def _download(self) -> List[Document]:
        from llama.data_loader import GithubLoader

        loader = GithubLoader()
        return loader.load()

    def _indexing(self, docs: List[Document]) -> None:
        from llama_index import GPTVectorStoreIndex

        index = GPTVectorStoreIndex.from_documents(
            docs, service_context=self.service_context_manager.get_service_context()
        )
        index.storage_context.persist(persist_dir=self.dataset_path)
        self.storage_context = index.storage_context
