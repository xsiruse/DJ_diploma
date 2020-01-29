import json
from shop.settings import DATABASES
from django.core.management import call_command

file = 'youla.json'
fixt = 'initial_data'

def converter(file):
    with open(file, encoding='utf-8') as json_file:
        data = json.load(json_file)
    # pprint(data)
    result = []

    for i, item in enumerate(data['data']):
        # print(i, item)
        fixture = {}
        fixture['model'] = 'app.product'
        fixture['pk'] = i + 1
        fixture['fields'] = {}
        fixture['fields']['category'] = item['subcategory_Id']
        fixture['fields']['title'] = item['title']
        fixture['fields']['price'] = item['price']
        fixture['fields']['image'] = item['images']
        fixture['fields']['description'] = item['description']
        result.append(fixture)

    return result


def write_fixture(name):
    with open(name + '.json', 'w') as json_file:
        f = json.dump(converter(file), json_file)
    return json_file.name


if __name__ == '__main__':
    x = write_fixture(fixt)
    call_command('loaddata', x, database=DATABASES)
