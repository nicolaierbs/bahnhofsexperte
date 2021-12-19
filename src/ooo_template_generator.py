import pymongo
import numpy as np


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['bahnhofsexperte']
stations_collection = db['stations']
ooo_collection = db['ooo_templates']
ooo_collection.drop({})


def ooo_list(field):
    for element in stations_collection.distinct(field):
        if stations_collection.count_documents({field: element}) >= 3:
            # print(element)
            ooo_collection.insert_one({
                'dimension': field,
                'discriminator': element,
                'matchingstations': stations_collection.find({field: element}).distinct('_id'),
                'otherstations': stations_collection.find(
                    {"$and": [{field: {"$ne": element}}, {field: {"$exists": True}}]}).distinct('_id'),
            })


def ooo_integer(field, operator, limit):
    # print({field: {operator: limit}})
    # print(list(stations_collection.find({field: {operator: limit}})))
    if stations_collection.count_documents({field: {operator: limit}}) >= 3:
        ooo_collection.insert_one({
            'dimension': field,
            'discriminator': operator + ' ' + str(limit),
            'matchingstations': stations_collection.find({field: {operator: limit}}).distinct('_id'),
            'otherstations': stations_collection.find(
                {"$and": [{field: {"$not": {operator: limit}}},
                          {field: {"$ne": np.nan}},
                          {field: {"$exists": True}}
                          ]}).distinct('_id'),
        })


ooo_list('type')
ooo_list('accessible')
ooo_integer('opening', '$lt', 1900)
ooo_integer('opening', '$gt', 1945)
ooo_integer('movements', '$gt', 500)
ooo_integer('movements_sbahn', '$gt', 1000)
ooo_integer('platforms', '$gt', 20)
