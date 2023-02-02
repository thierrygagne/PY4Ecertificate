###################################
###################################
###################################
#
# PY4E CAPSTONE - PART 3
# Interactive map of commercial outlets with food safety violations in Montreal
#
###################################
###################################
###################################

# Started        January 31st 2023
# Last updated   January 31st 2023

###################################
#
# STEPS
# 
# 1. Create a list instance of all names, dates, lat, and lon from the SQLite database
# 2. Open these using the folium package
#
###################################



###################################
###################################
###################################

# CODE 

###################################
###################################
###################################

# Importing libraries
import sqlite3
import folium
import statistics

# Opening access to SQL database
conn = sqlite3.connect('montrealfoodsafetyviolation.sqlite')
cur = conn.cursor()
cur2 = conn.cursor()

# Start
print("\nThis program opens the SQLite database to create an inteactive map using the Folium package.")
limit = input("\nHow many entries should we seek? ")
if len(limit) <= 0: limit = 6411
limit = int(limit)
if limit > 6411: limit = 6411
    
# 1. Create a list instance from the SQLite database
sqlstr = 'SELECT name, date, amount, lat, lon FROM montrealfoodsafety LIMIT {}'.format(limit)
sqlstr = sqlstr.replace("(", "")
sqlstr = sqlstr.replace(")", "")
sqlstr = sqlstr.replace("'", "")

data = []
print("\nAccessing the SQLite database...")      
for row in cur.execute(sqlstr):
    if row[3] != None:
        line = {}
        line[0] = row[0]
        line[1] = row[1]
        line[2] = row[2]
        line[3] = row[3]
        line[4] = row[4]
        data.append(line)
    else:
        continue

lat = []
lon = []

for x in data:
    lat.append(x[3])
    lon.append(x[4])

datamean = [lat, lon]

# 2. Create that interactive map

print("\nProducing the Folium Map...")    
print("Mean latitude: " + str(statistics.mean(datamean[0])))
print("Mean longitude: " + str(statistics.mean(datamean[1])))

print("\nPlease wait a bit...") 
map = folium.Map(location=[statistics.mean(datamean[0]), statistics.mean(datamean[1])])
for x in data:
    folium.Circle(
        [x[3], x[4]], radius=min(9, max(1, x[2]/1000))*30
        ).add_to(map)
map.save("capstone.html")



# End of program
cur.close() 
conn.close()
print("\nIf you are in the terminal, you can type open capstone.html to see the map.")
print("\nN.B. Bigger circles indicate larger fines.")
print("\nN.B. There is no jittering, so circles with a wide border likely indicate multiple fines of different amounts.")
print("\nEND OF PROGRAM \n")


