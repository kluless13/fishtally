# YOLO-REACT: Application - Fish Tally

Objective: Use yolov8 to build a tracking model. Model weights can be used by the ByteTrack tracking algorithm.  The fish counter can be used to count fish (in this insatance) and keep a tally of the count. The machine can identify fish far better than the human eye at longer intervals of time. The AI tracker can tally fish from surveys to better understand their range and count with almost little to no human error. The application of this tool can be vast, ranging from helping marine survey teams using AUVs or other video collecting machines, to helping ecologists make informed decisions and better understand habitat structure. This is only an example of what can be done, this use case can be tailored for more specific needs depending on the context of the task.

<div align="center">
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/Tang-result.gif" width="49%"/>
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/tang-tracker%20(2).gif" width="49%"/>
</div>

Certainly! Below is a setup guide suitable for inclusion in a `README.md` file for your fish tallying tool, `fishtally.py`. This guide covers the necessary steps to get the tool up and running.

---

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
   ```

3. **Install Python Dependencies**

   Install the required Python packages using the `requirements.txt` file.

   ```bash
   pip install -r requirements.txt
   ```

   This command installs all necessary Python packages for `fishtally.py`.

4. **Verification**

   To verify that the installation is successful, you can run a simple test command or check the versions of critical components like Python, Git, and Pip.

   ```bash
   python --version
   git --version
   pip --version
   ```

Certainly! Here's a guide for running `fishtally.py`, which can be included in your `README.md` file or other documentation. This guide will provide instructions on how to use the command-line interface (CLI) of the tool.

---

## Running `fishtally.py`

### Usage Instructions

The `fishtally.py` tool is a command-line application that can be used for fish counting in videos using different detection methods (single line, multiple lines, and polygon). 

To use the tool, follow these steps:

1. **Open the Terminal**

   Open a terminal window and navigate to the directory where `fishtally.py` is located.

2. **Running the Tool**

   Use the following command structure to run the tool:

   ```bash
   python fishtally.py --model_weights <path_to_weights> --source_video <path_to_source_video> --target_video <path_to_output_video> --detector_type <detector_type> [additional_arguments]
   ```

   Replace `<path_to_weights>`, `<path_to_source_video>`, and `<path_to_output_video>` with the respective paths. For `<detector_type>`, choose from `single_line`, `multi_line`, or `polygon`.

   - For `single_line` and `multi_line`, you need to specify line coordinates. 
   - For `polygon`, provide the polygon points.

3. **Example Commands**

   Here are some example commands for each detector type:

   - **Single Line:**
     ```bash
     python fishtally.py --model_weights weights.pt --source_video source.mp4 --target_video output.mp4 --detector_type single_line --line_start 100 200 --line_end 300 400
     ```

   - **Multiple Lines:**
     ```bash
     python fishtally.py --model_weights weights.pt --source_video source.mp4 --target_video output.mp4 --detector_type multi_line --line_start 100 200 --line_end 300 400 --line_start2 500 600 --line_end2 700 800
     ```

   - **Polygon:**
     ```bash
     python fishtally.py --model_weights weights.pt --source_video source.mp4 --target_video output.mp4 --detector_type polygon --polygon_points 100 200 300 400 500 600 700 800
     ```

    Replace the coordinates in these examples with those relevant to your specific use case.

4. **Viewing the Results**

   After running the command, the tool will process the video and output the results to the path specified in `--target_video`. Check this file to view the results of the fish counting process.

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
  - Three-Striped-Damselfish, Dascyllus aruanus :white_check_mark:
  - Yellow-Tang, Zebrasoma flavescens :white_check_mark: :white_check_mark:

Videos in Asset folder.
