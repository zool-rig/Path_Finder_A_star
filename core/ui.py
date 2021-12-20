from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QRadioButton, QCheckBox, QPushButton
from PyQt5.QtCore import Qt
from .grid import Grid
from .api import PathFinderAPI
from .movie import Movie


class PathFinderUI(QDialog):
    def __init__(self):
        super(PathFinderUI, self).__init__(parent=None)

        '''Layouts'''
        self.main_layout = None
        self.options_h_layout = None

        '''Widgets'''
        self.paint_mode_lbl = None
        self.wall_mode_rdo = None
        self.start_mode_rdo = None
        self.end_mode_rdo = None
        self.erase_mode_rdo = None
        self.recode_chk = None
        self.grid = None
        self.movie = None
        self.run_btn = None
        self.clear_btn = None

        self.init_ui()

    def init_ui(self):
        self.setWindowTitle('Path Finder v1.0')
        self.init_layouts()
        self.init_widgets()
        self.set_layouts()
        self.set_connections()
        self.set_default()

    def init_layouts(self):
        self.main_layout = QVBoxLayout(self)
        self.options_h_layout = QHBoxLayout()

    def init_widgets(self):
        self.paint_mode_lbl = QLabel('Painting Mode:')
        self.wall_mode_rdo = QRadioButton('Walls')
        self.start_mode_rdo = QRadioButton('Start')
        self.end_mode_rdo = QRadioButton('End')
        self.erase_mode_rdo = QRadioButton('Erase')
        self.recode_chk = QCheckBox('Record')
        self.grid = Grid()
        self.movie = Movie()
        self.run_btn = QPushButton('RUN')
        self.clear_btn = QPushButton('CLEAR')

    def set_layouts(self):
        self.main_layout.addLayout(self.options_h_layout)
        self.options_h_layout.addWidget(self.paint_mode_lbl)
        self.options_h_layout.addWidget(self.start_mode_rdo)
        self.options_h_layout.addWidget(self.end_mode_rdo)
        self.options_h_layout.addWidget(self.wall_mode_rdo)
        self.options_h_layout.addWidget(self.erase_mode_rdo)
        self.options_h_layout.addWidget(self.recode_chk)
        self.main_layout.addWidget(self.grid)
        self.main_layout.addWidget(self.movie)
        self.main_layout.addWidget(self.run_btn)
        self.main_layout.addWidget(self.clear_btn)

    def set_connections(self):
        self.wall_mode_rdo.toggled.connect(lambda state: self.set_drawing_mode(state, 'paint_walls'))
        self.start_mode_rdo.toggled.connect(lambda state: self.set_drawing_mode(state, 'paint_start'))
        self.end_mode_rdo.toggled.connect(lambda state: self.set_drawing_mode(state, 'paint_end'))
        self.erase_mode_rdo.toggled.connect(lambda state: self.set_drawing_mode(state, 'erase'))
        self.run_btn.clicked.connect(self.run)
        self.clear_btn.clicked.connect(self.clear)

    def set_default(self):
        self.main_layout.setAlignment(Qt.AlignTop)
        self.options_h_layout.setAlignment(Qt.AlignLeft)
        self.start_mode_rdo.setChecked(True)
        self.recode_chk.setChecked(True)
        self.movie.setHidden(True)

    def set_drawing_mode(self, state, mode):
        if state:
            self.grid.drawing_mode = mode

    def clear(self):
        self.grid.reset()
        self.wall_mode_rdo.setChecked(True)
        self.grid.setHidden(False)
        if self.movie.movie:
            self.movie.stop()
        self.movie.setHidden(True)

    def run(self):
        if not self.grid.start or not self.grid.end:
            print('ERROR: End or Start are not defined')
            return
        api = PathFinderAPI(self.grid, self.recode_chk.isChecked())
        api.gif_is_ready.connect(lambda gif_path: self.show_movie(gif_path))
        api.run()

    def paint_cells(self, mod, cell_list):
        self.grid.drawing_mode = mod
        for c in cell_list:
            self.grid.draw(c.pixel_pos)

    def show_movie(self, gif_path):
        self.movie.setHidden(False)
        self.grid.setHidden(True)
        self.movie.set_movie(gif_path)
        self.movie.start()
