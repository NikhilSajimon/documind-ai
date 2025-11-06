import os
from PIL import Image
import pandas as pd # For clean table output

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

# Assuming the get_image_dimensions function is defined or imported here:
# ... (insert get_image_dimensions function code if not using a utility module) ...

def generate_layout_variance_table(doc_ids, image_dir):
    """
    Retrieves the original dimensions (W x H) for a list of documents.
    """
    variance_data = []
    
    for doc_id in doc_ids:
        width, height = get_image_dimensions(doc_id, image_dir)
        
        # Calculate Aspect Ratio (Width / Height) as an additional metric
        aspect_ratio = round(width / height, 2) if height else 0
        
        variance_data.append({
            'Document ID': doc_id,
            'Original Width (W)': width,
            'Original Height (H)': height,
            'Aspect Ratio (W/H)': aspect_ratio
        })

    # Create a DataFrame for professional tabular output
    df = pd.DataFrame(variance_data)
    
    # Calculate min/max range for the report summary
    min_w = df['Original Width (W)'].min()
    max_w = df['Original Width (W)'].max()
    
    print("\n--- Document Layout Variance Report ---")
    print(f"Width Range: {min_w} to {max_w} pixels")
    print("-" * 50)
    print(df.to_string(index=False))
    print("-" * 50)
    
    return df

# --- Execution Block ---
IMAGE_DIR = 'data/raw/funsd/dataset/training_data/images' 
sample_doc_ids = [
    '00040534', '00070353', '00093726', '00283813', '660978',
    '716552', '00836244','00836816', '00837285', '00838511_00838525'
]

variance_df = generate_layout_variance_table(sample_doc_ids, IMAGE_DIR)