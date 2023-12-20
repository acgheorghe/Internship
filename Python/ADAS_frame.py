"""
This python module, named IVI_frame, contains functions for manipulating In-Vehicle Infotainment (IVI) frame payloads used in Advanced Driver Assistance Systems (ADAS).
The module specifically focuses on modifying signals within the ADAS payloads and converting between binary and hexadecimal representations.
"""


import IVI_frame

ADAS_PAYLOADS = ["00 06 02 08 80 00 00 00 00 00 00 00 00 05 D0 08 FF 60 00 00 02 00 00 00 00 06 01 08 80 00 00 00 00 00 00 00 00 00 10 C7 77 8A 70 AB AF 88 2A 8C",
                 "00 06 02 08 40 00 00 10 00 00 00 00 00 05 D0 08 21 20 00 00 02 00 00 00 00 06 01 08 80 00 00 00 00 00 00 00 00 00 00 11 29 FB 84 33 1D E5 5E 9D"]

MAPPING_LDW_ALERT_STATUS = (2, 5, 2)
MAPPING_LCA_OVERRIDE_DISPLAY = (5, 2, 1)
MAPPING_DW_FOLLOWUP_TIME_DISPLAY = (4, 7, 6)


def binary_string_to_hex(binary_string):
    """
    Converts a binary string to a hex string.
    Args:
        binary_string (str): Binary string.
    Returns:
        str: Hexadecimal string.
    """
    hex_value = hex(int(binary_string, 2))[2:]
    return hex_value.zfill(len(hex_value) + (len(hex_value) % 2))  # Ensure even length


def modify_signal(mapping, dlc, new_value):
    """
        Modifies a signal value in the payload based on the provided mapping.
        Args:
            mapping (tuple): Tuple containing byte position, bit position, and size of the signal.
            dlc (list): List of binary strings representing the dlc.
            new_value (int): The new value to set for the signal.
        Returns:
            list: Updated list of binary strings representing the modified payload, in hex format.
    """
    byte_val, bit_val, size = mapping
    binary_new_value = str(bin(new_value)[2:].zfill(size))
    bit_val = 7 - bit_val
    dlc[byte_val] = dlc[byte_val][:bit_val] + binary_new_value + dlc[byte_val][bit_val+size:]
    res=""
    for p in dlc:
        res=" ".join([res,(binary_string_to_hex(p)).upper()])

    return res[1:]

def set_values(payload):
    """
        Parses an ADAS payload, modifies specific signals based on predefined mappings, and returns the updated payload.
        Parameters:
            payload (str): Hexadecimal string representing the ADAS payload.
        Returns:
            str: Updated ADAS payload in hexadecimal representation.
    """
    dlc_num = 1
    # variable contor to track out position in the payload
    contor = 0
    res = ""
    while dlc_num <= 3:
        contor += 9
        size = int(payload[contor:(contor+2)])
        contor += 3
        pdu = payload[contor:(contor + size*3 - 1)]
        contor += size*3
        # using the hex_to_binary function from the IVI_frame.py file
        pdu = IVI_frame.hex_to_binary_payload(pdu)
        match dlc_num:
            case 1:
                res = "".join(payload[0:contor - size * 3])
                res = "".join([res,modify_signal(MAPPING_LDW_ALERT_STATUS, pdu, 2)])
            case 2:
                res = " ".join([res, payload[(contor - size*3 - 12):(contor - size * 3)]])
                res = "".join([res, modify_signal(MAPPING_DW_FOLLOWUP_TIME_DISPLAY, pdu, 45)])
            case 3:
                res = " ".join([res, payload[(contor - size * 3 - 12):(contor - size * 3)]])
                res = "".join([res, modify_signal(MAPPING_LCA_OVERRIDE_DISPLAY, pdu, 1)])
                res = " ".join([res, payload[contor:]])

        dlc_num += 1

    return res


# Example usage in main
if __name__ == '__main__':
    for payload in ADAS_PAYLOADS:
        print("\nBefore modifying:")
        print(payload)
        value = set_values(payload)
        print("\nAfter modifying:")
        print(value)
