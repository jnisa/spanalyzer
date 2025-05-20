# Script containing the engine that will be capturing all the functions in a certain folder.

import os

from typing import List

from pathlib import Path

from spanalyzer.script import ScriptSniffer
from spanalyzer.constants.exceptions import ExcludedPaths

class Engine:
    """
    Class containing the engine that will be capturing all the functions in a certain folder.

    This class will be used to navigate through a nested folder structure - like python projects i.e. 
    python packages, modules, etc. -, an capture all the functions in the scripts.

    Along with that, it will also capture the telemetry specs of these functions, to generate a telemetry
    report later on.

    Args:
        folder_path [str]: the path to the folder containing the scripts to be analyzed
    """

    def _list_python_scripts(self, folder_path: Path, excluded_paths: set[str] = ExcludedPaths.values()) -> List[str]:
        """
        List all the python scripts in the folder.

        Args:
            folder_path [Path]: the path to the folder containing the scripts to be analyzed
            excluded_paths [set[str]]: the paths to be excluded from the search

        Returns:
            [List[str]]: the list of python scripts in the folder
        """

        return [
            os.path.join(root, file)
            for root, dirs, files in os.walk(folder_path)
            for file in files
            if file.endswith('.py') and
            not any(excluded_path in os.path.join(root, file) for excluded_path in excluded_paths)
        ]
    
    # TODO. add a function that will generate a report table with the telemetry specs like the coverage table

    def run(self):
        """
        Heart of the operation.

        Where all of the routines will be executed - i.e. the script sniffing, the telemetry specs capture, etc.
        """

        self.script_sniffer.run()

        return self.script_sniffer.functions_list