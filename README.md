# Parser and Plotter for SEG files from CONTEC

## Overview

Parses and visualizes data from a .seg file that contains Plethysmography, Pulse Rate, SpO2, Abdomen and Thorax expansion.
Tested with files from Contec RS10. Comes with a small example dataset.

The recording files are structured into 1-second segments, each containing multiple blocks of data. Each segment starts with a header and is followed by specific blocks of data.

### Segment Structure

Each segment has the following structure:

1. **Segment Header**

   - **Size**: 4 bytes
   - **Content**: `FF FF` (2 bytes) + Block Number (2 bytes)
2. **Data Segments**

   - **Abdomen Segment**
     - **Size**: 200 bytes
     - **Data Type**: `uint16` (100 values)
   - **Thorax Segment**
     - **Size**: 200 bytes
     - **Data Type**: `uint16` (100 values)
   - **Flow Segment**
     - **Size**: 200 bytes
     - **Data Type**: `uint16` (100 values)
   - **spO2 Segment**
     - **Size**: 25 bytes
     - **Data Type**: `uint8` (25 values)
   - **PR Segment**
     - **Size**: 25 bytes
     - **Data Type**: `uint8` (25 values)
   - **Pleth Segment**
     - **Size**: 60 bytes
     - **Data Type**: `uint8` (60 values)
   - **Unknown Segment**
     - **Size**: 3 bytes - Please contribute if you uncover their use.

## Requirements

- Python 3.x
- NumPy
- Matplotlib

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/StepUp-Solutions/ContecSEGParser.git
   ```
2. Install the required packages:
   ```bash
   pip install numpy matplotlib
   ```

## Usage

1. Edit the FILE_NAME variable in the beginning of the file.
2. Run the script:
   ```bash
   python segparser.py
   ```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

For more details, refer to the source code and comments within the script.
