from pathlib import Path
from json import load
import os

directory: str = "mtsd_v2_fully_annotated/annotations" # the directory containing all of the image annotations in JSON format.
classes = dict()
files = Path(directory).glob("*.json")

# The YOLO data format directory.
os.makedirs("data", exist_ok=True)

for file in files:
    data = dict()

    # Get the name of the traffic sign class
    with open(file, "r") as f:
        data = load(f)
        # Check to see if the labels are present
        try: 
            data["objects"][0]["label"]
        except:
            continue
    
    # Iterate through all the objects
    for bounding_box_object in data["objects"]:
        traffic_sign_class = bounding_box_object["label"]

        # Save the traffic sign class information into classes.txt
        if traffic_sign_class not in classes:
            classes[traffic_sign_class] = len(classes)
            with open("classes.txt", "a") as f:
                f.write(f"\t{len(classes)}: {traffic_sign_class}\n")

        # Convert the JSON format to the YOLO format
        image_width = data["width"]
        image_height = data["height"]

        bounding_box_coords = bounding_box_object["bbox"]

        # Get all the coordinate data and normalize
        x_center = (bounding_box_coords["xmax"] + bounding_box_coords["xmin"]) / 2
        x_center /= image_width
        y_center = (bounding_box_coords["ymax"] + bounding_box_coords["ymin"]) / 2
        y_center /= image_height

        bounding_box_width = (bounding_box_coords["xmax"] - bounding_box_coords["xmin"]) / image_width
        bounding_box_height = (bounding_box_coords["ymax"] - bounding_box_coords["ymin"]) / image_height
        
        # Save the values in the YOLO data format
        with open(f"data/{file.stem}.txt", "a") as f:
            f.write(f"{classes[traffic_sign_class]} {x_center} {y_center} {bounding_box_width} {bounding_box_height}\n")