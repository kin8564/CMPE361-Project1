import serial
import random

# Initial testing for Trojans through bitstream output
input_hex = 10
sample = 100
com_port = 'COM8'  # TO-DO, change the com port of the FPGA device
baud_rate = 115200  # Don't change this
random_seed = 0
trigger_input = []
payload_bits = []


"""
Generates a random string of binary inputs to be tested on the hardware.
Params:
    stringLength: length of string to be generated
Return:
    String of random hex characters
"""
def generate_random_h_string(stringLength):
    hex_chars = '0123456789abcdef'
    return ''.join(random.choice(hex_chars) for _ in range(stringLength))

"""
Gathers the sample at x amount and stores them into text files. Function have to be run on two different instance, once
with the trojan and once without to get the output data based on random inputs.
Param:
    filename: File of resulting output for each input to the bitstream
"""
def gather_hardware_samples(filename):
    # Open the COM port
    ser = serial.Serial(com_port, baud_rate, timeout=1)
    if ser.is_open:
        try:
                with open(filename, 'w') as file_out:
                    with open('inputs.txt', 'w') as file_in:
                        print(f"Connected to {com_port} at {baud_rate} baud\n")
                        random.seed(random_seed)
                        for i in range(sample):
                            data_to_send = generate_random_h_string(input_hex)
                            file_in.writelines(data_to_send + f"\n")
                            data_to_send = data_to_send[2:] if data_to_send[0:2] == "0x" else data_to_send
                            data_bytes = bytes.fromhex(data_to_send)
                            print(data_to_send)
                            ser.write(data_bytes)

                            # Read data from the FPGA
                            received_data = ser.read(
                                16)  # to-do, change the parameter into the number of bytes needed to read from FPGA
                            # Convert the received bytes to a hexadecimal string
                            hex_string = ''.join(f'{byte:02X}' for byte in received_data)
                            print(hex_string)

                            file_out.writelines(hex_string + f"\n")
        except KeyboardInterrupt:
            pass
        finally:
            ser.close()
            print("Connection Closed")
    else:
        print(f"Failed to connect to {com_port}")


"""
Compares the lists of trojan and the safe output. For every input to the system the two resulting outputs are XORed to
highlight the payload of the trojan.
Params:
    filename1: Safe system output
    filename2: Trojan system output
"""
def compare_outputs(filename1, filename2):
    with open(filename1, "r") as out_safe, open(filename2, "r") as out_trojan:
        f1_lines = out_safe.readlines()
        f2_lines = out_trojan.readlines()
        for i in range(len(f1_lines)):
            if f1_lines[i] != f2_lines[i]:
                value1 = int(f1_lines[i], 16)
                value2 = int(f2_lines[i], 16)
                payload = (value1 ^ value2)
                payload_bits.append(payload)
                trigger_input.append(i)


"""
Finds the active low and high bits for the bitstream. Active high triggers are found by calculating a running xor with
every trojan input. Active low triggers are found from by calculating a running or for evey trojan input, then
inverting the result.
Params:
    filename1: 
"""
def find_trigger_bits(filename1):
    with open(filename1, "r") as input:
        lines = input.readlines()
        trojan_list = []
        hex = "FFFFFFFFFF"
        hex = int(hex, 16)
        for i in trigger_input:
            trojan_list.append(lines[i][0:10])
        for j in trojan_list:
            v1 = int(j,16)
            hex = v1 & hex

        int_values = [int(h, 16) for h in trojan_list]

        # Perform the bitwise OR across all values
        or_result = int_values[0]
        for val in int_values[1:]:
            or_result |= val

        max_bit_length = max(len(bin(val)[2:]) for val in int_values)
        nor_result = ~or_result & ((1 << max_bit_length) - 1)  # Limit the result to the same bit length

        # Convert the result to binary string
        binary_nor_result = bin(nor_result)[2:].zfill(max_bit_length)
        print(binary_nor_result)

        binary_str = bin(hex)[2:]
        high_bit_positions = []
        for i, bit in enumerate(reversed(binary_str)):
            if bit == '1':
                high_bit_positions.append(i)
        print("The active high trigger bits are", high_bit_positions)

        low_bit_positions = []
        for i, bit in enumerate(reversed(binary_nor_result)):  # Enumerate starting from the right (reverse string)
            if bit == '1':
                low_bit_positions.append(i)  # Append the position if the bit is '1'
        print("The active low trigger bits are", low_bit_positions)


gather_hardware_samples("out_trojan.txt") # RUN THESE SEPARATELY. COMMENT 1 OUT
gather_hardware_samples("out_safe.txt")
compare_outputs("out_safe.txt","out_trojan.txt")
find_trigger_bits("inputs.txt")