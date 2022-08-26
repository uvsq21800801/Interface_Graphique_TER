from email.charset import QP
import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton
from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, 
                             QApplication, QPushButton)
import matplotlib.pyplot as plt


class AppDemo(QMainWindow):
    def __init__(self, t_min, t_max):
        super().__init__()


        self.centralwidget = QWidget()
        self.setCentralWidget(self.centralwidget)
        self.lay = QVBoxLayout(self.centralwidget)
        #self.setText('Launch Chart')
        self.setStyleSheet('font-size: 40px;')
        self.resize(1200,800)
        
        for i in range(t_min, t_max):
            self.btn = QPushButton('Button {}'.format(i +1), self)            
            text = self.btn.text()
            self.btn.clicked.connect(lambda ch, text=text : print("\nclicked--> {}".format(text)))
            self.lay.addWidget(self.btn)
        
        self.numButton = 4

        pybutton = QPushButton('Create a button', self)
        pybutton.clicked.connect(self.clickMethod)

        self.lay.addWidget(pybutton)
        self.lay.addStretch(1)

        #self.clicked.connect(self.update_graph)

    def clickMethod(self):
        newBtn = QPushButton('New Button{}'.format(self.numButton), self)
        self.numButton += 1
        newBtn.clicked.connect(lambda : print("\nclicked===>> {}".format(newBtn.text())))
        self.lay.addWidget(newBtn)

    def update_graph(self):
        fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, figsize=(6,6), dpi=200)
        plt.subplots_adjust(hspace=0)

        x = range(0,10)
        y1 = range(0,10)
        y2 = range(0,10)
        ax1.plot(x,y1)
        ax2.plot(x, y2)

        plt.show()

def display(t_min, t_max):
    app = QApplication(sys.argv)

    demo = AppDemo(t_min, t_max)
    demo.show()

    app.exit(app.exec_())