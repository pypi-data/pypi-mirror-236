import time
from typing import Callable


class Timer:
    def __init__(
        self,
        duration_ms: int,
        callback: Callable[[], None] | None = None,
    ) -> None:
        self.duration_ms = duration_ms
        self.callback = callback
        self.start_time = None

    @staticmethod
    def current_ms_time() -> int:
        return round(time.time() * 1000)

    @property
    def active(self) -> bool:
        return self.start_time is not None

    def activate(self) -> None:
        self.start_time = Timer.current_ms_time()

    def deactivate(self) -> None:
        self.start_time = None

    def update(self) -> None:
        if (
            self.active
            and (Timer.current_ms_time() - self.start_time) >= self.duration_ms
        ):
            if self.callback is not None:
                self.callback()

            self.deactivate()
