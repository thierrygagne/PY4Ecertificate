###################################
###################################
###################################
#
# PY4E CAPSTONE - PART 1
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
# 1. Access the Montreal City API
# 2. Create a SQLite database capturing all entries of the food safety violation database.
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

# Ignore SSL certificate errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# Printing an introduction
print("\nThis program creates an SQLite database of all outlets with food safety violations in Montreal")
print("\nAPI resource_id: 7f939a08-be8a-45e1-b208-d8744dca8fc6")

# Open dataset
limit = 6411                # Important, you HAVE to set a limit (total is 6411)
url = 'https://www.donneesquebec.ca/recherche/api/3/action/datastore_search?resource_id=7f939a08-be8a-45e1-b208-d8744dca8fc6&limit={}'.format(limit)  
fileobj = urllib.request.urlopen(url, context = ctx)
fileobj_read = fileobj.read()                                              # This creates a byte class instance
fileobj_str = fileobj_read.decode("UTF-8")                                 # This creates a string class instance 
fileobj_str_replace = fileobj_str.replace("true", "True")
fileobj_str_replace = fileobj_str_replace.replace("null", "None")
fileobj_str_replace = fileobj_str_replace.replace("false", "False")
fileobj_dict = eval(fileobj_str_replace)                                   # This creates a dictionary class instance
data = list(fileobj_dict["result"]["records"])

# Debug: Just want to print the good parts.
print("\nExample for ID 1 \n")

count = 0
for x in data:
    count = count + 1
    print(x["etablissement"])
    print(x["categorie"])
    print(x["adresse"])
    print(x["date"][0:4] + "-" + x["date"][4:6] + "-" + x["date"][6:8])
    print("Amende:", x["montant"] + "$")
    if count == 1:
        break

# print("\n", data[0], "\n")

# Create the SQLite file and add the info in
conn = sqlite3.connect('montrealfoodsafetyviolation.sqlite')
cur = conn.cursor()
cur.execute('DROP TABLE IF EXISTS montrealfoodsafety')
print("\nDropping the montrealfoodsafety table if it exists...")
cur.execute('CREATE TABLE montrealfoodsafety (id INTEGER, name TEXT, category TEXT, address TEXT, date INTEGER, amount INTEGER, lat INTEGER, lon INTEGER)')
print("\nCreating the montrealfoodsafety table...")

count = 0
for x in data:
    count = count + 1
    id = x["_id"]
    name = x["etablissement"]
    category = x["categorie"]
    address = x["adresse"]
    date = str((x["date"][0:4] + "-" + x["date"][4:6] + "-" + x["date"][6:8]))
    amount = x["montant"]
    cur.execute('''INSERT INTO montrealfoodsafety (id, name, category, address, date, amount)
        VALUES (?, ?, ?, ?, ?, ?)''', (id, name, category, address, date, amount))

print("\nCommitting...")
conn.commit()

text = "\nNumber of fines: {}".format(count)
print(text)

# Debut that SQLite file creation
print("\nPrinting top ten rows of data from the SQLite table ... \n")
sqlstr = 'SELECT * FROM montrealfoodsafety ORDER BY id LIMIT 10'

for row in cur.execute(sqlstr):
    if row[0] < 10:
        print(str(row[0]) + " ", row[1] + ",", row[3])
    else:
        print(row[0], row[1], row[3])

# Test: Top ten highest fines
print("\nPrinting top ten rows of data with highest fines ... \n")
sqlstr = 'SELECT name, category, address, date, amount FROM montrealfoodsafety ORDER BY amount DESC LIMIT 10'

count = 0
for row in cur.execute(sqlstr):
    count = count + 1
    if count < 10:
        print(str(count) + " ", row[0] + ",", row[1] + ",", row[3] + ",", str(row[4]) + "$")
    else: 
        print(str(count), row[0] + ",", row[1] + ",", row[3] + ",", str(row[4]) + "$")
    
# End of program
cur.close() 
print("\nEND OF PROGRAM \n")





###################################
###################################
###################################

# GARBAGE 

###################################
###################################
###################################

# cd /Users/thierrygagne/Desktop/Learning/Python/PY4E/capstone


###################################

# NOTES

# Data out of the Montreal API is shaped that way:

# b'{"help": "https://www.donneesquebec.ca/recherche/api/3/action/help_show?name=datastore_search", "success": true, "result": {"include_total": true, "limit": 5, "records_format": "objects", "resource_id": "7f939a08-be8a-45e1-b208-d8744dca8fc6", "total_estimation_threshold": null, "records": [{"_id":1,"id_poursuite":"1219","business_id":"52059","date":"20110628","description":"Le produit alt\xc3\xa9rable \xc3\xa0 la chaleur \xc3\xa0 l\'exception des fruits et l\xc3\xa9gumes frais entiers doit \xc3\xaatre refroidi sans retard et maintenu constamment \xc3\xa0 une temp\xc3\xa9rature interne et ambiante ne d\xc3\xa9passant pas 4C jusqu\'\xc3\xa0 sa livraison au consommateur, sauf pendant le temps requis pour l\'application d\'un proc\xc3\xa9d\xc3\xa9 de fabrication ou d\'un traitement reconnu en industrie alimentaire et qui exige une plus haute temp\xc3\xa9rature.","adresse":"2368 Ch. Lucerne, Mont-Royal, Qu\xc3\xa9bec","date_jugement":"20111206","etablissement":"SOLLY THE BAKER","montant":"1500","proprietaire":"3099-5773 QUEBEC INC.","ville":"Mont-Royal","statut":"Ferm\xc3\xa9","date_statut":"20120227","categorie":"\xc3\x89picerie avec pr\xc3\xa9paration"}, 
# [...]

    # help
    # success
    # results

# Inside the "results" key, itself a dictionary, there is a "records" list.

# We want to create rows of data based on what is in the "records" list.

###################################

###################################

# EXTRA HELP

#  1. LE API DE MONTREAL PROPOSE CE CODE COMME EXAMPLE:
#
#     import urllib
#     url = 'https://www.donneesquebec.ca/recherche/api/3/action/datastore_search?resource_id=7f939a08-be8a-45e1-b208-d8744dca8fc6&limit=5'  
#     fileobj = urllib.urlopen(url)
#     print fileobj.read()

#  2. Convert a String representation of a Dictionary to a dictionary

#     https://stackoverflow.com/questions/988228/convert-a-string-representation-of-a-dictionary-to-a-dictionary

###################################