import json

#define data
staffdata = {'admin': 'superman',
             '1002345': 'staff'
} #room: level , capacity, office/classroom

#writes JSON file
with open('staffdata.json','w',encoding='utf8') as outfile:
    str_ = json.dumps(staffdata,
                      indent=4,
                      separators=(',', ': '), ensure_ascii=False)
    outfile.write(str_)
    #indent: Use 4 spaces to indent each entry, e.g. when a new dict is started (otherwise all will be in one line),
    #separators: To prevent Python from adding trailing whitespaces

#read JSON file
with open('staffdata.json') as data_file:
    data_loaded = json.load(data_file)

print(staffdata==data_loaded)

