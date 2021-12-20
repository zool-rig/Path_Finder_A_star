import heapq
import sys
import time
import os
import glob
from PIL import Image
from PyQt5.QtCore import pyqtSignal, QObject


class PathFinderAPI(QObject):
    gif_is_ready = pyqtSignal(str)

    def __init__(self, grid, record):
        super(PathFinderAPI, self).__init__()
        self.grid = grid
        self.do_record = record
        path_finder_dir = os.path.split(os.path.split(__file__)[0])[0].replace('\\', '/')
        self.img_root_dir = f'{path_finder_dir}/images'
        self.img_sequence_dir = None
        self.sequence_number = 0

    @staticmethod
    def distance(vec1, vec2):
        return abs(((vec2.x - vec1.x) ** 2) + ((vec2.y - vec1.y) ** 2)) ** 0.5

    @staticmethod
    def construct_path(travel_dict, current):
        total_path = [current]
        while current in travel_dict.keys():
            current = travel_dict[current]
            total_path.insert(0, current)
        return total_path

    def save_sequence(self):
        if not self.img_sequence_dir:
            time_stamp = str(int(time.time()))
            self.img_sequence_dir = os.path.join(self.img_root_dir, time_stamp).replace('\\', '/')
            if not os.path.exists(self.img_sequence_dir):
                os.makedirs(self.img_sequence_dir)
        img_path = f'{self.img_sequence_dir}/{self.sequence_number:03d}.png'
        self.grid.save_image(img_path)
        self.sequence_number += 1

    def create_gif(self):
        gif_path = f'{self.img_sequence_dir}/_sequence.gif'
        img, *img_list = [Image.open(f) for f in sorted(glob.glob(f'{self.img_sequence_dir}/*.png'))]
        img.save(fp=gif_path, format='GIF', append_images=img_list, save_all=True, duration=200, loop=0)
        self.gif_is_ready.emit(gif_path)
        for i in glob.glob(f'{self.img_sequence_dir}/*.png'):
            os.remove(i)

    def run(self):
        print('>>> Start processing...')
        start_time = time.time()
        closed_list = list()
        open_list = [self.grid.start]
        travel_dict = dict()
        self.img_sequence_dir = None
        self.sequence_number = 0

        while open_list:
            current = heapq.heappop(open_list)

            for mod, cell_list in [('paint_opened', open_list),
                                   ('paint_closed', closed_list),
                                   ('paint_path', self.construct_path(travel_dict, current))]:
                self.grid.drawing_mode = mod
                for c in cell_list:
                    self.grid.draw(c.pixel_pos)

            if current == self.grid.end:
                path = self.construct_path(travel_dict, current)
                print('\nSUCCESS: End point reached with a path measuring {} cells. '
                      'Done in {} seconds'.format(len(path), round(time.time() - start_time, 5)))
                if self.do_record:
                    self.create_gif()
                return path

            current.closed = True
            closed_list.append(current)

            for n in current.neighbors:
                if n in set(closed_list):
                    continue
                n.cost = current.cost + 1
                travel_dict[n] = current

                if n not in open_list:
                    heapq.heappush(open_list, n)

            sys.stdout.write(f'\rCurrent: {current} Open:{len(open_list)} Closed:{len(closed_list)}')
            if self.do_record:
                self.save_sequence()
        print('\nERROR: No solution found')
        self.create_gif()
        return list()
