# filename: simple_calculator.py

import sys

def add(a, b):
    """Return the sum of a and b."""
    return a + b

def subtract(a, b):
    """Return the difference of a and b."""
    return a - b

def multiply(a, b):
    """Return the product of a and b."""
    return a * b

def divide(a, b):
    """Return the quotient of a and b. Raises ValueError if b is zero."""
    if b == 0:
        raise ValueError("Cannot divide by zero.")
    return a / b

def calculator():
    """Simple calculator that performs addition, subtraction, multiplication, and division."""
    print("Welcome to the Simple Calculator!")
    print("Please select an operation:")
    print("1. Add")
    print("2. Subtract")
    print("3. Multiply")
    print("4. Divide")

    operation = input("Enter the operation number (1/2/3/4): ")
    num1 = float(input("Enter the first number: "))
    num2 = float(input("Enter the second number: "))

    if operation == '1':
        print(f"{num1} + {num2} = {add(num1, num2)}")
    elif operation == '2':
        print(f"{num1} - {num2} = {subtract(num1, num2)}")
    elif operation == '3':
        print(f"{num1} * {num2} = {multiply(num1, num2)}")
    elif operation == '4':
        try:
            print(f"{num1} / {num2} = {divide(num1, num2)}")
        except ValueError as e:
            print(e)
    else:
        print("Invalid operation selected.")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Run with sample inputs in demo mode
        print("Demo mode: Performing a series of calculations.")
        print("1. Add 5 and 3")
        print(f"Result: {add(5, 3)}")
        print("2. Subtract 10 from 6")
        print(f"Result: {subtract(10, 6)}")
        print("3. Multiply 4 and 7")
        print(f"Result: {multiply(4, 7)}")
        print("4. Divide 8 by 2")
        try:
            print(f"Result: {divide(8, 2)}")
        except ValueError as e:
            print(e)
    else:
        calculator()