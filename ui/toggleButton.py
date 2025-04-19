from PyQt6.QtCore import Qt, QPropertyAnimation, pyqtProperty, QSize, QRectF, QEasingCurve
from PyQt6.QtGui import QPainter, QColor, QBrush
from PyQt6.QtWidgets import QAbstractButton

class ToggleSwitch(QAbstractButton):
    def __init__(self, parent=None, thumb_radius=10, track_radius=12, margin=3):
        super().__init__(parent)
        self.setCheckable(True)
        self._thumb_radius = thumb_radius
        self._track_radius = track_radius
        self._margin = margin

        self._position = 0.0  # 0.0 = off, 1.0 = on

        # animation setup
        self._anim = QPropertyAnimation(self, b"position", self)
        self._anim.setDuration(200)
        self._anim.setEasingCurve(QEasingCurve.Type.InOutCubic)

        self.toggled.connect(self._on_toggled)

        # colors
        self._track_color_off = QColor("#777")
        self._track_color_on  = QColor("#44b78b")
        self._thumb_color     = QColor("#FFF")

        # make sure sizeHint is respected
        self.setMinimumSize(self.sizeHint())

    def sizeHint(self):
        w = (self._track_radius * 2) + (self._margin * 2)
        h = (self._track_radius * 2) + (self._margin * 2)
        return QSize(w, h)

    def _on_toggled(self, checked):
        start = self._position
        end = 1.0 if checked else 0.0
        self._anim.stop()
        self._anim.setStartValue(start)
        self._anim.setEndValue(end)
        self._anim.start()

    def paintEvent(self, e):
        p = QPainter(self)
        p.setRenderHint(QPainter.RenderHint.Antialiasing)

        # draw track
        track_rect = QRectF(
            self._margin,
            self._margin,
            self.width()  - 2*self._margin,
            self.height() - 2*self._margin
        )
        p.setBrush(QBrush(
            self._track_color_on  if self.isChecked() else self._track_color_off
        ))
        p.setPen(Qt.PenStyle.NoPen)
        p.drawRoundedRect(track_rect, self._track_radius, self._track_radius)

        # compute thumb position
        x_min = self._margin + (self._thumb_radius * 0)
        x_max = self.width() - self._margin - (2*self._thumb_radius)
        x = x_min + (x_max - x_min) * self._position
        y = (self.height() - 2*self._thumb_radius) / 2

        # draw thumb
        thumb_rect = QRectF(x, y, 2*self._thumb_radius, 2*self._thumb_radius)
        p.setBrush(QBrush(self._thumb_color))
        p.drawEllipse(thumb_rect)
        p.end()

    def getPosition(self):
        return self._position

    def setPosition(self, pos):
        self._position = pos
        self.update()

    position = pyqtProperty(float, fget=getPosition, fset=setPosition)
