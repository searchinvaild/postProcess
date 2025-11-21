# postProcess Script Collection

This repository contains a set of Python scripts based on ParaView, designed for visualization and data extraction tasks for OpenFOAM models. Each script addresses specific post-processing needs, such as generating contours, exporting velocity along a line, creating slice sequence GIFs, or calculating cross-sectional volume fractions. The table below provides a script overview:

| Script | Main Function |
| --- | --- |
| `ContourCreater.py` | Extracts contours at specified time steps and exports XY coordinates. |
| `ExtractVelocityAlongLine.py` | Extracts velocity (or other field quantities) along a given line at a specified time and outputs to CSV. |
| `GifCreater.py` | Generates time-series screenshots for each data source and synthesizes them into a GIF. |
| `SliceGifCreater.py` | Creates fixed-plane slices for all data sources, saving PNGs for each time step. |
| `TotalValueCaculaterBehindSlice_all.py` | Calculates the total volume fraction on both sides of a slice over time and exports the results. |
| `meanValueCaculaterInSlice_all.py` | Calculates the time-series average of field quantities on a specified cross-section and saves to CSV. |

## Usage Instructions

All scripts are assumed to run within the ParaView Python environment (`paraview.simple` available) with OpenFOAM data loaded. Some scripts contain hard-coded output paths and field names; please adjust these according to your actual paths and fields before use.

### ContourCreater.py
- **Purpose**: Generates contours (isosurface value 0.5) for `alpha.sludge` at the target time step (default 39s) and exports the contour line XY coordinates to a CSV file on the desktop.
- **Key Points**:
  - Uses the currently active data source and list of time steps; throws an error if the time step is missing.
  - Automatically processes MultiBlock datasets, writing the point coordinates from all blocks to the CSV.

### ExtractVelocityAlongLine.py
- **Purpose**: Iterates through all data sources in the current session, exports a specified field (default `U_X`) along a given line at a specified time point to CSV.
- **Key Points**:
  - Selects the closest available time step and verifies the existence of the specified time point.
  - Uses `PlotOverLine` and `Calculator` filters to extract point data along the line and writes the results to CSV files in `G:\data`.
  - The default line is from `[0, 1.9, 1.5]` to `[20, 1.9, 1.5]` and can be modified.

### GifCreater.py
- **Purpose**: Takes screenshots for each data source according to a specified time window and composites them into a GIF.
- **Key Points**:
  - Configure the output directory, viewport size, time window, GIF playback parameters, color field, etc., in `CUSTOM_PARAMS`.
  - When generating each GIF, it hides other data sources, resets the camera, applies the color scale, and optionally removes the white background.
  - PNG files are retained in the output directory for potential reuse.

### SliceGifCreater.py
- **Purpose**: Creates fixed-plane slices (default normal `[1,0,0]`, origin `[5.5, 10, 10]`) for all data sources, iterates through time steps, and saves PNGs.
- **Key Points**:
  - The view/legend should be adjusted beforehand; the script hides the original sources and keeps the slices visible.
  - The color mapping defaults to using `p_rgh` point data but can be changed as needed.
  - The output directory is created under `G:\data` based on the data source folder name.

### TotalValueCaculaterBehindSlice_all.py
- **Purpose**: Batch reads `.foam` cases from a specified directory, calculates the total sum of `alpha.water` on both sides of a slice (`y<5.5` and `y>=5.5`) over time, and exports to CSV.
- **Key Points**:
  - Requires setting `foam_dir` (path to .foam files) and `output_dir`.
  - For each time step, it obtains the slice data, iterates through the MultiBlock data, and sums the `alpha.water` values at the points.
  - The CSV columns are `Time, Left Volume Fraction Sum, Right Volume Fraction Sum`.

### meanValueCaculaterInSlice_all.py
- **Purpose**: For each data source, calculates the average value of `alpha.sludge` on a specified cross-section (default `x=5.5`) over time and saves to CSV.
- **Key Points**:
  - Iterates through time steps, creates a slice, uses `IntegrateVariables` to compute cell data, and then calculates the average.
  - The default output path is `G:\data2`, and the filename includes the case name.
  - Prints the average value series for each case upon completion for quick verification.

## Quick Start
1.  Before running a script in the ParaView Python Shell or with `pvpython`, ensure your target OpenFOAM data is loaded, or change the path parameters in the script to your file locations.
2.  Update the hard-coded paths (e.g., `G:\data`, `G:\case`), field names (e.g., `alpha.water`, `alpha.sludge`, `U_X`), and parameters like slice definitions or time windows within the scripts according to your environment.
3.  Run the required scripts individually to complete the corresponding post-processing tasks.

## Notes
- The scripts default to using Windows path separators; please adjust accordingly for other platforms.
- Some scripts rely on third-party libraries like Pillow and imageio; ensure they are available in your ParaView Python environment.
- It is recommended to save your ParaView session before running scripts for quick recovery of view and data source configuration in case of exceptions.
