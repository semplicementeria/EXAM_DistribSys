# %% [markdown]
# ### Functional Programming in Python

# %%
# Higher-order functions
def square(x):
    return x * x

numbers = [1, 2, 3, 4, 5]
squared_numbers = list(map(square, numbers))
print("Squared numbers:", squared_numbers)

# %%
# Lambda expressions
double = lambda x: x * 2
print("Double of 5:", double(5))

# %%
# functools module

from functools import reduce, lru_cache

product_all = reduce(lambda x, y: x * y, numbers)
print("Sum of all numbers:", product_all)

# %%
# Example of using lru_cache() to memorize a recursive function

@lru_cache(maxsize=None)
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# Calculate Fibonacci numbers efficiently with caching
print("Fibonacci(10):", fibonacci(10))  # Output: 55


# %%
# Example of caching results of an expensive function
import time

@lru_cache(maxsize=128)
def expensive_calculation(n):
    # Simulate expensive computation
    time.sleep(3)
    return n * 2

# Calculate and cache results of expensive calculations
print("Result 1:", expensive_calculation(10))  # Takes 3 seconds
print("Result 2:", expensive_calculation(10))  # Cached result, takes no time


# %%
# Example of limiting the size of the cache

@lru_cache(maxsize=3)
def square(x):
    return x ** 2

# Cache size is limited to 3
print("Square of 2:", square(2))
print("Square of 3:", square(3))
print("Square of 4:", square(4))  # Cached result, cache size is still 3
print("Square of 5:", square(5))  # Least recently used result is evicted from cache


