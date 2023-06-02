import json

def check_arra_first(file_name):
    with open(file_name, 'r') as file:
        data = json.load(file)
    return data

def check_array_second(data):
    male_data = []
    female_data = []
    for item in data:
        if item['sex'] not in ['M', 'F']:
            continue
        if item['age'] <= 0:
            continue
        if not (0 < len(item['name']) <= 64):
            continue
        if item['sex'] == 'M':
            male_data.append(item)
        else:
            female_data.append(item)
    return male_data, female_data

data = check_arra_first('test.json')
male_data, female_data = check_array_second(data)
print("M array", male_data , "\n")
print("F array", female_data)