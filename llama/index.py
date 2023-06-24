from core.lifecycle import Lifecycle
from llama.context import ServiceContextManager


class IndexManager(Lifecycle):

    def __init__(self, context_manager: [ServiceContextManager]):
        super().__init__()
        self.index = None
        self.context_manager = context_manager

    def get_index(self):
        if not self.lifecycle_state.is_started():
            raise Exception("Lifecycle state is not correct")
        return self.index
