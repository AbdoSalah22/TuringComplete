from PyQt5.QtWidgets import QGraphicsObject
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import QRectF

class HeadItem(QGraphicsObject):
    def __init__(self, position):
        super().__init__()
        self.setPos(position * 50, -40)
        self.mypixmap = QPixmap("arrow_head.png")
    def boundingRect(self) -> QRectF:
        return QRectF(0, 0, 50, 50)
    def paint(self, painter, option, widget):
        painter.setOpacity(1)
        painter.drawPixmap(0,0,50, 50, self.mypixmap)