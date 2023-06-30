from llama_index import StorageContext
from typing import List
from abc import abstractmethod, ABC

from llama_index import Document

from core.lifecycle import Lifecycle
from llama.service_context import ServiceContextManager


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
