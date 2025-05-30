# Script containing the engine that will be capturing all the functions in a certain folder.

import os
import ast

from typing import List
from typing import Dict

from pathlib import Path

from spanalyzer.script import ScriptSniffer

from spanalyzer.observability import TelemetryDetector

from spanalyzer.constants.exceptions import ExcludedPaths

from spanalyzer.reports import terminal_report
from spanalyzer.reports import detailed_report

from spanalyzer.utils.operations import folder_trim

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
    
    def _has_telemetry_attrs(self, data: Dict) -> Dict:
        """
        Check if the telemetry attributes are empty.

        Args:
            data [Dict]: the data to be filtered

        Returns:
            [Dict]: the filtered data

        _Example_:
        >>> data = {
        ...     'tracers': [
        ...         TelemetryCall(func='test_tracer_1', line_number=1, args=None),
        ...         TelemetryCall(func='test_tracer_2', line_number=24, args=None),
        ...     ],
        ...     'spans': [],
        ...     'attributes': [
        ...         TelemetryCall(func='test_attribute_1', line_number=1, args=None),
        ...         TelemetryCall(func='test_attribute_2', line_number=24, args=None),
        ...     ],
        ... }
        >>> _is_empty_attrs(data)
        {
            'tracers': True,
            'spans': False,
            'attributes': True,
        }
        """

        return {
            key: True if len(val) > 0 else False
            for key, val in data.items()
        }
    
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
                print(terminal_report(folder_trim(report_data)))

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

        telemetry_report = []

        for script in self._list_python_scripts(self.folder_path):
            match self.report_type:
                case 'basic':
                    telemetry_report.append({
                        **{'script': script},
                        **self._has_telemetry_attrs(TelemetryDetector().run(ast.parse(open(script).read()))),
                    })

                case 'detailed':
                    raise NotImplementedError
                
                case _:
                    raise ValueError(f"Invalid report type: {self.report_type}")
            
        self._switch_report(telemetry_report)