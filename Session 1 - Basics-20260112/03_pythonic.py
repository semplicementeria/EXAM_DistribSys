# %% [markdown]
# ### Pythonic Coding Techniques

# %%
# List comprehensions

numbers = list(range(10))
print("Numbers:", numbers)

numbers = [n for n in range(10)]
print("Numbers:", numbers)


# %%
# List Comprehension Example

# Suppose we have a list of numbers and we want to create a new list
# containing the squares of each number

# Traditional approach using a for loop
numbers = [1, 2, 3, 4, 5]
squares = []
for num in numbers:
    squares.append(num ** 2)
print("Squares (Traditional):", squares)

# Using list comprehension
squares_comp = [num ** 2 for num in numbers]
print("Squares (Comprehension):", squares_comp)

# Another example: filtering even numbers
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

# Traditional approach using a for loop
even_numbers = []
for num in numbers:
    if num % 2 == 0:
        even_numbers.append(num)
print("Even Numbers (Traditional):", even_numbers)

# Using list comprehension
even_numbers_comp = [num for num in numbers if num % 2 == 0]
print("Even Numbers (Comprehension):", even_numbers_comp)

# %%
# Filtering dictionary based on a condition

original_dict = {"a": 1, "b": 2, "c": 3, "d": 4}
filtered_dict = {k: v for k, v in original_dict.items() if v % 2 == 0}
print("Filtered Dictionary:", filtered_dict)

# %%
# Dictionary Comprehension Example

# Suppose we have a list of students and their corresponding grades
students = ["Alice", "Bob", "Charlie"]
grades = [85, 90, 75]

# We want to create a dictionary where the keys are the students' names
# and the values are their grades

# Traditional approach using a for loop
grade_dict = {}
for i in range(len(students)):
    grade_dict[students[i]] = grades[i]
print("Grade Dictionary (Traditional):", grade_dict)

# Using dictionary comprehension
grade_dict_comp = {students[i]: grades[i] for i in range(len(students))}
print("Grade Dictionary (Comprehension):", grade_dict_comp)

# Another example: converting Celsius temperatures to Fahrenheit
celsius_temps = {"Monday": 20, "Tuesday": 25, "Wednesday": 22}

# Formula to convert Celsius to Fahrenheit: F = C * 9/5 + 32
fahrenheit_temps = {day: (temp * 9/5) + 32 for day, temp in celsius_temps.items()}
print("Fahrenheit Temperatures:", fahrenheit_temps)

# %%
# Generator expressions

squares = (x**2 for x in range(5))
print(squares)
print("Square:", next(squares))
print("Square:", next(squares))
print("Square:", next(squares))


# %%
# Decorators

def uppercase_decorator(func):
    def wrapper(name):
        result = func(name)
        return result.upper()
    return wrapper

@uppercase_decorator
def greet(name):
    return "Hello, " + name

print(greet("Bob"))

# %%
# Decorator to measure execution time
import time

def measure_execution_time(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time of '{func.__name__}': {execution_time:.6f} seconds")
        return result
    return wrapper

# Example function to be measured
@measure_execution_time
def example_function(n):
    # Simulate some computation
    sum_value = sum(range(n))
    return sum_value

# Call the example function and measure its execution time
result = example_function(1000000)
print("Result of example function:", result)

# %%
# Context Managers

with open("example.txt", "w") as f:
    f.write("Hello, context managers!")

with open("example.txt") as f:
    content = f.read()

print(content)


