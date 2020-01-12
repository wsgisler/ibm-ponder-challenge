from scipy import optimize

# First we prepare sample values which we will use for the curve fitting
start_value = -1
end_value = 1
increment = 0.001
number_of_test_values = int((end_value-start_value)/increment)+1
test_values = [i*increment+start_value for i in range(number_of_test_values)]

# Then, we define a mathematical function which we think could fit the curve fitting problem
# This takes some trying. Obviously, the abs(x) function is symmetrical, so it makes sense to avoid x^3, x^5 etc. in the function
def f(x, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11):
    return (x**2*x2 + x**4*x4 + x8)/(x**2*x10 + x11)
    
# Let's also add a method to print the function
def write_f(x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11):
    return_string = '('
    if x1 != 0:
        return_string += str(x1)+"*x+"
    if x2 != 0:
        return_string += str(x2)+"*x*x+"
    if x3 != 0:
        return_string += str(x3)+"*x*x*x+"
    if x4 != 0:
        return_string += str(x4)+"*x*x*x*x+"
    if x5 != 0:
        return_string += str(x5)+"*x*x*x*x*x+"
    if x6 != 0:
        return_string += str(x6)+"*x*x*x*x*x*x+"
    if x7 != 0:
        return_string += str(x7)+"*x*x*x*x*x*x*7+"
    if x8 != 0:
        return_string += str(x8)
    return_string += ')/('
    if x9 != 0:
        return_string += str(x9)+"*x+"
    if x10 != 0:
        return_string += str(x10)+"*x*x+"
    if x11 != 0:
        return_string += str(x11)
    return_string += ')'
    return_string = return_string.replace('+-','-')
    return_string = return_string.replace('+)',')')
    return return_string

# Generate the list of test values
x = test_values
y = [abs(x) for x in test_values]

# Use the Scipy curve fitting algorithm to find the best function parameters
p, params_cov = optimize.curve_fit(f, x, y, p0 = [0, 0.8, 0, 0, 0, 0, 0, 0.2, 0, 1000, 1000])

# Calculate the MSE and print it
mse = sum([(abs(x)-f(x, p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10]))**2 for x in test_values])/number_of_test_values
print(mse)

# Print the approximation method
f_string = write_f(p[0], p[1], p[2], p[3], p[4], p[5], p[6], p[7], p[8], p[9], p[10])
print(f_string)
print(f_string.count('*') + f_string.count('+') + f_string.count('/') + f_string.count('-'))
