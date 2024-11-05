
#%%

import matplotlib.pyplot as plt
import os

#%%

# Constants for block and segment sizes
BLOCK_START_MARKER = b'\xff\xff\x01\x00'
BLOCK_HEADER_SIZE = 4
ABDOMEN_SEGMENT_SIZE = 200
THORAX_SEGMENT_SIZE = 200
FLOW_SEGMENT_SIZE = 200
SPO2_SEGMENT_SIZE = 25
PR_SEGMENT_SIZE = 25
PLETH_SEGMENT_SIZE = 60
UKN_SEGMENT_SIZE = 3
#%%
def parse_recording_file(file_path):
    """
    Parse the recording file and extract the data blocks.

    Parameters
    ----------
    file_path : str
        Path to the recording file.

    Returns
    -------
    dict
        A dictionary containing the parsed data arrays.
    """
    with open(file_path, 'rb') as file:
        data = file.read()

    # Initialize lists to store the parsed data
    abdomen_data = []
    thorax_data = []
    flow_data = []
    spo2_data = []
    pr_data = []
    pleth_data = []

    # Find the start of the first block
    start_index = data.find(BLOCK_START_MARKER)
    if start_index == -1:
        raise ValueError("First block start marker not found.")

    # Iterate through the data blocks
    while start_index < len(data):
        # Print the block in hex format
        # block_data = data[start_index:start_index + BLOCK_HEADER_SIZE + ABDOMEN_SEGMENT_SIZE + THORAX_SEGMENT_SIZE + FLOW_SEGMENT_SIZE + SPO2_SEGMENT_SIZE + PR_SEGMENT_SIZE + PLETH_SEGMENT_SIZE]
        # hex_block = ' '.join(f'{byte:02x}' for byte in block_data)
        # print(f"Block at index {start_index}:\n{hex_block}\n")

        # Check if the block starts with FF FF
        if data[start_index:start_index + 2] != b'\xff\xff':
            raise ValueError(f"Block at index {start_index} does not start with FF FF.")

        # Move to the start of the next block
        start_index += BLOCK_HEADER_SIZE  # Skip the block number

        # Check if we have reached the end of the data
        if start_index + ABDOMEN_SEGMENT_SIZE + THORAX_SEGMENT_SIZE + FLOW_SEGMENT_SIZE + SPO2_SEGMENT_SIZE + PR_SEGMENT_SIZE + PLETH_SEGMENT_SIZE > len(data):
            break

        # Extract and convert the data segments
        abdomen = np.frombuffer(data[start_index:start_index + ABDOMEN_SEGMENT_SIZE], dtype=np.uint16)
        abdomen_data.extend(abdomen)
        start_index += ABDOMEN_SEGMENT_SIZE

        thorax = np.frombuffer(data[start_index:start_index + THORAX_SEGMENT_SIZE], dtype=np.uint16)
        thorax_data.extend(thorax)
        start_index += THORAX_SEGMENT_SIZE

        flow = np.frombuffer(data[start_index:start_index + FLOW_SEGMENT_SIZE], dtype=np.uint16)
        flow_data.extend(flow)
        start_index += FLOW_SEGMENT_SIZE

        spo2 = np.frombuffer(data[start_index:start_index + SPO2_SEGMENT_SIZE], dtype=np.uint8)
        spo2_data.extend(spo2)
        start_index += SPO2_SEGMENT_SIZE

        pr = np.frombuffer(data[start_index:start_index + PR_SEGMENT_SIZE], dtype=np.uint8)
        pr_data.extend(pr)
        start_index += PR_SEGMENT_SIZE

        pleth = np.frombuffer(data[start_index:start_index + PLETH_SEGMENT_SIZE], dtype=np.uint8)
        pleth_data.extend(pleth)
        start_index += PLETH_SEGMENT_SIZE

        start_index += UKN_SEGMENT_SIZE

    # Return the parsed data as a dictionary
    return {
        'abdomen': abdomen_data,
        'thorax': thorax_data,
        'flow': flow_data,
        'spo2': spo2_data,
        'pr': pr_data,
        'pleth': pleth_data
    }

import numpy as np  # Import numpy for array operations

def plot_data(data):
    """
    Plot the parsed data in a matplotlib plot with 6 subplots.

    Parameters
    ----------
    data : dict
        A dictionary containing the parsed data arrays.
    """
    fig, axes = plt.subplots(6, 1, sharex=True, figsize=(10, 15))
    fig.suptitle('Recording Data Plot')

    # Calculate the time scale based on the segment sizes
    time_scale = np.arange(0, len(data['abdomen']) / (ABDOMEN_SEGMENT_SIZE // 2), 1/(ABDOMEN_SEGMENT_SIZE // 2))

    # Plot Abdomen data
    axes[0].plot(time_scale, data['abdomen'], label='Abdomen')
    axes[0].set_title('Abdomen Data')
    axes[0].set_ylabel('Amplitude')
    axes[0].legend()

    # Plot Thorax data
    axes[1].plot(time_scale, data['thorax'], label='Thorax')
    axes[1].set_title('Thorax Data')
    axes[1].set_ylabel('Amplitude')
    axes[1].legend()

    # Plot Flow data
    axes[2].plot(time_scale, data['flow'], label='Flow')
    axes[2].set_title('Flow Data')
    axes[2].set_ylabel('Amplitude')
    axes[2].legend()

    time_scale_spo2 = np.arange(0, len(data['spo2']) / (SPO2_SEGMENT_SIZE), 1/(SPO2_SEGMENT_SIZE))

    # Plot spO2 data
    axes[3].plot(time_scale_spo2, data['spo2'], label='spO2')
    axes[3].set_title('spO2 Data')
    axes[3].set_ylabel('Amplitude')
    axes[3].legend()

    # Plot PR data
    axes[4].plot(time_scale_spo2, data['pr'], label='PR')
    axes[4].set_title('PR Data')
    axes[4].set_ylabel('Amplitude')
    axes[4].legend()

    time_scale_pleth = np.arange(0, len(data['pleth']) / (PLETH_SEGMENT_SIZE), 1/(PLETH_SEGMENT_SIZE))

    # Plot Pleth data
    axes[5].plot(time_scale_pleth, data['pleth'], label='Pleth')
    axes[5].set_title('Pleth Data')
    axes[5].set_xlabel('Time (s)')
    axes[5].set_ylabel('Amplitude')
    axes[5].legend()

    # Adjust layout and show the plot
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()
#%%


if __name__ == "__main__":
    # Parse the recording file
    #%%
    data = parse_recording_file('001.seg')
#%%
    # Plot the parsed data
    plot_data(data)
# %%
# %%
