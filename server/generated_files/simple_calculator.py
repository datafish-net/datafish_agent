# filename: simple_calculator.py

import sys

def add(x, y):
    """Return the sum of x and y."""
    return x + y

def subtract(x, y):
    """Return the difference of x and y."""
    return x - y

def multiply(x, y):
    """Return the product of x and y."""
    return x * y

def divide(x, y):
    """Return the quotient of x and y. Raises ValueError if y is zero."""
    if y == 0:
        raise ValueError("Cannot divide by zero.")
    return x / y

def calculator(operation, x, y):
    """Perform the specified operation on x and y."""
    if operation == 'add':
        return add(x, y)
    elif operation == 'subtract':
        return subtract(x, y)
    elif operation == 'multiply':
        return multiply(x, y)
    elif operation == 'divide':
        return divide(x, y)
    else:
        raise ValueError("Invalid operation. Use 'add', 'subtract', 'multiply', or 'divide'.")

def main():
    """Main function to take user input and perform calculations."""
    print("Simple Calculator")
    operation = input("Enter operation (add, subtract, multiply, divide): ").strip().lower()
    x = float(input("Enter first number: "))
    y = float(input("Enter second number: "))
    
    try:
        result = calculator(operation, x, y)
        print(f"The result of {operation}ing {x} and {y} is: {result}")
    except ValueError as e:
        print(e)

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Demo mode with sample inputs
        print("Demo mode activated.")
        demo_operations = [
            ('add', 5, 3),
            ('subtract', 10, 4),
            ('multiply', 7, 6),
            ('divide', 8, 2),
            ('divide', 8, 0)  # This will raise an error
        ]
        
        for operation, x, y in demo_operations:
            try:
                result = calculator(operation, x, y)
                print(f"The result of {operation}ing {x} and {y} is: {result}")
            except ValueError as e:
                print(f"Error: {e}")
                
    else:
        main()