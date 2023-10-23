import yaml


yaml_data = """
# This handles building the project

compiler: gcc # Change to whatever will compile your c/c++ code. You can even use emscripten!
name: App name # The name of the project, used for debugging.
output: app.exe # The output file.

# These are the flags that will be passed to the compiler, such as -std=c++17
flags: 
    - std=c++17

# The c/c++ files that will be compiled in order. 
files: 
    - main.cpp

# Where are the header files located?
# includes:
#    - include/

# Not to be confused with libraries, these are the paths to the libraries.
# libs:
#     - path/to/lib

# These are the libraries that will be linked to the project. Path must be specified in libs.
# libraries: 
#    - libname

# Shell commands to run before or after building.
# This is more (CMake) style, where you can run shell commands before building. 
# Also, you can run shell commands after building.
# shell:
#     before:
#         - echo "Hello, world!"
#     after:
#         - app.exe # Usually you want to run the program after building it.
#         - echo "Goodbye, world!"

"""


def build_file(config_path):
    with open(config_path, 'w') as f:
        f.write(yaml_data)


def build_file_with_data(current_config):
    data = None
    with open(current_config, 'r') as f:
        data = yaml.safe_load(f)

    outline = {
        "compiler": "g++",
        "name": "App name",
        "output": "app.exe",
        "flags": [],
        "files": [],
        "includes": [],
        "libs": [],
        "libraries": [],
        "shell": {
            "before": [],
            "after": []
        }
    }
    # Load data into outline
    for key, value in data.items():
        if key in outline.keys():
            outline[key] = value
    
    # Write to config file
    with open(current_config, 'w') as f:
        yaml.safe_dump(outline, f)