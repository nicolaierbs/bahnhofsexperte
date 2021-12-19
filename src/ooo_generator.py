import pymongo
import random

client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client['bahnhofsexperte']
stations_collection = db['stations']
ooo_collection = db['ooo_templates']


def name(mongo_id):
    return stations_collection.find_one({'_id': mongo_id})['name']


def question():
    template = ooo_collection.aggregate([{"$sample": {"size": 1}}]).next()
    print('Welcher Bahnhof passt nicht in diese Gruppe?')
    # print(template)
    stations = random.sample(template['matchingstations'], 3)
    wrong_station = random.choice(template['otherstations'])
    random.shuffle(stations)

    position = random.randint(0, len(stations))
    stations.insert(position, wrong_station)
    stations = [name(station) for station in stations]
    n = 1
    for station in stations:
        print(f'{n}: {station}')
        n += 1

    return [position+1, name(wrong_station), template['dimension'], str(template['discriminator'])]


if __name__ == '__main__':
    while True:
        solution = question()
        response = input()
        if int(response) == solution[0]:
            print(f'Richtig! Alle anderen Bahnhöfe sind ähnlich in der Dimension {solution[2]} ({solution[3]}).')
        else:
            print(f'Richtig ist {solution[1]}. '
                  f'Alle anderen Bahnhöfe sind ähnlich in der Dimension {solution[2]} ({solution[3]}).')
        # print(solution)
        print('-------')
