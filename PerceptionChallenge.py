import cv2
import numpy as np

# load the image
input_img = cv2.imread("red.png")

# convert color space from BGR to HSV
hsv_img = cv2.cvtColor(input_img, cv2.COLOR_BGR2HSV)

# Image thresholding:

# set lower and upper bounds for red color in HSV image
lower_red = np.array([0, 135, 135])
upper_red = np.array([15, 255, 255])
thresh_low = cv2.inRange(hsv_img, lower_red, upper_red) # binary image of the red regions

# set lower and upper bounds for orange color in HSV image
lower_orange = np.array([160, 135, 135])
upper_orange = np.array([180, 255, 255])
thresh_high = cv2.inRange(hsv_img, lower_orange, upper_orange) # binary image of the orange regions

binary_img = cv2.bitwise_or(thresh_low, thresh_high) # combined binary image of thresh_low and thresh_high

# Morphological operations to reduce noise:
kernel = np.ones((5,5), np.uint8)
opened_img = cv2.morphologyEx(binary_img, cv2.MORPH_OPEN, kernel)

# More noise reduction:
blurred_img = cv2.medianBlur(opened_img, 5)

# Canny edge detection:
edges_img = cv2.Canny(blurred_img, 80, 160) # image of just edges of the objects

# Contours in edges_img:
contours, _ = cv2.findContours(edges_img, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Empty lists for contours and convex hulls:
approx_contours = []
convex_hulls = []

# Approximate contours:
for contour in contours:
    approx = cv2.approxPolyDP(contour, 10, closed=True)
    approx_contours.append(approx)

# Compute convex hulls of cones:
for approx_contour in approx_contours:
    convex_hulls.append(cv2.convexHull(approx_contour))

# Filter convex hulls by size:
convex_hulls_filtered = []
for convex_hull in convex_hulls:
    if 3 <= len(convex_hull) <= 10:
        convex_hulls_filtered.append(convex_hull)

# Empty lists for cones and bounding rectangles:
cones_detected = []
bounding_rectangles = []

# Iterate through convex hulls:
for ch in convex_hulls_filtered:
    area = cv2.contourArea(ch)
    if 50 < area < 3250:
        cones_detected.append(ch)
        rect = cv2.boundingRect(ch)
        bounding_rectangles.append(rect)

# Calculate middle x-coordinates of all detected cones:
mid_x = sum([rect[0] + rect[2]//2 for rect in bounding_rectangles]) // len(bounding_rectangles)

# Define cone as left or right based on their x-coordinate:
left_cones = [rect for rect in bounding_rectangles if rect[0] + rect[2] // 2 < mid_x]
right_cones = [rect for rect in bounding_rectangles if rect[0] + rect[2] // 2 >= mid_x]

# Closest and farthest cones on each side:
closest_left = min(left_cones, key=lambda rect: abs(rect[0] + rect[2] // 2 - mid_x))
closest_right = min(right_cones, key=lambda rect: abs(rect[0] + rect[2] // 2 - mid_x))

farthest_left = max(left_cones, key=lambda rect: abs(rect[0] + rect[2] // 2 - mid_x))
farthest_right = max(right_cones, key=lambda rect: abs(rect[0] + rect[2] // 2 - mid_x))

answer_img = input_img.copy()
height, width, _ = answer_img.shape

# Slope for left side:
left_slope = ((farthest_left[1] + farthest_left[3] // 2 - closest_left[1] - closest_left[3] // 2) /
              (farthest_left[0] + farthest_left[2] // 2 - closest_left[0] - closest_left[2] // 2))

# y-coordinates of borders:
y_top_left = int(-closest_left[0] * left_slope + closest_left[1] + closest_left[3] // 2)
y_bottom_left = int((width - closest_left[0]) * left_slope + closest_left[1] + closest_left[3] // 2)

# Draw line on left side:
cv2.line(answer_img, (0, y_top_left), (width, y_bottom_left), (0,0,255),3)

# Slope for right side:
right_slope = ((farthest_right[1] + farthest_right[3] // 2 - closest_right[1] - closest_right[3] // 2) /
               (farthest_right[0] + farthest_right[2] // 2 - closest_right[0] - closest_right[2] // 2))

# y-coordinates of borders:
y_top_right = int(-closest_right[0] * right_slope + closest_right[1] + closest_right[3] // 2)
y_bottom_right = int((width - closest_right[0]) * right_slope + closest_right[1] + closest_right[3] // 2)

# Draw line on right side:
cv2.line(answer_img, (0,y_top_right), (width, y_bottom_right), (0,0,255), 3)

cv2.imwrite("answer.png", answer_img)

cv2.imshow("Answer", answer_img)
cv2.waitKey(0)
cv2.destroyAllWindows()


