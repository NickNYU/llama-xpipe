import enum
import os

from core.helper import LifecycleHelper
from xpipe_wiki.robot_manager import XPipeWikiRobotManager, AzureXPipeWikiRobotManager


class XPipeRobotRevision(enum.Enum):
    SIMPLE_OPENAI_VERSION_0 = 1






class XPipeRobotManagerFactory:
    """
    CAPABLE: Dict[XPipeRobotRevision, XPipeWikiRobotManager] = {XPipeRobotRevision.SIMPLE_OPENAI_VERSION_0: XPipeWikiRobotManager()}
    """
    CAPABLE = dict()
    @classmethod
    def get_or_create(cls, revision: XPipeRobotRevision) -> XPipeWikiRobotManager:
        if cls.CAPABLE.get(revision) is not None:
            return cls.CAPABLE[revision]
        if revision == XPipeRobotRevision.SIMPLE_OPENAI_VERSION_0:
            manager = cls.create_simple_openai_version_0()
        cls.CAPABLE[revision] = manager
        return manager

    @classmethod
    def create_simple_openai_version_0(cls) -> AzureXPipeWikiRobotManager:
        from llama.context import AzureServiceContextManager
        from langchain_manager.manager import LangChainAzureManager

        service_context_manager = AzureServiceContextManager(
            lc_manager=LangChainAzureManager()
        )

        from llama.context import LocalStorageContextManager

        dataset_path = os.getenv("XPIPE_WIKI_DATASET_PATH", "./dataset")
        storage_context_manager = LocalStorageContextManager(
            dataset_path=dataset_path, service_context_manager=service_context_manager
        )

        robot_manager = AzureXPipeWikiRobotManager(
            service_context_manager=service_context_manager,
            storage_context_manager=storage_context_manager,
        )
        LifecycleHelper.initialize_if_possible(robot_manager)
        LifecycleHelper.start_if_possible(robot_manager)
        return robot_manager

