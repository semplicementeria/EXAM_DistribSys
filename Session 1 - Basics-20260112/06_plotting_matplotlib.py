# %% [markdown]
# ### Data Visualization with Matplotlib

# %%
# Import necessary libraries
import numpy as np
import matplotlib.pyplot as plt

# Generate some sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a figure and axis object
plt.figure(figsize=(10, 6))

# Line plot
plt.subplot(2, 2, 1)
plt.plot(x, y)
plt.title("Line Plot")
plt.xlabel("Radians")
plt.ylabel("sin(x)")
plt.grid(True)

# Set ticks at multiples of pi/2
plt.xticks(
    np.linspace(0, 3 * np.pi, 7),
    [
        "0",
        r"$\frac{\pi}{2}$",
        r"$\pi$",
        r"$\frac{3\pi}{2}$",
        r"$2\pi$",
        r"$\frac{5\pi}{2}$",
        r"$3\pi$",
    ],
)

# Scatter plot
plt.subplot(2, 2, 2)
plt.scatter(x, y, color="red", label="Data Points")
plt.title("Scatter Plot")
plt.xlabel("X-axis")
plt.ylabel("Y-axis")
plt.legend()
plt.grid(True)

# Histogram
data = np.random.normal(loc=0, scale=1, size=1000)
plt.subplot(2, 2, 3)
plt.hist(data, bins=30, color="green", alpha=0.5)
plt.title("Histogram")
plt.xlabel("Value")
plt.ylabel("Frequency")
plt.grid(True)

# Bar plot
categories = ["A", "B", "C", "D", "E"]
values = [20, 35, 30, 25, 40]
plt.subplot(2, 2, 4)
plt.bar(categories, values, color="blue", alpha=0.7)
plt.title("Bar Plot")
plt.xlabel("Categories")
plt.ylabel("Values")
plt.grid(True)

# Adjust layout
plt.tight_layout()

# Show the plots
plt.show()


