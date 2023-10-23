from operator import attrgetter
from typing import Any, Iterable, Annotated
from dataclasses import dataclass

from pygame.rect import Rect
from pygame.math import Vector2
from pygame.surface import Surface
from pygame.sprite import AbstractGroup, Group, Sprite


@dataclass
class ValueRange:
    lo: float
    hi: float


class Camera2D(Group):
    def __init__(
        self,
        bg_surface: Surface | None,
        camera_delay: Annotated[float, ValueRange(1, 100)],
        *sprites: Any | AbstractGroup | Iterable
    ) -> None:
        assert 1 <= camera_delay <= 100, "camera_delay must be between 1 and 100"

        super().__init__(*sprites)

        self.camera_delay = camera_delay
        self.offset = Vector2(0, 0)
        self.bg_surface = bg_surface

    def draw(self, surface: Surface, target: Sprite) -> list[Rect]:
        self.offset += (
            Vector2(target.rect.center) - Vector2(surface.get_size()) / 2 - self.offset
        ) / self.camera_delay

        if self.bg_surface is not None:
            surface.blit(self.bg_surface, -self.offset)

        return surface.blits(self.get_visible_sprites(surface), True)

    def get_visible_sprites(self, surface: Surface) -> list[tuple[Surface, Sprite]]:
        surface_rect = surface.get_rect(topleft=self.offset)

        return [
            (sprite.image, sprite.rect.topleft - self.offset)
            for sprite in self.sprites()
            if surface_rect.colliderect(sprite.rect)
        ]

    def sprites(self) -> list[Sprite]:
        return sorted(super().sprites(), key=attrgetter("rect.centery"))
