# filename: hello_world.py

def print_hello_world():
    """Function to print 'Hello, World!' to the console."""
    print("Hello, World!")

if __name__ == "__main__":
    import sys

    # Check if the '--demo' argument is provided
    if len(sys.argv) > 1 and sys.argv[1] == "--demo":
        # Run with demo mode
        print_hello_world()
    else:
        # Normal execution
        print_hello_world()