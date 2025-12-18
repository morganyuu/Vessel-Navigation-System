# Question 1: Set the Horizon: Define the World
# Initial global variables and math + random module for later questions

import math
import random

# Constants for earth and constraints
MIN_LAT = -90        # Minimum valid latitude
MAX_LAT = 90         # Maximum valid latitude
MIN_LONG = -180      # Minimum valid longitude
MAX_LONG = 180       # Maximum valid longitude
EARTH_RADIUS = 6378  # Earth radius in km, used for distance calculation
STORM_STEPS = 5      # Number of turns before storm arrives


# Question 2: Calibrate the Compass: Degrees to Radian
def degrees_to_radians(deg):
    """""
    Convert an angle from degrees to radians.

    Parameters:
    deg (float): Angle in degrees.

    Returns:
    float: Angle in radians, rounded to 2 decimal places.

    Examples:
    >>> degrees_to_radians(180)
    3.14
    >>> degrees_to_radians(90)
    1.57
    >>> degrees_to_radians(45)
    0.79
    """""
    radians = deg * math.pi / 180 # Conversion formula
    return round(radians, 2)


# Question 3: Acquire a Fix: Validate a Coordinate
def get_valid_coordinate(val_name, min_float, max_float):
    """
    Ask user for a coordinate and validate it is within a range.

    Parameters:
    val_name (str): Name of the coordinate.
    min_float (float): Minimum valid value.
    max_float (float): Maximum valid value.

    Returns:
    float: Validated coordinate value.

    Examples:
    >>> get_valid_coordinate("latitude", -90, 90)  # user enters 45
    45.0
    >>> get_valid_coordinate("longitude", -180, 180)  # user enters -75
    -75.0
    >>> get_valid_coordinate("latitude", -90, 90)  # user enters 100 then 60
    60.0
    """
    # Ask for user input
    float_value = float(input("What is your " + val_name + "?"))

    # Keep asking until input is valid
    while float_value < min_float or float_value > max_float:
        print("Invalid " + val_name)
        float_value = float(input("What is your " + val_name + "?"))
    return float_value


# Question 4: Plot Our Position: Get GPS Location
def get_gps_location():
    """
    Ask the user to input latitude and longitude coordinates

    Returns:
    (latitude, longitude) as floats.

    Examples:
    >>> get_gps_location()  # 45 for latitude, -75 for longitude
    (45.0, -75.0)
    >>> get_gps_location()  #   -30, 120
    (-30.0, 120.0)
    >>> get_gps_location()  #  90, 180
    (90.0, 180.0)
    """
    # Get latitude and longitude separately with validation
    latitude = get_valid_coordinate("latitude", MIN_LAT, MAX_LAT)
    longitude = get_valid_coordinate("longitude", MIN_LONG, MAX_LONG)

    return latitude, longitude


# Question 5: Chart the Distance: Great-circle Calculator
def distance_two_points(latitude_1, longitude_1, latitude_2, longitude_2):
    """
    Calculate the great-circle distance between two points 

    Parameters:
    latitude_1, longitude_1 (float): First point coordinates in degrees.
    latitude_2, longitude_2 (float): Second point coordinates in degrees.

    Returns:
    float: Distance in kilometers, rounded to 2 decimal places.

    Examples:
    >>> distance_two_points(0, 0, 0, 90)
    10007.54
    >>> distance_two_points(45, -75, 46, -76)
    131.78
    >>> distance_two_points(-30, 120, 30, -60)
    15007.55
    """
    # Convert input coordinates from degrees to radians
    lat_1 = degrees_to_radians(latitude_1)
    long_1 = degrees_to_radians(longitude_1)
    lat_2 = degrees_to_radians(latitude_2)
    long_2 = degrees_to_radians(longitude_2)

    # Compute differences in coordinates
    delta_lat = lat_2 - lat_1
    delta_long = long_2 - long_1

    # Haversine formula for great-circle distance
    a = ((math.sin(delta_lat / 2)) ** 2 + math.cos(lat_1) * math.cos(lat_2) *
        math.sin(delta_long / 2) ** 2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))

    distance = EARTH_RADIUS * c
    return round(distance, 2)


# Question 6: Helm Nudge: Apply Wave Impact to a Coordinate
def apply_wave_impact(position, min_float, max_float):
    """
      Apply a random wave impact to a coordinate

      Parameters:
      position (float): Current coordinate
      min_float (float): Minimum allowed value
      max_float (float): Maximum allowed value.

      Returns:
      float: Updated coordinate after impact, rounded to 2 decimals.

      Examples:
      >>> apply_wave_impact(45, -90, 90)
      44.23  # random output may vary
      >>> apply_wave_impact(-75, -180, 180)
      -74.57  # random output may vary
      >>> apply_wave_impact(0, -180, 180)
      -0.68  # random output may vary
      """
    # Compute random step between -1 and +1
    step = 2 * random.random() - 1
    # Make sure new position stays within valid range
    while position + step < min_float or position + step > max_float:
        step = 2 * random.random() - 1

    return round(position + step, 2)


# Question 7: Wave Hit Event: Reorient and Recheck
def wave_hit_vessel(latitude, longitude):
    """
    Adjust vessel coordinates randomly due to wave impact.

    Parameters:
    latitude (float): Current latitude.
    longitude (float): Current longitude

    Returns:
    New (latitude, longitude) after impact.

    Examples:
    >>> wave_hit_vessel(45, -75)
    (45.57, -74.42)  # random output may vary
    >>> wave_hit_vessel(0, 0)
    (0.23, -0.54)  # random output may vary
    >>> wave_hit_vessel(-30, 120)
    (-29.84, 119.76)  # random output may vary
    """
    # Apply random shift simulating wave hit to both latitude and longitude
    new_latitude = apply_wave_impact(latitude, MIN_LAT, MAX_LAT)
    new_longitude = apply_wave_impact(longitude, MIN_LONG, MAX_LONG)

    return new_latitude, new_longitude


# Question 8: Helm Advance: Move Toward Waypoint
def move_toward_waypoint(current_latitude, current_longitude,
    waypoint_latitude, waypoint_longitude):
    """
        Move the vessel a step closer toward a waypoint.

    Parameters:
    current_latitude, current_longitude (float): Current vessel coordinates.
    waypoint_latitude, waypoint_longitude (float): Target waypoint coordinates.

    Returns:
    Updated (latitude, longitude) after moving toward waypoint.

    Examples:
    >>> move_toward_waypoint(45, -75, 46, -74)
    (45.53, -74.53)  # random output may vary
    >>> move_toward_waypoint(0, 0, 10, 10)
    (5.67, 5.33)  # random output may vary
    >>> move_toward_waypoint(-30, 120, -25, 125)
    (-27.89, 122.34)  # random output may vary
    """
    # Random scale gives partial movement toward waypoint
    scale = random.random() + 1

    # Shift position closer to waypoint
    new_latitude = current_latitude + (waypoint_latitude -
                    current_latitude)/scale
    new_longitude = current_longitude + (waypoint_longitude -
                    current_longitude)/scale

    # Make sure latitude within valid bounds
    if new_latitude < MIN_LAT:
        new_latitude = MIN_LAT
    elif new_latitude > MAX_LAT:
        new_latitude = MAX_LAT

    # Make sure longitude within valid bounds
    if new_longitude < MIN_LONG:
        new_longitude = MIN_LONG
    elif new_longitude > MAX_LONG:
        new_longitude = MAX_LONG

    return round(new_latitude, 2), round(new_longitude, 2)


# Question 9: Bridge Console: Storm Run to Waypoint

def vessel_menu():
    """
        Interactive console menu for vessel navigation simulation

        The function allows to
        -Set a waypoint
        -Move the vessel toward waypoint
        -Random wave impacts (20% chance each step).
        -Track storm countdown (mission must finish before storm arrives).
        -Exit the console when asked

        Gameplay rules:
        -Initial position input by user.
        -Each move updates position closer to the waypoint.
        -If vessel reaches within 10 km of the waypoint before storm hits,
          mission succeeds.
        -If storm counter hits 0 before arrival, mission fails.

        Parameters:
        None (input is collected from input functions by
        calling other functions).

        Returns:
        None (prints updates to console until mission ends).

        Examples:
        >>> vessel_menu()
        Welcome to the boat menu
        Please select an option below:
        1) Set waypoint
        2) Move toward waypoint and Status report
        3) Exit boat menu
        Choose: 1
        Enter waypoint coordinates.
        Waypoint set to latitude of 45.0 and longitude of -75.0
        Choose: 2
        Captain Log: Journeyed towards waypoint.
        Current position is latitude of 44.5 and longitude of -75.3
        Distance to waypoint: 60.4 km
        Storm T-minus: 4
        Choose: 3
        Console closed by captain.
        """
    print("Welcome to the boat menu")

    # Initialize state
    waypoint_latitude, waypoint_longitude = None, None
    set_waypoint = False
    storm_counter = STORM_STEPS
    num_choice = True

    # Get initial position from user
    current_latitude, current_longitude = get_gps_location()
    
    print("Please select an option below:\n"
          "1) Set waypoint\n"
          "2) Move toward waypoint and Status report\n"
          "3) Exit boat menu")
    # Main menu loop
    while num_choice:
        choice = input("Please select an option below:\n"
                       "1) Set waypoint\n"
                       "2) Move toward waypoint and Status report\n"
                       "3) Exit boat menu\n"
                       "Choose: ")

        if choice == "1":

            # User sets waypoint
            print("Enter waypoint coordinates.")
            waypoint_latitude, waypoint_longitude = get_gps_location()
            print("Waypoint set to latitude of " + str(waypoint_latitude) +
                  " and longitude of "  + str(waypoint_longitude))
            set_waypoint = True

        elif choice == "2":

            # Attempt to move toward waypoint
            if not set_waypoint:
                print("No waypoint set.") # Checks if waypoint missing

            else:
                # Move vessel closer to waypoint
                current_latitude, current_longitude = move_toward_waypoint(
                    current_latitude, current_longitude, waypoint_latitude,
                    waypoint_longitude)

                print("Captain Log: Journeyed towards waypoint.")

                # Random 20% chance of wave impact
                if random.random() < 0.2:
                    current_latitude, current_longitude = wave_hit_vessel(
                        current_latitude, current_longitude)
                    print("Captain Log: Wave impact recorded")

                # Report current position
                print("Current position is latitude of " +
                      str(current_latitude) + "and longitude of " +
                      str(current_longitude))

                # Calculate distance to waypoint
                distance = distance_two_points(current_latitude,
                    current_longitude, waypoint_latitude, waypoint_longitude)
                print("Distance to waypoint:", distance, "km")

                # Check success condition if less than 10 km away
                if distance_two_points(current_latitude, current_longitude,
                    waypoint_latitude, waypoint_longitude) <= 10:

                    print("Mission success: waypoint reached before the storm.")
                    num_choice = False

                else:
                    # Substract storm countdown
                    storm_counter = storm_counter - 1
                    print("Storm T-minus: " + str(storm_counter))

                    # If storm hits then mission fails
                    if storm_counter == 0:
                        print("Mission failed: storm hit before arrival")
                        num_choice = False

        elif choice == "3":
            # Quits menu
            print("Console closed by captain.")
            num_choice = False













