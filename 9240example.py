# This is one of the solutions to a previous run.
# Ready to run if you have xfoil.exe in the same directory

import subprocess
import matplotlib.pyplot as plt

tempNum = '9240'
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
# input_file.write("\n\n")
# input_file.write("quit\n")
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
plt.title(f'Airfoil Profile {foilName}, L/D = 9.758')
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
