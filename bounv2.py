

import sys
from PyQt6.QtCore import Qt, QTimer, QPoint, QRect, QSize
from PyQt6.QtGui import QPainter, QColor, QMouseEvent, QShortcut, QKeySequence
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QFrame

#class BouncingBallWidget(QWidget):
class BouncingBallWidget(QFrame):
    def __init__(self, ancho, alto):
        super().__init__()
        self.ball_radius = 20
        
        # Primer círculo (pelota rebotando)
        self.ball_position = QPoint(50, 50)
        self.ball_velocity = QPoint(5, 5)
        
        # Rectangulo IZQ controlado por el usiario (Teclas W y S)
        self.rect_size_width = 30
        self.rect_size_height = 100
        self.rect_pos = QPoint(1, int(alto/2)-self.rect_size_height)
        self.velocity = QPoint(0, 10)  # QShortcut Velocidad en x y y ## Solo se mueven en Y

        # Rectangulo DER controlado por el usiario (TEclas UP y Down)
        self.rect_size_width2 = 30
        self.rect_size_height2 = 100
        self.rect_pos2 = QPoint(ancho-(self.rect_size_width2*2)+10, int(alto/2)-self.rect_size_height2)
        self.velocity2 = QPoint(0, 10)  # Velocidad en x y y ## Solo se mueven en Y

        # Timer para controlar el movimiento	
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_position)
        self.timer.start(30)  # Actualiza la animación cada 30 ms
        
        self.paused = False
        self.setMinimumSize(ancho-50, alto-50)
    
    def update_position(self):
        # Evento que es llamado cada vez que expira el timer
        if not self.paused:
            # Actualiza la posición de la pelota rebotando
            self.ball_position += self.ball_velocity

            # Rebote en los bordes del widget (parte superior e inferior)
            if self.ball_position.y() - self.ball_radius <= 0 or self.ball_position.y() + self.ball_radius >= self.height():
                self.ball_velocity.setY(-self.ball_velocity.y())

            # Detección de colisión con el rectángulo izquierdo
            rect_izq = QRect(self.rect_pos, QSize(self.rect_size_width, self.rect_size_height))
            if rect_izq.contains(self.ball_position - QPoint(self.ball_radius, 0)):
                self.ball_velocity.setX(abs(self.ball_velocity.x()))  # Rebota hacia la derecha

            # Detección de colisión con el rectángulo derecho
            rect_der = QRect(self.rect_pos2, QSize(self.rect_size_width2, self.rect_size_height2))
            if rect_der.contains(self.ball_position + QPoint(self.ball_radius, 0)):
                self.ball_velocity.setX(-abs(self.ball_velocity.x()))  # Rebota hacia la izquierda

            # Rebote en los bordes izquierdo y derecho de la ventana
            if self.ball_position.x() - self.ball_radius <= 0 or self.ball_position.x() + self.ball_radius >= self.width():
                self.ball_velocity.setX(-self.ball_velocity.x())

            self.update()  # Redibuja el widget

    
    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Dibujar la pelota que rebota (primer círculo)
        painter.setBrush(QColor(0, 100, 200))
        painter.drawEllipse(self.ball_position, self.ball_radius, self.ball_radius)

        # Dibuja el rectangulo izquierdo
        painter.setBrush(QColor(0, 128, 0))  # Color del rectángulo
        painter.drawRect(QRect(self.rect_pos, QSize(self.rect_size_width, self.rect_size_height)))

        # Dibuja el rectangulo derecho
        painter.setBrush(QColor(128, 0, 0))  # Color del rectángulo
        painter.drawRect(QRect(self.rect_pos2, QSize(self.rect_size_width2, self.rect_size_height2)))


    def toggle_pause(self):
        self.paused = not self.paused

    def mousePressEvent(self, event: QMouseEvent):
        # Mueve la pelota que rebota a la posición donde el usuario hace clic
        if event.button() == Qt.MouseButton.LeftButton:
            self.ball_position = event.position().toPoint()
            self.update()  # Redibuja para reflejar la nueva posición
    
#    def keyPressEvent(self, event):
	



class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.Ancho=900
        self.Alto=700
        self.setFixedSize(QSize(self.Ancho, self.Alto))
		
        
        self.ball_widget = BouncingBallWidget(self.Ancho,self.Alto)
        self.ball_widget.setStyleSheet("background-color: cyan;") 

        self.pause_button = QPushButton("Pausar")
        
        self.pause_button.clicked.connect(self.toggle_animation)
        
        layout = QVBoxLayout()
        layout.addWidget(self.ball_widget)
        layout.addWidget(self.pause_button)
        
        self.setLayout(layout)

        # Lo siguiente es para detectar cuando el usuario presina las teclas de flecha
        self.shortcutL = QShortcut(QKeySequence(Qt.Key.Key_Left), self)
        self.shortcutR = QShortcut(QKeySequence(Qt.Key.Key_Right), self)
        self.shortcutU = QShortcut(QKeySequence(Qt.Key.Key_Up), self)
        self.shortcutD = QShortcut(QKeySequence(Qt.Key.Key_Down), self)
        self.shortcutL.activated.connect(self.TeclaIzquierda)
        self.shortcutR.activated.connect(self.TeclaDerecha)
        self.shortcutU.activated.connect(self.TeclaArriba)
        self.shortcutD.activated.connect(self.TeclaAbajo)

    def TeclaArriba(self):
        print ("Tecla Arriba")  
        self.ball_widget.rect_pos2 -= self.ball_widget.velocity2          
        self.update()  # Redibujar después de cada movimiento
    def TeclaAbajo(self):
        print ("Tecla Abajo")  
        self.ball_widget.rect_pos2 += self.ball_widget.velocity2          
        self.update()  # Redibujar después de cada movimiento
        
          
    def TeclaIzquierda(self):
        print ("Tecla izquierda")            
    def TeclaDerecha(self):
        print ("Tecla derecha")            

    
    def toggle_animation(self):
        if self.ball_widget.paused:
            self.pause_button.setText("Pausar")
        else:
            self.pause_button.setText("Reanudar")
        
        self.ball_widget.toggle_pause()

    
    def keyPressEvent(self, event):
        # Los siguientes IFs no JALAN, 
        #if event.key() == Qt.Key.Key_Left.value:
        #    print ("Left")
        #elif event.key() == Qt.Key.Key_Up.value:
        #    print ("Up")		
        #elif event.key() == Qt.Key.Key_Down.value:
        #    print ("Down")		
        #elif event.key() == Qt.Key.Key_Right.value:
        #    print ("Right")	      

        if event.key() == Qt.Key.Key_Escape.value:
            self.close()
        # Movimiento del segundo círculo con WASD
        if event.key() == Qt.Key.Key_W:  # Mover hacia arriba
            self.ball_widget.rect_pos -= self.ball_widget.velocity
        elif event.key() == Qt.Key.Key_S:  # Mover hacia abajo
            self.ball_widget.rect_pos += self.ball_widget.velocity
            XX=1
        elif event.key() == Qt.Key.Key_A:  # Mover hacia la izquierda
            XX=1
        elif event.key() == Qt.Key.Key_D:  # Mover hacia la derecha
            XX=1

        self.update()  # Redibujar después de cada movimiento



def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.setWindowTitle("Bouncing Ball with WASD Control")
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
