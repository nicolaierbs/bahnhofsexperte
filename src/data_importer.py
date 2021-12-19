import pandas as pd
import pymongo


client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['bahnhofsexperte']
stations_collection = db['stations']


def stations():
    df = pd.read_csv('data/BahnhofErsteKlasse.csv', sep=';')
    return df


station_df = stations()
station_df['type'] = station_df.type.apply(lambda x: x.split(','))
stations_collection.insert_many(station_df.to_dict('records'))
