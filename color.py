from neopixel import *
import numpy as np
import time

def transition_colors(total_colors, start_color, end_color):
    """
    Generates a list of colors that smoothly transition from
    a start color to an ending color. 
    
    Args:
        total_colors: The desired number of colors 
        start_color:  The first color
        end_color:    The final color
    
    Returns:
        list: The generated colors
    """
    start_red = (start_color >> 16) & 0xff
    start_green = (start_color >> 8) & 0xff
    start_blue = start_color & 0xff

    end_red = (end_color >> 16) & 0xff
    end_green = (end_color >> 8) & 0xff
    end_blue = end_color & 0xff

    red_low = min(start_red, end_red)
    red_high = max(start_red, end_red)
    green_low = min(start_green, end_green)
    green_high = max(start_green, end_green)
    blue_low = min(start_blue, end_blue)
    blue_high = max(start_blue, end_blue)

    colors = []
    for i in range(total_colors):
        i_r = i if start_red < end_red else total_colors - i - 1
        i_g = i if start_green < end_green else total_colors - i - 1
        i_b = i if start_blue < end_blue else total_colors - i - 1

        red = int(np.interp(i_r, [0, total_colors], [red_low, red_high]))
        green = int(np.interp(i_g, [0, total_colors], [green_low, green_high]))
        blue = int(np.interp(i_b, [0, total_colors], [blue_low, blue_high]))
        colors.append(Color(red, green, blue))

    return colors

def get_color_map(total_colors, colors):
    """
    Generates a color map that smoothly transitions from
    the given list of colors.

    Args:
        total_colors: The desired number of colors in the map
        colors:       List of colors to transition from over the map

    Returns:
        list: The generated color map
    """
    color_map = []
    if len(colors) > 1:
        color_step = total_colors / (len(colors) - 1)
        for i in range(1, len(colors)):
            color_map += transition_colors(color_step, colors[i - 1], colors[i])
    else:
        color_map = [colors[0]] * total_colors

    return color_map
