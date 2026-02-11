"""
helper utilities for data formatting and conversion
"""


def validate_coordinates(latitude: float, longitude: float) -> None:
    """
    Validate latitude and longitude are within valid ranges.

    args:
        latitude: latitude in degrees (-90 to 90)
        longitude: longitude in degrees (-180 to 180)

    raises:
        ValueError: if latitude or longitude is out of range
    """
    if not -90 <= latitude <= 90:
        raise ValueError(
            f"Invalid coordinates: latitude must be between -90 and 90, got {latitude}"
        )
    if not -180 <= longitude <= 180:
        raise ValueError(
            f"Invalid coordinates: longitude must be between -180 and 180, got {longitude}"
        )


def degrees_to_compass(degrees: float) -> str:
    """
    convert degrees to compass direction (n, ne, e, se, s, sw, w, nw)

    args:
        degrees: direction in degrees (0-360)

    returns:
        compass direction string
    """
    # normalize to 0-360
    degrees = degrees % 360

    # 16-point compass rose for more precision
    # each direction covers 22.5 degrees (360/16)
    directions = [
        "n",
        "nne",
        "ne",
        "ene",
        "e",
        "ese",
        "se",
        "sse",
        "s",
        "ssw",
        "sw",
        "wsw",
        "w",
        "wnw",
        "nw",
        "nnw",
    ]

    # calculate index (add 11.25 to center each range)
    index = int((degrees + 11.25) / 22.5) % 16

    return directions[index]


def format_direction(degrees: float, uppercase: bool = True) -> str:
    """
    format direction as "270° (w)" or "270° (W)"

    args:
        degrees: direction in degrees
        uppercase: whether to uppercase the compass direction

    returns:
        formatted direction string
    """
    compass = degrees_to_compass(degrees)
    if uppercase:
        compass = compass.upper()
    return f"{degrees:.0f}° ({compass})"
