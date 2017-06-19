#This code iteratively parses the map file to determine what tags exist, and how many there are of each tag
#Program name: mapparser.py

import xml.etree.cElementTree as ET
import pprint

def count_tags(filename):
    tag_count = {}
    for _, element in ET.iterparse(filename, events=("start",)):
        add_tag(element.tag, tag_count)
    return tag_count

def add_tag(tag, tag_count):
    if tag in tag_count:
        tag_count[tag] += 1
    else:
        tag_count[tag] = 1
        
tags = count_tags('Irvine_OSM_full.txt')
pprint.pprint(tags)