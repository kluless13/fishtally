# Step 1 of using AI to replace marine scientists

FishTally is highly customisable tool that can automate fish counting, at a species level. This tool can be:
- used by marine ecologists to speed up and automate surveying to better study and understand population dynamics
- installed in ROVs and AUVs to conduct counting in real time
- used outside of marine ecology, to survey sea floors, map the seabed and create a reliable baseline database

CLI tool plan:
- have a custom .py file with the right args
- args: path to video/path to wts/path to detector type - single line/multi line/polygon
- if: single line/set threshold level after checking matplotlib coords - 2 points
- if: multi line/same procedure as before - multiple 2 points
- if: polygon/as as before - 4 point arrays

#TODO:
make classes an argument

Limitations:
- datasets for model training
- model weights 
- overfitting
- video capturing techniques
- source video quality

___File Structure
|
|__ft_demo_single_line
|
|__ft_single_line_invasive
|
|__ft_custom_multiple_lines
|
|__ft_custom_polygon 

Notebooks with significance:
- fishtally-demo-single-line -> using single line as a threshold to show pipeline works for single and multi class 
- fishtally-invasive -> single line threshold applied to an invasive species
- fishtally_demo_multio_lines ->
- fishtally_polyon ->

What I have done so far:
- ~compared yolov7 and yolov8 for an invasive species (Lionfish) and a marine pest (COTS)~
- ~created a fish counting algorithm that tracks a specific species, and then counts automatically, but with only one line~
- ~applied this process to the invasive lionfish species~
- ~add more lines as thresholds to track and count fish movement~
- make polygon and track within that
- address limitations

What I would like to add:
- turn FishTally into CLI command to automate process
- ~have weights ready for use~

### Methodology

- off the shelf base models, yolov7 and yolov8 were used to train on the invasive species datasets. yolov8 was the winner.
- fishtally - a demo - used with certain species of fish listed in the dataset info - multiclass model weights, so stronger than regular single class model
- how fishtally works - describe build on yolov8
- running fish tally with invasive species weights - dataset made with two different species from scratch - applying same procedure as fishtally - multiclass model

- Step 1: Model Comparison :white_check:
- Result 1: Yolov8 superior :white_check:
- Step 2: FishTally demo w multiclass model - 4 species :white_check:
- Result 2: FishTally works; Result 2A: freedom of class choice for counter; Result 2B: multiclass usage :white_check:
- Step 3: Customize FishTally to the max :white_check:
- Result 3: Have CLI tool ready for max use :white_check:

What the fuck did i do?
I built an AI fish counter that can be species specific, with customisable counting thresholds, to address the pain staking process of counting reef fish to study population dynamics. The counter works on top of a tracker, that is run using weights created by training a YOLOv8 model on a training set.
I start by choosing a SOTA YOLO model:
On comparing the YOLOv7 and the YOLOv8 model on an marine invasive species and a marine pest (Lionfish and COTS. respectively), I observed that YOLOv8 had a better overall performance. COTs are sessile in their adult form, and they blend/camo well with their surroundings, whereas the Lionfish may exist freely in the water coloumn or may be found amongst various surfaces. The YOLOv7 and v8 had no problem identifying the Lionfish, but the YOOv8 outperformed v7 in detecting COTs.
I now set up my multiple object tracker (MoT):
I use ByteTrack, a SOTA MoT. About ByteTrack: Multi-object tracking (MOT) aims at estimating bounding boxes and identities of objects in videos. Most methods obtain identities by associating detection boxes whose scores are higher than a threshold. The objects with low detection scores, e.g. occluded objects, are simply thrown away, which brings non-negligible true object missing and fragmented trajectories. To solve this problem, we present a simple, effective and generic association method, tracking by associating every detection box instead of only the high score ones. For the low score detection boxes, we utilize their similarities with tracklets to recover true objects and filter out the background detections. When applied to 9 different state-of-the-art trackers, our method achieves consistent improvement on IDF1 scores ranging from 1 to 10 points. To put forwards the state-of-the-art performance of MOT, we design a simple and strong tracker, named ByteTrack. For the first time, we achieve 80.3 MOTA, 77.3 IDF1 and 63.1 HOTA on the test set of MOT17 with 30 FPS running speed on a single V100 GPU.
Now, using Supervision, an OpenCV like library, I set up counting thresholds:
The first counting threshold line is a single line, to show proof of concept, and to demonstrtate that the tool works for classes within a trained model and that the counter can be class specific or multi-class. I even set an "in" and "out" counter, which may help with potential double counting, a common error in counting any organism. This demonstration was even run on footage of lionfish, with lionfish-specific weights.
But this may not be optimal in every case, so I set up a way to add more than one line to count. The code is easily customisable and can be tuned to fit any need. In several cases, the camera may be moving, for which the lines may be adjusted accordingly. For example, auxillary threshold lines at the left and right edges may be placed for a camera moving in a forward direction so that any fish tha enter from the left or the right may be counted; and in case a fish leaves, that may be accounted for as well.
The final customisation form that I have created is a free form polygon. Customisable 4 points plotted so that whatever enters the polygon will be counted. This may be especially useful for statically placed cameras.
The tool has all components needed to customise it in any way one can think of, with certain limitations:
- the weights will have to be pre-loaded/should already exist for the tool to work
- this tool has not been tested on edge devices, but as this is a light weight tool, it should not take up too much run time and can potentially work in real time.
- the CLI version of this tool is for the user to play around with the three modes: single line, multi line and polygon zone.
- the CLI tool is built upon the prototype and can be enhanced and optimised based on the task at hand. A scenario where a camera is being towed to check for lionfish may call for an implementation where there are two or three lines strategically placed within the frame. Here the idea would be to accurately capture the presence of the species, rather than double counting. In a case where population dynamics are being studied, fish count needs to be as accurate as possible and for such a case, anti-double counting measures can be intelligently implemented, such as the in and out feature and/or threshold lines at the left and right edges of a forward moving camera's frame. 


### Discussion

- model comparison results - best model for such a use case - yolov8 - a note on it's architecture
- The nature of counting fish, time and labour intensive - if only there was a solution for this
- FishTally's results on stock footage
- The invasive species issue - single model problem - use FishTally
