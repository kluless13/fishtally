# Step 1 of using AI to replace marine scientists

___File Structure
|
|__Multiclass_wts.pt [for Step 2]
|
|__lionfish_wt.pt [for step 3]
|
|__cots_wt.pt [for step 3]

### Methodology

- off the shelf base models, yolov7 and yolov8 were used to train on the invasive species datasets. yolov8 was the winner.
- fishtally - a demo - used with certain species of fish listed in the dataset info - multiclass model weights, so stronger than regular single class model
- how fishtally works - describe build on yolov8
- running fish tally with invasive species weights - dataset made with two different species from scratch - applying same procedure as fishtally - multiclass model

- Step 1: Model Comparison :white_check:
- Result 1: Yolov8 superior :white_check:
- Step 2: FishTally demo w multiclass model - 4 species
- Result 2: FishTally works; Result 2A: freedom of class choice for counter; Result 2B: multiclass usage
- Step 3: Create weights for invasive species - lionfish & COTs 
- Result 3: AI counter for invasive species

### Discussion

- model comparison results - best model for such a use case - yolov8 - a note on it's architecture
- The nature of counting fish, time and labour intensive - if only there was a solution for this
- FishTally's results on stock footage
- The invasive species issue - single model problem - use FishTally
