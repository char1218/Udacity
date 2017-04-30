
# coding: utf-8

# In[ ]:

import sqlite3

con = sqlite3.connect("Markham.db")
con.text_factory = str
cur = con.cursor()

cur.execute('''DROP TABLE IF EXISTS nodes''')
cur.execute("CREATE TABLE nodes (id, lat, lon, user, uid, version, changeset, timestamp);")
with open ('nodes.csv','r', encoding = 'utf8') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['lat'], i['lon'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]

cur.executemany("INSERT INTO nodes (id, lat, lon, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()

cur.execute('''DROP TABLE IF EXISTS nodes_tags''')
cur.execute("CREATE TABLE nodes_tags (id, key, value, type);")
with open ('nodes_tags.csv','r', encoding = 'utf8') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]
cur.executemany("INSERT INTO nodes_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
con.commit()

cur.execute('''DROP TABLE IF EXISTS ways''')
cur.execute("CREATE TABLE ways (id, user, uid, version, changeset, timestamp);")
with open ('ways.csv','r', encoding = 'utf8') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['user'], i['uid'], i['version'], i['changeset'], i['timestamp']) for i in dr]
cur.executemany("INSERT INTO ways (id, user, uid, version, changeset, timestamp) VALUES (?, ?, ?, ?, ?, ?);", to_db)
con.commit()

cur.execute('''DROP TABLE IF EXISTS ways_nodes''')
cur.execute("CREATE TABLE ways_nodes (id, node_id, position);")
with open ('ways_nodes.csv','r', encoding = 'utf8') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['node_id'], i['position']) for i in dr]
cur.executemany("INSERT INTO ways_nodes (id, node_id, position) VALUES (?, ?, ?);", to_db)
con.commit()

cur.execute('''DROP TABLE IF EXISTS ways_tags''')
cur.execute("CREATE TABLE ways_tags (id, key, value, type);")
with open ('ways_tags.csv','r', encoding = 'utf8') as fin:
    dr = csv.DictReader(fin)
    to_db = [(i['id'], i['key'], i['value'], i['type']) for i in dr]
cur.executemany("INSERT INTO ways_tags (id, key, value, type) VALUES (?, ?, ?, ?);", to_db)
con.commit()

