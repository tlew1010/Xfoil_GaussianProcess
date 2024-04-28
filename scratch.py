# import os

# CL_values = []
# CD_values = []
# alphaVAL = []
# rowNum = 1

# with open('polar_file.txt', 'r') as file:
#     # Read each line in the file
#     for line in file:
#         print(line)
#         # # Split the line into components
#         components = line.split()

#         # # Check if the line contains data and is not a header
#         if len(components) == 0:
#             rowNum += 1
#             continue

#         if components[0]== 'alpha':
#             print('alpha found')

#         if rowNum >= 13:
#             # Extract CL and CD values and convert them to float
#             CL = float(components[1])
#             CD = float(components[2])
#             alpha = float(components[0])
#             # Append CL and CD values to their respective lists
#             CL_values.append(CL)
#             CD_values.append(CD)
#             alphaVAL.append(alpha)

#         rowNum += 1

# L_D = [x/y for x,y in zip(CL_values , CD_values)] 

# print(L_D)
# print(alphaVAL)
    
# file.close()

# x = [.13,.02]
# print(x[:1][0])


# def objective_function(x):
#     thickness, camber = x[:1][0], x[1:][0]
#     # Simplified model for demonstration: assume the lift-to-drag ratio is
#     # some function of thickness and camber.
#     # This is just a placeholder and should be replaced with a realistic
#     # aerodynamic model.
#     lift_to_drag_ratio = (4*thickness - thickness**2 + 2*camber - camber**2)
#     lift_to_drag_ratio = [lift_to_drag_ratio, None]
#     return lift_to_drag_ratio

# print(objective_function(x))


    
# if os.path.exists(f'{airfoil_name}.dat'):
#     os.remove(f'{airfoil_name}.dat')

    
# tempNum = '0012'
# airfoil_name = f'naca{tempNum}' 

# # Inputs
# alpha_i = 0
# alpha_f = 20
# alpha_step = .5
# n_iter = 100
# Re = 1000000 # This may be messing up scaling of l/d ratios



# print(airfoil_name)

# #create new dat file
# inputDAT = open("inputDAT.in", 'w')
# inputDAT.write(f"naca {tempNum}\n")
# inputDAT.write(f"save\n")
# inputDAT.write(f"{airfoil_name}.dat\n")
# inputDAT.write("quit\n")
# inputDAT.close()
# subprocess.call("xfoil.exe < inputDAT.in", shell=True)

# input_file = open("input_file.in", 'w')
# input_file.write(f"LOAD {airfoil_name}.dat\n")
# input_file.write(airfoil_name + '\n')
# input_file.write("PANE\n")
# input_file.write("OPER\n")
# input_file.write("Visc {0}\n".format(Re))
# input_file.write("PACC\n")
# input_file.write("polar_file.txt\n\n")
# input_file.write("ITER {0}\n".format(n_iter))
# input_file.write("ASeq {0} {1} {2}\n".format(alpha_i, alpha_f,
#                                              alpha_step))
# input_file.write("\n\n")
# input_file.write("quit\n")
# input_file.close()

# subprocess.call("xfoil.exe < input_file.in", shell=True)

# polar_data = np.loadtxt("polar_file.txt", skiprows=12)


# #%%
# print()
# print()


# print(f"Original Thickness: {tempNum[-2:]}%")
# print(f"Original Camber: {tempNum[:1]}%")