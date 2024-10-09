# Counting B. Subtilis

#### Description:
This program reads in an SEM image or any other microscopic image of B. Subtilis and counts the cells and thier connectivity or abundance based on outlines. The program outputs the cell abundance distribution of a given image. Furthermore, detected cells are highlighted to ensure a valid result..

**Table of contents:**

1. [Usage](#Usage)
2. [Parameters](#requirements)
3. [Limitations](#limitations)

### Usage

In order to use the program type the following command into your terminal:

`python subtilis.py image_path magnification`

The image_path is the path to your image to analyse and the magnification is a given integer of the magnification used for the image.

### Parameters

Ther are several parameters within the code in order to adjust for the input image

| Parameter | Explaination 
| :------| :----------------------
| `cell_size` | Accouts for a minimum cell size. In order to reduce noice this number should not be below 50 to prevent false detections.
| `brightness_ajustment`| Various image brightness can has an impact on the count. To take this into account the brightness might need adjustments via this parameter.
| `cell_abundance` | This array adjusts the output histogram for any supected cell connectivity.


### Limitations

1. **Tested Organisms**:  
   This program has been specifically tested and optimized for *Bacillus subtilis*. While it may work with other bacterial species or pathogens, the accuracy and validity of the results cannot be guaranteed for organisms beyond *B. subtilis* without further testing.

2. **Biofilm Analysis**:  
   When applied to grown biofilms, the algorithm may **underestimate cell numbers** due to the following factors:
   - Some bacteria may be covered by others, making them difficult to detect.
   - Cells that are adjacent to each other may be mistakenly counted as a single connected structure, rather than as individual cells.

3. **Error Margin**:  
   Users should account for a potential error margin of **±25%** in the reported cell counts due to the aforementioned limitations in detecting individual cells in complex biofilm structures.

It is recommended to validate the results with independent methods for critical applications.
