import os
import json
import ijson
   
def loadObjects():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'objects__to large.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return data["data"]

def load_json(filename):
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, filename)
    with open(file_path, 'r') as f:
        return json.load(f)


js=load_json('objects__to large.json')
print('done')

