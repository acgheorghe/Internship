"""
Python module that contains an EV Range Calculator
"""

TOTAL_CAPACITY = 62  # Total battery capacity in kWh
ENERGY_CONSUMPTION = 15.6  # Energy consumption in kWh per 100 km



def calculate_range(battery_level):
    """
    This function will calculate the 'Estimated available range' of the vehicle based on the following:
    Total battery capacity: 62kwh
    Energy Consumption: 15.6kWh/100km
    Battery level: X%
    """

    available_energy_kwh = (battery_level / 100) * TOTAL_CAPACITY
    estimated_range_km = (available_energy_kwh / ENERGY_CONSUMPTION) * 100
    return estimated_range_km


# Example of usage
# if __name__ == "__main__":
#     battery_level = int(input("Enter the battery level (0-100): "))
#     if not (0 <= battery_level <= 100):
#         print("Invalid input. Battery level should be between 0 and 100.")
#     else:
#         estimated_range = calculate_range(battery_level)
#         print(f"Estimated Available Range: {estimated_range:.2f} km")