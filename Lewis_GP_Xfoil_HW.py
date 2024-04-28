# Talon Lewis
# I found it kinda funny when I learned about the xfoil github code via youtube prior to receiving and reading the email sent 
# with a link to it. Youtube university wins agian.

# For some reason, naca9010 does not want to work. If you run this and the system freezes on this naca, or anyothers, then restart.
# Do not give up hope, you will eventually land on somethign that will work. 

# if you need to, feel free to delete naca dat files.
# press run cell
#%%
import os
import subprocess
import numpy as np
import time

import numpy as np 
import GPyOpt 
from GPyOpt.methods import BayesianOptimization
import matplotlib.pyplot as plt

# Clean directory from previosly ran trials
if os.path.exists("polar_file.txt"):
    os.remove("polar_file.txt")
if os.path.exists("inputDAT.in"):
    os.remove("inputDAT.in")
if os.path.exists("input_file.in"):
    os.remove("input_file.in")


# x needs to be equal to [thickness, camber]

def objective_function(x):
    thickness, camber, camPos=x[:,0], x[:,1],x[:,2]      # , x[:,2]
    tempNum = f'{int(camber*100)}{int(camPos*10)}{int(thickness*100)}'
    airfoil_name = f'naca{tempNum}'

    if os.path.exists(f"{airfoil_name}.dat"):
        os.remove(f"{airfoil_name}.dat")

    # Inputs
    alpha_i = 0
    alpha_f = 20
    alpha_step = 1
    n_iter = 100
    Re = 1000000 # This may be messing up scaling of l/d ratios

    #create new dat file
    inputDAT = open("inputDAT.in", 'w')
    inputDAT.write(f"naca {tempNum}\n")
    inputDAT.write(f"save\n")
    inputDAT.write(f"{airfoil_name}.dat\n")
    inputDAT.write("quit\n")
    inputDAT.close()
    subprocess.call("xfoil.exe < inputDAT.in", shell=True)

    input_file = open("input_file.in", 'w')
    input_file.write(f"LOAD {airfoil_name}.dat\n")
    input_file.write(airfoil_name + '\n')
    input_file.write("PANE\n")
    input_file.write("OPER\n")
    input_file.write("Visc {0}\n".format(Re))
    input_file.write("PACC\n")
    input_file.write("polar_file.txt\n\n")
    input_file.write("ITER {0}\n".format(n_iter))
    input_file.write("ASeq {0} {1} {2}\n".format(alpha_i, alpha_f,
                                                alpha_step))
    input_file.write("\n\n")
    input_file.write("quit\n")
    input_file.close()

    subprocess.call("xfoil.exe < input_file.in", shell=True)

    polar_data = np.loadtxt("polar_file.txt", skiprows=12)

    if os.path.exists(f"{airfoil_name}.dat"):
        os.remove(f"{airfoil_name}.dat")

    # Evaluate and pull data from polar file
    CL_values = []
    CD_values = []
    alphaVAL = []
    rowNum = 1
    
    
    with open('polar_file.txt', 'r') as file:
    # Read each line in the file
        for line in file:
            # print(line)
            components = line.split()    # Split the line into components

            if len(components) == 0:  # Check if the line contains data and is not blank
                rowNum += 1
                continue

            if rowNum >= 13:       #row 13 is usually where data is first pulled 
                # Extract CL and CD values and convert them to float
                CL = float(components[1])
                CD = float(components[2])
                alpha = float(components[0])
                # Append CL and CD values to their respective lists
                CL_values.append(CL)
                CD_values.append(CD)
                alphaVAL.append(alpha)

            rowNum += 1

        L_D = [x/y for x,y in zip(CL_values , CD_values)]

        if L_D == []:
            L_D=[-1]

    lift_to_drag_ratio = max(L_D)
    file.close()
    os.remove('polar_file.txt')
    return -lift_to_drag_ratio  # Return the negative of the L/D ratio to maximize it




# Bounds of the design variables (e.g., thickness-to-chord ratio and camber)
bounds = [{'name': 'thickness', 'type': 'continuous', 'domain': (0.10, 0.30)},
          {'name': 'camber', 'type': 'continuous', 'domain': (0.00, 0.09)},
          {'name': 'camber_pos', 'type': 'continuous', 'domain': (0.2, 0.9)}]   #{'name': 'angle', 'type': 'continuous', 'domain': (0.00, 20)}
# Optimization domain
domain = bounds


# Create a Bayesian Optimization object
optimizer = BayesianOptimization(f=objective_function,
                                domain=domain,
                                model_type='GP',
                                acquisition_type='EI', # Expected Improvement
                                acquisition_jitter=0.05,
                                exact_feval=True,
                                maximize=True)
# Number of initial points and subsequent evaluations
initial_design_numdata = 10
max_iter = 30
# Run the optimization
optimizer.run_optimization(max_iter=max_iter, verbosity=True)
# Print the optimal design
print("Optimal design:", optimizer.x_opt)

print("Optimal lift-to-drag ratio:", optimizer.fx_opt)
# Plot convergence
optimizer.plot_convergence()



# present best airfoil the system landed on
thickness, camber, camPos = optimizer.x_opt[0], optimizer.x_opt[1], optimizer.x_opt[2]
tempNum = f'{int(camber*100)}{int(camPos*10)}{int(thickness*100)}'
foilName = f'naca{tempNum}'
file_path = f'naca{tempNum}.dat'

# Inputs
alpha_i = 0
alpha_f = 20
alpha_step = 1
n_iter = 100
Re = 1000000 # This may be messing up scaling of l/d ratios

#create polar file for best airfoil
inputDAT = open("inputDAT.in", 'w')
inputDAT.write(f"naca {tempNum}\n")
inputDAT.write(f"save\n")
inputDAT.write(f"{foilName}.dat\n")
inputDAT.write("quit\n")
inputDAT.close()
subprocess.call("xfoil.exe < inputDAT.in", shell=True)

input_file = open("input_file.in", 'w')
input_file.write(f"LOAD {foilName}.dat\n")
input_file.write(foilName + '\n')
input_file.write("PANE\n")
input_file.write("OPER\n")
input_file.write("Visc {0}\n".format(Re))
input_file.write("PACC\n")
input_file.write("polar_file.txt\n\n")
input_file.write("ITER {0}\n".format(n_iter))
input_file.write("ASeq {0} {1} {2}\n".format(alpha_i, alpha_f,
                                            alpha_step))
input_file.write("\n\n")
input_file.write("quit\n")
input_file.close()

subprocess.call("xfoil.exe < input_file.in", shell=True)

# Lists to store coordinates
x_coordinates = []
y_coordinates = []

# Open the data file and read line by line
row = 1
with open(file_path, 'r') as file:
    for line in file:
        if row == 1:
            row+=1
            continue

        parts = line.split()
        x_coordinates.append(float(parts[0]))
        y_coordinates.append(float(parts[1]))

plt.figure(figsize=(8, 6))
plt.plot(x_coordinates, y_coordinates)
plt.title(f'Airfoil Profile {foilName}, L/D = {optimizer.fx_opt}')
plt.xlabel('x')
plt.ylabel('y')
plt.grid(True)
plt.axis('equal')  # Equal aspect ratio for better visualization
plt.show()


# find the best angle of attack
# Evaluate and pull data from polar file
CL_values = []
CD_values = []
alphaVAL = []
rowNum = 1

with open('polar_file.txt', 'r') as file:
# Read each line in the file
    for line in file:
        # print(line)
        components = line.split()    # Split the line into components

        if len(components) == 0:  # Check if the line contains data and is not blank
            rowNum += 1
            continue

        if rowNum >= 13:       #row 13 is usually where data is first pulled 
            # Extract CL and CD values and convert them to float
            CL = float(components[1])
            CD = float(components[2])
            alpha = float(components[0])
            # Append CL and CD values to their respective lists
            CL_values.append(CL)
            CD_values.append(CD)
            alphaVAL.append(alpha)

        rowNum += 1

    L_D = [x/y for x,y in zip(CL_values , CD_values)]

bestAngle = L_D.index(max(L_D))
file.close()
print(f"Best angle for naca{tempNum} = {bestAngle}\u00B0")


# %%
