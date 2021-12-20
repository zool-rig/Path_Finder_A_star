from PyQt5.QtCore import QPoint


class Cell(object):
    def __init__(self, grid, x, y):
        self.grid = grid
        self.x = x
        self.y = y
        self.is_start = False
        self.is_end = False
        self.is_wall = False
        self.cost = 0

    def __repr__(self):
        return f'Cell(x:{self.x}, y:{self.y})'

    def __eq__(self, other):
        if type(other) != type(self):
            raise ValueError(f'{type(other)} is incompatible with {type(self)}')
        return self.x == other.x and self.y == other.y

    def __ne__(self, other):
        if type(other) != type(self):
            raise ValueError(f'{type(other)} is incompatible with {type(self)}')
        return not self.__eq__(other)

    def __lt__(self, other):
        if type(other) != type(self):
            raise ValueError(f'{type(other)} is incompatible with {type(self)}')
        return self.heuristic < other.heuristic

    def __le__(self, other):
        if type(other) != type(self):
            raise ValueError(f'{type(other)} is incompatible with {type(self)}')
        return self.heuristic <= other.heuristic

    def __gt__(self, other):
        if type(other) != type(self):
            raise ValueError(f'{type(other)} is incompatible with {type(self)}')
        return self.heuristic > other.heuristic

    def __ge__(self, other):
        if type(other) != type(self):
            raise ValueError(f'{type(other)} is incompatible with {type(self)}')
        return self.heuristic >= other.heuristic

    def __hash__(self):
        return hash((self.x, self.y))

    @property
    def pixel_pos(self):
        return QPoint((self.x * self.grid.pen_size) + self.grid.pen_size,
                      (self.y * self.grid.pen_size) + self.grid.pen_size)

    def _neighbors_indexes_generator(self):
        range_x = list(filter(lambda i: 0 <= i < len(self.grid.cells), [self.x - 1, self.x, self.x + 1]))
        range_y = list(filter(lambda i: 0 <= i < len(self.grid.cells), [self.y - 1, self.y, self.y + 1]))
        for x in range_x:
            for y in range_y:
                if x == self.x and y == self.y:
                    continue
                yield (x, y)

    @property
    def neighbors(self):
        return [self.grid.get_cell(*coord) for coord in self._neighbors_indexes_generator()
                if not self.grid.get_cell(*coord).is_wall]

    @property
    def heuristic(self):
        return self.cost + (abs(((self.grid.end.x - self.x) ** 2) + ((self.grid.end.y - self.y) ** 2)) ** 0.5)
