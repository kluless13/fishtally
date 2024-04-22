`dist.py` aims to measure the distance of the object from the camera. This is not an accurate measure and needs better guidance. 

However, creating a utility where users can input camera specifications to automatically calculate the field of view (FOV) and subsequently use this to determine the scale of pixels per meter or centimeter is a very practical and useful approach. This method can help in automatically adjusting the measurement scale based on different camera setups without manual calibration.

Here's a breakdown of what the code can do and how to structure it:

### Steps to Implement the Code

1. **Input Camera Specifications**:
   - The user will input the camera's sensor size (width in mm), focal length (in mm), and the distance from the camera to the object (in meters).

2. **Calculate the Horizontal Field of View**:
   - Use the formula for the horizontal field of view:
     \[
     FOV = 2 \times \text{atan}\left(\frac{\text{sensor width}}{2 \times \text{focal length}}\right)
     \]
   - This gives you the FOV in radians, which you can convert to degrees if needed.

3. **Determine Real-world Width of the View at a Certain Distance**:
   - Calculate the real-world width of the view at the given distance using the FOV:
     \[
     \text{Width at distance} = 2 \times (\text{distance to object} \times \text{tan}(\text{FOV}/2))
     \]

4. **Convert the Real-world Width to Pixels**:
   - Using the video's resolution (width in pixels), establish how many pixels represent the real-world width calculated in the previous step.

5. **Implement Pixel per Meter/Centimeter Conversion**:
   - Use the pixel width to determine the scale of pixels per meter or centimeter.

Example code in `fov.py`.

To use the function `calculate_pixels_per_meter` effectively, you'll need realistic values for the camera's sensor width, focal length, distance to the object, and video resolution width. Here are some typical values you might encounter with a standard digital camera or a smartphone, which you can use as input for the calculations:

### Example Inputs

1. **Camera Sensor Width**: This is typically measured in millimeters. For most consumer cameras and smartphones, sensor widths can range from around 4 mm to around 35 mm for more professional equipment. Let's use a common sensor size for smartphones:
   - **Sensor Width**: 6 mm (0.006 meters when converted)

2. **Focal Length**: This is the distance between the camera sensor and the lens when the subject is in focus, typically measured in millimeters. Common focal lengths for smartphone cameras range from about 4 mm to 10 mm.
   - **Focal Length**: 4.5 mm (0.0045 meters when converted)

3. **Distance to Object**: This depends on what you are measuring. For instance, if you are measuring something in a room or at a short distance:
   - **Distance to Object**: 5 meters

4. **Video Resolution Width**: This depends on the camera's video capturing resolution. Common widths include:
   - 1920 pixels (for full HD)
   - 1280 pixels (for HD)
   - 3840 pixels (for 4K)

Assuming you are using a fairly typical modern smartphone camera capturing in full HD, here are the inputs you might use:

- **Sensor Width**: 6 mm
- **Focal Length**: 4.5 mm
- **Distance to Object**: 5 meters
- **Video Width**: 1920 pixels

This is assuming we know how far at least one object is in front of the camera. An ideal set up would include a calibration object place within the field of vision to get an accurate estimate.

Unhappy with perception.py, mouse click trigger very dodgy.