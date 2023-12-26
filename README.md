# FishTally

Objective: Use yolov8 to build a tracking model. Model weights can be used by the ByteTrack tracking algorithm.  The fish counter can be used to count fish (in this insatance) and keep a tally of the count. The machine can identify fish far better than the human eye at longer intervals of time. The AI tracker can tally fish from surveys to better understand their range and count with almost little to no human error. The application of this tool can be vast, ranging from helping marine survey teams using AUVs or other video collecting machines, to helping ecologists make informed decisions and better understand habitat structure. This is only an example of what can be done, this use case can be tailored for more specific needs depending on the context of the task.

Here is FishTally being used on a video of Yellow Tang.
<div align="center">
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/Tang-result.gif" width="49%"/>
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/tang-tracker%20(2).gif" width="49%"/>
</div>

FishTally's tracker has also been used for other classes, here is an example for the three-striped damselfish.
<div align="center">
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/damselfish.gif" width="49%"/>
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/damselfish-tracker.gif" width="49%"/>
</div>

An example for FishTally would be to use it to count invasive species, such as Lionfish.
<div align="center">
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/lionfish.gif">
</div>

Here is a test to check if the tool worked at a multi-species level:
<div align="center">
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/multiclass.gif">
</div>

FishTally goes beyond a single line threshold, it contains source code to adjust for more than one line, and keep a count for each line used.
<div align="center">
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/2lines.gif" width="49%"/>
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/3lines
    .gif" width="49%"/>
</div>

Polygon zones can also be introduced to check species count in a particular zone. So far, FishTally has source code for 1 polygon, but more can be created.
<div align="center">
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/polygon.gif">
</div>

Snippets of videos have been used to demonstrate the theory into practice. A simple version of the FishTally tool has been created into a CLI tool which can be used with ease. The source code can be adjusted accordingly.

## Setup Guide

### Prerequisites

Ensure you have the following prerequisites installed on your system:

- Python 3.6 or higher
- Git
- Pip (Python package manager)

### Installation Steps

1. **Clone the Repository**

   First, clone the repository containing the `fishtally.py` tool and its associated files to your local machine.

   ```bash
   git clone https://github.com/kluless13/paper2.git
   cd paper2
   ```

2. **Install Requirements**

   The `fishtally.py` tool relies on ByteTrack for object tracking. Run the provided setup script to clone and set up ByteTrack.

   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

3. **Verification**

   To verify that the installation is successful, you can run a simple test command or check the versions of critical components like Python, Git, and Pip.

   ```bash
   python --version
   git --version
   pip --version
   ```

# Running FishTally

This repository contains tools for detecting and counting fish in video footage using YOLO-based models. There are two main scripts: `fishtally.py` for processing videos and `list_classes.py` for listing available classes in the YOLO model.

## Usage

### Listing Available Classes

Before using the fish tallying tool, you can list the available classes in your YOLO model. This will help you identify the correct class ID for detection. [This is the weights file: https://github.com/kluless13/paper2/blob/main/Assets/multiclass-wts.pt]

**List Classes**

   Run `list_classes.py` with the path to your model weights:

   ```bash
   python list_classes.py --model_weights <path_to_weights>
   ```

   Replace `<path_to_weights>` with the path to your YOLO model weights file. This will print out the class names and their corresponding indices.

### Checking frame to plot points 

To make sure you know where to plot the ploints for your detector, use `frames.py` as mentioned below:


**Frame Check**

   ```bash
   python frames.py --source_video <path_to_source_video.mp4> --save_path <path_to_reference_img.jpg>
   ```

### Running the Fish Tallying Tool

After identifying the correct class ID, you can proceed to use `fishtally.py`.

1. **Open the Terminal**

   Open a terminal window and navigate to the directory where `fishtally.py` is located.

2. **Running the Tool**

   Use the following command structure to run the tool:

   ```bash
   python fishtally.py --model_weights <path_to_weights> --source_video <path_to_source_video> --target_video <path_to_output_video> --detector_type <detector_type> --class_id <class_id>
   ```

   Replace `<path_to_weights>`, `<path_to_source_video>`, and `<path_to_output_video>` with the respective paths. For `<detector_type>`, choose from `single_line`, `multi_line`, or `polygon`. Replace `<class_id>` with the ID of the class you want to detect.

   - For `single_line` and `multi_line`, specify the line coordinates.
   - For `polygon`, provide the polygon points [bottom left, top left, top right and bottom right].

3. **Example Commands**

   - **Single Line:**
     ```bash
     python fishtally.py --model_weights weights.pt --source_video source.mp4 --target_video output.mp4 --detector_type single_line --line_start 100 200 --line_end 300 400 --class_id 3
     ```

   - **Multiple Lines:**
     ```bash
     python fishtally.py --model_weights weights.pt --source_video source.mp4 --target_video output.mp4 --detector_type multi_line --line1_start 100 200 --line1_end 300 400 --line2_start 500 600 --line2_end 700 800 --class_id 3
     ```

   - **Polygon:**
     ```bash
     python fishtally.py --model_weights weights.pt --source_video source.mp4 --target_video output.mp4 --detector_type polygon --polygon_points 100 200 300 400 500 600 700 800 --class_id 3
     ```

    Replace the coordinates and the class ID in these examples with those relevant to your specific use case. Here is the arrangement of the coordinates: bottom left, top left, top right and bottom right.

4. **Viewing the Results**

   After running the command, the tool will process the video and output the results to the path specified in `--target_video`. Check this file to view the results of the fish counting process based on the specified class ID.

### Notes

- Ensure that the paths to the model weights and videos are correct.
- The coordinates for lines or polygons should be adjusted based on the requirements of your specific task.

Model trained on a multiclass dataset (listed below), 