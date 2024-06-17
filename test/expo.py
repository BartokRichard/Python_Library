import numpy as np

# Define an exponential function
def exp_f(t):
    return 2**t

# Choose t values that show exponential growth
t_values = np.array([0, 1, 2, 3, 4, 5])

# Calculate the function values for exponential growth
exp_values = exp_f(t_values)

# Print the results
print("Exponential Growth:")
for t, value in zip(t_values, exp_values):
    print(f"t = {t}, exp_f(t) = {value}")
