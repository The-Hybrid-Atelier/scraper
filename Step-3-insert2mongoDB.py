
# Hedieh Moradi- 2021- Hybrid Atelier
#  This program will connect to the MondoDB database and allow you to 
# load files from your local directory and insert it into your collection.


# Packages to import
import pymongo
from pymongo import MongoClient
from pprint import pprint
import datetime
import warnings
import json
import os

warnings.filterwarnings('ignore')

# Connection to the database; replace "YOUR_***" with your information,
myclient = MongoClient('YOUR_MongoDB',username='YOUR_UserName',
                     password='YOUR_PassWord')

mydb = myclient['YOUR_DB']
mycol = mydb["YOUR-Collection"]

#  I am using os listdir to get the file from my local path.
#  Please replace this with your file path
def main():
    for item in os.listdir("YOUR_FilePath"):
        with open(os.path.join('YOUR_FilePath', item)) as glaze:
            glaze_dct = json.load(glaze)

        result = mycol.insert_one(glaze_dct)
        print('Inserted post id %s ' % result.inserted_id)

if __name__ == "__main__":
    main()