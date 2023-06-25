import logging
from unittest import TestCase

from core.lifecycle import Lifecycle

logging.basicConfig()


class SubLifecycle(Lifecycle):
    def __init__(self) -> None:
        super().__init__()
        self.init_counter = 0

    def do_init(self) -> None:
        self.init_counter += 1

    def do_start(self) -> None:
        self.init_counter += 1

    def do_stop(self) -> None:
        self.init_counter += 1

    def do_dispose(self) -> None:
        self.init_counter += 1


class TestLifecycle(TestCase):
    def test_initialize(self) -> None:
        ls = SubLifecycle()
        ls.initialize()
        ls.logger.info(ls.lifecycle_state.get_phase())
        ls.start()
        ls.logger.info(ls.lifecycle_state.get_phase())
        ls.stop()
        ls.logger.info(ls.lifecycle_state.get_phase())
        ls.dispose()
        ls.logger.info(ls.lifecycle_state.get_phase())

    def test_start(self) -> None:
        self.fail()

    def test_stop(self) -> None:
        self.fail()

    def test_dispose(self) -> None:
        self.fail()

    def test_do_init(self) -> None:
        self.fail()

    def test_do_start(self) -> None:
        self.fail()

    def test_do_stop(self) -> None:
        self.fail()

    def test_do_dispose(self) -> None:
        self.fail()
