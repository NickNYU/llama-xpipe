from core.lifecycle import Lifecycle


class LifecycleHelper:
    @classmethod
    def initialize_if_possible(cls, ls: Lifecycle) -> None:
        if isinstance(ls, Lifecycle) and ls.lifecycle_state.can_initialize(
            ls.lifecycle_state.phase
        ):
            ls.initialize()

    @classmethod
    def start_if_possible(cls, ls: Lifecycle) -> None:
        if isinstance(ls, Lifecycle) and ls.lifecycle_state.can_start(
            ls.lifecycle_state.phase
        ):
            ls.start()

    @classmethod
    def stop_if_possible(cls, ls: Lifecycle) -> None:
        if isinstance(ls, Lifecycle) and ls.lifecycle_state.can_stop(
            ls.lifecycle_state.phase
        ):
            ls.stop()

    @classmethod
    def dispose_if_possible(cls, ls: Lifecycle) -> None:
        if isinstance(ls, Lifecycle) and ls.lifecycle_state.can_dispose(
            ls.lifecycle_state.phase
        ):
            ls.dispose()
