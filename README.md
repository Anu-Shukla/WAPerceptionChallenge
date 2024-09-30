**Perception Challenge**

**Files**
answer.png: Output image of the program which has the lines drawn through the cones 

PerceptionChallenge.py: Python program used for this cone detection challenge

**Methodology**

Color Space Conversion: The input image is converted from BGR to HSV color space.

Thresholding: The HSV image is thresholded to isolate red and orange regions using specified color bounds.

Morphological Operations: Morphological operations are applied to the binary image to reduce noise and improve the quality of the detection.

Edge Detection: Canny edge detection is utilized to highlight the edges of detected objects in the image.

Contour Detection: Contours are extracted from the edge-detected image to identify the shapes of the objects.

Approximation and Convex Hulls: Contours are approximated, and convex hulls are computed to capture the outer shape of the detected objects.

Filtering by Size: Convex hulls that do not meet size criteria are filtered out to focus on relevant detections.

Calculating Midpoint: The midpoint of all detected cones is calculated to differentiate between left and right cones.

Separating Cones: Cones are categorized into left and right based on their x-coordinates.

Finding Closest and Farthest Cones: The closest and farthest cones on each side are identified.

Drawing Lines: Lines are drawn through the identified cones to indicate the detected borders.

Output: The resulting image with drawn lines is saved as answer.png.

**What was tried**

Various color spaces and thresholding ranges were used to try to isolate desired regions.
Also tried different morphological operations for better results.

**Libraries Used**

OpenCV: Used for image processing tasks: color space conversion, thresholding, edge detection, and contour finding.

NumPy: Used for numerical operations and arrays.