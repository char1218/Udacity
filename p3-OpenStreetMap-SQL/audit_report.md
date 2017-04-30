
# OpenStreetMap Case Study
### Map Area: Markham, Ontario, Canada

#### Name: Heron Lau
---

  I currently reside in Markham and this is a perfect opportunity to take some time and explore my area!
  
Here's the map of <a href="http://www.openstreetmap.org/search?query=markham%20ontario#map=12/43.8803/-79.2995">Markham</a> via Open Street Map.
I used a custom data OSM extract from MapZen to conduct my audit.

# 1. Markham .OSM Audit
---
The Markham OSM file, <code>Markham_map.osm</code> was parsed through 

<code>Markham_audit.py</code> 

and quantified the following elements:

<code>bounds = 1</code> <br />
<code>memeber = 17860</code> <br />
<code>nd = 709023 </code><br />
<code>node = 630074 </code><br />
<code>osm = 1 </code><br />
<code>relation = 815 </code><br />
<code>tag = 608925 </code><br />
<code>way 89300 </code><br />

A key describes a topic, category, or type of feature within the map.
I checked the key, or <code>k</code> value within the tags with the three expressions listed blelow:
lower: key values that only contain lower case
lower_colon: keys that contain colons
problemchars: keys that contain special characters
other: keys that don't fall within the above expressions

We come back with the follwing findings:

<code>lower = 372327 </code><br />
<code>lower_colon = 224692 </code><br />
<code>other = 11905 </code><br />
<code>problemchars = 1 </code><br />


# 2. Problems with the dataset
---

While auditing through the <code>Markham.osm</code>, I encountered some inconsistancies within the dataset.

The audit can be found in <code>Markham_audit.py</code>.

## 2.1 Street Names

There were 3 types of problems that occured when auditing street names
1. Non-Uniformed Abbreviations<br/>
<code>Bur Oak Dr. => Bur Oak Drive</code><br/>
<code>Disera Dr #110 => Disera Drive #110</code>

2. Atypical Abbreaviations<br/>
<code>Kingfisher Cv => Kingfisher Cove Way</code><br/>
<code>Sandpiper Ky => Sandpiper Key Way</code><br/>

3. Extra Spacing<br/>
<code>Highway  404  South => Highway 404 South</code><br/>
<code>Concession Road  8 => Concession Road 8</code><br/>

## 2.2 Postal Codes

As for postal codes, I've noticed two of the following issues:
1. Lack of spacing after the third digit<br/>
<code>M1W3E6 => M1W 3E6</code><br/>

2. Captialized letters<br/>
<code>l6c2t2 => L6C 2T2</code><br/>

# 3.0 Insertion of Markham Data into SQL database
---

Here's a rundown of the file sizes of my .csv files after I passed <code>Markham_map.osm</code> through <code>data_to_csv.py</code>.

<code>Markham_map.osm file size: 143.2 MB</code><br/>
<code>nodes.csv file size: 48.8 MB</code><br/>
<code>nodes_tags.csv file size: 9.7 MB</code><br/>
<code>ways.csv file size: 4.9 MB</code><br/>
<code>ways_tags.csv file size: 11.8 MB</code><br/>
<code>ways_nodes.csv file size: 15.8 MB</code><br/>
<code>toronto_canada2 file size: 12.0 KB</code><br/>

The schema used for SQL insertion is located in <code>schema.py</code>.
<code>csv_to_SQL.py</code>was used to insert files into SQL database <code>Markham.db</code>.<br/>
Since the Markham_map.osm was 143.2 MB in size, I used a smaller file called <code>toronto_canada2.osm</code> to test the validity of <code>data_to_csv.py</code>.

# 4.0 Queries
---

SQL Database queries can be found in <code>db_queries.py</code>.

## 4.1 Markham SQL DB Stats

There are a lot of nodes and ways in the Markham dataset!<br/>
<code>Number of Markham nodes:  630074</code><br/>
<code>Number of Markham ways:  89300</code><br/>

There's 509 unique contributors with 136 users with one time contributions.<br/>
<code>Number of unique users who contribute to Makrham:  509</code><br/>
<code>One time contributors:  136</code><br/>

## 4.2 User Contributions

Top 5 contributors:
+ andrewpmk: 598,230 entries
+ Kevo: 14,150 entries
+ geobase_stevens: 13,234 entries
+ Mojan Jadidi: 13,109 entries
+ andrewpmk_imports, 6,322 entries

<code>Top 5 contributors:  [('andrewpmk', 598230), ('Kevo', 14150), ('geobase_stevens', 13234), ('Mojgan Jadidi', 13109), ('andrewpmk_imports', 6322)]
</code><br/>
If we put the top contributor, andrewpmk with the fifth most contributor, andrewpmk_imports together, the user would have a whopping 604,552 entries! Thank you andrewpmk for your contribution to this dataset!

## 4.3  Top 10 Ammentities

Top 10 Ammenities:
+ Restaurants: 288
+ Post_box: 241
+ Fast_food: 224
+ Benches: 179
+ Waste_basket: 137
+ Bank: 136
+ Cafe: 135
+ Parking: 127
+ Fuel: 110
+ Pharmacy: 72

<code>Top 10 ammenities:  [('restaurant', 288), ('post_box', 241), ('fast_food', 224), ('bench', 179), ('waste_basket', 137), ('bank', 136), ('cafe', 135), ('parking', 127), ('fuel', 110), ('pharmacy', 72)]</code><br/>

In terms of ammenities, the list shows people mostly go around eating. The abundance of fast food joints, waste baskets, and benches indidcate that people want to sit and eat outside while enjoying a sugary drink from their neighbourhood cafe. If they're not eating, they're at parked at the bank to withdraw money, possibly used for future eating. Or they could be found at the pharmancy, possibly refilling perscription medication for various diseases related to overeating. There's also an abundance of fuel stations, ie. restaurants for cars!

## 4.4 Top 5 Places of Worship

Top 5 Places of Worship:
+ Christian: 19
+ Jewish: 3
+ Taoist: 2
+ Buddhist: 1
+ Hindu: 1

<code>Top 5 places of worship:  [('christian', 19), ('jewish', 3), ('taoist', 2), ('buddhist', 1), ('hindu', 1)]</code><br/>

Jesus reigns supreme with 19 places of worship! Asian faiths round off the bottom three of the top five with the Jewish faith coming in second.

The religion section of the <a href="https://www.markham.ca/wps/wcm/connect/markhampublic/1d50758a-9236-4f2e-b818-a9a4115a77c6/Demographics-Fact-Sheet-2014.pdf?MOD=AJPERES&CACHEID=1d50758a-9236-4f2e-b818-a9a4115a77c6">Markham Demographics 2011, Quick facts</a> provide the following statistics:

Number Percent (%)
+ Christian: 44
+ Hindu: 10
+ Muslim: 8
+ Buddhist: 4
+ Jewish: 2
+ Sikh: 1
+ Other: less than 1
+ No religious affiliation: 30

Hmm, seems like religious affiliation in private households don't necessarily correlate with places of worship. There might be some reasons to explain this:

1. Ethnicity in a given area may change over time therefore, religion may change before places of worship can be erected.
2. People have a preference to their place of worship: They might reside in Markham, but choose to worship outside of Markham

## 4.5 Top 10 Cuisines

Top 10 Cuisines:
+ Chinese: 40
+ Pizza: 9
+ Asian: 8
+ Japanese: 8
+ Indian: 7
+ Vietnamese: 7
+ American: 6
+ Italian: 6
+ Sushi: 6
+ Breakfast: 3

<code>[('chinese', 40), ('pizza', 9), ('asian', 8), ('japanese', 8), ('indian', 7), ('vietnamese', 7), ('american', 6), ('italian', 6), ('sushi', 6), ('breakfast', 3)]</code><br/>

Again, let's take a look Markham Demographics, 2011 data but this time for Ethnic Origin and Place of Birth for Immigrants

Ethnic Origins (total responses in %)
+ Asian: 61
+ European: 25
+ North American: 8
+ Caribbean: 3
+ African: 2
+ Latin, Central and South American: 1
+ North American Aboriginal: less than 1
+ Oceania: less than 1

Place of Birth of Immigrants:
Total Immigrants (%)
Asia: 77
Europe: 10
Americas: 8
Africa: 4
Oceania and other: less than 1

6 of the top 10 spots are occupied by asian cuisine! Demographic data shows that Asian ethnicity (64%) lead the pack in Markham and new Immigrants are overwhelmingly asian (77%). It looks like the immigrants who come here are opening restaurants or asians who have established themselves in Canada are opening up restaurants in Markham, catering to the asian population.

Oh, restaurants are easier to open than Places of worship. Perhaps this is why cuisine reflects the population better than places of worship.

According to the dataset, Markham is the place to go for asian food!

# 5.0 Possible Improvements
---

Wait a minute, something doesn't add up. ONLY 40 CHINESE RESTAURANTS IN ALL OF MARKHAM?! Let's take a look at OpenStreetMap.

This <a href="http://www.openstreetmap.org/#map=18/43.89333/-79.29227">plaza</a> is located right by my house. From the looks of it, a couple of restaurants are missing. If that's the case, I'm going to assume that a lot of restaurants are missing from this dataset; meaning the data is incomplete. Since restaurants constantly change, I'll also make the assumption that the dataset may be out of date.

Again, there are only 509 contributors for the Markham dataset; 26.7% of which are one time contributors. Before this project, I've never even heard of OpenStreetMap. Word of this awesome application needs to spread! 

Hmm, I guess since I learned of the app from Udacity, more people should just enroll to this program.

Or perhaps OpenStreetMap needs to gain access to data like Yelp to update its restaurant list. My suggestion would then be an Open source Yelp to help with Open Source Street Mapping.


# 6.0 Conclusion
---

Although the dataset was not completely accurate, OpenStreetMap demonstrates the beauty in people coming together in providing a map that is compeletely free to use. With all data that is user generated, there were bound to be errors within the entries. With the techniques I've gained through Udacity's data wrangling course, I was able to programmatically correct some of those entries and generate a couple of neat facts using the SQL database on the City of Markham, Ontario.


