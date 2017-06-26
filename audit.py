#This code audits street names & city names to ensure consistency and uniformity of the street & city names.
#Program name: audit.py

import xml.etree.cElementTree as ET
import re
import pprint
from collections import defaultdict
import string

OSMFILE = "Irvine_OSM_full.txt"
street_type_re = re.compile('([\w\s,+)([\s(\w]+)', re.IGNORECASE)
city_name_re = re.compile('([\w\s,+)([\s(\w]+)')

expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road", 
            "Trail", "Parkway", "Commons"]

mapping = { "St ": "Street",
            "St.": "Street",
            "Ave ": "Avenue",
            "Rd.": "Road"
            }


expected_cities = ["Irvine", "Santa Ana", "Newport Beach", "Tustin", "Lake Forest", "Costa Mesa", "Fountain Valley"]

city_mapping = { "Tustin, CA": "Tustin",
                "irvine": "Irvine"
                }

def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(update_name(street_name, mapping))

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def update_name(street_name, mapping):
    for key in mapping:
        if key in street_name:
            better_name = re.sub(r'#\d+',"",street_name)
            street_name = string.replace(better_name,key,mapping[key])
    return street_name

def audit_street(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])
    osm_file.close()
    return street_types

def audit_city_name(city_names, city_name):
    m = city_name_re.search(city_name)
    if m:
        city_name = m.group()
        if city_name not in expected_cities:
            city_names[city_name].add(update_city_name(city_name, city_mapping))

def is_city_name(elem):
    return (elem.attrib['k'] == "addr:city")

def update_city_name(city_name, city_mapping):
    for key in city_mapping:
        if key in city_name:
            city_name = string.replace(city_name,key,city_mapping[key])           
    return city_name

def audit_city(osmfile):
    osm_file = open(osmfile, "r")
    city_names = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_city_name(tag):
                    audit_city_name(city_names, tag.attrib['v'])
    osm_file.close()
    return city_names

ct_names = audit_city(OSMFILE)
st_types = audit_street(OSMFILE)
pprint.pprint(dict(ct_names))
pprint.pprint(dict(st_types))