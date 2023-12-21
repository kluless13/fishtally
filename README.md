# YOLO-REACT: Application - Fish Tally

Objective: Use yolov8 to build a tracking model. Model weights can be used by the ByteTrack tracking algorithm.  The fish counter can be used to count fish (in this insatance) and keep a tally of the count. The machine can identify fish far better than the human eye at longer intervals of time. The AI tracker can tally fish from surveys to better understand their range and count with almost little to no human error. The application of this tool can be vast, ranging from helping marine survey teams using AUVs or other video collecting machines, to helping ecologists make informed decisions and better understand habitat structure. This is only an example of what can be done, this use case can be tailored for more specific needs depending on the context of the task.

<div align="center">
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/Tang-result.gif" width="49%"/>
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/tang-tracker%20(2).gif" width="49%"/>
</div>

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

2. **Install ByteTrack**

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

Before using the fish tallying tool, you can list the available classes in your YOLO model. This will help you identify the correct class ID for detection.

1. **List Classes**

   Run `list_classes.py` with the path to your model weights:

   ```bash
   python list_classes.py --model_weights <path_to_weights>
   ```

   Replace `<path_to_weights>` with the path to your YOLO model weights file. This will print out the class names and their corresponding indices.

### Running the Fish Tallying Tool

After identifying the correct class ID, you can proceed to use `fishtally.py`.

1. **Open the Terminal**

   Open a terminal window and navigate to the directory where `fishtally.py` is located.

2. **Running the Tool**

   Use the following command structure to run the tool:

   ```bash
   python fishtally.py --model_weights <path_to_weights> --source_video <path_to_source_video> --target_video <path_to_output_video> --detector_type <detector_type> --class_id <class_id> [additional_arguments]
   ```

   Replace `<path_to_weights>`, `<path_to_source_video>`, and `<path_to_output_video>` with the respective paths. For `<detector_type>`, choose from `single_line`, `multi_line`, or `polygon`. Replace `<class_id>` with the ID of the class you want to detect.

   - For `single_line` and `multi_line`, specify the line coordinates.
   - For `polygon`, provide the polygon points.

3. **Example Commands**

   - **Single Line:**
     ```bash
     python fishtally.py --model_weights weights.pt --source_video source.mp4 --target_video output.mp4 --detector_type single_line --line_start 100 200 --line_end 300 400 --class_id 3
     ```

   - **Multiple Lines:**
     ```bash
     python fishtally.py --model_weights weights.pt --source_video source.mp4 --target_video output.mp4 --detector_type multi_line --line_start 100 200 --line_end 300 400 --line_start2 500 600 --line_end2 700 800 --class_id 3
     ```

   - **Polygon:**
     ```bash
     python fishtally.py --model_weights weights.pt --source_video source.mp4 --target_video output.mp4 --detector_type polygon --polygon_points 100 200 300 400 500 600 700 800 --class_id 3
     ```

    Replace the coordinates and the class ID in these examples with those relevant to your specific use case.

4. **Viewing the Results**

   After running the command, the tool will process the video and output the results to the path specified in `--target_video`. Check this file to view the results of the fish counting process based on the specified class ID.

### Notes

- Ensure that the paths to the model weights and videos are correct.
- The coordinates for lines or polygons should be adjusted based on the requirements of your specific task.

Model trained on a multiclass dataset (listed below), 

#### Dataset info:
- @misc{ mergetest-tl3d3_dataset,
    title = { MergeTest Dataset },
    type = { Open Source Dataset },
    author = { Test },
    howpublished = { \url{ https://universe.roboflow.com/test-fnuaq/mergetest-tl3d3 } },
    url = { https://universe.roboflow.com/test-fnuaq/mergetest-tl3d3 },
    journal = { Roboflow Universe },
    publisher = { Roboflow },
    year = { 2023 },
    month = { feb },
    note = { visited on 2023-11-19 },
}

- Classes: (1 check-mark: model tested on video specific to species; 2 check-marks: tracker built)
  - Blue-Tang, Paracanthurus hepatus
  - Orange-Clown, Amphiprion percula :white_check_mark:
  - Three-Striped-Damselfish, Dascyllus aruanus :white_check_mark :white_check_mark:
  - Yellow-Tang, Zebrasoma flavescens :white_check_mark: :white_check_mark:

Videos in Asset folder.
