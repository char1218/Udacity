
# coding: utf-8
# In[73]:

import xml.etree.cElementTree as ET
import pprint
import re
import codecs

Markham_file = "Markham_sample.osm"


# In[81]:

import os


def convert_bytes(num):
    """
    this function will convert bytes to MB.... GB... etc
    """
    for x in ['bytes', 'KB', 'MB', 'GB', 'TB']:
        if num < 1024.0:
            return "%3.1f %s" % (num, x)
        num /= 1024.0


def file_size(file_path):
    """
    this function will return the file size
    """
    if os.path.isfile(file_path):
        file_info = os.stat(file_path)
        return convert_bytes(file_info.st_size)


# Lets check the file size of MS Paint exe 
# or you can use any file path
# file_path = r"C:\Windows\System32\mspaint.exe"
nodes = "nodes2.csv"
nodes_tags = "nodes_tags2.csv"
ways = "ways2.csv"
ways_tags = "ways_tags2.csv"
ways_nodes = "ways_nodes2.csv"
toronto_canada2 = "toronto_canada2.osm"
print ("Markham_map.osm file size:", file_size(Markham_file))
print ("nodes.csv file size:", file_size(nodes))
print ("nodes_tags.csv file size:", file_size(nodes_tags))
print ("ways.csv file size:", file_size(ways))
print ("ways_tags.csv file size:", file_size(ways_tags))
print ("ways_nodes.csv file size:", file_size(ways_nodes))
print ("toronto_canada2 file size:", file_size(toronto_canada2))


# In[68]:

from collections import defaultdict

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)

# The abbreviations were found in the Road Classification System for City of Toronto - Street Name Index, 2012.

expected = ["Avenue", "Bridge", "Boulevard", "Circle", "Circuit", "Crescent", "Court", "Close", "Drive", "Gardens",
           "Green", "Grove", "Gate", "Hill", "Heights", "Lane", "Line", "Lawn", "Mews", "Path", "Park", "Parkway",
           "Place", "Ramp", "Road", "Roadway", "Square", "Street", "Terrace", "Trail", "View", "Walk", "Way", "Woods", "Wood"]

mapping = { "Ave": "Avenue",
            "Bdge": "Bridge",
            "Blvd": "Boulevard",
            "Crcl": "Circle",
            "Crct": "Circuit",
            "Cres": "Crescent",
            "Ct": "Court",
            "Crt": "Court",
            "Cs": "Close",
            "Cv": "Cove Way",
            "Dr": "Drive",
            "Dr.": "Drive",
            "Gdns": "Gardens",
            "Grn": "Green",
            "Grv": "Grove",
            "Gt": "Gate",
            "Hill": "Hill",
            "Hts": "Heights",
            "Hrbr": "Harbour",
            "Ky": "Key Way",
            "Lane": "Lane",
            "Ldg": "Landing",
            "Line": "Line",
            "Lwn": "Lawn",
            "Mews": "Mews",
            "Path": "Path",
            "Pk": "Park",
            "Pkwy": "Parkway",
            "Pl": "Place",
            "Ramp": "Ramp",
            "Rd": "Road",
            "Rd.": "Road",
            "Rdwy": "Roadway",
            "Sq": "Square",
            "St": "Street",
            "Ste": "Suite",
            "Ter": "Terrace",
            "Trl": "Trail",
            "View": "View",
            "Walk": "Walk",
            "Way": "Way",
            "Wds": "Woods",
            "Wood": "Wood",
            "W": "West",
            "N": "North",
            "S": "South",
            "E": "East"}
        
def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)

def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")

def audit_street(osmfile):
    osm_file = open(osmfile, "r", encoding="utf8")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types

map_audit_street = audit_street(Markham_file)
pprint.pprint(dict(map_audit_street))


# Above is a dictionary of the street names we got back when compared against our expected list.
# 
# {'101': {'4466 Sheppard Ave E #101'},
#  '110': {'Disera Dr #110'},
#  '19': {'Woodbine Avenue #19'},
#  '200': {'Highway 7 E #200'},
#  '202': {'Finch Avenue East #202'},
#  '23B': {'B Yonge Street #23B'},
#  '26': {'Sideline 26', 'Pickering Sideline 26'},
#  '28': {'Pickering Sideline 28'},
#  '3': {'Steeles Ave W #3', 'Concession Road 3'},
#  '32': {'Pickering Sideline 32'},
#  '332': {'Fairview Mall Dr #332'},
#  '4': {'Concession Road 4'},
#  '48': {'Highway 48'},
#  '5': {'Regional Road 5'},
#  '500': {'Allstate Parkway, Ste 500'},
#  '7': {'Highway 7'},
#  '8': {'Concession Road  8'},
#  'Acres': {'Mid-Dominion Acres'},
#  'Augusta': {'Augusta'},
#  'Ave': {'Warden Ave'},
#  'Beach': {'Blue Heron Beach'},
#  'Berryway': {'Thimble Berryway'},
#  'Birchway': {'Yellow Birchway'},
#  'Blvd': {'Simonston Blvd', 'Huntsmill Blvd'},
#  'Briarway': {'Tangle Briarway', 'Wild Briarway'},
#  'By-pass': {'Woodbine By-pass'},
#  'Bypass': {'Markham Bypass'},
#  'Byway': {'Moonstone Byway', 'Pebble Byway'},
#  'Chart': {'Woodmans Chart'},
#  'Chase': {'Longwater Chase', 'Thornwood Chase'},
#  'Club': {'Pinehurst Club'},
#  'Coachway': {'Courville Coachway'},
#  'Corner': {'Knights Corner'},
#  'Corners': {"Hunter's Corners", 'Knights Corners'},
#  'Courtway': {'Candy Courtway'},
#  'Creekway': {'Rainbow Creekway'},
#  'Crestway': {'Rusty Crestway'},
#  'Croft': {'Harpers Croft'},
#  'Ct': {'Fabray Ct'},
#  'Cv': {'Kingfisher Cv'},
#  'Dr': {'Rouge Bank Dr'},
#  'Dr.': {'Bur Oak Dr.'},
#  'E': {'Major Mackenzie Dr E'},
#  'East': {'7 Highway East',
#           'Buttonville Crescent East',
#           'Centre Street East',
#           'Commerce Valley Drive East',
#           'Commerce Valley East',
#           'Don Mills Road East',
#           'Donald Buttress Boulevard East',
#           'Elgin Mills Road East',
#           'Finch Avenue East',
#           'Gormley Road East',
#           'Highway 7 East',
#           'Langstaff Road East',
#           'Lawrence Avenue East',
#           'Major MacKenzie Drive East',
#           'Major Mackenzie Drive East',
#           'Sheppard Avenue East',
#           'Steelcase Road East',
#           'Steeles Avenue East',
#           'Weldrick Road East'},
#  'Fairways': {'The Fairways'},
#  'Fernway': {'Bead Fernway',
#              'Bracken Fernway',
#              'Cliff Fernway',
#              'Crest Fernway',
#              'Lace Fernway',
#              'Lady Fernway',
#              'Log Fernway',
#              'Pond Fernway',
#              'Rock Fernway',
#              'Sand Fernway',
#              'Slender Fernway',
#              'Wood Fernway'},
#  'Foxway': {'James Foxway'},
#  'Gateway': {'Azalea Gateway', 'Harpers Gateway'},
#  'Gloryway': {'Morning Gloryway'},
#  'Hawkway': {'Black Hawkway', 'Dove Hawkway', 'Sea Hawkway'},
#  'Highway': {'7 Highway'},
#  'Hillway': {'Lofty Hillway', 'Spire Hillway', 'Turret Hillway'},
#  'Hollow': {'Barkwood Hollow',
#             'Basswood Hollow',
#             'Cricket Hollow',
#             'Falconwood Hollow',
#             'Marshfield Hollow',
#             'Pinebrook Hollow',
#             'Quail Hollow',
#             'Stonehedge Hollow'},
#  'Hrbr': {'Loon Hrbr'},
#  'Island': {'Wood Duck Island'},
#  'Ivyway': {'English Ivyway'},
#  'Ky': {'Sandpiper Ky'},
#  'Ldg': {'Willow Ldg'},
#  'Lea': {'The Barley Lea'},
#  'Liteway': {'Candle Liteway', 'Coach Liteway'},
#  'Manor': {'Allen Manor',
#            'Hawkweed Manor',
#            'Heritage Woods Manor',
#            'Lindcrest Manor',
#            'Pine Bough Manor'},
#  'Markway': {'Paul Markway'},
#  'Meadoway': {'Burnt Meadoway',
#               'Frosty Meadoway',
#               'Grass Meadoway',
#               'Low Meadoway',
#               'Rye Meadoway',
#               'Song Meadoway'},
#  'Mossway': {'Rock Mossway', 'Spanish Mossway'},
#  'N': {'Main St N'},
#  'North': {'2nd Street North',
#            'Bellamy Road North',
#            'Bridgeford Street North',
#            'Church Street North',
#            'Elizabeth Street North',
#            'Fernleigh Circle North',
#            'Main Street Markham North',
#            'Paliser Crescent North',
#            'Taylor Mills Drive North',
#            'Wootten Way North'},
#  'Passage': {'Southeast Passage', 'Northwest Passage'},
#  'Pathway': {'Coopman Pathway',
#              'Forest Creek Pathway',
#              'Frontier Pathway',
#              'Nature Pathway',
#              'Pioneer Pathway',
#              'Plumrose Pathway',
#              'Prosperity Pathway',
#              'Scarfair Pathway',
#              'Whispering Willow Pathway',
#              'Wilcox Creek Pathway'},
#  'Peak': {'Atlas Peak'},
#  'Point': {'Echo Point', 'Fox Point'},
#  'Rd': {'McCowan Rd'},
#  'Royalway': {'Renata Royalway', 'Remora Royalway', 'Sego Royalway'},
#  'Sageway': {'Purple Sageway'},
#  'Sideroad': {'Bethesda Sideroad', 'Jefferson Sideroad'},
#  'South': {'Bridgeford Street South',
#            'Chartland Boulevard South',
#            'Church Street South',
#            'Elizabeth Street South',
#            'Fernleigh Circle South',
#            'Highway  404  South',
#            'Laureleaf Road South',
#            'Leafield Drive South',
#            'Main Street Markham South',
#            'Paliser Crescent South',
#            'Park Drive South',
#            'Second Street South',
#            'Taylor Mills Drive South',
#            'Wootten Way South'},
#  'Sparroway': {'Field Sparroway', 'Tree Sparroway'},
#  'Townline': {'Pickering Townline', 'Uxbridge Pickering Townline'},
#  'Treeway': {'Lime Treeway', 'Plum Treeway'},
#  'Trl': {'Goldhawk Trl'},
#  'Unionville': {'Main Street Unionville'},
#  'Vineway': {'Curly Vineway',
#              'Elsa Vineway',
#              'Pepper Vineway',
#              'Thorny Vineway',
#              'Woody Vineway'},
#  'West': {'Bloomington Road West',
#           'Buttonville Crescent West',
#           'Centre Street West',
#           'Clark Avenue West',
#           'Commerce Valley Drive West',
#           'Don Mills Road West',
#           'Donald Buttress Boulevard West',
#           'Elgin Mills Road West',
#           'Finch Avenue West',
#           'Gormley Road West',
#           'Harding Boulevard West',
#           'Major Mackenzie Drive West',
#           'Rouge Valley Drive West',
#           'Steelcase Road West',
#           'Steeles Avenue West',
#           'Taunton Road West',
#           'Weldrick Road West'},
#  'Wheelway': {'Water Wheelway'},
#  'Willoway': {'Leaf Willoway', 'Peach Willoway'},
#  'Wrenway': {'Jenny Wrenway', 'Carol Wrenway'},
#  'Yonge': {'Yonge'}}

# In[70]:

def update_name(name, mapping):
    after = []
    if name.split("  "):
        name = " ".join(name.split())
    for part in name.split(" "):
        if part in mapping.keys():
            part = mapping[part]
        after.append(part)
    return " ".join(after)
    return name

for street_type, ways in map_audit_street.items():
    for name in ways:
        better_name = update_name(name, mapping)
        print (name, "=>", better_name)
#         print (better_name)


# Problems encounered
# 1. Non-Uniformed Abbreviations
# 2. Non-Typical Abbreviations
# 3. Inconsistent spacing
# 
# Steelcase Road East => Steelcase Road East
# Elgin Mills Road East => Elgin Mills Road East
# Weldrick Road East => Weldrick Road East
# 7 Highway East => 7 Highway East
# Commerce Valley East => Commerce Valley East
# Don Mills Road East => Don Mills Road East
# Buttonville Crescent East => Buttonville Crescent East
# Sheppard Avenue East => Sheppard Avenue East
# Finch Avenue East => Finch Avenue East
# Major MacKenzie Drive East => Major MacKenzie Drive East
# Major Mackenzie Drive East => Major Mackenzie Drive East
# Centre Street East => Centre Street East
# Langstaff Road East => Langstaff Road East
# Lawrence Avenue East => Lawrence Avenue East
# Donald Buttress Boulevard East => Donald Buttress Boulevard East
# Commerce Valley Drive East => Commerce Valley Drive East
# Highway 7 East => Highway 7 East
# Gormley Road East => Gormley Road East
# Steeles Avenue East => Steeles Avenue East
# Wootten Way North => Wootten Way North
# Fernleigh Circle North => Fernleigh Circle North
# Elizabeth Street North => Elizabeth Street North
# Bellamy Road North => Bellamy Road North
# 2nd Street North => 2nd Street North
# Paliser Crescent North => Paliser Crescent North
# Church Street North => Church Street North
# Main Street Markham North => Main Street Markham North
# Bridgeford Street North => Bridgeford Street North
# Taylor Mills Drive North => Taylor Mills Drive North
# Highway 7 => Highway 7
# Bracken Fernway => Bracken Fernway
# Lace Fernway => Lace Fernway
# Slender Fernway => Slender Fernway
# Cliff Fernway => Cliff Fernway
# Log Fernway => Log Fernway
# Crest Fernway => Crest Fernway
# Pond Fernway => Pond Fernway
# Wood Fernway => Wood Fernway
# Lady Fernway => Lady Fernway
# Bead Fernway => Bead Fernway
# Sand Fernway => Sand Fernway
# Rock Fernway => Rock Fernway
# Steeles Ave W #3 => Steeles Avenue West #3
# Concession Road 3 => Concession Road 3
# Bloomington Road West => Bloomington Road West
# Centre Street West => Centre Street West
# Clark Avenue West => Clark Avenue West
# Elgin Mills Road West => Elgin Mills Road West
# Steelcase Road West => Steelcase Road West
# Steeles Avenue West => Steeles Avenue West
# Donald Buttress Boulevard West => Donald Buttress Boulevard West
# Taunton Road West => Taunton Road West
# Major Mackenzie Drive West => Major Mackenzie Drive West
# Finch Avenue West => Finch Avenue West
# Rouge Valley Drive West => Rouge Valley Drive West
# Commerce Valley Drive West => Commerce Valley Drive West
# Don Mills Road West => Don Mills Road West
# Gormley Road West => Gormley Road West
# Harding Boulevard West => Harding Boulevard West
# Weldrick Road West => Weldrick Road West
# Buttonville Crescent West => Buttonville Crescent West
# Concession Road 4 => Concession Road 4
# Lindcrest Manor => Lindcrest Manor
# Pine Bough Manor => Pine Bough Manor
# Hawkweed Manor => Hawkweed Manor
# Heritage Woods Manor => Heritage Woods Manor
# Allen Manor => Allen Manor
# Taylor Mills Drive South => Taylor Mills Drive South
# Highway  404  South => Highway 404 South
# Church Street South => Church Street South
# Paliser Crescent South => Paliser Crescent South
# Second Street South => Second Street South
# Laureleaf Road South => Laureleaf Road South
# Main Street Markham South => Main Street Markham South
# Park Drive South => Park Drive South
# Elizabeth Street South => Elizabeth Street South
# Fernleigh Circle South => Fernleigh Circle South
# Bridgeford Street South => Bridgeford Street South
# Wootten Way South => Wootten Way South
# Leafield Drive South => Leafield Drive South
# Chartland Boulevard South => Chartland Boulevard South
# Coopman Pathway => Coopman Pathway
# Pioneer Pathway => Pioneer Pathway
# Wilcox Creek Pathway => Wilcox Creek Pathway
# Plumrose Pathway => Plumrose Pathway
# Scarfair Pathway => Scarfair Pathway
# Prosperity Pathway => Prosperity Pathway
# Frontier Pathway => Frontier Pathway
# Forest Creek Pathway => Forest Creek Pathway
# Nature Pathway => Nature Pathway
# Whispering Willow Pathway => Whispering Willow Pathway
# Pickering Sideline 28 => Pickering Sideline 28
# Regional Road 5 => Regional Road 5
# Pickering Townline => Pickering Townline
# Uxbridge Pickering Townline => Uxbridge Pickering Townline
# Concession Road  8 => Concession Road 8
# Pickering Sideline 32 => Pickering Sideline 32
# Sideline 26 => Sideline 26
# Pickering Sideline 26 => Pickering Sideline 26
# Longwater Chase => Longwater Chase
# Thornwood Chase => Thornwood Chase
# Augusta => Augusta
# Cricket Hollow => Cricket Hollow
# Quail Hollow => Quail Hollow
# Marshfield Hollow => Marshfield Hollow
# Barkwood Hollow => Barkwood Hollow
# Basswood Hollow => Basswood Hollow
# Pinebrook Hollow => Pinebrook Hollow
# Stonehedge Hollow => Stonehedge Hollow
# Falconwood Hollow => Falconwood Hollow
# The Barley Lea => The Barley Lea
# Pinehurst Club => Pinehurst Club
# Markham Bypass => Markham Bypass
# Knights Corner => Knights Corner
# Highway 48 => Highway 48
# The Fairways => The Fairways
# Bethesda Sideroad => Bethesda Sideroad
# Jefferson Sideroad => Jefferson Sideroad
# Echo Point => Echo Point
# Fox Point => Fox Point
# Courville Coachway => Courville Coachway
# Water Wheelway => Water Wheelway
# Rock Mossway => Rock Mossway
# Spanish Mossway => Spanish Mossway
# Moonstone Byway => Moonstone Byway
# Pebble Byway => Pebble Byway
# Frosty Meadoway => Frosty Meadoway
# Burnt Meadoway => Burnt Meadoway
# Song Meadoway => Song Meadoway
# Grass Meadoway => Grass Meadoway
# Low Meadoway => Low Meadoway
# Rye Meadoway => Rye Meadoway
# Renata Royalway => Renata Royalway
# Remora Royalway => Remora Royalway
# Sego Royalway => Sego Royalway
# Thimble Berryway => Thimble Berryway
# Yellow Birchway => Yellow Birchway
# Purple Sageway => Purple Sageway
# Jenny Wrenway => Jenny Wrenway
# Carol Wrenway => Carol Wrenway
# Paul Markway => Paul Markway
# Morning Gloryway => Morning Gloryway
# Woody Vineway => Woody Vineway
# Curly Vineway => Curly Vineway
# Thorny Vineway => Thorny Vineway
# Elsa Vineway => Elsa Vineway
# Pepper Vineway => Pepper Vineway
# Rusty Crestway => Rusty Crestway
# Tangle Briarway => Tangle Briarway
# Wild Briarway => Wild Briarway
# Field Sparroway => Field Sparroway
# Tree Sparroway => Tree Sparroway
# Leaf Willoway => Leaf Willoway
# Peach Willoway => Peach Willoway
# Main Street Unionville => Main Street Unionville
# Harpers Croft => Harpers Croft
# Woodmans Chart => Woodmans Chart
# Azalea Gateway => Azalea Gateway
# Harpers Gateway => Harpers Gateway
# James Foxway => James Foxway
# Rainbow Creekway => Rainbow Creekway
# English Ivyway => English Ivyway
# Candy Courtway => Candy Courtway
# Black Hawkway => Black Hawkway
# Dove Hawkway => Dove Hawkway
# Sea Hawkway => Sea Hawkway
# Candle Liteway => Candle Liteway
# Coach Liteway => Coach Liteway
# Hunter's Corners => Hunter's Corners
# Knights Corners => Knights Corners
# Willow Ldg => Willow Landing
# Atlas Peak => Atlas Peak
# Kingfisher Cv => Kingfisher Cove Way
# Loon Hrbr => Loon Harbour
# Wood Duck Island => Wood Duck Island
# Blue Heron Beach => Blue Heron Beach
# Sandpiper Ky => Sandpiper Key Way
# McCowan Rd => McCowan Road
# Southeast Passage => Southeast Passage
# Northwest Passage => Northwest Passage
# Lofty Hillway => Lofty Hillway
# Spire Hillway => Spire Hillway
# Turret Hillway => Turret Hillway
# Lime Treeway => Lime Treeway
# Plum Treeway => Plum Treeway
# Goldhawk Trl => Goldhawk Trail
# Mid-Dominion Acres => Mid-Dominion Acres
# Warden Ave => Warden Avenue
# Main St N => Main Street North
# Yonge => Yonge
# 7 Highway => 7 Highway
# Woodbine By-pass => Woodbine By-pass
# Allstate Parkway, Ste 500 => Allstate Parkway, Suite 500
# Disera Dr #110 => Disera Drive #110
# Highway 7 E #200 => Highway 7 East #200
# Finch Avenue East #202 => Finch Avenue East #202
# Fairview Mall Dr #332 => Fairview Mall Drive #332
# Woodbine Avenue #19 => Woodbine Avenue #19
# Major Mackenzie Dr E => Major Mackenzie Drive East
# B Yonge Street #23B => B Yonge Street #23B
# 4466 Sheppard Ave E #101 => 4466 Sheppard Avenue East #101
# Simonston Blvd => Simonston Boulevard
# Huntsmill Blvd => Huntsmill Boulevard
# Bur Oak Dr. => Bur Oak Drive
# Rouge Bank Dr => Rouge Bank Drive
# Fabray Ct => Fabray Court

# In[71]:

POSTCODE = re.compile(r'[A-z]\d[A-z]\s?\d[A-z]\d')

def audit_post_code(post_types, post_code):
    m = POSTCODE.search(post_code)
    if m is not None:
          if " " not in post_code:
#             post_code = post_code[:3] + " " + post_code[3:]
            post_types[post_code].add(post_code.upper())

def is_post_code(elem):
    return (elem.attrib['k'] == "addr:postcode")

def audit_postal(osmfile):
    osm_file = open(osmfile, "r", encoding="utf8")
    post_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):
        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_post_code(tag):
                    audit_post_code(post_types, tag.attrib['v'])
    
    return post_types

map_audit_postal = audit_postal(Markham_file)
pprint.pprint(dict(map_audit_postal))


# In[72]:

def update_postal(postal, post_types):
    post_codes = post_types[:3] + " " + post_types[3:]
    post_codes2 = post_codes.upper()
    return post_codes2

for post_types, codes in map_audit_postal.items():
        better_postal = update_postal(codes, post_types)
        print (post_types, "=>", better_postal)


# I've cleaned the Postal Codes for Markham for the following:
# 
# 1. spacing after the third digit in the postal code
# 2. the letters be in all caps
