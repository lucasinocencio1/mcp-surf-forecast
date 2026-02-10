"""
helper utilities for data formatting and conversion
"""


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
