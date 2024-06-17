import numpy as np

# Define the function 1 / (1 - t)

def f(t):
    return 1 / (1 - t)

t_values_left = np.array([0.9, 0.99, 0.999, 0.9999, 0.99999])  
t_values_right = np.array([1.1, 1.01, 1.001, 1.0001, 1.00001]) 

f_values_left = f(t_values_left)
f_values_right = f(t_values_right)

print("When t < 1:")
for t, value in zip(t_values_left, f_values_left):
    print(f"t = {t}, f(t) = {value}")

print("\nWhen t > 1:")
for t, value in zip(t_values_right, f_values_right):
    print(f"t = {t}, f(t) = {value}")
