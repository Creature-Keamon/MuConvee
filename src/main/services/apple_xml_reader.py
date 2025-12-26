import xml.etree.ElementTree as ET 

def read_apple_xml_file(file):
    tree = ET.parse(file)
    root = tree.getroot()