import unittest
from pathlib import Path

import pygame
from pygutils.sprite import SpriteSheet
from pygame.image import load as load_image


class SpriteSheetTest(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)

        pygame.init()
        pygame.display.set_mode((100, 100), pygame.HIDDEN)

        sheet_path = Path(__file__).parent.parent / "images" / "Player.png"
        self.sheet = load_image(sheet_path).convert_alpha()

    def test_can_get_individual_surface_by_row_and_column(self):
        row = 1
        column = 2
        surface_width = self.sheet.get_width() // 14
        surface_height = self.sheet.get_height() // 5

        expected_surface = self.sheet.subsurface(
            column * surface_width, row * surface_height, surface_width, surface_height
        )

        sprite_sheet = SpriteSheet(self.sheet, 5, 14)
        surface = sprite_sheet.get_surface(row, column)

        self.assertEqual(surface.get_offset(), expected_surface.get_offset())

    def test_can_retrieve_entire_row_by_index(self):
        sprite_sheet = SpriteSheet(self.sheet, 5, 14)
        surfaces = sprite_sheet.get_surfaces_row(1)

        self.assertEqual(8, len(surfaces))

    def test_can_retrieve_entire_column_by_index(self):
        sprite_sheet = SpriteSheet(self.sheet, 5, 14)
        surfaces = sprite_sheet.get_surfaces_column(6)

        self.assertEqual(2, len(surfaces))
