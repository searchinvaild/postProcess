import sys
sys.path.append('c:\\python312\\lib\\site-packages')
import os
import glob
import csv
import numpy as np
from paraview.simple import *
## 获得某截面左侧和右侧的浆液总体积随时间的变化规律
# Directory to save CSV files
output_dir = "G:/data"

# Ensure output directory exists
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Set the directory containing .foam files
foam_dir = "G:/case/ABBB"  # 替换为实际的 .foam 文件所在目录

# Get all case files in the specified directory (assuming .foam files)
case_files = glob.glob(os.path.join(foam_dir, "*.foam"))

# Debug output: print found case files
print(f"Found case files: {case_files}")

# Check if case_files is empty
if not case_files:
    print("No .foam files found. Please check the directory path and file extensions.")
else:
    for case_file in case_files:
        # Extract case name from file path
        case_name = os.path.basename(case_file).replace('.foam', '')

        # Load the case
        reader = OpenFOAMReader(FileName=case_file)
        reader.MeshRegions = ['internalMesh']
        reader.CellArrays = ['alpha.water']  # Assuming alpha.water is the scalar field of slurry volume fraction

        # Update pipeline to read data
        UpdatePipeline()

        # Create a slice at x=5.5
        slice = Slice(Input=reader)
        slice.SliceType = 'Plane'
        slice.SliceOffsetValues = [0.0]
        slice.SliceType.Origin = [5.5, 0.0, 0.0]
        slice.SliceType.Normal = [1.0, 0.0, 0.0]

        # Prepare data for CSV
        csv_data = [['Time', 'Left Volume Fraction Sum', 'Right Volume Fraction Sum']]

        # Get time steps
        time_steps = reader.TimestepValues
        for time in time_steps:
            # Update pipeline to the current time step
            reader.UpdatePipeline(time)
            
            # Update pipeline to apply slice
            slice.UpdatePipeline(time)

            # Get data from the slice
            slice_data = servermanager.Fetch(slice)

            # Initialize lists for points and alpha.water values
            points = []
            alpha_water = []

            # Traverse all blocks in the MultiBlockDataSet
            for i in range(slice_data.GetNumberOfBlocks()):
                block = slice_data.GetBlock(i)
                if block is not None:
                    num_points = block.GetNumberOfPoints()
                    points.extend([block.GetPoint(i) for i in range(num_points)])
                    alpha_array = block.GetPointData().GetArray('alpha.water')
                    if alpha_array is not None:
                        alpha_water.extend([alpha_array.GetValue(i) for i in range(num_points)])
                    else:
                        alpha_water.extend([0.0] * num_points)  # 或者处理没有数据的情况

            # Convert lists to numpy arrays
            points = np.array(points)
            alpha_water = np.array(alpha_water)

            # Separate points into left and right based on y-coordinate
            left_mask = points[:, 1] < 5.5
            right_mask = points[:, 1] >= 5.5

            left_alpha_water = alpha_water[left_mask]
            right_alpha_water = alpha_water[right_mask]

            # Compute the volume fraction sums
            left_volume_fraction_sum = np.sum(left_alpha_water)
            right_volume_fraction_sum = np.sum(right_alpha_water)

            csv_data.append([time, left_volume_fraction_sum, right_volume_fraction_sum])

        # Write data to CSV
        csv_file_path = os.path.join(output_dir, f"{case_name}_right_slice_left.csv")
        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(csv_data)

        print(f"Data for {case_name} exported to {csv_file_path}")
