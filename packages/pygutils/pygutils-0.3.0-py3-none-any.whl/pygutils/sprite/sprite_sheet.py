from pygame.surfarray import pixels_alpha
from pygame.surface import Surface
from pygame.rect import Rect


class SpriteSheet:
    def __init__(self, sheet: Surface, rows: int, columns: int) -> None:
        self.sheet = sheet
        self.rows = rows
        self.columns = columns

        self.__rect_width = self.sheet.get_width() // columns
        self.__rect_height = self.sheet.get_height() // rows

        self.__surfaces_map = self.__build_surfaces_map()

    def __get_subsurface(self, row: int, column: int) -> Surface:
        return self.sheet.subsurface(
            Rect(
                column * self.__rect_width,
                row * self.__rect_height,
                self.__rect_width,
                self.__rect_height,
            )
        )

    def __build_surfaces_map(self) -> dict[tuple[int, int], Surface]:
        surfaces_map = {}

        for row in range(self.rows):
            for column in range(self.columns):
                subsurface = self.__get_subsurface(row, column)

                if pixels_alpha(subsurface).any():
                    surfaces_map[(row, column)] = subsurface

        return surfaces_map

    def get_surface(self, row: int, column: int) -> Surface:
        return self.__surfaces_map[(row, column)]

    def get_surfaces_row(self, row: int) -> list[Surface]:
        return [
            self.__surfaces_map[(row, column)]
            for column in range(self.columns)
            if (row, column) in self.__surfaces_map
        ]

    def get_surfaces_column(self, column: int) -> list[Surface]:
        return [
            self.__surfaces_map[(row, column)]
            for row in range(self.rows)
            if (row, column) in self.__surfaces_map
        ]
