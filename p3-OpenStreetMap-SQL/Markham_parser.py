
# coding: utf-8

# In[2]:

import xml.etree.cElementTree as ET
import pprint
import re
import codecs

Markham_file = "Markham_map.osm"

# Iterparse the Toronto dataset to populate my dictionary for common tags.

def count_tags(filename):
        tags = {}
        for event, elem in ET.iterparse(filename):
            if elem.tag in tags: 
                tags[elem.tag] += 1
            else:
                tags[elem.tag] = 1
        return tags
    
tot_tags = count_tags(Markham_file)
pprint.pprint(tot_tags)


# We found the following elements in the Markham file:
# 
# bounds = 1 <br />
# memeber = 17860 <br />
# nd = 709023 <br />
# node = 630074 <br />
# osm = 1 <br />
# relation = 815 <br />
# tag = 608925 <br />
# way 89300 <br />
# 
# Cool!

# 2 Auditing through our dataset
# 2.1 parsing through tag elements for problems

# In[3]:

'''
Checking the k value for each tag with the 3 expressions listed below:
lower - tags that only contain lower case
lower_colon - valid tags with colon in their names
problemchars - tags with problematic characters
other - tags that didn't fall into the above three categories
'''

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')

def key_type(element, keys):
    if element.tag == "tag":
        k_value = element.attrib['k']
        if lower.search(k_value) is not None:
            keys['lower'] += 1
        elif lower_colon.search(k_value) is not None:
            keys['lower_colon'] += 1
        elif problemchars.search(k_value) is not None:
            keys['problemchars'] += 1
        else:
            keys['other'] += 1
    return keys

def process_map(filename):
    keys = {"lower": 0, "lower_colon": 0, "problemchars": 0, "other": 0}
    for _, element in ET.iterparse(filename):
        keys = key_type(element, keys)
    return keys

tot_k = process_map(Markham_file)
pprint.pprint(tot_k)


# Parsing through the tags came back with some interesting findings!
# 
# lower = 372327 <br />
# lower_colon = 224692 <br />
# other = 11905 <br />
# problemchars = 1 <br />

