from abc import ABC, abstractmethod
from typing import Any

from llama_index import load_index_from_storage
from llama_index.indices.query.base import BaseQueryEngine

from core.helper import LifecycleHelper
from core.lifecycle import Lifecycle
from llama.service_context import ServiceContextManager, StorageContextManager


class XPipeWikiRobot(ABC):
    @abstractmethod
    def ask(self, question: str) -> Any:
        pass


class AzureOpenAIXPipeWikiRobot(XPipeWikiRobot):
    query_engine: BaseQueryEngine

    def __init__(self, query_engine: BaseQueryEngine) -> None:
        super().__init__()
        self.query_engine = query_engine

    def ask(self, question: str) -> Any:
        return self.query_engine.query(question).response


class XPipeWikiRobotManager(Lifecycle):
    @abstractmethod
    def get_robot(self) -> XPipeWikiRobot:
        pass


class AzureXPipeWikiRobotManager(XPipeWikiRobotManager):
    service_context_manager: ServiceContextManager
    storage_context_manager: StorageContextManager
    query_engine: BaseQueryEngine

    def __init__(
        self,
        service_context_manager: ServiceContextManager,
        storage_context_manager: StorageContextManager,
    ) -> None:
        super().__init__()
        self.service_context_manager = service_context_manager
        self.storage_context_manager = storage_context_manager

    def get_robot(self) -> XPipeWikiRobot:
        return AzureOpenAIXPipeWikiRobot(self.query_engine)

    def do_init(self) -> None:
        LifecycleHelper.initialize_if_possible(self.service_context_manager)
        LifecycleHelper.initialize_if_possible(self.storage_context_manager)

    def do_start(self) -> None:
        LifecycleHelper.start_if_possible(self.service_context_manager)
        LifecycleHelper.start_if_possible(self.storage_context_manager)
        index = load_index_from_storage(
            storage_context=self.storage_context_manager.get_storage_context(),
            service_context=self.service_context_manager.get_service_context(),
        )
        self.query_engine = index.as_query_engine(
            service_context=self.service_context_manager.get_service_context()
        )

    def do_stop(self) -> None:
        LifecycleHelper.stop_if_possible(self.storage_context_manager)
        LifecycleHelper.stop_if_possible(self.service_context_manager)

    def do_dispose(self) -> None:
        LifecycleHelper.dispose_if_possible(self.storage_context_manager)
        LifecycleHelper.dispose_if_possible(self.service_context_manager)
