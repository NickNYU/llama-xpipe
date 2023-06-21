import enum
from abc import ABC, abstractmethod

class Iterable(ABC):
    @abstractmethod
    def has_next(self) -> bool:
        pass

    @abstractmethod
    def next(self):
        pass
class FinalStateMachine(Iterable, ABC):
    @abstractmethod
    def get_state(self) -> str:
        pass

    @classmethod
    def entry_point(cls):
        return STAGE_ONE()

class STAGE_THREE(FinalStateMachine):
    def get_state(self):
        return "stage-three"

    def next(self):
        return None

    def has_next(self) -> bool:
        return False

class STAGE_TWO(FinalStateMachine):
    def get_state(self):
        return "stage-two"

    def next(self):
        return STAGE_THREE()

    def has_next(self):
        return True

class STAGE_ONE(FinalStateMachine):
    def get_state(self):
        return "stage-one"

    def next(self):
        return STAGE_TWO()

    def has_next(self):
        return True

if __name__ == '__main__':
    s = FinalStateMachine.entry_point()
    print(s.get_state())
    while s.has_next():
        s = s.next()
        print(s.get_state())


