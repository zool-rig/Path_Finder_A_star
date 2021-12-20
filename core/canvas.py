from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter, QPen, QColor, QPixmap
from . import constants


class Canvas(QLabel):
    def __init__(self, size=None):
        super(Canvas, self).__init__()
        self._size = size or constants.DEFAULT_CANVAS_SIZE
        self.pen_color = constants.DEFAULT_PEN_COLOR
        self.pen_size = constants.DEFAULT_PEN_SIZE
        self.init_background()

    def mousePressEvent(self, event):
        if 0 <= event.pos().x() < self.size().width() and 0 <= event.pos().y() < self.size().height():
            self.draw(event.pos())
        super(Canvas, self).mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if 0 <= event.pos().x() < self.size().width() and 0 <= event.pos().y() < self.size().height():
            self.draw(event.pos())
        super(Canvas, self).mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        super(Canvas, self).mouseReleaseEvent(event)

    def get_painter(self, pen_color=None, pen_size=None):
        painter = QPainter(self.pixmap())
        pen_color = pen_color or self.pen_color
        pen_size = pen_size or self.pen_size
        painter.setPen(QPen(QColor(*pen_color), pen_size))
        return painter

    def init_background(self):
        pixmap = QPixmap(*[self._size[0] + (self.pen_size * 2),
                           self._size[1] + (self.pen_size * 2)])
        self.setPixmap(pixmap)
        self.pixmap().fill(QColor(*constants.DEFAULT_BACKGROUND_COLOR))
        painter = self.get_painter(pen_color=constants.DEFAULT_PEN_COLOR)
        painter.drawLine(0, 0, pixmap.size().width(), 0)
        painter.drawLine(pixmap.size().width(), 0, pixmap.size().width(), pixmap.size().width())
        painter.drawLine(pixmap.size().width(), pixmap.size().width(), 0, pixmap.size().width())
        painter.drawLine(0, pixmap.size().width(), 0, 0)
        painter.end()

    def draw(self, pos):
        pos = self.round_pos(pos)
        painter = self.get_painter()
        painter.drawPoint(pos.x(), pos.y())
        painter.end()
        self.update()

    def round_pos(self, pos):
        return QPoint((round(abs(pos.x()) / self.pen_size) * self.pen_size),
                      (round(abs(pos.y()) / self.pen_size) * self.pen_size))
