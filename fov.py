import math

def calculate_pixels_per_meter(sensor_width, focal_length, distance_to_object, video_width):
    # Calculate the field of view in radians
    fov = 2 * math.atan((sensor_width / 2) / focal_length)
    
    # Calculate the width in meters at the given distance
    width_at_distance = 2 * (distance_to_object * math.tan(fov / 2))
    
    # Calculate how many pixels represent one meter
    pixels_per_meter = video_width / width_at_distance
    
    return pixels_per_meter

# User inputs
sensor_width = float(input("Enter the camera sensor width (mm): ")) / 1000  # Convert mm to meters
focal_length = float(input("Enter the focal length (mm): ")) / 1000  # Convert mm to meters
distance_to_object = float(input("Enter the distance to the object (meters): "))
video_width = int(input("Enter the video resolution width (pixels): "))

# Calculate pixels per meter
ppm = calculate_pixels_per_meter(sensor_width, focal_length, distance_to_object, video_width)
print(f"Pixels per meter: {ppm}")