###################################
###################################
###################################
#
# PY4E CAPSTONE - PART 2
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
# 1. Get addresses from the SQLite database
# 2. Connect with a API to obtain coordinates based on these addresses
#
# Note: One address, 5650 Boul Métropolitain E, Saint-Léonard, QC H1S 1A7, just cannot be found on OpenStreetMap...
#
###################################



###################################
###################################
###################################

# CODE 

###################################
###################################
###################################

# Import libraries
import ast
import ssl
import urllib.request
import sqlite3
import re
from geopy.geocoders import Nominatim
import time
from pprint import pprint

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Opening access to SQL database
conn = sqlite3.connect('montrealfoodsafetyviolation.sqlite')
cur = conn.cursor()
cur2 = conn.cursor()

# Setting up the geolocalisation app
app = Nominatim(user_agent="tutorial")

# Doing the work
print("\nThis program opens the SQLite database of MTL outlets with food safety violations, and uses the OpenStreetMap API to find their coordinates.")
print("\nThere are 6,411 observations in the dataset.")
print("\nN.B. OpenStreetMap is not perfect, so some will give a warning message if they fail.")

limit = input("\nOK! What is the number of entries for which you want to find its coordinates? ")
if len(limit) <= 0: limit = 6411
if limit > 6411: limit = 6411
limitnumber = "LIMIT", str(limit)

sqlstr = 'SELECT id, address FROM montrealfoodsafety {}'.format(limitnumber)
sqlstr = sqlstr.replace("(", "")
sqlstr = sqlstr.replace(")", "")
sqlstr = sqlstr.replace("'", "")
sqlstr = sqlstr.replace("LIMIT,", "LIMIT")

count = 0
countmissing = 0
start = time.time()

for row in cur.execute(sqlstr):
    
    print("")
    conn.commit()
    
    if count % 5 == 0:
        update = time.time()
        timer = round(update - start, 0)
        print("Time elapsed: " + str(timer) + " seconds\n")
    
    count = count + 1
    
    print(str(row[0]), row[1])
    id = row[0]
    address = row[1]
    lat = None
    lon = None
    
    # EXCEPTIONS
    
    # This skips entries that already have data
    print("Checking if entry has coordinates...")
    cur2.execute('SELECT lat FROM montrealfoodsafety WHERE id = ? ', (id,))
    check = cur2.fetchall()[0]
    print(check[0])
    # print(check)
    if check[0] != None:
        print("WARNING: Coordinates already in the SQLite database\n")
        continue
    
    # This checks if it has a "Local" info and removes it.
    checklocal = address.find("Local")
    if checklocal != -1:
            splitstring = address.split(",")
            address = splitstring[0] + "," + splitstring[2] + "," + splitstring[3]
            print("Found invalid address with a local number. Now trying " + str(address))
    
    # Exception 1 - 1231 Mtée de Liesse, St-Laurent, Québec
    checkex = address.find("1231 Mtée de Liesse")
    if checkex != -1:
        address = address.replace("1231 Mtée", "1231 Montée")
        print("Found exception. Now trying " + str(address))
    
    # Exception 2 - 10420B Boul. Gouin Ouest, Roxboro, Québec
    checkex = address.find("10420B Boul. Gouin Ouest")
    if checkex != -1:
        address = address.replace("10420B", "10420")
        print("Found exception. Now trying " + str(address))
        
    # Exception 3 - 990 et 930 Herron Rd, Dorval, Québec
    checkex = address.find("Herron Rd")
    if checkex != -1:
        address = address.replace("Herron Rd", "Herron")
        print("Found exception. Now trying " + str(address))

    # Exception 4 - 8774A Rue Lajeunesse, Montréal, Québec    
    checkex = address.find("8774A Rue Lajeunesse")
    if checkex != -1:
        address = address.replace("8774A", "8774")
        print("Found exception. Now trying " + str(address))
    
    # Exception 5 - 7234A Rue Hutchison, Montréal, Québec
    checkex = address.find("7234A Rue Hutchison")
    if checkex != -1:
        address = address.replace("7234A", "7234")
        print("Found exception. Now trying " + str(address))
        
    # Exception 6 - 6852A Rue Jean-Talon Est, St-Léonard, Québec
    checkex = address.find("6852A Rue Jean-Talon Est")
    if checkex != -1:
        address = address.replace("6852A", "6852")
        print("Found exception. Now trying " + str(address))
        
    # Exception 7 - 6245 Boul. Métropolitain Est, St-Léonard, Québec
    checkex = address.find("6245 Boul. Métropolitain Est")
    if checkex != -1:
        address = address.replace("6245 Boul. Métropolitain Est", "H1P 1X7")
        print("Found exception. Now trying " + str(address))
        
    # Exception 8 - 9160P Rue Airlie, LaSalle, Québec
    checkex = address.find("9160P Rue Airlie")
    if checkex != -1:
        address = address.replace("9160P", "9160")
        print("Found exception. Now trying " + str(address))
        
    # Exception 9 - Addresses sur Rue du Centre 
    checkex = address.find("Rue du Centre")
    if checkex != -1:
        address = address.replace("Rue du Centre", "Centre")
        print("Found exception. Now trying " + str(address))
    
    # Exception 10 - 9440A Rue Charles-De La Tour, Montréal, Québec
    checkex = address.find("9440A Rue Charles-De La Tour")
    if checkex != -1:
        address = address.replace("9440A", "9440")
        print("Found exception. Now trying " + str(address))
    
    # Exception 11 - Addresses sur Rue Charles-de-Latour
    checkex = address.find("Rue Charles-De La Tour")
    if checkex != -1:
        address = address.replace("Rue Charles-De La Tour", "Rue Charles-de-Latour")
        print("Found exception. Now trying " + str(address))
        
    # Exception 12 - 1219 Rue du Square-Phillips, Montréal, Québec
    checkex = address.find("1219 Rue du Square-Phillips")
    if checkex != -1:
        address = address.replace("Rue du Square-Phillips", "Square-Phillips")
        print("Found exception. Now trying " + str(address))
    
    # Exception 13 - 7064A Boul. Pie-IX, Montréal, Québec
    checkex = address.find("7064A Boul. Pie-IX")
    if checkex != -1:
        address = address.replace("7064A", "7064")
        print("Found exception. Now trying " + str(address))
    
    # Exception 14 - 75 Av. des Pins Ouest, Montréal, Québec
    checkex = address.find("75 Av. des Pins Ouest")
    if checkex != -1:
        address = address.replace("Pins Ouest", "Pins")
        print("Found exception. Now trying " + str(address))
        
    # Exception 15 - 7472A Boul. Maurice-Duplessis, Montréal, Québec
    checkex = address.find("7472A Boul. Maurice-Duplessis")
    if checkex != -1:
        address = address.replace("7472A", "7472")
        print("Found exception. Now trying " + str(address))
        
    # Exception 16 - 5493B Av. Victoria, Montréal, Québec
    checkex = address.find("5493B Av. Victoria")
    if checkex != -1:
        address = address.replace("5493B", "5493")
        print("Found exception. Now trying " + str(address))
        
    # Exception 17 - 1 Westmount Sq., Westmount, Québec
    checkex = address.find("1 Westmount Sq., Westmount, Québec")
    if checkex != -1:
        address = address.replace("1 Westmount Sq., Westmount, Québec", "Westmount Square")
        print("Found exception. Now trying " + str(address))
        
    # Exception 18 - 7086A Boul. Saint-Laurent, Montréal, Québec
    checkex = address.find("7086A Boul. Saint-Laurent, Montréal, Québec")
    if checkex != -1:
        address = address.replace("7086A", "7086")
        print("Found exception. Now trying " + str(address))
        
    # Exception 19 - 6538A Av. Somerled, Montréal, Québec
    checkex = address.find("6538A Av. Somerled, Montréal, Québec")
    if checkex != -1:
        address = address.replace("6538A", "6538")
        print("Found exception. Now trying " + str(address))
        
    # Exception 20 - 216 Pr. Ronald, Montréal-Ouest, Québec
    checkex = address.find("216 Pr. Ronald, Montréal-Ouest, Québec")
    if checkex != -1:
        address = address.replace("216 Pr. Ronald", "216 Ronald")
        print("Found exception. Now trying " + str(address))
        
    # Exception 21 - Addresses sur 3343 Boul. des Sources, Dollard-des-Ormeaux, Québec 
    checkex1 = address.find("3343D Boul. des Sources, Dollard-des-Ormeaux, Québec")
    checkex2 = address.find("3343E Boul. des Sources, Dollard-des-Ormeaux, Québec")
    checkex3 = address.find("3343F Boul. des Sources, Dollard-des-Ormeaux, Québec")
    if checkex1 != -1 or checkex2 != -1 or checkex3 != -1:
        address = address.replace("3343D Boul. des Sources", "3343 Boul. des Sources")
        address = address.replace("3343E Boul. des Sources", "3343 Boul. des Sources")
        address = address.replace("3343F Boul. des Sources", "3343 Boul. des Sources")
        print("Found exception. Now trying " + str(address))
        
        
    
    # REST OF THE CODE
    
    # This checks if there are any other entries with the same address that already have the coordinates
    print("Checking if another entry with same address has coordinates...")
    cur2.execute('SELECT * FROM montrealfoodsafety WHERE address = ?', (address,))
    line = cur2.fetchall()
    for x in line:
        if x[6] != None:
            lat = x[6]
            lon = x[7]
            break
    if lat != None:
        print("MATCH!")
        cur2.execute('UPDATE montrealfoodsafety SET lat = ?, lon = ? WHERE id = ?', (lat, lon, id))
        print("Copying new coordinates...")    
        print("Latitude:", str(location["lat"])) 
        print("Longitude:", str(location["lon"]))
        lat = None
        lon = None
        continue
    else:
        print("None")
    
    # This gets the API data:
    time.sleep(1) 
    try:
        location = app.geocode(address, timeout=5).raw
    except:
        print("WARNING: Couldn't find a match, skipping it.")
        print("")
        countmissing = countmissing + 1
        continue
    
    lat = location["lat"]
    lon = location["lon"]
    cur2.execute('UPDATE montrealfoodsafety SET lat = ?, lon = ? WHERE id = ?', (lat, lon, id))
    print("Seeking new coordinates from the internet...")    
    print("Latitude:", str(location["lat"])) 
    print("Longitude:", str(location["lon"]))
    
print("\nCommitting...")
conn.commit()

print("\nOut of the " + str(limit) + " entries checked, " + str(countmissing) + " were not found using the OpenStreetMap API.")
end = time.time()
timer = round(end - start, 0)
print("\nTotal time elapsed: " + str(timer) + " seconds")

# End of program
cur.close() 
conn.close()
print("\nEND OF PROGRAM \n")








###################################
###################################
###################################

# GARBAGE 

###################################
###################################
###################################

# cd /Users/thierrygagne/Desktop/Learning/Python/PY4E/capstone

# LINK 1

# https://www.thepythoncode.com/article/get-geolocation-in-python

# LINK 2

# There was an issue with SSL stuff, but following the advice here worked: https://www.youtube.com/watch?v=dEBN1M609zk
