from PyQt5.QtWidgets import QLabel, QApplication
from PyQt5.QtGui import QDrag, QPixmap, QPainter
from PyQt5.QtCore import QMimeData, Qt
import funciones


class DraggableLabel(QLabel):
    def __init__(self, ventana, tipo, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tipo = tipo
        self.ventana = ventana

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drag_start_position = event.pos()

    def mouseMoveEvent(self, event):
        if not (event.buttons() & Qt.LeftButton):
            return
        if (event.pos() - self.drag_start_position).manhattanLength() < \
                QApplication.startDragDistance():
            return
        if not self.ventana.estado == "pre-ronda":
            return
        drag = QDrag(self)
        mimedata = QMimeData()
        mimedata.setText(self.tipo)
        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(event.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)


class DropLabel(QLabel):
    def __init__(self, ventana, *args, **kwargs):
        QLabel.__init__(self, *args, **kwargs)
        self.setAcceptDrops(True)
        self.ventana = ventana

    def dragEnterEvent(self, event):
        if event.mimeData().hasText():
            event.acceptProposedAction()

    def dropEvent(self, event):
        if self.ventana.estado == "pre-ronda":
            text = event.mimeData().text()
            if text == "mesa":
                pos_x = event.pos().x() - 10
                pos_y = event.pos().y() + 40
            else:
                pos_x = event.pos().x() - 30
                pos_y = event.pos().y() + 20
            pos = [pos_x, pos_y]
            if funciones.aceptar_drop(self.ventana.mesas, self.ventana.chefs, self.ventana.mesero,
                                      pos, text):
                self.ventana.agregar([pos, text])
                event.acceptProposedAction()
