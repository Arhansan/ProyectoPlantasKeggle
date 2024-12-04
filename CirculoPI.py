import sys
import math
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget
from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QPainter, QColor, QPen, QFont

class PiAnimation(QWidget):
    def __init__(self):
        super().__init__()
        self.progress = 0  # Progreso del movimiento
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_progress)
        self.timer.start(50)  # Actualizar cada 50 ms
        self.circle_radius = 80  # Aumentar aún más el tamaño del círculo
        self.show_pi = False  # Flag para mostrar el símbolo de Pi
        self.pause_timer = None  # Temporizador para la pausa de 5 segundos

    def update_progress(self):
        # Incrementar el progreso del círculo sobre la regla
        self.progress += 0.05
        if self.progress >= math.pi:
            self.show_pi = True  # Mostrar símbolo de Pi cuando se alcance 3.14

        if self.progress >= 4:
            if not self.pause_timer:  # Si no hay un temporizador de pausa activo, crearlo
                self.timer.stop()
                self.pause_timer = QTimer(self)
                self.pause_timer.timeout.connect(self.reset_animation)
                self.pause_timer.start(5000)  # Pausar durante 5 segundos

        self.update()

    def reset_animation(self):
        # Reiniciar la animación después de la pausa
        self.progress = 0
        self.show_pi = False
        self.pause_timer.stop()
        self.pause_timer = None
        self.timer.start(50)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Dibujar la línea de la regla (parte inferior)
        rule_y = 500  # Ajuste de la posición de la regla
        rule_start_x = 100
        rule_end_x = 700
        painter.setPen(QPen(Qt.GlobalColor.black, 5))
        painter.drawLine(int(rule_start_x), int(rule_y), int(rule_end_x), int(rule_y))  # Línea de la regla

        # Dibujar marcas de la regla
        for i in range(5):
            x = rule_start_x + i * (rule_end_x - rule_start_x) / 4
            painter.drawLine(int(x), int(rule_y - 15), int(x), int(rule_y + 15))  # Marcas más largas
            painter.drawText(int(x - 10), int(rule_y + 40), f"{i}")  # Valores de la regla

        # Dibujar el círculo rodando sobre la regla
        rule_range = rule_end_x - rule_start_x
        circle_x = rule_start_x + rule_range * (self.progress / 4)
        circle_y = rule_y - self.circle_radius

        # Dibujar el círculo
        painter.setPen(QPen(Qt.GlobalColor.red, 4))  # Línea más gruesa para el círculo
        painter.drawEllipse(int(circle_x - self.circle_radius), int(circle_y - self.circle_radius), 2 * self.circle_radius, 2 * self.circle_radius)

        # Dibujar una línea que representa el "giro" del círculo mientras se mueve
        angle = (self.progress * 2 * math.pi) % (2 * math.pi)  # Ángulo para simular el giro
        end_x = circle_x + self.circle_radius * math.cos(angle)
        end_y = circle_y + self.circle_radius * math.sin(angle)
        painter.setPen(QPen(Qt.GlobalColor.blue, 3))
        painter.drawLine(int(circle_x), int(circle_y), int(end_x), int(end_y))

        # Dibujar el progreso en la línea de la regla hasta el valor de PI
        max_value = 4  # Valor máximo en la regla
        progress_x = rule_start_x + rule_range * (self.progress / 4)
        
        # Dibujar la línea de progreso verde
        painter.setPen(QPen(Qt.GlobalColor.green, 8))
        painter.drawLine(int(rule_start_x), int(rule_y), int(progress_x), int(rule_y))

        # Resaltar el punto de PI en la regla
        if self.progress >= math.pi:
            painter.setPen(QPen(Qt.GlobalColor.red, 12))  # Línea roja más gruesa
            pi_x = rule_start_x + rule_range * (math.pi / 4)
            # Hacer la línea mucho más grande que el círculo
            painter.drawLine(int(pi_x), int(rule_y - 120), int(pi_x), int(rule_y + 60))  # Línea roja mucho más grande

            # Mostrar "PI" sobre la línea roja
            painter.setFont(QFont('Arial', 30))  # Fuente grande para el símbolo de Pi
            painter.setPen(QPen(Qt.GlobalColor.black))
            painter.drawText(int(pi_x - 30), int(rule_y - 130), "π")  # Posicionar el texto "PI" en la parte superior

        # Mostrar el símbolo de PI encima del círculo cuando se alcance 3.14
        if self.show_pi:
            painter.setFont(QFont('Arial', 40))  # Fuente más grande para el símbolo de Pi
            painter.setPen(QPen(Qt.GlobalColor.black))
            painter.drawText(int(circle_x - 30), int(circle_y - 100), "π")  # Posición ajustada del símbolo de Pi

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pi Animation")
        self.setGeometry(100, 100, 800, 600)  # Ventana más grande
        self.animation = PiAnimation()
        self.setCentralWidget(self.animation)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec())
