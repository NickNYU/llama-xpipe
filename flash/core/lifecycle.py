from abc import ABC, abstractmethod, ABCMeta

from core.lifecycle_control import LifecycleAware
import atomic


class Initializable(ABC):

    @abstractmethod
    def initialize(self) -> None:
        pass

class Startable(ABC):
    @abstractmethod
    def start(self) -> None:
        pass


class Stoppable(ABC):

    @abstractmethod
    def stop(self) -> None:
        pass


class Disposable(ABC):

    @abstractmethod
    def dispose(self) -> None:
        pass

class Lifecycle(ABC, Initializable, Startable, Stoppable, Disposable, LifecycleAware):
    pass

class LiteLifecycle(ABC, Startable, Stoppable):

    def __init__(self):


    def start(self) -> None:

