""" Python module that contains a function that extracts the last word from a log file
between the given timestamps: 17:56:07.996 and 17:56:08.357
"""


def last_word_from_file(file_path):
    """
    Extracts the last word from each line of a log file within the timestamp range
    specified (between "17:56:07.996" and "17:56:08.357").
    Args:
        file_path (str): The path to the log file.
    Returns:
        list: A list containing the last word of each line within the specified
            timestamp range. If a line does not contain enough words or does not
            fall within the range, its last word is not included in the result list.
    """
    result_list = []

    with open(file_path, "r") as file:
        in_target_range = False
        for line in file:
            words = line.split()

            if len(words) >= 2:
                timestamp_str = words[1]
                if "17:56:07.996" <= timestamp_str <= "17:56:08.357":
                    in_target_range = True
                else:
                    in_target_range = False

                if in_target_range:
                    last_word = words[-1]
                    result_list.append(last_word.strip())

    #print(result_list)
    return result_list


#example of usage in main
# if __name__ == "__main__":
#     res = last_word_from_file("/home/cristinagheorghe/Downloads/logcat_applications.txt")
#     print(res)