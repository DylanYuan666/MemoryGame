from PyQt5.QtWidgets import QPushButton
from PyQt5.QtCore import pyqtProperty, QPoint
from PyQt5.QtGui import QPainter

class AnimatedPushButton(QPushButton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rotation = 0

    @pyqtProperty(int)
    def rotation(self):
        return self._rotation

    @rotation.setter
    def rotation(self, value):
        self._rotation = value
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        # 保存原始状态
        painter.save()
        
        # 旋转中心
        center = self.rect().center()
        painter.translate(center)
        painter.rotate(self._rotation)
        painter.translate(-center)
        
        # 绘制按钮
        super().paintEvent(event)
        
        # 恢复状态
        painter.restore()