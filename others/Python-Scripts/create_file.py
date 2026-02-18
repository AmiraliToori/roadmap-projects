#!/usr/bin/env python3

from pathlib import Path
import sys

try:
    option = int(
        input("""What kind of file you want to create?
    1. Python
    2. Lua
    3. Shell (Bash)
    4. Custom (txt, csv and etc)
    """)
    )
except ValueError:
    print("Wrong Input. Please enter INTEGER number between the OPTIONS.")
    sys.exit(1)


if option == 1:
    format = ".py"
elif option == 2:
    format = ".lua"
elif option == 3:
    format = ".sh"
elif option == 4:
    format = input('Enter your desired format: (e.g ".txt" ".csv")\n>')

    if format.isspace():
        print("Input cannot be EMPTY SPACE.\n")
        sys.exit(1)
    elif " " in format:
        print("Format could not contain SPACE characters.\n")
        sys.exit(1)
else:
    print("Enter a valid number!")
    sys.exit(1)


try:
    file_name = input("Enter the name of the file:\n>")
    complete_file_name = file_name + format
    address = "./" + complete_file_name
    path = Path(address)
except FileExistsError:
    print(f"The file {complete_file_name} already exists!")
    sys.exit(1)
