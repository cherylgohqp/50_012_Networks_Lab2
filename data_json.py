import json

#define data
data = {'1.205': ['level 2','50', 'Classroom'],
        '1.208': ['level 2','45','Classroom'],
        '1.704': ['level 7','20','Office']
} #room: level , capacity, office/classroom

#writes JSON file
with open('data.json','w',encoding='utf8') as outfile:
    str_ = json.dumps(data,
                      indent=4,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(str_)
    #indent: Use 4 spaces to indent each entry, e.g. when a new dict is started (otherwise all will be in one line),
    #separators: To prevent Python from adding trailing whitespaces

#read JSON file
with open('data.json') as data_file:
    data_loaded = json.load(data_file)

print(data==data_loaded)

