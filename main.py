import json
import os
from copy import copy

# Declare USERID here
USERID = ""

# Define vanilla blocks
block_obj = {
	"color": str,
	"controller": dict,
	"pos": dict,
	"shapeId": str,
	"xaxis": int,
	"zaxis": int
}

# Define controller dict within block
vanilla_controller = {
	"active": bool,
	"controllers": any,
	"id": int,
	"joints": any,
	"mode": int # MODIFY
}
non_vanilla_controller = {
	"containers": any,
	"controllers": any,
	"data": str, # MODIFY
	"id": int,
	"joints": any
}

# Define shape ids
shapeids = {
	"vanilla": "9f0f56e8-2c31-4d83-996c-d00a9b296c3f",
	"circuits": "8f98db04-72eb-4a3a-88a1-f4f3e8d818ee",
	"vincling": "bc336a10-675a-4942-94ce-e83ecb4b501a"
}

# Define modes
vanilla_modes = {
	"AND": 0,
	"OR": 1,
	"XOR": 2,
	"NAND": 3,
	"NOR": 4,
	"XNOR": 5
}

vincling_data = {
	"AND": "gExVQQAAAAEFBQDAAgAAAAIAbW9kZQgA",
	"OR": "gExVQQAAAAEFBQDAAgAAAAIAbW9kZQgB",
	"XOR": "gExVQQAAAAEFBQDAAgAAAAIAbW9kZQgC",
	"NAND": "gExVQQAAAAEFBQDAAgAAAAIAbW9kZQgD",
	"NOR": "gExVQQAAAAEFBQDAAgAAAAIAbW9kZQgE",
	"XNOR": "gExVQQAAAAEFBQDAAgAAAAIAbW9kZQgF"
}

circuits_data = {
	"AND": "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggA",
	"OR": "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggB",
	"XOR": "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggC",
	"NAND": "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggD",
	"NOR": "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggE",
	"XNOR": "gExVQQAAAAEFBQDwAgIAAAAEgG9wZXJhdGlvbggF"
}

# Define file footer content for specifying mod dependencies
dependencies_format = {
	"vanilla": None,
	"circuits": {
		"contentId": "5a69ed67-ebbc-481e-b7e1-cbd1455b916a",
		"name": "Circuit Creator",
		"shapeIds": list(circuits_data.values()),
		"steamFileId":2289714402
	},
	"vincling": {
		"contentId": "a81e02e7-a084-43a4-933d-09f64078770d",
		"name": "Vincling's Logic Tools & Parts Mod",
		"shapeIds": list(vincling_data.values()),
		"steamFileId":2568516747
	}
}

def get_blueprint(user, fname):
    location = os.getenv('APPDATA') + f"\\Axolot Games\\Scrap Mechanic\\User\\{user}\\Blueprints\\{fname}\\blueprint.json"
    print(f"Loading blueprint now...")
    try:
        with open(location, "r") as f:
            print("File loaded!")
            return True, f.read()
    except Exception as e:
        print(f"Failed to load file! \n{e}")
        return False, None

def save_blueprint(user, fname, updated_contents):
    location = os.getenv('APPDATA') + f"\\Axolot Games\\Scrap Mechanic\\User\\{user}\\Blueprints\\{fname}\\blueprint.json"
    print(f"Saving blueprint now...")
    try:
        with open(location, "w") as f:
            f.write(json.dumps(updated_contents))
            f.close()
            print("File saved!")
    except Exception as e:
        print(f"Failed to save file! \n{e}")

def index_blueprint(blueprint_data):
    index = 0
    index_data = list()
    index_count = {
        "vanilla": 0,
        "vincling": 0,
        "circuits": 0
    }
    
    for body_index in range(len(blueprint_data["bodies"])):
        # Reset index counter for each new child iteration
        index = 0
        for child in blueprint_data["bodies"][body_index]["childs"]:
            # Test if a specific child object is a logic block
            if child.keys() == block_obj.keys():
                for key in child.keys():
                    if type(child[key]) != block_obj[key]:
                        break
                
                # Vanilla type
                if child["controller"].keys() == vanilla_controller.keys():
                    for key in child["controller"].keys():
                        # Ignore if any
                        if vanilla_controller[key] == any:
                            continue
                        
                        # Verify datatype
                        if type(child["controller"][key]) not in [type(vanilla_controller[key]), vanilla_controller[key]]:
                            print(f"Datatype missmatch found while testing for a vanilla block at index {index}. \n key {key} in {child['controller']}\n Expected: {type(vanilla_controller[key])} or {vanilla_controller[key]}, got: {type(child['controller'][key])}")
                            exit()
                    
                    for key in vanilla_modes.keys():
                        if vanilla_modes[key] == child["controller"]["mode"]:
                            index_data.append({
                                "index": index,
                                "body_index": body_index,
                                "type": "vanilla",
                                "mode": key
                            })
                            break
                    index_count["vanilla"] += 1
                
                # Modded type
                if child["controller"].keys() == non_vanilla_controller.keys():
                    for key in child["controller"].keys():
                        # Ignore if any
                        if non_vanilla_controller[key] == any:
                            continue
                        
                        # Verify datatype
                        if type(child["controller"][key]) not in [type(non_vanilla_controller[key]), non_vanilla_controller[key]]:
                            print(f"Datatype missmatch found while testing for a modded block at index {index}. \n key {key} in {child['controller']}\n Expected: {type(non_vanilla_controller[key])} or {non_vanilla_controller[key]}, got: {type(child['controller'][key])}")
                            exit()
                    
                    # Determine what specific type of modded block
                    
                    # Vincling type
                    if child["controller"]["data"] in vincling_data.values():
                        for key in vincling_data.keys():
                            if vincling_data[key] == child["controller"]["data"]:
                                index_data.append({
                                    "index": index,
                                    "body_index": body_index,
                                    "type": "vincling",
                                    "mode": key
                                })
                                break
                        index_count["vincling"] += 1
                    
                    # Circuits type
                    if child["controller"]["data"] in circuits_data.values():
                        for key in circuits_data.keys():
                            if circuits_data[key] == child["controller"]["data"]:
                                index_data.append({
                                    "index": index,
                                    "body_index": body_index,
                                    "type": "circuits",
                                    "mode": key
                                })
                                break
                        index_count["circuits"] += 1
            index += 1
    return index_data, index_count

def convert_vanilla(index, blueprint_data_full, blueprint_data):
    for child_selection in index:
        # Do not modify if already vanilla
        if child_selection["type"] == "vanilla":
            continue
        
        # Simplify
        child = blueprint_data["bodies"][child_selection["body_index"]]["childs"][child_selection["index"]]
        
        if "controller" in child:
            # Backup the controller data
            controller = copy(child["controller"])
        
        # Change the shape ID to vanilla
        child["shapeId"] = shapeids["vanilla"]
        
        # Convert the block mode
        child["controller"] = {
            "active": False,
            "controllers": controller["controllers"],
            "id": controller["id"],
            "joints": controller["joints"],
            "mode": vanilla_modes[child_selection["mode"]]
        }
    
    # Save blueprint but do not modify dependencies
    blueprint_data_full = blueprint_data

def convert_vincling(index, blueprint_data_full, blueprint_data):
    for child_selection in index:
        # Do not modify if already vincling
        if child_selection["type"] == "vincling":
            continue
        
        # Simplify
        child = blueprint_data["bodies"][child_selection["body_index"]]["childs"][child_selection["index"]]
        
        if "controller" in child:
            # Backup the controller data
            controller = copy(child["controller"])
        
        # Change the shape ID to vincling
        child["shapeId"] = shapeids["vincling"]
        
        # Convert the block
        child["controller"] = {
            "containers": None,
            "controllers": controller["controllers"],
            "data": vincling_data[child_selection["mode"]],
            "id": controller["id"],
            "joints": controller["joints"]
        }
    
    # Save blueprint
    blueprint_data_full = blueprint_data
    
    # Update file dependencies
    if "dependencies" in blueprint_data_full:
        if dependencies_format["vincling"] not in blueprint_data_full["dependencies"]:
            blueprint_data_full["dependencies"].append(dependencies_format["vincling"])
    
    else:
        blueprint_data_full["dependencies"] = [
            dependencies_format["vincling"]
        ]

def convert_circuits(index, blueprint_data_full, blueprint_data):
    for child_selection in index:
        # Do not modify if already circuits
        if child_selection["type"] == "circuits":
            continue
        
        # Simplify
        child = blueprint_data["bodies"][child_selection["body_index"]]["childs"][child_selection["index"]]
        
        if "controller" in child:
            # Backup the controller data
            controller = copy(child["controller"])
        
        # Change the shape ID to circuits
        child["shapeId"] = shapeids["circuits"]
        
        # Convert the block
        child["controller"] = {
            "containers": None,
            "controllers": controller["controllers"],
            "data": circuits_data[child_selection["mode"]],
            "id": controller["id"],
            "joints": controller["joints"]
        }
    
    blueprint_data_full = blueprint_data
    
    # Update file dependencies
    if "dependencies" in blueprint_data_full:
        if dependencies_format["circuits"] not in blueprint_data_full["dependencies"]:
            blueprint_data_full["dependencies"].append(dependencies_format["circuits"])
    
    else:
        blueprint_data_full["dependencies"] = [
            dependencies_format["circuits"]
        ]

if __name__ == "__main__":
    # Get JSON file contents
    fname = input("Enter the UUID of the blueprint to load: ")
    result, payload = get_blueprint(USERID, fname)
    
    # Exit script if failed to load blueprint
    if not result:
        exit()
    
    # Parse the JSON contents
    blueprint_json = json.loads(payload)
    
    # Detect required keys
    for key in ["bodies", "version"]:
        if not key in blueprint_json.keys():
            print("Not a Scrap Mechanic blueprint file!")
            exit()
    
    # Make a backup
    blueprint_json_full = copy(blueprint_json)
    
    # Index all exisitng logic blocks in the file, and verify integrity
    print("Indexing and verifying blueprint structure and data...")
    index, counts = index_blueprint(blueprint_json)
    print(f"Found {counts['vanilla']} Vanilla blocks, {counts['vincling']} Vincling blocks, and {counts['circuits']} Circuits blocks.")
    
    # Menu
    print("=== Convert Menu ===\nPlease enter the menu number to convert all blocks into.\n1. Vanilla\n2. Vincling\n3. Circuits\n4. Abort")
    match int(input("> ")):
        case 1:
            print("Converting all blocks into vanilla...")
            convert_vanilla(index, blueprint_json_full, blueprint_json)
            match input("Converted! Are you sure you want to save? y/n\n> "):
                case "y":
                    save_blueprint(USERID, fname, blueprint_json_full)
                case _:
                    print("Aborting...")
        case 2:
            print("Converting all blocks into vincling blocks...")
            convert_vincling(index, blueprint_json_full, blueprint_json)
            match input("Converted! Are you sure you want to save? y/n\n> "):
                case "y":
                    save_blueprint(USERID, fname, blueprint_json_full)
                case _:
                    print("Aborting...")
        case 3:
            print("Converting all blocks into circuits blocks...")
            convert_circuits(index, blueprint_json_full, blueprint_json)
            match input("Converted! Are you sure you want to save? y/n\n> "):
                case "y":
                    save_blueprint(USERID, fname, blueprint_json_full)
                case _:
                    print("Aborting...")
        case _:
            print("Aborting...")
    