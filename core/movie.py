from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMovie


class Movie(QLabel):
    def __init__(self, *args, **kwargs):
        super(Movie, self).__init__(*args, **kwargs)
        self.movie = None

    def set_movie(self, gif_path):
        self.movie = QMovie(gif_path)
        self.setMovie(self.movie)

    def start(self):
        self.movie.start()

    def stop(self):
        self.movie.stop()
