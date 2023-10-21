import os
import yaml
import subprocess
from . import build_file


class PyMake:
    command = ""
    debug_mode = False
    config:dict = {}

    def read_args(self, build_file, options):
        with open(build_file, 'r') as f:
            self.config = yaml.safe_load(f)
        self.debug_mode = options.get("-d", False)

    def add_flags(self, flag, arguments, add_slash=True, add_dash=True):
        """
        Add flags to the command.

        Args:
        - flag (str): The flag to add to the command.
        - arguments (list): A list of arguments to add to the command.
        - add_slash (bool): Whether to add a slash after each argument.
        """
        dash = "-" if add_dash else ""
        # Add flags
        for arg in arguments:
            self.command += f' {dash}{flag}{arg}'
            if add_slash:
                self.command += " / \n"
            elif arguments[-1] == arg:
                    break

    def debug_print(self, data):
        if self.debug_mode:
            print(f"Debugging: {data}")

    def build(self):
        if self.config == {}:
            self.debug_print("Config is empty")
            exit(2)
        
        self.command = f"{self.config['compiler']} -o {self.config['output']} "

        self.debug_print("Building " + self.config["name"])
        actions_in_order = [
            "files",
            "source",
            "includes",
            "libs",
            "libraries",
            "flags",
        ]
        actions = {
            "compiler": lambda x: f'{x}',
            "files": lambda x: self.add_flags("", x, add_dash=False),
            "includes": lambda x: self.add_flags("I", x),
            "libs": lambda x: self.add_flags("L", x),
            "libraries": lambda x: self.add_flags("l", x),
            "flags": lambda x: self.add_flags("", x, add_slash=False),
        }

        # Apply transformations
        for action in actions_in_order:
            if action in self.config:
                actions[action](self.config[action])

        # Add source

        # Print command
        print(self.command)
        # Remove pretty print
        self.command = self.command.replace("/ \n", " ")
        
    def run(self):
        # Call command and check if command has output
        # If it does, it failed
        res = subprocess.call(self.command, shell=True)
        if res != 0:
            self.debug_print("Build failed")
            exit(3)
        # Build succeeded, run program
        self.debug_print("Build succeeded")
        if self.config.get("run", False):
            self.debug_print("Running program")

            # Run program
            build = self.config['output'].replace("/", "\\")
            subprocess.call(build, shell=True)


class PyMakeCLI:
    command:str = None
    command_args:list = []
    options:dict = {}

    def get_args(self):
        args = os.sys.argv[1:]
        if len(args) == 0:
            print("No commmand specified")
            exit(1)
        # We got args, must be in this format: pymake.py <command> <command_args> [options]
        self.command = args[0]
        self.command_args = args[1:]
        if len(self.command_args) == 0:
            print("No arguments specified")
            exit(1)
            
        self.options = self.parse_options()

    def parse_options(self):
        options = {}
        # If arg starts with "-", it's an option
        for arg in self.command_args:
            if arg.startswith("-"):
                options[arg] = True
        return options

    def create_config(self):
        # pymake.py create <config_name>
        # Create a .yaml file at the current directory
        build_file.build_file(self.command_args[0])

    def build(self):
        # pymake.py build <config_name>
        # Build the project
        pymake = PyMake()
        pymake.read_args(self.command_args[0], self.options)
        pymake.build()
        pymake.run()


