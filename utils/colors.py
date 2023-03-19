
color_codes = {
    "black": "30",
    "red": "31",
    "green": "32",
    "yellow": "33",
    "blue": "34",
    "magenta": "35",
    "cyan": "36",
    "white": "37",
    "bright_black": "90",
    "bright_red": "91",
    "bright_green": "92",
    "bright_yellow": "93",
    "bright_blue": "94",
    "bright_magenta": "95",
    "bright_cyan": "96",
    "bright_white": "97",
}

bold_color_codes = {f"bright_{k}": f"{v};1" for k, v in color_codes.items()}
color_codes.update(bold_color_codes)

special_codes = {
    "reset": "0",
    "bold": "1",
    "inverse": "7",
    "bright_inverse": "7;1",
}

color_codes.update(special_codes)

# Useful dictionary with color codes for easy access.
COLORMAP = {k: f"\x1b[{v}m" for k, v in color_codes.items()}

# Some commonly used colours for easier access.
BLACK = COLORMAP["black"]
RED = COLORMAP["red"]
GREEN = COLORMAP["green"]
YELLOW = COLORMAP["yellow"]
BLUE = COLORMAP["blue"]
RESET = COLORMAP["reset"]

# Some commonly used styles for easier access.
BOLD = COLORMAP["bold"]
INVERSE = COLORMAP["inverse"]
BRIGHT_INVERSE = COLORMAP["bright_inverse"]
