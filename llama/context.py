from llama_index import ServiceContext, LLMPredictor, LangchainEmbedding

from core.lifecycle import Lifecycle
from langchain.manager import LangChainManager


class ServiceContextManager(Lifecycle):

    def __init__(self, manager: [LangChainManager]):
        super().__init__()
        self.manager = manager
        self.service_context = None

    def get_service_context(self) -> ServiceContext:
        if self.lifecycle_state.is_started():
            raise Exception("incorrect lifecycle state: {}".format(self.get_lifecycle_state()))
        return self.service_context

    def do_init(self):
        # define embedding
        embedding = LangchainEmbedding(self.manager.get_embedding())
        # define LLM
        llm_predictor = LLMPredictor(llm=self.manager.get_llm())
        # configure service context
        self.service_context = ServiceContext.from_defaults(llm_predictor=llm_predictor, embed_model=embedding)

    def do_start(self):
        pass

    def do_stop(self):
        pass

    def do_dispose(self):
        pass


class StorageContextManager(Lifecycle):

    def __init__(self, dataset_path: [str] = './dataset'):
        super().__init__()
        self.dataset_path = dataset_path

    def do_init(self):
        pass

    def do_start(self):
        pass

    def do_stop(self):
        pass

    def do_dispose(self):
        pass
