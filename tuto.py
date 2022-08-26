from qtpy.QtWidgets import (QApplication, QLabel, QWidget,
                            QVBoxLayout, QPushButton)
def say_hello(event):
    print('Hello, world!')

app = QApplication([])

button = QPushButton('Say hello')
button.clicked.connect(say_hello)
# Create label
label = QLabel('Zzzzz')

def say_hello(event):
    label.setText('Hello, world!')

# Create button
button = QPushButton('Press me!')
button.clicked.connect(say_hello)

# Create layout and add widgets
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(button)

# Apply layout to widget
widget = QWidget()
widget.setLayout(layout)

widget.show()

#label.show()
#button.show()


app.exec_()