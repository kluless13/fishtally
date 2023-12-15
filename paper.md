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
- fishtally-invasive -> single line threshold applied to fishtally

What I have done so far:
- compared yolov7 and yolov8 for an invasive species (Lionfish) and a marine pest (COTS)
- created a fish counting algorithm that tracks a specific species, and then counts automatically, but with only one line
- applied this process to the invasive lionfish species
- add more lines as thresholds to track and count fish movement
- make polygon and track within that
- address limitations

What I would like to add:
- turn FishTally into CLI command to automate process
- have weights ready for use

### Methodology

- off the shelf base models, yolov7 and yolov8 were used to train on the invasive species datasets. yolov8 was the winner.
- fishtally - a demo - used with certain species of fish listed in the dataset info - multiclass model weights, so stronger than regular single class model
- how fishtally works - describe build on yolov8
- running fish tally with invasive species weights - dataset made with two different species from scratch - applying same procedure as fishtally - multiclass model

- Step 1: Model Comparison :white_check:
- Result 1: Yolov8 superior :white_check:
- Step 2: FishTally demo w multiclass model - 4 species
- Result 2: FishTally works; Result 2A: freedom of class choice for counter; Result 2B: multiclass usage
- Step 3: Customize FishTally to the max: 
- Step 4: Create weights for invasive species - lionfish & COTs 
- Result 4: AI counter for invasive species

### Discussion

- model comparison results - best model for such a use case - yolov8 - a note on it's architecture
- The nature of counting fish, time and labour intensive - if only there was a solution for this
- FishTally's results on stock footage
- The invasive species issue - single model problem - use FishTally
