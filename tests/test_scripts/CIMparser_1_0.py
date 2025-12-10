## Objective - Read an xml file, extract tree, output Classes, Attributes
##

from lxml import etree
from collections import defaultdict

# === INPUT ===
# Path to your CIM-based RDF/XML file
xml_file = "your_file.xml"

# === PARSING ===
tree = etree.parse(xml_file)
root = tree.getroot()

# Namespaces used in CIM RDF/XML files
ns = {
    'rdf': 'http://www.w3.org/1999/02/22-rdf-syntax-ns#',
    'cim': 'http://iec.ch/TC57/CIM100#'  # You might need to adjust this if your file uses another version
}

# Data structures to store results
class_attribute_map = defaultdict(set)
class_instance_map = defaultdict(list)

# === PROCESS ===
for element in root:
    # Get full tag like {namespace}ClassName
    tag = etree.QName(element.tag)
    class_name = tag.localname  # e.g., ACLineSegment
    class_id = element.get('{%s}ID' % ns['rdf']) or element.get('{%s}about' % ns['rdf'])

    # Add instance ID to map
    class_instance_map[class_name].append(class_id)

    # Loop through child tags to find attributes
    for child in element:
        child_tag = etree.QName(child.tag).localname
        class_attribute_map[class_name].add(child_tag)

# === OUTPUT ===

print("=== Classes Found ===")
for cls in class_attribute_map:
    print(f"Class: {cls}")

# print("\n=== Class Attributes ===")
# for cls, attrs in class_attribute_map.items():
#     print(f"\n{cls}:")
#     for attr in sorted(attrs):
#         print(f"  - {attr}")

# print("\n=== Class Instances ===")
# for cls, ids in class_instance_map.items():
#     print(f"\n{cls}: {len(ids)} instance(s)")
#     for cid in ids[:5]:  # show only first 5 IDs to keep it clean
#         print(f"  - {cid}")








