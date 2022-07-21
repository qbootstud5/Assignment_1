#! /usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wednesday July 20
@author: Jon Oillarburu

This file solves the Assignment 1
"""

from typing import Any

import numpy as np
from matplotlib import pyplot as plt
from numpy.typing import NDArray


# Part 1
def print_chart(canvas: NDArray) -> None:
    """
    Function to print the chart
    :param canvas: The numpy array containing the chart characters
    """
    string: str = "".join(["".join(canvas[k, :]) + "\n" for k in range(canvas.shape[0] - 1)] + ["".join(canvas[-1, :])])

    print(string)


# Part 2
def create_chart(height: int, width: int, display_grid: bool = False) -> NDArray:
    """
    Function to create the chart, an array of dimension height*width containing the string character
    :param width: The width of the chart
    :param height: the height of the chart
    :param display_grid: the boolean to tell if we display a grid or not
    """
    char_to_fill_with: str = "." if display_grid else " "

    array: NDArray = np.empty((height, width), dtype=str)

    # Fill the interior of the array
    array[1:-1, 1:-1] = char_to_fill_with
    # Fill the horizontal border of the array
    array[1:-1, ::width - 1] = "|"
    # Fill the vertical border of the array
    array[::height - 1, 1:-1] = "-"
    # Fill the corner of the array
    array[::height - 1, ::width - 1] = "+"

    return array


# Part 3

def min_max_normalization(array: list[Any]) -> NDArray:
    """
    Nested function to apply the min max normalization
    :param array: a list of input values
    :return: the array rescaled

    >>> x = [1,3,7,11]
    >>> new_array = min_max_normalization(x)
    >>> list(new_array) == [0,0.2,0.7,1]
    True
    """
    np_array: NDArray = np.asarray(array, dtype=float)

    min_value: Any
    max_value: Any
    min_value, max_value = np.min(np_array), np.max(np_array)

    np_array -= min_value
    np_array /= (max_value - min_value)

    return np_array


def normalize_and_scale(
        x_data_points: list[Any],
        y_data_points: list[Any],
        height: int,
        width: int
) -> tuple[NDArray, NDArray]:
    """
    Function to normalize the data according to the min max normalization, and scale it.
    :param x_data_points: list of numbers
    :param y_data_points: list of numbers
    :param height: the height to scale with
    :param width: the width to scale with

    Some doctests:
    >>> x_data = [1, 3, 2]
    >>> y_data = [0.5,1.5,1.25]
    >>> h, w = 5, 8
    >>> final_x, final_y = normalize_and_scale(x_data, y_data, h, w)
    >>> list(final_x) == [0,8,4]
    True
    >>> list(final_y) == [0, 5, 3]
    True
    """
    x_rescaled: NDArray = min_max_normalization(x_data_points)

    y_rescaled: NDArray = min_max_normalization(y_data_points)

    def mult_and_floor(array: NDArray, factor: int) -> NDArray:
        """
        Nested function to apply the multiplication by a factor, and floor operation
        :param array: The array to rescale
        :param factor: the multiplying factor
        :return: the rescaled numpy array
        """
        return np.floor(array * factor)

    return mult_and_floor(x_rescaled, width)[:].astype(int), mult_and_floor(y_rescaled, height)[:].astype(int)


# Part IV
def draw_on_canvas(canvas: NDArray, x_data_points: NDArray, y_data_points: NDArray, display_grid: bool = False) -> None:
    """
    Function to draw the points on canvas
    :param canvas: The NDarray representing the chart
    :param x_data_points: the x data points rescaled
    :param y_data_points: the y data points rescaled
    :param display_grid: the bool deciding of the character to fill with
    :return: None
    """
    char_to_fill_with = "*" if display_grid else "•"

    canvas[[-1 * (k + 1 - canvas.shape[0]) for k in y_data_points], x_data_points] = char_to_fill_with


# Part V
def extend_main_canvas(canvas: NDArray, min_x_value: float, max_x_value: float, min_y_value: float, max_y_value: float,
                       legend: str = "", horizontal_space: int = 2, vertical_space: int = 0) -> NDArray:
    """
    The function to extend the canvas, by adding x and y axes

    :param canvas: the canvas containing the chart as an array of strings
    :param min_x_value: the minimum x value
    :param max_x_value: the max x value
    :param min_y_value: the min y value
    :param max_y_value: the max y value
    :param legend: the legend to add in x axis
    :param horizontal_space: the horizontal space between y axis and the main chart
    :param vertical_space: the vertical space between the x axis and the main chart
    :return: the array containing all the strings to display the chart
    """
    # Setting all integer values to string
    string_min_x: str = str(min_x_value)
    string_max_x: str = str(max_x_value)
    string_min_y: str = str(min_y_value)
    string_max_y: str = str(max_y_value)

    # Necessary offset to ensure there is space between y axis and the chart
    max_len_y_value: int = max(len(string_min_y), len(string_max_y))
    y_axis: NDArray = np.empty((canvas.shape[0] + 1 + vertical_space, max_len_y_value + horizontal_space), dtype=str)

    y_axis[:] = " "

    # center the integer representing strings
    y_axis[0, :max_len_y_value] = list(string_max_y.center(max_len_y_value, " "))
    y_axis[canvas.shape[0] - 1, :max_len_y_value] = list(string_min_y.center(max_len_y_value, " "))

    # Setting the x array representing the x axis
    x_axis: NDArray = np.empty((1 + vertical_space, canvas.shape[1]), dtype=str)

    if len(legend) > canvas.shape[1] - len(string_min_x) - len(string_max_x):
        raise ValueError("The legend is too big to be plotted")

    # Plot the legend centered
    x_axis[-1, :] = list(legend.center(canvas.shape[1], " "))
    x_axis[-1, :len(string_min_x)], x_axis[-1, -len(string_max_x):] = list(string_min_x), list(string_max_x)

    # Concatenate the arrays
    new_array: NDArray = np.hstack((y_axis, np.vstack((canvas, x_axis))))

    return new_array


# Part VI
def add_plot_title(canvas: NDArray, title: str = "") -> NDArray:
    """
    Function to add the title to the chart
    :param canvas: The main canvas
    :param title: the string title to add
    :return: the NDArray which is the concatenation of the title and the chart
    """
    title_array: NDArray = np.empty(canvas.shape[1], dtype=str)
    title_array[:] = list(title.center(canvas.shape[1], " "))
    return np.vstack((title_array, canvas))


# Part VII
def plot_with_maptlotlib(x_data: list[int], y_data: list[int], title: str = "", legend: str = "",
                         display_grid: bool = False) -> None:
    """
    Function to plot the functions with matplolib
    :param x_data: the x data
    :param y_data: the y data
    :param title: the title of the plot
    :param legend: the legend of the plot
    :param display_grid: the boolean to say if we display a grid or not
    :return:
    """
    fig, ax = plt.subplots(figsize=(11, 6))
    ax.plot(x_data, y_data)

    ax.legend(legend)

    ax.set_title(title)

    if display_grid:
        plt.grid()
    plt.show()


def plot(x: list[Any], y: list[Any], display_grid: bool = False, height: int = 15, width: int = 100, title: str = "",
         legend: str = "") -> None:
    """
    The final function gathering all preceeding functions, to plot a function depending on x and y data
    :param x: x data
    :param y: y data
    :param display_grid: the boolean telling if it displays a grid or not
    :param height: the height of the chart
    :param width: the width of the chart
    :param title: the title of the chart
    :param legend: the legend of the chart
    """
    # Necessary to add a - 1 as after rescaling, the x data is an integer between [0,height] and [0, width],
    # But the index height is out of bounds for an array of size height
    x_array, y_array = normalize_and_scale(x, y, height - 1, width - 1)

    # Initialize the plot canvas
    canvas = create_chart(height, width, display_grid=display_grid)

    # Draw on canvas in place
    draw_on_canvas(canvas, x_array, y_array, display_grid=display_grid)

    # Extend canvas
    min_x_value: int
    max_x_value: int
    min_x_value, max_x_value = round(min(x)), round(max(x))

    min_y_value: int
    max_y_value: int
    min_y_value, max_y_value = round(min(y)), round(max(y))

    extended_canvas = extend_main_canvas(canvas, min_x_value, max_x_value, min_y_value, max_y_value, legend=legend)

    # Add title to canvas
    final_canvas = add_plot_title(extended_canvas, title=title)

    # Print canvas
    print_chart(final_canvas)

    # Compare with matplotlib canvas
    plot_with_maptlotlib(x, y, title=title, legend=legend, display_grid=display_grid)
