from llama_index import ServiceContext, LLMPredictor, LangchainEmbedding
from type import Optional
from core.lifecycle import Lifecycle
from langchain.manager import BaseLangChainManager


class ServiceContextManager(Lifecycle):
    service_context: Optional[ServiceContext]

    def __init__(self, manager: BaseLangChainManager) -> None:
        super().__init__()
        self.manager = manager
        self.service_context = None

    def get_service_context(self) -> ServiceContext:
        if self.lifecycle_state.is_started():
            raise KeyError(
                "incorrect lifecycle state: {}".format(self.lifecycle_state.phase)
            )
        if self.service_context is None:
            raise ValueError(
                "service context is not ready, check for lifecycle statement"
            )
        return self.service_context

    def do_init(self) -> None:
        # define embedding
        embedding = LangchainEmbedding(self.manager.get_embedding())
        # define LLM
        llm_predictor = LLMPredictor(llm=self.manager.get_llm())
        # configure service context
        self.service_context = ServiceContext.from_defaults(
            llm_predictor=llm_predictor, embed_model=embedding
        )

    def do_start(self) -> None:
        pass

    def do_stop(self) -> None:
        pass

    def do_dispose(self) -> None:
        pass


class StorageContextManager(Lifecycle):
    def __init__(self, dataset_path: Optional[str] = "./dataset") -> None:
        super().__init__()
        self.dataset_path = dataset_path

    def do_init(self) -> None:
        pass

    def do_start(self) -> None:
        pass

    def do_stop(self) -> None:
        pass

    def do_dispose(self) -> None:
        pass
