from abc import ABCMeta, abstractmethod

from pygame.surface import Surface


class AnimationContract(metaclass=ABCMeta):
    @abstractmethod
    def next(self) -> Surface:
        pass

    @abstractmethod
    def reset(self) -> None:
        pass

    @abstractmethod
    def update(self, delta_time: float) -> None:
        pass
