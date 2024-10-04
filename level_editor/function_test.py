# function_test.py

import json

# Define a basic structure
data = {
    "actor_name": "SampleActor",
    "view_mesh": "sample_view.gltf",
    "collider_mesh": "sample_collider.gltf",
    "position": [0, 1, 0],
    "velocity": [0, 0, 0],
    "acceleration": [0, 0, 0]
}

# Save the structure to a JSON file
def save_to_json(data, filename):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)

# Load the structure from a JSON file
def load_from_json(filename):
    with open(filename, 'r') as file:
        return json.load(file)

# Example usage
filename = "actor_test.json"
save_to_json(data, filename)
loaded_data = load_from_json(filename)

print("Saved data:", data)
print("Loaded data:", loaded_data)
