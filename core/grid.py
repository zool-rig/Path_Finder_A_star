from .canvas import Canvas
from .cell import Cell
from . import constants
from PIL import Image


class Grid(Canvas):
    def __init__(self, size=None):
        super(Grid, self).__init__(size=size)
        self.cells = self.init_cells()
        self.drawing_modes_dict = {
            'paint_walls': {
                'color': constants.WALL_COLOR,
                'state': {'is_wall': True, 'is_start': False, 'is_end': False},
                'method': self.set_wall
            },
            'paint_start': {
                'color': constants.START_COLOR,
                'state': {'is_wall': False, 'is_start': True, 'is_end': False},
                'method': self.set_start
            },
            'paint_end': {
                'color': constants.END_COLOR,
                'state': {'is_wall': False, 'is_start': False, 'is_end': True},
                'method': self.set_end
            },
            'erase': {
                'color': constants.DEFAULT_BACKGROUND_COLOR,
                'state': {'is_wall': False, 'is_start': False, 'is_end': False},
                'method': self.erase
            },
            'paint_path': {'color': constants.PATH_COLOR},
            'paint_closed': {'color': constants.CLOSED_COLOR},
            'paint_opened': {'color': constants.OPEN_COLOR}
        }
        self.drawing_mode = 'paint_start'
        self.start = None
        self.end = None
        self.walls = list()

    def init_cells(self):
        return [[Cell(self, x, y) for y in range(0, (self._size[1] // 10) + 1)]
                for x in range(0, (self._size[0] // 10) + 1)]

    def get_cell(self, x, y):
        return self.cells[x][y]

    def get_cell_at_pos(self, canvas_pos):
        x = (canvas_pos.x() - self.pen_size) // self.pen_size
        y = (canvas_pos.y() - self.pen_size) // self.pen_size
        if x < len(self.cells) and y < len(self.cells[0]):
            return self.cells[x][y]

    def set_cell(self, pos):
        cell = self.get_cell_at_pos(pos)
        if not cell:
            return
        if self.drawing_modes_dict[self.drawing_mode].get('state'):
            cell.__dict__.update(self.drawing_modes_dict[self.drawing_mode]['state'])
        if self.drawing_modes_dict[self.drawing_mode].get('method'):
            self.drawing_modes_dict[self.drawing_mode]['method'](cell)

    def set_start(self, cell):
        if self.start:
            self.drawing_mode = 'erase'
            self.draw(self.start.pixel_pos)
            self.drawing_mode = 'paint_start'
        self.start = cell

    def set_end(self, cell):
        if self.end:
            self.drawing_mode = 'erase'
            self.draw(self.end.pixel_pos)
            self.drawing_mode = 'paint_end'
        self.end = cell

    def set_wall(self, cell):
        if cell not in set(self.walls):
            self.walls.append(cell)

    def erase(self, cell):
        if self.start and cell == self.start:
            self.start = None
        if self.end and cell == self.end:
            self.end = None
        if cell in set(self.walls):
            self.walls.remove(cell)

    def draw(self, pos):
        self.pen_color = self.drawing_modes_dict[self.drawing_mode]['color']
        super(Grid, self).draw(pos)
        self.set_cell(self.round_pos(pos))

    def reset(self):
        self.init_background()
        self.cells = self.init_cells()
        self.drawing_mode = 'paint_walls'
        self.start = None
        self.end = None
        self.walls = list()

    def save_image(self, img_path):
        img = self.pixmap().toImage()
        data = img.constBits().asstring(img.byteCount())
        pil_img = Image.frombuffer('RGBA', (img.width(), img.height()), data, 'raw', 'RGBA', 0, 1)
        pil_img.save(img_path)
        return pil_img
