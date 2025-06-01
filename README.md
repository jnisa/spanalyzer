<!-- TODO: Add an image later -->
<!-- <p align='center'>
    <img src='./.docs/spanalyzer.png' width='20%' height='20%'>
</p> -->

<h1 align='center'><strong>Spanalyzer</strong></h1>

<p align='center'>
    Get a comprehensive report on the telemetry implementation within your Python codebase.
</p>

<div align="center">

  ![Coverage](https://img.shields.io/badge/coverage-99%25-brightgreen)
  ![Tests](https://img.shields.io/badge/tests-34%20passed%2C%200%20failed-brightgreen)
  ![Python Version](https://img.shields.io/badge/python-3.11.4-blue?logo=python&logoColor=white)

</div>

### **TODO**
- Adjust the badges later
- Add visual assets (e.g., diagram or architecture overview)

---

### **1. Introduction**

**Spanalyzer** is a Python package that helps you analyze and audit the telemetry instrumentation (e.g., spans, metrics, events) within your codebase.

The module [`spanalyzer.observability`](./spanalyzer/observability.py) includes the keywords and logic used to scan and extract telemetry data from Python scripts.

Once analyzed, the package generates a report summarizing or detailing telemetry coverage across your codebase.

---

### **2. Installation**

Install the package like any other Python library:

```bash
pip install spanalyzer
```

---

### **3. Usage**

The course of action of this package encompasses two procedures:
1. provide the path to the codebase you want to analyze;
2. pick the type of report you want to generate (**_basic_** or **_detailed_**).

#### **3.1. Basic Report**

The basic report will provide the user a very generic but clear view over the telemetry implementation within the codebase.

The output printed on the terminal will be as follows:

```bash
Script                    Spans    Traces    Metrics    Events    Attributes    Coverage
--------------------------------------------------------------------------------------------
script_1.py               ✓        ✓         ✓          ✓         ✓             100%
script_2.py               ✓        ✗         ✗          ✓         ✓             60%
script_3.py               ✓        ✓         ✓          ✗         ✓             90%
--------------------------------------------------------------------------------------------
```

This kind of report can be useful during the development stage to get a glimpse of the type of telemetry resources we're allocating to the code being produced.

And you can obtain this report on the terminal by running the following command:
```bash
spanalyzer basic --path /path/to/codebase
```

#### **3.2. Detailed Report**

On the other hand, the detailed report, will not only capture what type of telemetry resources are being allocated to the codebase as you can also get further details about those resources.

In this report, we will have the list of scripts that were submitted to the analysis and per script details like the name of the span under usage, which metrics were captured, which events were recorded, etc. will all be part of this type of report.

Here's an example of the content of the detailed report:
```bash
- file_path: /path/to/file.py

functions:
- name: csv_adaptor
    span_id: csv_adaptor
    span_type: context_manager
    has_span: true
    span_ended: true
    exceptions_recorded: true
    metrics_emitted: ["messages_sent", "message_lag", "message_size"]
    events_emitted: ["message_sent", "message_received"]
    attributes: ["message_id", "message_type", "message_source", "message_destination"]

- name: retry_wrapper
    span_id: span_2
    span_type: manual
    has_span: true
    span_ended: false
    exceptions_recorded: false
    metrics_emitted: []
    events_emitted: []
    attributes: []

- name: schema_validation
    span_id: schema_validation
    span_type: manual
    has_span: true
    span_ended: false
    exceptions_recorded: true
    metrics_emitted: [{"shacl_provided": True, "ontology_provided": True}]
    events_emitted: ["validation_failure"]
    attributes: []
```

And you can obtain this report by running the following command:

```bash
spanalyzer detailed --path /path/to/codebase --output /path/to/output/file
```

The output file will be a file containing the same information pointed out above.


### **4. Diagram**

**[ADD A DIAGRAM HERE]**


---

### **A. Acknowledgements**

There's some future work and implementations that should be held into account:
- Add support for other telemetry resources;
- Add support for other programming languages;
- Add telemetry to the package itself.

---

### **B. Changelog**

- [ ] Add support for other telemetry resources;
- [x] Add support for other programming languages;
- [ ] Add telemetry to the package itself.