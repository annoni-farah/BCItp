import json

n = '2'
s = '2'
x= '3'
y = '3'

with open("text", "w") as file:
    file.write(json.dumps({'numbers':"1 2 3 4 5", 'strings':s, 'x':x, 'y':y}, file, indent=4))


from pprint import pprint

with open('text') as data_file:    
    data = json.load(data_file)

pprint(data)
