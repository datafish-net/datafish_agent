# filename: fibonacci_sequence.py

def fibonacci(n):
    """
    Calculate the Fibonacci sequence up to the n-th term.

    Parameters:
    n (int): The number of terms in the Fibonacci sequence to return.

    Returns:
    list: A list containing the Fibonacci sequence up to the n-th term.
    """
    if n <= 0:
        return []  # Return an empty list for non-positive input
    elif n == 1:
        return [0]  # The first term of Fibonacci sequence
    elif n == 2:
        return [0, 1]  # The first two terms of Fibonacci sequence

    # Initialize the Fibonacci sequence with the first two terms
    fib_sequence = [0, 1]
    
    # Calculate the Fibonacci terms and append them to the list
    for i in range(2, n):
        next_term = fib_sequence[i - 1] + fib_sequence[i - 2]
        fib_sequence.append(next_term)

    return fib_sequence

# Example usage
if __name__ == "__main__":
    num_terms = 10  # Specify how many terms of the Fibonacci sequence to calculate
    result = fibonacci(num_terms)
    print(f"Fibonacci sequence up to {num_terms} terms: {result}")