from typing import Callable

from pygame.surface import Surface

from .animation_contract import AnimationContract


class Animation(AnimationContract):
    def __init__(
        self,
        frames_sequence: list[Surface],
        animation_speed: int,
        on_finish: Callable[[], None] | None = None,
        loop: bool = True,
    ) -> None:
        self.index: float = 0

        self.loop = loop
        self.on_finish = on_finish
        self.frames_sequence = frames_sequence
        self.animation_speed = animation_speed

    @property
    def finished(self) -> bool:
        return self.index >= len(self.frames_sequence)

    def next(self) -> Surface:
        current_index = int(self.index)
        last_index = len(self.frames_sequence) - 1

        return self.frames_sequence[min(current_index, last_index)]

    def reset(self) -> None:
        self.index = 0

    def update(self, delta_time: float) -> None:
        if self.finished:
            return

        self.index += self.animation_speed * delta_time

        if self.finished:
            if self.on_finish is not None:
                self.on_finish()

            if self.loop:
                self.reset()

    def copy(self) -> "Animation":
        return Animation(
            frames_sequence=self.frames_sequence[:],
            animation_speed=self.animation_speed,
            on_finish=self.on_finish,
            loop=self.loop,
        )
