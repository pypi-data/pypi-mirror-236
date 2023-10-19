from typing import Any
from typing import Dict
from typing import List


# https://pop.readthedocs.io/en/latest/tutorial/quickstart.html#adding-configuration-data
# In this dictionary goes all the immutable values you want to show up under hub.OPT.web_retriever
CONFIG: Dict[str, Dict[str, Any]] = {
    "config": {
        "default": None,
        "help": "Load extra options from a configuration file onto hub.OPT.web_retriever",
    },
    "rules": {
        "default": None,
        "help": "Rule engine rules to load onto hub.OPT.web_retriever.rules",
    },
}

# The selected subcommand for your cli tool will show up under hub.SUBPARSER
# The value for a subcommand is a dictionary that will be passed as kwargs to argparse.ArgumentParser.add_subparsers
SUBCOMMANDS: Dict[str, Dict[str, Any]] = {
    # "my_sub_command": {}
}

# Include keys from the CONFIG dictionary that you want to expose on the cli
# The values for these keys are a dictionaries that will be passed as kwargs to argparse.ArgumentParser.add_option
CLI_CONFIG: Dict[str, Dict[str, Any]] = {
    "config": {"options": ["-c"]},
    # "my_option1": {"subcommands": ["A list of subcommands that exclusively extend this option"]},
    # This option will be available under all subcommands and the root command
    # "my_option2": {"subcommands": ["_global_"]},
}

# These are the namespaces that your project extends
# The hub will extend these keys with the modules listed in the values
DYNE: Dict[str, List[str]] = {"web_retriever": ["web_retriever"]}
