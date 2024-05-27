def generate_fibonacci_sequence(num_terms):

    fibonacci_sequence = [0, 1]

    for _ in range(2, num_terms):
        next_number = fibonacci_sequence[-1] + fibonacci_sequence[-2]
        fibonacci_sequence.append(next_number)

    return fibonacci_sequence

def main():
    num_terms = int(input("Enter the number of Fibonacci terms to generate: "))
    fibonacci_sequence = generate_fibonacci_sequence(num_terms)
    
    print("Fibonacci sequence:")
    for term in fibonacci_sequence:
        print(term, end=" ")

if __name__ == "__main__":
    main()
