# YOLO-REACT: Application - Fish Tally

Objective: Use yolov8 to build a tracking model. Model weights can be used by the ByteTrack tracking algorithm.  The fish counter can be used to count fish (in this insatance) and keep a tally of the count. The machine can identify fish far better than the human eye at longer intervals of time. The AI tracker can tally fish from surveys to better understand their range and count with almost little to no human error. The application of this tool can be vast, ranging from helping marine survey teams using AUVs or other video collecting machines, to helping ecologists make informed decisions and better understand habitat structure. This is only an example of what can be done, this use case can be tailored for more specific needs depending on the context of the task.

<div align="center">
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/Tang-result.gif" width="49%"/>
    <img src="https://github.com/kluless13/paper2/blob/main/Assets/tang-tracker%20(2).gif" width="49%"/>
</div>

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
