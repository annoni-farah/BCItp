'''
Tests to save a python object to a file and load it again

two options: 
(1) - using json
- humand readable
- hard to decode (need to specify all attr of class)

(2) - using pickle
- not human readable
- easy to decode
'''


class teste():
	def __init__(self):
		self.a = 'lala'
		self.b_val = 1
		self.c = 1.2

t = teste()

# WITH JSON

# import json

# t_ser = json.dumps(t.__dict__)

# with open('t.txt', 'w') as file_name:
# 	file_name.write(t_ser)

# with open('t.txt', "w") as file:
#     file.write(json.dumps(t.__dict__, file, indent=4))

# WITH PICKLE

import pickle

with open('t.pkl', 'w') as file_name:
	pickle.dump(t, file_name)


with open('t.pkl', 'r') as file_name:
	t2 = pickle.load(file_name)

