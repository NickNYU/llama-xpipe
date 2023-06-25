from core.lifecycle import Lifecycle
from llama.context import ServiceContextManager
from llama_index.indices.vector_store import VectorStoreIndex
from typing import Optional


class IndexManager(Lifecycle):
    index: Optional[VectorStoreIndex]

    def __init__(self, context_manager: ServiceContextManager) -> None:
        super().__init__()
        self.index = None
        self.context_manager = context_manager

    def get_index(self) -> Optional[VectorStoreIndex]:
        if not self.lifecycle_state.is_started():
            raise Exception("Lifecycle state is not correct")
        return self.index
