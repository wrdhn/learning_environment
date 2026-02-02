import json
import os

file_path = os.path.join(os.path.dirname(__file__), '..', 'materials', 'python.json')

def material(type):
    if type == 'r':
        with open(file_path, 'r') as f:
            return json.load(f)
    elif type == 'w':
        with open(file_path, 'w') as f:
            json.dump({}, f)
    else:
        print('Invalid param!')