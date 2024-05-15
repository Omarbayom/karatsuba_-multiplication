import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QLabel, QTextEdit
from PyQt5.QtGui import QIcon, QFont

class VirtualKeyboard(QWidget):
    def __init__(self, target=None):
        super().__init__()
        self.target = target
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        buttons = [
            ('1', '2', '3'),
            ('4', '5', '6'),
            ('7', '8', '9'),
            ('', '0', ''),  # Empty string for the middle button
            ('Clear',)
        ]

        for row in buttons:
            h_layout = QHBoxLayout()
            for char in row:
                if char:
                    button = QPushButton(char)
                    button.setFont(QFont("Arial", 16))
                    button.clicked.connect(lambda _, ch=char: self.emitCharacter(ch))
                    h_layout.addWidget(button)
            layout.addLayout(h_layout)

        self.setLayout(layout)

    def emitCharacter(self, char):
        if char == 'Clear':
            if self.target:
                self.target.backspace()  # Clear one character from the end
        else:
            if self.target:
                self.target.insert(char)

class KaratsubaGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Karatsuba Multiplication')
        self.setWindowIcon(QIcon('addaccount5.ico'))  
        self.setGeometry(100, 100, 400, 400)

        layout = QVBoxLayout()

        self.num1_label = QLabel('First Number:', self)
        self.num1_input = QLineEdit(self)

        self.num2_label = QLabel('Second Number:', self)
        self.num2_input = QLineEdit(self)

        self.result_label = QLabel('Result:', self)
        self.result_output = QLineEdit(self)
        self.result_output.setReadOnly(True)

        self.num1_input.setPlaceholderText("Enter numbers here")
        self.num2_input.setPlaceholderText("Enter numbers here")

        self.result_steps_label = QLabel('Steps:', self)
        self.result_steps_output = QTextEdit(self)
        self.result_steps_output.setReadOnly(True)

        self.calculate_button = QPushButton('Calculate', self)
        self.calculate_button.clicked.connect(self.calculate)

        self.num1_keyboard = VirtualKeyboard(target=self.num1_input)
        self.num2_keyboard = VirtualKeyboard(target=self.num2_input)

        layout.addWidget(self.num1_label)
        layout.addWidget(self.num1_input)
        layout.addWidget(self.num1_keyboard)

        layout.addWidget(self.num2_label)
        layout.addWidget(self.num2_input)
        layout.addWidget(self.num2_keyboard)

        layout.addWidget(self.result_label)
        layout.addWidget(self.result_output)
        layout.addWidget(self.result_steps_label)
        layout.addWidget(self.result_steps_output)
        layout.addWidget(self.calculate_button)

        self.setLayout(layout)

    def calculate(self):
        num1 = self.num1_input.text()
        num2 = self.num2_input.text()

        try:
            result, _, _, _, steps = perform_multiplication(int(num1), int(num2))
            self.result_output.setText(str(result))
            self.result_steps_output.setText(steps + f"\nFinal Result: {result}")
        except ValueError:
            self.result_output.setText("Error")
            self.result_steps_output.setText("Please enter valid numbers")

def perform_multiplication(x, y, step=''):
    # Convert the input strings to integers if they are not already
    if not isinstance(x, int):
        x = int(x)
    if not isinstance(y, int):
        y = int(y)

    # Base case: if either x or y is a single digit number, return their product
    if x < 10 or y < 10:
        return x * y, x * y, x * y, x * y, step

    # Determine the number of digits in the larger number
    n = max(len(str(x)), len(str(y)))

    # Split the numbers into halves
    m = n // 2

    # Split x and y into halves
    high1, low1 = divmod(x, 10**m) 
    high2, low2 = divmod(y, 10**m)
    # Recursively compute the three products needed for Karatsuba's algorithm
    z0, _, _, _, step_z0 = perform_multiplication(low1, low2, step=f"{step} - Step 1: Calculate z0 = {low1} * {low2}\n")
    z1, _, _, _, step_z1 = perform_multiplication((low1 + high1), (low2 + high2), step=f"{step} - Step 2: Calculate z1 = ({low1} + {high1}) * ({low2} + {high2})\n" if step.count("Step 2") == 0 else "")
    z2, _, _, _, step_z2 = perform_multiplication(high1, high2, step=f"{step} - Step 3: Calculate z2 = {high1} * {high2}\n")

    # Apply the formula for Karatsuba multiplication
    result = (z2 * pow(10,2*m)) + ((z1 - z2 - z0) * pow(10,m)) + z0



    return result, z0, z1, z2, step + step_z0 + step_z1 + step_z2

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = KaratsubaGUI()
    window.show()
    sys.exit(app.exec_())
