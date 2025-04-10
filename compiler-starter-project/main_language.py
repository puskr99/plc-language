import sys
from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWidgets import QMainWindow, QLineEdit, QPushButton, QTextEdit

from components.lexica import Lexer
from components.parsers import Parser, ASTParser
from components.memory import Memory

class MainWindow(QMainWindow):

    # Do this for intellisense
    input_code: QLineEdit
    run_button: QPushButton
    output_console: QTextEdit
    clear_button: QPushButton

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./components/main_language.ui", self)

        #### Binding button to function ####
        self.run_button.clicked.connect(self.execute_code)

        # Ensure the output console is read-only
        self.output_console.setReadOnly(True)
        self.clear_button.clicked.connect(self.output_console.clear)

    def execute_code(self):
        self.output_console.clear()
        print("Running code...")
        parser = ASTParser(self.output_console)
        memory = Memory()

        # Retrieve the input code
        input_text = str(self.code_input.toPlainText())
        lexer:Lexer = Lexer()

        try:
            # Parse and execute the code
            tokens = lexer.tokenize(input_text)
            result = parser.parse(tokens)
            
            # Display results in the output console
            # for val in result:
            #     self.output_console.append(str(val))

        except Exception as e:
            # Handle and display any errors
            self.output_console.append(f"Error: {str(e)}")

        # For debugging purposes
        print(memory)
        memory.reset_memory()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
