# WSP Programming Language

This document serves as a guide for using and understanding the WSP programming language. The language supports basic data types, functions, control structures (if, while), and basic operations like arithmetic and string concatenation.

---

## How to Run

### Running in Remote Container
Follow these steps to get started:

1. Open the project in a remote container.
2. Launch the application:
   ```sh
   pdm run app
   ```
3. To open the UI designer:
   ```sh
   pdm run ui
   ```

---

## Requirements
Make sure you have the necessary dependencies installed via:
```sh
pdm install
```

---

## Features

### 1. Data Types

* **int**: Integer values.
* **float**: Floating-point values.
* **string**: Textual data.
* **bool**: Boolean values (`true`, `false`).

### 2. Operations

* Arithmetic: `+`, `-`, `*`, `/`
* String Concatenation: `+`

### 3. Control Structures

* **if**: Conditional execution.
* **while**: Loop execution based on a condition.

### 4. Functions

* Functions can return values and accept parameters of any supported type.
* Functions can include nested logic such as `if` and `while` statements.

---

## Example Programs

### Simple Arithmetic Function

```text
int func addNumbers(int a, int b) {
    return a + b;
}
```

### Conditional Example (If-Else)

```text
string func checkNumber(int num) {
    if (num > 0) {
        return "Positive";
    } else {
        return "Negative or Zero";
    }
}
```

### While Loop Example

```text
int func sumToN(int n) {
    int sum = 0;
    int i = 1;
    while (i <= n) {
        sum = sum + i;
        i = i + 1;
    }
    return sum;
}
```

### String Concatenation

```text
string func concatenateStrings(string str1, string str2) {
    string result = str1 + str2;
    return result;
}
```

---

## Using the Language

### Writing Code

Write your program using the supported syntax and save it in the editor.

### Running the Code

1. Enter your code in the editor section of the application.
2. Click the **Run** button.
3. View the output in the console on the right-hand side.

### Error Handling

* Ensure all variable declarations and functions have valid names.
* The parser will report any syntax errors encountered.
* Empty code submissions will result in a warning.

---

## UI Overview

The application provides an intuitive interface:

* **Code Editor (Left Panel)**: Write your code here.
* **Output Console (Right Panel)**: Displays results or errors.
* **Run Button**: Executes the code entered in the editor.
* **Clear Button**: Clears the output console.

---

## Tips

* Avoid using unsupported operators (e.g., `%`).
* Use meaningful names for functions and variables to improve code readability.
* Debugging: Add print statements to trace variable values.

---
