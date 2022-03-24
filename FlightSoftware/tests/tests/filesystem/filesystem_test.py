import os
import micropython
import ujson

print("Listing directory: " + os.getcwd())
for file in os.ilistdir(os.getcwd()):
    print(file)
print()
print("Memory information")
print(micropython.mem_info())

