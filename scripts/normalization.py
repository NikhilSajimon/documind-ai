import math


def normalize_single_coord(coord_value, original_dimension):
    """ Scales a single raw pixel coordinate (x or y) into the 0-1000 range
    
    Args: 
        coord_value (int): The raw pixel coordiante
        original_dimension (int): The images original width or height
        
    Returns: 
        int: The normalized coordinate, clamped between 0 and 1000
    """

    if original_dimension == 0:
        return 0
    normalized = (coord_value / original_dimension)*1000
    normalized = round(normalized)
    return max(0, min(normalized, 1000))




def normalize_bbox(bbox, width, height):
    """
    Normalizes a full bounding box using the image's original dimensions.
    
    Args:
        bbox (list): Raw box [x0, y0, x1, y1] in pixel values.
        width (int): Original image width.
        height (int): Original image height.
        
    Returns:
        list: Normalized box [x0_norm, y0_norm, x1_norm, y1_norm].
    """
    x0, y0, x1, y1 = bbox
    
    # Normalize X coordinates (x0 and x1) using the original WIDTH
    x0_norm = normalize_single_coord(x0, width)
    x1_norm = normalize_single_coord(x1, width)
    
    # Normalize Y coordinates (y0 and y1) using the original HEIGHT
    y0_norm = normalize_single_coord(y0, height)
    y1_norm = normalize_single_coord(y1, height)
    
    # Return the new, scaled bounding box
    return [x0_norm, y0_norm, x1_norm, y1_norm]




# --- Verification using your sample data ---
test_w, test_h = 762, 1000
test_box = [110, 109, 185, 124] 

normalized_box = normalize_bbox(test_box, test_w, test_h)

# Check the results:
# Xmin (110) should be ~144.
# Ymin (109) should be ~109.
# Xmax (185) should be ~243.
# Ymax (124) should be ~124.

print(f"Resulting Normalized Box: {normalized_box}")