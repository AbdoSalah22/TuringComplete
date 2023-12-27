from PyQt5.QtWidgets import QGraphicsRectItem, QGraphicsTextItem

class TapeItem(QGraphicsRectItem):
    def __init__(self, value, position):
        super().__init__(0, 0, 50, 50)
        self.setPos(position * 50, 0)
        self.value = str(value)
        self.text_item = QGraphicsTextItem(str(value), parent=self)
        self.text_item.setPos(18,
                              15)