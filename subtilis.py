import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

# Detection parameters
cell_size = 50
brightness_ajustment = 90  # Adjust this to find the right cell detection
cell_abundance = [32,16,8,4,2,1]
min_area_values = [cell_size * x for x in cell_abundance]  # Different area thresholds for cell abundance

# Command line argument parsing
parser = argparse.ArgumentParser(description='Process an image to detect cells and connections. Add image and Magnification')
parser.add_argument('image_path', type=str, help='Path to the image file')
parser.add_argument('magnification', type=int, help='Image magnification')
args = parser.parse_args()

# Load the image
image_path = args.image_path
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)  # Read directly as grayscale

# Check if the image was loaded properly
if image is None:
    print(f"Error: Image at path {image_path} could not be loaded.")
    exit()

# Crop the lowest 100 pixels of the image to get rid of data bar
height, width = image.shape
cropped_image = image[:height - 150, :]  # Crop the bottom 100 pixels

# Apply a binary threshold to isolate the cells
_, binary_image = cv2.threshold(cropped_image, brightness_ajustment, 255, cv2.THRESH_BINARY_INV)

# Find contours (cell boundaries) in the binary image
contours, _ = cv2.findContours(binary_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Convert image size from pixels to square millimeters
# Get imagage magnification and transform into horizontal field view:
hfw = 127000 / args.magnification 
pixel_to_micrometer = hfw / width
pixel_area_to_micrometer_squared = (pixel_to_micrometer) ** 2
image_area_in_micrometers_squared = height * width * pixel_area_to_micrometer_squared
image_area_in_mm_squared = image_area_in_micrometers_squared / 10**6  # Convert micrometer² to mm²

# Initialize list to store cell counts for different min_area values
cell_counts_per_mm2 = []

# Prepare for plotting
fig, ax = plt.subplots(1, 2, figsize=(15, 7))

# Draw contours on a color version of the cropped image
image_with_contours = cv2.cvtColor(cropped_image, cv2.COLOR_GRAY2BGR)

# Process the image for each min_area value
for i, min_area in enumerate(min_area_values):
    # Filter contours by area
    filtered_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
    
    # Count the number of cells for the current min_area
    cell_count = len(filtered_contours)
    # Convert the raw cell count to cells per mm²
    cells_per_mm2 = cell_count / image_area_in_mm_squared
    if i > 0:
        for j in range(i - i, i):
            cells_per_mm2 -= cell_counts_per_mm2[j]
    cell_counts_per_mm2.append(cells_per_mm2)
    
    # Draw the contours on the image
    cv2.drawContours(image_with_contours, filtered_contours, -1, (0, 255, 0), 2)
            
# Show the image with contours
ax[0].imshow(cv2.cvtColor(image_with_contours, cv2.COLOR_BGR2RGB))
ax[0].set_title(f'Cell image')

# Plot the histogram of cell counts for different min_area thresholds
cell_abundance.reverse()
cell_counts_per_mm2.reverse()
bars = ax[1].bar([str(ma) for ma in cell_abundance], cell_counts_per_mm2, color='black')

ax[1].set_title('cell Abundance Distribution')
ax[1].set_xlabel('Abundance')
ax[1].set_ylabel('Cell number per mm²')

# Add numbers on top of the bars
for bar, count in zip(bars, cell_counts_per_mm2):
    ax[1].text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(int(count)), 
               ha='center', va='bottom', fontsize=12)

# Show the plots
plt.tight_layout()
plt.show()