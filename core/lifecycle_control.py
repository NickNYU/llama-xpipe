from abc import ABC, abstractmethod


class LifecycleState(ABC):
    @abstractmethod
    def is_initializable(self) -> bool:
        pass

    @abstractmethod
    def is_startable(self) -> bool:
        pass

    @abstractmethod
    def is_stoppable(self) -> bool:
        pass

    @abstractmethod
    def is_disposable(self) -> bool:
        pass

class LifecycleAware(ABC):
    @abstractmethod
    def get_lifecycle_state(self) -> LifecycleState:
        pass