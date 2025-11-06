import json
import os
import matplotlib.pyplot as plt
import numpy as np
# Assuming your normalize_bbox and get_image_dimensions functions are imported or defined above

import math
import os
from PIL import Image
import json
import numpy as np

# --- 1. CORE SCALING FUNCTION ---

def normalize_single_coord(coord_value, original_dimension):
    """
    Scales a single raw pixel coordinate (X or Y) to the 0-1000 range.
    
    Args:
        coord_value (int): The raw pixel coordinate.
        original_dimension (int): The image's original width or height.
        
    Returns:
        int: The normalized coordinate, clamped between 0 and 1000.
    """
    if original_dimension == 0:
        return 0
        
    # Apply the scaling formula and round
    normalized = round((coord_value / original_dimension) * 1000)
    
    # Ensure the value stays within [0, 1000] bounds
    return max(0, min(1000, normalized))


# --- 2. FULL BOUNDING BOX NORMALIZATION ---

def normalize_bbox(bbox, width, height):
    """
    Normalizes a full bounding box [x0, y0, x1, y1] using the image dimensions.
    """
    x0, y0, x1, y1 = bbox
    
    # Normalize X coordinates using Width
    x0_norm = normalize_single_coord(x0, width)
    x1_norm = normalize_single_coord(x1, width)
    
    # Normalize Y coordinates using Height
    y0_norm = normalize_single_coord(y0, height)
    y1_norm = normalize_single_coord(y1, height)
    
    return [x0_norm, y0_norm, x1_norm, y1_norm]


# --- 3. IMAGE DIMENSION RETRIEVAL ---

def get_image_dimensions(doc_id, image_dir='data/raw/funsd/dataset/training_data/images'):
    """
    Gets the original pixel width and height of an image using PIL/Pillow.
    
    Args:
        doc_id (str): Document ID (e.g., '000010').
        image_dir (str): Path to the image folder.
        
    Returns:
        tuple: (width, height) tuple, or (0, 0) if file not found.
    """
    # Assuming FUNSD images are PNG
    image_path = os.path.join(image_dir, f'{doc_id}.png')
    
    try:
        with Image.open(image_path) as img:
            return img.size # Returns (width, height)
    except FileNotFoundError:
        print(f"Error: Image not found for ID {doc_id}.")
        return 0, 0

def plot_spatial_clustering(doc_ids, json_dir, image_dir):
    """
    Analyzes and plots the normalized center-point coordinates of meaningful entities.
    """
    # Lists to store normalized center-points for plotting
    x_centers = []
    y_centers = []
    
    for doc_id in doc_ids:
        # Load JSON and get dimensions (using functions from Phase 1)
        json_path = os.path.join(json_dir, f'{doc_id}.json')
        width, height = get_image_dimensions(doc_id, image_dir)
        
        if width == 0 or height == 0:
            continue
            
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except FileNotFoundError:
            continue
        
        # Process each entity in the document
        for entity in data['form']:
            label = entity.get('label')
            
            # CRITICAL FILTER: Only process 'meaningful' labels (questions/answers)
            if label in ['question', 'answer']:
                raw_box = entity['box']
                
                # 1. Normalize the raw box
                norm_box = normalize_bbox(raw_box, width, height)
                x0, y0, x1, y1 = norm_box
                
                # 2. Calculate the center point (Xc, Yc)
                x_center = (x0 + x1) / 2
                y_center = (y0 + y1) / 2
                
                x_centers.append(x_center)
                y_centers.append(y_center)
                
    # --- Plotting the Results ---
    plt.figure(figsize=(8, 8))
    
    # Scatter plot: x_centers vs. y_centers
    # Note: In images, the Y-axis increases downward, so we typically plot 
    # the y_centers descending to match visual expectation.
    plt.scatter(x_centers, 1000 - np.array(y_centers), s=10, alpha=0.6, color='darkviolet')
    
    # Set the bounds to match the 0-1000 normalized grid
    plt.xlim(0, 1000)
    plt.ylim(0, 1000)
    
    plt.title('Spatial Clustering of Key Entities (Normalized $1000 \times 1000$ Grid)')
    plt.xlabel('Normalized X Coordinate (0 - 1000)')
    plt.ylabel('Normalized Y Coordinate (0 - 1000) [Bottom to Top]')
    plt.grid(True, linestyle='--', alpha=0.5)
    
    plt.gca().set_aspect('equal', adjustable='box') # Ensures the plot isn't distorted
    plt.savefig('eda_spatial_clustering.png')
    plt.show()



# --- Execution Block ---

# 1. Define your directories (Update these paths!)
JSON_DIR = 'data/raw/funsd/dataset/training_data/annotations'
IMAGE_DIR = 'data/raw/funsd/dataset/training_data/images' 

# 2. Sample enough documents (10-20 IDs) for a meaningful plot
sample_doc_ids = [
    '00040534', '00070353', '00093726', '00283813', '660978',
    '716552', '00836244','00836816', '00837285', '00838511_00838525'
]

# Run the analysis
plot_spatial_clustering(sample_doc_ids, JSON_DIR, IMAGE_DIR)

# Don't forget to implement or import the required functions:
# normalize_bbox_coord, normalize_bbox, and get_image_dimensions.