import json

class teste():
	def __init__(self):
		self.a = 'lala'
		self.b_val = 1
		self.c = 1.2



t = teste()

t_ser = json.dumps(t.__dict__)

with open('t.txt', 'w') as file_name:
	file_name.write(t_ser)

with open('t.txt', "w") as file:
    file.write(json.dumps(t.__dict__, file, indent=4))
