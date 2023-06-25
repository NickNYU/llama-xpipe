import logging
from unittest import TestCase

from core.lifecycle import Lifecycle

logging.basicConfig()


class SubLifecycle(Lifecycle):
    def __init__(self):
        super().__init__()
        self.init_counter = 0

    def do_init(self):
        self.init_counter += 1

    def do_start(self):
        self.init_counter += 1

    def do_stop(self):
        self.init_counter += 1

    def do_dispose(self):
        self.init_counter += 1


class TestLifecycle(TestCase):
    def test_initialize(self):
        ls = SubLifecycle()
        ls.initialize()
        ls.logger.info(ls.lifecycle_state.get_phase().name)
        ls.start()
        ls.logger.info(ls.lifecycle_state.get_phase().name)
        ls.stop()
        ls.logger.info(ls.lifecycle_state.get_phase().name)
        ls.dispose()
        ls.logger.info(ls.lifecycle_state.get_phase().name)

    def test_start(self):
        self.fail()

    def test_stop(self):
        self.fail()

    def test_dispose(self):
        self.fail()

    def test_do_init(self):
        self.fail()

    def test_do_start(self):
        self.fail()

    def test_do_stop(self):
        self.fail()

    def test_do_dispose(self):
        self.fail()
