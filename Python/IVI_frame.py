"""
Module Description:
    This module provides functions to parse IVI (In-Vehicle Infotainment) frames and extract specific signals.
"""


# Necessary constants
PAYLOADS = ["60 20 45 6C FE 3D 4B AA", "40 12 6C AF 05 78 4A 04"]
MAPPING_PASSENGER_SEAT = (0, 7, 3)
MAPPING_CLIM_FPRIGHT_BLOWING = (5, 7, 4)
MAPPING_TIME_FORMAT_DISPLAY = (5, 3, 1)

def hex_to_binary_payload(payload):
    """
        Converts a hex payload to a list of binary strings.
        Args:
            payload (str): Hexadecimal payload string.
        Returns:
            list: List of binary strings representing each hex value in the payload.
        """
    binary_list = [bin(int(hex_value, 16))[2:].zfill(8) for hex_value in payload.split()]
    return binary_list[:8]

def extract_signal(mapping, payload):
    """
        Extracts a signal value from the payload based on the provided mapping.
        Args:
            mapping (tuple): Tuple containing byte position, bit position, and size of the signal.
            payload (list): List of binary strings representing the payload.
        Returns:
            int: Extracted signal value.
        """
    byte_val, bit_val, size = mapping
    byte = payload[byte_val]
    # reversing it
    byte = byte[::-1]
    res=[]
    while size != 0:
        res.append(byte[bit_val])
        bit_val -= 1
        size -= 1
    res = int("".join(map(str, res)), 2)
    return res



def find_values(payload):
    """
        Finds and returns specific signal values from the given payload.
        Args:
            payload (str): Hexadecimal payload string.
        Returns:
            dict: Dictionary containing values for Passenger Seat Memo Request, ClimF PRight Blowing Request,
                  and Time Format Display signals.
    """
    payload = hex_to_binary_payload(payload)
    passenger_seat_value = extract_signal(MAPPING_PASSENGER_SEAT, payload)
    clim_fp_right_blowing_value = extract_signal(MAPPING_CLIM_FPRIGHT_BLOWING, payload)
    time_format_display_value = extract_signal(MAPPING_TIME_FORMAT_DISPLAY, payload)

    return {
        'PassengerSeatMemoRequest': passenger_seat_value,
        'ClimFPrightBlowingRequest': clim_fp_right_blowing_value,
        'TimeFormatDisplay': time_format_display_value
    }
    

# Example usage in main
if __name__ == '__main__':
    values = [find_values(payload) for payload in PAYLOADS]
    print(values)
