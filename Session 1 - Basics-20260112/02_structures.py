# %% [markdown]
# ### Advanced Data Structures

# %%
# Lists

my_list = [1, 2, 3, 4, 5]
print(my_list)

my_list = [1, 3.14, "a", [my_list]]
print(my_list)

# %%
# Example of wrong assignment of lists to variables

# Original list
original_list = [1, 2, 3, 4, 5]

# Assigning the original list to a new variable
copied_list = original_list

# Modifying the copied list
copied_list[0] = 100  # Change the first element of the copied list

# Printing both lists
print("Original List:", original_list)
print("Copied List:", copied_list)


# %%
# Example of using list.copy()

# Original list
original_list = [1, 2, 3, 4, 5]

# Creating a copy of the original list using list.copy()
copied_list = original_list.copy()

# Modifying the copied list
copied_list[0] = 100  # Change the first element of the copied list

# Printing both lists
print("Original List:", original_list)
print("Copied List:", copied_list)

# %%
# Dictionaries

my_dict = {"name": "Alice", "age": 30, "is_student": True}
print("Dictionary:", my_dict)
print("Name:", my_dict["name"])
print("Age:", my_dict.get("age"))

# %%
# Nested dictionary representing a database of students

students = {
    "Alice": {"age": 25, "grade": "A"},
    "Bob": {"age": 30, "grade": "B"},
    "Charlie": {"age": 27, "grade": "A"},
}

# Accessing nested values
print("Alice's age:", students["Alice"]["age"])
print("Bob's grade:", students["Bob"]["grade"])

# %%
# Sets

my_set = {1, 2, 3, 4, 5}
my_set.add(6)
my_set.remove(3)
print("Set:", my_set)

# %%
# Use sets to avoid duplicates

# Define a list with duplicate elements
my_list = [1, 2, 3, 4, 5, 1, 2, 3]

# Convert the list to a set
my_set = set(my_list)

# Print the set
print(my_set)

# %%
# Counter

from collections import Counter

c = Counter("hello world")
print("Character counts:", c)
print("Most common character:", c.most_common(1))


