# Script containing the engine that will be capturing all the functions in a certain folder.

import os

from typing import List
from typing import Dict

from pathlib import Path

from spanalyzer.script import ScriptSniffer

from spanalyzer.constants.exceptions import ExcludedPaths

from spanalyzer.reports import terminal_report
from spanalyzer.reports import detailed_report

class Engine:
    """
    Class containing the engine that will be capturing all the opentelemetry operations in a certain folder.

    This class will be used to navigate through a nested folder structure - like python projects i.e. 
    python packages, modules, etc. -, and capture all the opentelemetry operations in the scripts.

    Along with that, it will also capture the telemetry specs of these operations, to generate a telemetry
    report later on.

    Args:
        folder_path [str]: the path to the folder containing the scripts to be analyzed
        report_type [str]: the type of report to be generated (the options are 'basic' and 'detailed')
    """

    def __init__(self, folder_path: str, report_type: str):
        """
        Initialize the engine.
        """

        self.folder_path = folder_path
        self.report_type = report_type

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
    
    def _switch_report(self, report_data: Dict):
        """
        Switch the report type.

        Args:
            report_data [Dict]: the data to be reported

        Returns:
            [Dict]: the report data
        """

        match self.report_type:
            case 'basic':
                return terminal_report(report_data)

            # TODO. needs some work            
            case 'detailed':
                return detailed_report(report_data)
            
            case _:
                raise ValueError(f"Invalid report type: {self.report_type}")

    def run(self):
        """
        Heart of the operation.

        Where all of the routines will be executed - i.e. the script sniffing, the telemetry specs capture, etc.

        Through this method the engine will be performing the following operation by this order:
        1. Obtain the list of python scripts in the folder;
        2. Sniff the scripts to capture the functions;
        3. Capture the telemetry specs of these functions;
        4. Conciliate the telemetry with the script results;
        5. Generate the report.
        """


        for script in self._list_python_scripts(self.folder_path):

            functions_list = self.script_sniffer.run()

            # 2. Capture the telemetry specs
            telemetry_specs = self.telemetry_sniffer.run()

            # 3. Conciliate the telemetry with the script results
            conciliated_data = self.conciliate_data(functions_list, telemetry_specs)
            
            # 4. Generate the report
            report = self._switch_report(conciliated_data)
