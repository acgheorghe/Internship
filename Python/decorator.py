"""
    Romanian ID Number Interpreter Module
"""

def validate_id_number(func):
    """
        A decorator function to validate the format of a 13-digit ID number.
        Args:
            func (function): The function to be decorated, expecting a valid 13-digit ID number.
        Returns:
            function: Decorated function that raises a ValueError if the ID number is invalid.
        """
    def wrapper(id_number):
        if len(id_number) != 13 or not id_number.isdigit():
            raise ValueError("Invalid ID number: must be a 13-digit number.")
        return func(id_number)
    return wrapper

@validate_id_number
def interpret_id_number(id_number):
    """
       Interprets a 13-digit Romanian personal identification number (CNP).
       Args:
           id_number (str): A valid 13-digit ID number.
       Raises:
           ValueError: If the ID number has an invalid format or contains invalid information.
       Returns:
           dict: A dictionary containing information extracted from the ID number, including:
                 - "sex": Gender of the person (M/F).
                 - "birth_year": Year of birth.
                 - "birth_month": Month of birth.
                 - "birth_day": Day of birth.
                 - "county": County of origin.
                 - "sequential_number": Sequential number within the birth date and county.
    """
    sex_century = int(id_number[0])
    birth_year = int(id_number[1:3])
    birth_month = int(id_number[3:5])
    birth_day = int(id_number[5:7])
    county_code = int(id_number[7:9])
    sequential_number = int(id_number[9:12])
    control_digit = int(id_number[12])


    # Component S: Sex and Century
    sex_and_century = {
        1: (1900, 1999, "M"),
        2: (1900, 1999, "F"),
        3: (1800, 1899, "M"),
        4: (1800, 1899, "F"),
        5: (2000, 2099, "M"),
        6: (2000, 2099, "F"),
        7: (0, 0, "M"),  # Resident Male
        8: (0, 0, "F")   # Resident Female
    }
    birth_year = birth_year + sex_and_century[sex_century][0]
    birth_year_range = range(sex_and_century[sex_century][0], sex_and_century[sex_century][1] + 1)
    if birth_year not in birth_year_range:
        raise ValueError("Invalid birth year.")

    # Component JJ: County Code
    county_codes = {
        1: "Alba", 2: "Arad", 3: "Argeș", 4: "Bacău", 5: "Bihor", 6: "Bistrița-Năsăud", 7: "Botoșani",
        8: "Brașov", 9: "Brăila", 10: "Buzău", 11: "Caraș-Severin", 12: "Cluj", 13: "Constanța", 14: "Covasna",
        15: "Dâmbovița", 16: "Dolj", 17: "Galați", 18: "Gorj", 19: "Harghita", 20: "Hunedoara", 21: "Ialomița",
        22: "Iași", 23: "Ilfov", 24: "Maramureș", 25: "Mehedinți", 26: "Mureș", 27: "Neamț", 28: "Olt",
        29: "Prahova", 30: "Satu Mare", 31: "Sălaj", 32: "Sibiu", 33: "Suceava", 34: "Teleorman", 35: "Timiș",
        36: "Tulcea", 37: "Vaslui", 38: "Vâlcea", 39: "Vrancea", 40: "București", 41: "București - Sector 1",
        42: "București - Sector 2", 43: "București - Sector 3", 44: "București - Sector 4", 45: "București - Sector 5",
        46: "București - Sector 6", 51: "Călărași", 52: "Giurgiu"
    }
    if county_code not in county_codes:
        raise ValueError("Invalid county code.")


    control_constant = "279146358279"
    total = 0
    for i in range(0,12):
        total += int(control_constant[i])*int(id_number[i])
    print(total)
    control_value = total % 11
    if control_value >= 10:
        control_value = 1

    if control_value != control_digit:
        raise ValueError("Invalid control digit.")


    result = {
        "sex": sex_and_century[sex_century][2],
        "birth_year": birth_year,
        "birth_month": birth_month,
        "birth_day": birth_day,
        "county": county_codes[county_code],
        "sequential_number": sequential_number
    }

    print("Interpretation result:", result)


# Example of usage:
# id_number = "2990219469000"
# try:
#     interpret_id_number(id_number)
# except ValueError as e:
#     print(e)