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
    if_else_button: QPushButton
    while_button: QPushButton
    function_button: QPushButton
    basic_ex_button: QPushButton

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        uic.loadUi("./components/main_language.ui", self)

        #### Binding button to function ####
        self.run_button.clicked.connect(self.execute_code)

        # Ensure the output console is read-only
        self.output_console.setReadOnly(True)
        # self.output_console.setStyleSheet("QTextEdit { color: red; }")
        self.clear_button.clicked.connect(lambda: (self.output_console.clear(), self.code_input.clear()))

        self.basic_ex_button.clicked.connect(lambda: self.add_examples(1))
        self.if_else_button.clicked.connect(lambda: self.add_examples(2))
        self.while_button.clicked.connect(lambda: self.add_examples(3))
        self.function_button.clicked.connect(lambda: self.add_examples(4))

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
            # print("Tokens are  ")
            # for i in tokens:
            #     print(i)
            result = parser.parse(tokens)
            print("Result is this", result)
            parser.execute(result)
            
            # Display results in the output console
            # for val in result:
            #     self.output_console.append(str(val))

        except Exception as e:
            # Handle and display any errors
            self.output_console.append(f"Error: {str(e)}")

        # For debugging purposes
        print(memory)
        memory.reset_memory()

    def add_examples(self, button: int):
        if button == 1:
            code = """int a = 10;
float b = 10.5;
string c = "hello";
print(a+10);
print(b+1.1);
print(c+" world");
            """
            self.code_input.append(code)

        elif button == 2:
            code = """int num = 5;
if (num > 0) {
    print("Number is positive");
} else {
    print("Number is negative or zero");
}
    """
            self.code_input.append(code)

        elif button == 3:
            code = """int i = 1;
while (i <= 5) {
    print(i);
    i = i + 1;
}
    """
            self.code_input.append(code)

        elif button == 4:
            code = """int func swap(int x, int y) {
        int temp = x;
        x = y;
        y = temp;
    }
int p = 10;
int q = 20;
swap(p, q);
print(p);
print(q);
    """
            self.code_input.append(code)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
