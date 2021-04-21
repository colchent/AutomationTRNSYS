# AutomationTRNSYS
To run several simulations with the STD TRNSYS without adding parameters between each execution, I developped a Python program. The goal of the script is to take the data from an .xlsx file, write it in a .deck file readable by TRNSYS and execute it. There is also a part that trace curves from the results of the simulation.  The Python code is very specific to the studied case and the TRNSYS model but I believe it can be uddated and impoved.


To correctly execute the code, you need to insure that:
* All Pythons' files are located in TRNSYS18/yourfoldername, otherwise TRNSYS's model can't be launch with your program.
* The code copy an existing .dck file to modify the desired parameters, each parameters is mapped (by the line's number ) and a specific function modifies it. You need to modify the program to use a copy of youre model's .dck file. I think a better way to create an appropriate .dck file without copying an existing one can be done.
* The time step corresponds to the one expected in getMonotone.py, for now it is adapted to a 10 minutes time step.
If you want to add parameters, you first need to spot where it is written in the .dck file and then find a way to re-write your value.
