import json
import os

def main():
    objects = loadObjects()
    properties = loadProperties()
    r=None
    r=traverse(objects, [])
    #print(r)
    print("Gathering Objects...")
    return r
    
def loadObjects():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'objects.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        return data["data"]

def loadProperties():
    script_dir = os.path.dirname(__file__)
    file_path = os.path.join(script_dir, 'properties.json')
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
        col=data["data"]["collection"]
        collection = {}
        for c in col:
            collection[c["objectid"]] = c
        return collection
        
def lookupObjectProperties(dbid):
    properties=loadProperties()
    el=properties[dbid]
    return el

def traverse(objects,list_of_rows):
    if "name" in objects:
        p=lookupObjectProperties(objects["objectid"])
        if "properties" not in p:
            print()
            objName=objects["name"]
            print(f'Category: {objName}')
            list_of_rows.append([f"Category", f"{objName}"])
        else:
            objName=objects["name"]
            objCount=len(objects["objects"])
            print(f'  Type: {objName} ({objCount})')
            list_of_rows.append([f"{objName}", f"{objCount}"])
    if "objects" in objects:
        for o in objects["objects"]:
            if "objects" not in o:
                p=lookupObjectProperties(o["objectid"])
                print(f"    {o}")
            else:
                for o2 in o["objects"]:
                    traverse(o2, list_of_rows)
    print()
    return list_of_rows

if __name__ == "__main__":
    main()
