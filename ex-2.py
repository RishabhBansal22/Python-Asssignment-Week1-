# Exercise 2: Prime Number Generator (20 points) 
# Write a program that: 
# 1. Takes two positive integers as input (range start and end) 
# 2. Validates the input (must be positive integers) 
# 3. Finds all prime numbers within the given range (inclusive) 
# 4. Displays the primes in a formatted output (10 numbers per line) 
# 5. Handles invalid inputs gracefully


class PrimeNumberGen:
    """A class to generate and display prime numbers within a given range."""
    
    def validate_ints(self, start_num: int, end_num: int):
        """
        Validates that the input numbers are positive and start is less than end.
        Returns 'valid', 'validation_error', or 'range_error'.
        """
        # Check if both numbers are positive
        if not (start_num > 0 and end_num > 0):
            return "validation_error"
        # Check if start is less than end
        if not (start_num < end_num):
            return "range_error"
        return "valid"
    
    def is_prime(self, num):
        """
        Checks if a number is prime.
        Returns True if prime, False otherwise.
        """
        # Numbers less than 2 are not prime
        if num < 2:
            return False
        # 2 is the only even prime number
        if num == 2:
            return True
        # Even numbers greater than 2 are not prime
        if num % 2 == 0:
            return False
        
        # Check odd divisors up to square root of num
        # This is efficient because if num has a divisor greater than sqrt(num),
        # it must also have a corresponding divisor less than sqrt(num)
        for i in range(3, int(num ** 0.5) + 1, 2):
            if num % i == 0:
                return False
        return True
    
    def find_primes(self, start_num, end_num):
        """
        Finds all prime numbers in the given range (inclusive).
        Returns a list of prime numbers.
        """
        primes = []
        # Loop through each number in the range
        for num in range(start_num, end_num + 1):
            if self.is_prime(num):
                primes.append(num)
        return primes
    
    def display_primes(self, primes):
        """
        Displays the list of prime numbers in a formatted output.
        Shows 10 numbers per line.
        """
        # Check if any primes were found
        if not primes:
            print("No prime numbers found in the given range.")
            return
        
        # Display header with count
        print(f"\nFound {len(primes)} prime number(s):")
        print("-" * 60)
        
        # Print each prime number
        for i, prime in enumerate(primes):
            print(f"{prime:6}", end="")  # 6-character width for alignment
            # Print 10 numbers per line
            if (i + 1) % 10 == 0:
                print()
        print()  # Final newline
    
    def run(self):
        """
        Main method to run the prime number generator program.
        Handles user input, validation, and display.
        """
        print("Prime Number Generator")
        print("=" * 60)
        
        try:
            # Get input from user
            start_input = input("Enter the start of the range: ")
            end_input = input("Enter the end of the range: ")
            
            # Try to convert to integers
            start_num = int(start_input)
            end_num = int(end_input)
            
            # Validate the inputs
            validation_result = self.validate_ints(start_num, end_num)
            
            # Handle validation errors
            if validation_result == "validation_error":
                print("Error: Both numbers must be positive integers!")
                return
            
            if validation_result == "range_error":
                print("Error: Start number must be less than end number!")
                return
            
            # Find and display primes
            print(f"\nSearching for primes between {start_num} and {end_num}...")
            primes = self.find_primes(start_num, end_num)
            self.display_primes(primes)
            
        except ValueError:
            # Handle non-integer input
            print("Error: Please enter valid integer values!")
        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print("\n\nProgram interrupted by user.")
        except Exception as e:
            # Handle any other unexpected errors
            print(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    generator = PrimeNumberGen()
    generator.run()
    

