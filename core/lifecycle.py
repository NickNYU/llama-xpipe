import enum
from abc import ABC, abstractmethod
from typing import TypeVar

from core import logger_factory


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


class LifecycleAware(ABC):

    def __init__(self, state):
        self.state = state

    def get_lifecycle_state(self):
        return self.state


class Lifecycle(Initializable, Startable, Stoppable, Disposable, LifecycleAware, ABC):

    def __init__(self):
        self.logger = logger_factory.get_logger(self.__class__.__name__)
        self.lifecycle_state = LifecycleState(lifecycle=self)

    def initialize(self):
        if not self.lifecycle_state.can_initialize(self.lifecycle_state.get_phase()):
            self.logger.warning("[{}]cannot initialize".format(self.__class__.__name__))
            return
        self.lifecycle_state.set_phase(LifecyclePhase.INITIALIZING)
        self.do_init()
        self.lifecycle_state.set_phase(LifecyclePhase.INITIALIZED)

    def start(self):
        if not self.lifecycle_state.can_start(self.lifecycle_state.get_phase()):
            self.logger.warning("[{}]cannot start".format(self.__class__.__name__))
            return
        self.lifecycle_state.set_phase(LifecyclePhase.STARTING)
        self.do_start()
        self.lifecycle_state.set_phase(LifecyclePhase.STARTED)

    def stop(self):
        if not self.lifecycle_state.can_stop(self.lifecycle_state.get_phase()):
            self.logger.warning("[{}]cannot stop".format(self.__class__.__name__))
            return
        self.lifecycle_state.set_phase(LifecyclePhase.STOPPING)
        self.do_stop()
        self.lifecycle_state.set_phase(LifecyclePhase.STOPPED)

    def dispose(self):
        if not self.lifecycle_state.can_dispose(self.lifecycle_state.get_phase()):
            self.logger.warning("[{}]cannot dispose".format(self.__class__.__name__))
            return
        self.lifecycle_state.set_phase(LifecyclePhase.DISPOSING)
        self.do_dispose()
        self.lifecycle_state.set_phase(LifecyclePhase.DISPOSED)

    @abstractmethod
    def do_init(self):
        pass

    @abstractmethod
    def do_start(self):
        pass

    @abstractmethod
    def do_stop(self):
        pass

    @abstractmethod
    def do_dispose(self):
        pass


class LifecyclePhase(enum.Enum):
    INITIALIZING = 1
    INITIALIZED = 2
    STARTING = 3
    STARTED = 4
    STOPPING = 5
    STOPPED = 6
    DISPOSING = 7
    DISPOSED = 8


class LifecycleController(ABC):

    def can_initialize(self, phase: [LifecyclePhase]) -> bool:
        return phase is None or phase == LifecyclePhase.DISPOSED

    def can_start(self, phase: [LifecyclePhase]) -> bool:
        return phase is not None and (
                phase == LifecyclePhase.INITIALIZED or phase == LifecyclePhase.STOPPED)

    def can_stop(self, phase: [LifecyclePhase]) -> bool:
        return phase is not None and phase == LifecyclePhase.STARTED

    def can_dispose(self, phase: [LifecyclePhase]) -> bool:
        return phase is not None and (
                phase == LifecyclePhase.INITIALIZED or phase == LifecyclePhase.STOPPED)


LS = TypeVar("LS", bound=Lifecycle)


class LifecycleState(LifecycleController, ABC):

    def __init__(self, lifecycle: [LS]):
        self.phase = None
        self.prev_phase = None
        self.lifecycle = lifecycle
        self.logger = logger_factory.get_logger(__name__)

    def is_initializing(self) -> bool:
        return self.phase == LifecyclePhase.INITIALIZING

    def is_initialized(self) -> bool:
        return self.phase == LifecyclePhase.INITIALIZED

    def is_starting(self) -> bool:
        return self.phase == LifecyclePhase.STARTING

    def is_started(self) -> bool:
        return self.phase == LifecyclePhase.STARTED

    def is_stopping(self) -> bool:
        return self.phase == LifecyclePhase.STOPPING

    def is_stopped(self) -> bool:
        return self.phase == LifecyclePhase.STOPPED

    def is_disposing(self) -> bool:
        return self.phase == LifecyclePhase.DISPOSING

    def is_disposed(self) -> bool:
        return self.phase == LifecyclePhase.DISPOSED

    def get_phase(self) -> LifecyclePhase:
        return self.phase

    def set_phase(self, phase: [LifecyclePhase]) -> None:
        prev = "None" if self.phase is None else self.phase.name
        self.logger.info("[setPhaseName][{}]{} --> {}".format(self.lifecycle.__class__.__name__, prev, phase.name))
        self.phase = phase

    def rollback(self, err: [Exception]) -> None:
        self.phase = self.prev_phase
        self.prev_phase = None
