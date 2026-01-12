# %%
# Example of handling division by zero
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Error: Division by zero!")

# %%
# Example of handling file not found error
try:
    with open("nonexistent_file.txt", "r") as file:
        contents = file.read()
except FileNotFoundError:
    print("Error: File not found!")

# %%
# Example of handling IndexError
try:
    my_list = [1, 2, 3]
    print(my_list[4])
except IndexError:
    print("Error: Index out of range!")

# %%
# Example of handling multiple exceptions

my_dict = {
    f"key{i}": i for i in range(10)
}

try:
    value = my_dict["key3"] / 0
except KeyError:
    print("Error: Key not found!")
except ZeroDivisionError:
    print("Error: Division by zero!")


