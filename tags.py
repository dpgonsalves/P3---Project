#Check the "k" value for each "<tag>" and resolve any problematic characters
#Program name: tags.py

import xml.etree.cElementTree as ET
import pprint
import re

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        attribute = element.attrib['k']
        if(re.match(lower, attribute) != None):
            keys['lower'] += 1
        elif(re.match(lower_colon, attribute) != None):
            keys['lower_colon'] += 1
        elif(re.match(problemchars, attribute) != None):
            keys['problemchars'] += 1
        else:
            keys['other'] +=  1
            
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)

    return keys

keys = process_map('Irvine_OSM_full.txt')
pprint.pprint(keys)