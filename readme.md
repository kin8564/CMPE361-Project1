# Trojan Detection through Bitstream Analysis

This project focuses on detecting hardware Trojans in FPGA devices by analyzing bitstreams generated during the testing process. Random input sequences are fed into the FPGA, and the resulting outputs are compared between a "Trojan" and a "Safe" instance of the hardware.

## Table of Contents
- [Usage](#usage)
- [Functions](#functions)
  - [generate_random_h_string](#generate_random_h_string)
  - [gather_hardware_samples](#gather_hardware_samples)
  - [compare_outputs](#compare_outputs)
  - [find_trigger_bits](#find_trigger_bits)
- [Contributing](#contributing)


## Usage

1. Update the `com_port` variable in the code with the correct COM port for your FPGA device.
2. Run the `gather_hardware_samples` function twice:
   - First, to gather data from the hardware with the Trojan, using `out_trojan.txt`.
   - Then, to gather data from the safe hardware, using `out_safe.txt`.
3. Use the `compare_outputs` function to identify differences between the Trojan and Safe outputs.
4. Run `find_trigger_bits` to locate active high and low trigger bits responsible for the Trojan behavior.

## Functions

### `generate_random_h_string(stringLength)`
Generates a random hexadecimal string of length `stringLength` to be used as input for FPGA testing.

**Parameters:**
- `stringLength`: Length of the string to be generated.

### `gather_hardware_samples(filename)`
Gathers hardware samples from the FPGA and saves them to a text file.

**Parameters:**
- `filename`: Name of the output file to save the gathered samples.

**Steps:**
- The function opens a serial connection to the FPGA and sends random hexadecimal inputs.
- The FPGA's output is read and saved to a file for comparison.

### `compare_outputs(filename1, filename2)`
Compares outputs from the Trojan and Safe hardware. Discovers the payload of the trojan.

**Parameters:**
- `filename1`: File containing safe output data.
- `filename2`: File containing Trojan output data.

**Steps:**
- This function compares the two sets of outputs line by line, identifying differences. It records the XOR result of different outputs in a list of payload bits.

### `find_trigger_bits(filename1)`
Identifies the active low and high trigger bits for the Trojan input.

**Parameters:**
- `filename1`: File containing the input data to analyze.

**Steps:**
- This function examines the XOR results of the different outputs to find which bits are responsible for triggering the Trojan behavior. It calculates active high and active low trigger bits.

## Contributing

Made By Yu Tan, Kingsley Nwabeke, Jian Zhuang Jiang

