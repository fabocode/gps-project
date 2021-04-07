import json

def write_to_json_file(path, filename, data):
	file_path_name_wext = './' + path + '/' + filename + '.json'
	with open(file_path_name_wext, 'w') as fp:
		json.dump(data, fp)


path = './'
filename = 'write2'
data = {}
string1= 'nuevo'
string2 = 'nuevo2'
data['test'] = ['test3]']
data['test'].append(string1)
data["hello"] = ['world2']
data['hello'].append(string2)


write_to_json_file(path, filename, data)