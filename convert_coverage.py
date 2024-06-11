import json
import xml.etree.ElementTree as ET
from datetime import datetime

def convert_json_to_cobertura(json_path, xml_path):
    with open(json_path, 'r') as f:
        coverage_data = json.load(f)

    timestamp_iso = coverage_data['meta']['timestamp']
    timestamp_unix = int(datetime.fromisoformat(timestamp_iso).timestamp())

    root = ET.Element("coverage", {
        "line-rate": "0.0",
        "branch-rate": "0.0",
        "lines-covered": "0",
        "lines-valid": "0",
        "branches-covered": "0",
        "branches-valid": "0",
        "complexity": "0.0",
        "version": "0.1",
        "timestamp": str(timestamp_unix)
    })

    sources = ET.SubElement(root, "sources")
    source = ET.SubElement(sources, "source")
    source.text = coverage_data['meta'].get('source', '')

    packages = ET.SubElement(root, "packages")
    package = ET.SubElement(packages, "package", {
        "name": "",
        "line-rate": "0.0",
        "branch-rate": "0.0",
        "complexity": "0.0"
    })

    classes = ET.SubElement(package, "classes")

    for file_path, file_data in coverage_data['files'].items():
        class_elem = ET.SubElement(classes, "class", {
            "name": file_path,
            "filename": file_path,
            "line-rate": "0.0",
            "branch-rate": "0.0",
            "complexity": "0.0"
        })

        lines = ET.SubElement(class_elem, "lines")

        for line_num, line_data in file_data['lines'].items():
            line_elem = ET.SubElement(lines, "line", {
                "number": str(line_num),
                "hits": str(line_data['hits']),
                "branch": "false"
            })

    tree = ET.ElementTree(root)
    tree.write(xml_path)

if __name__ == "__main__":
    convert_json_to_cobertura('coverage.json', 'coverage.xml')
