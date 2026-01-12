# %% [markdown]
# ### Python Basics

# %%
# Basic data types
x = 10              # Integer
y = 3.14            # Float
z = "Hello, world!" # String
is_student = True   # Boolean

# Basic operations
sum_result = x + y
concat_result = z + " How are you?"
is_student_str = str(is_student) # Convert boolean to string

print("Sum:", sum_result)
print("Concatenation:", concat_result)
print("Is student?", is_student_str)

# %%
# Using different methods for string formatting

name = "Alice"
age = 30

# Old style formatting
message_old = "Hello, %s! You are %d years old." % (name, age)

# New style formatting
message_new = "Hello, {}! You are {} years old.".format(name, age)

# f-Strings (Python 3.6+)
message_fstring = f"Hello, {name}! You are {age} years old."

# Print all messages
print("Old Style Formatting:", message_old)
print("New Style Formatting:", message_new)
print("f-Strings:", message_fstring)

# %%
# Example of str.join()

# List of strings
words = ["Hello", "world", "Python", "is", "awesome"]

# Joining the list of strings into a single string using str.join()
sentence = " ".join(words)

# Printing the joined string
print("Joined Sentence:", sentence)

# %%
# Example of iterating over a string

# Original string
my_string = "Hello, world!"

# Iterate over the characters of the string using a for loop
print("Iterating over characters using a for loop:")
for char in my_string:
    print(char)

# %%
# Example of string replacement

# Original string
original_string = "The quick brown fox jumps over the lazy dog."

# Replace a substring
new_string = original_string.replace("brown", "red")

# Print the original and modified strings
print("Original string:", original_string)
print("Modified string:", new_string)

# %%
# Example of string stripping

# Original string with leading and trailing whitespace
original_string = "   Hello, world!   "

# Strip leading and trailing whitespace
stripped_string = original_string.strip()

# Print the original and stripped strings
print("Original string:", original_string)
print("Stripped string:", stripped_string)

# %%
# Example of string splitting

# Original string
sentence = "This is a sample sentence."

# Split the string into words using whitespace as the delimiter
words = sentence.split()

# Print the list of words
print("List of words:", words)

# Split the string into words using a custom delimiter (e.g., comma)
csv_string = "apple,banana,orange"
fruits = csv_string.split(',')
print("List of fruits:", fruits)


# %%
# Control Structures
for i in range(5):
    if i % 2 == 0:
        print(i, "is even")
    else:
        print(i, "is odd")

# %%
# Functions and Modules
def greet(name):
    print("Hello,", name)

greet("Alice")

# %%
import math

print("Square root of 16:", math.sqrt(16))


