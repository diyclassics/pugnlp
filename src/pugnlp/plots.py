#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Constants and discovered values, like path to current installation of pug-nlp."""
from __future__ import division, print_function, absolute_import, unicode_literals
from builtins import (
    bytes,
    dict,
    int,
    list,
    object,
    range,
    str,  # noqa
    ascii,
    chr,
    hex,
    input,
    next,
    oct,
    open,
    pow,
    round,
    super,
    filter,
    map,
    zip,
)
import os
import logging

import matplotlib

matplotlib.use("TkAgg")  # noqa
import seaborn as sb
import pandas as pd
from matplotlib import pyplot as plt
import bisect

from pandas.plotting import scatter_matrix

from pugnlp.constants import DATA_PATH

from mpl_toolkits.mplot3d import Axes3D

from plotly import offline
import plotly.graph_objs as go

logger = logging.getLogger(__name__)
import numpy as np


#####################################################################################
# Based on the statistics plotting wrapper from Udacity ST-101
# https://www.udacity.com/wiki/plotting_graphs_with_python


def scatterplot(x, y):
    plt.ion()
    plt.plot(x, y, "b.")
    plt.xlim(min(x) - 1, max(x) + 1)
    plt.ylim(min(y) - 1, max(y) + 1)
    plt.draw()


def barplot(labels, data):
    pos = np.arange(len(data))
    plt.ion()
    plt.xticks(pos + 0.4, labels)
    plt.bar(pos, data)
    plt.grid("on")
    # plt.draw()


def histplot(data, bins=None, nbins=5):
    if not bins:
        minx, maxx = min(data), max(data)
        space = (maxx - minx) / float(nbins)
        bins = np.arange(minx, maxx, space)
    binned = [bisect.bisect(bins, x) for x in data]
    h = (
        ["%.1g" % x for x in list(bins) + [maxx]]
        if space < 1 or space > 1000
        else [str(int(x)) for x in list(bins) + [maxx]]
    )
    print(h)
    if len(str(h[1]) + "-" + h[2]) > 10:
        displab = h[:-1]
    else:
        displab = [x + "-\n " + y for x, y in zip(h[:-1], h[1:])]
    barplot(displab, [binned.count(x + 1) for x in range(len(bins))])


def barchart(x, y, numbins=None):
    if numbins is None:
        numbins = int(len(x) ** 0.75) + 1
    datarange = max(x) - min(x)
    bin_width = float(datarange) / numbins
    pos = min(x)
    bins = [0 for i in range(numbins + 1)]

    for i in range(numbins):
        bins[i] = pos
        pos += bin_width
    bins[numbins] = max(x) + 1
    binsum = [0 for i in range(numbins)]
    bincount = [0 for i in range(numbins)]
    binaverage = [0 for i in range(numbins)]

    for i in range(numbins):
        for j in range(len(x)):
            if x[j] >= bins[i] and x[j] < bins[i + 1]:
                bincount[i] += 1
                binsum[i] += y[j]

    for i in range(numbins):
        binaverage[i] = float(binsum[i]) / bincount[i]
    barplot(range(numbins), binaverage)
    return x, y


def piechart(labels, data):
    plt.ion()
    fig = plt.figure(figsize=(7, 7))
    plt.pie(data, labels=labels, autopct="%1.2f%%")
    plt.draw()
    return fig


def regress(x, y=None):
    """
    Fit a line to the x, y data supplied and plot it along with teh raw samples

    >>> # Gainseville, FL census data shows 14 more new homes are built each year, starting with 517 completed in 1991
    >>> poly = regress([483, 576, 529, 551, 529, 551, 663, 639, 704, 675, 601, 621, 630, 778, 831, 610])
    """
    if y is None:
        y = x
        x = range(len(x))
    if not isinstance(x[0], (float, int, np.float64, np.float32)):
        x = [row[0] for row in x]
    A = np.vstack([np.array(x), np.ones(len(x))]).T
    fit = np.linalg.lstsq(A, y, rcond=None)
    # if fit is None:
    #     fit = [(1, 0), None, None, None]
    poly = fit[0][0], fit[0][-1]
    poly = regressionplot(x, y, poly)
    return poly


def regression_and_plot(x, y=None):
    """
    Fit a line to the x, y data supplied and plot it along with teh raw samples

    >>> age = [25, 26, 33, 29, 27, 21, 26, 35, 21, 37, 21, 38, 18, 19, 36, 30, 29, 24, 24, 36, 36, 27,
    ...        33, 23, 21, 26, 27, 27, 24, 26, 25, 24, 22, 25, 40, 39, 19, 31, 33, 30, 33, 27, 40, 32,
    ...        31, 35, 26, 34, 27, 34, 33, 20, 19, 40, 39, 39, 37, 18, 35, 20, 28, 31, 30, 29, 31, 18,
    ...        40, 20, 32, 20, 34, 34, 25, 29, 40, 40, 39, 36, 39, 34, 34, 35, 39, 38, 33, 32, 21, 29,
    ...        36, 33, 30, 39, 21, 19, 38, 30, 40, 36, 34, 28, 37, 29, 39, 25, 36, 33, 37, 19, 28, 26, 18, 22,
    ...        40, 20, 40, 20, 39, 29, 26, 26, 22, 37, 34, 29, 24, 23, 21, 19, 29, 30, 23, 40, 30, 30, 19, 39,
    ...        39, 25, 36, 38, 24, 32, 34, 33, 36, 30, 35, 26, 28, 23, 25, 23, 40, 20, 26, 26, 22, 23, 18, 36,
    ...        34, 36, 35, 40, 39, 39, 33, 22, 37, 20, 37, 35, 20, 23, 37, 32, 25, 35, 35, 22, 21, 31, 40, 26,
    ...        24, 29, 37, 19, 33, 31, 29, 27, 21, 19, 39, 34, 34, 40, 26, 39, 35, 31, 35, 24, 19, 27, 27, 20,
    ...        28, 30, 23, 21, 20, 26, 31, 24, 25, 25, 22, 32, 28, 36, 21, 38, 18, 25, 21, 33, 40, 19, 38, 33,
    ...        37, 32, 31, 31, 38, 19, 37, 37, 32, 36, 34, 35, 35, 35, 37, 35, 39, 34, 24, 25, 18, 40, 33, 32,
    ...        23, 25, 19, 39, 38, 36, 32, 27, 22, 40, 28, 29, 25, 36, 26, 28, 32, 34, 34, 21, 21, 32, 19, 35,
    ...        30, 35, 26, 31, 38, 34, 33, 35, 37, 38, 36, 40, 22, 30, 28, 28, 29, 36, 24, 28, 28, 28, 26, 21,
    ...        35, 22, 32, 28, 19, 33, 18, 22, 36, 26, 19, 26, 30, 27, 28, 24, 36, 37, 20, 32, 38, 39, 38, 30,
    ...        32, 30, 26, 23, 19, 29, 33, 34, 23, 30, 32, 40, 36, 29, 39, 34, 34, 22, 22, 22, 36, 38, 38, 30,
    ...        26, 40, 34, 21, 34, 38, 32, 35, 35, 26, 28, 20, 40, 23, 24, 26, 24, 39, 21, 33, 31, 39, 39, 20,
    ...        22, 18, 23, 36, 32, 37, 36, 26, 30, 30, 30, 21, 22, 40, 38, 22, 27, 23, 21, 22, 20, 30, 31, 40,
    ...        19, 32, 24, 21, 27, 32, 30, 34, 18, 25, 22, 40, 23, 19, 24, 24, 25, 40, 27, 29, 22, 39, 38, 34,
    ...        39, 30, 31, 33, 34, 25, 20, 20, 20, 20, 24, 19, 21, 31, 31, 29, 38, 39, 33, 40, 24, 38, 37, 18,
    ...        24, 38, 38, 22, 40, 21, 36, 30, 21, 30, 35, 20, 25, 25, 29, 30, 20, 29, 29, 31, 20, 26, 26, 38,
    ...        37, 39, 31, 35, 36, 30, 38, 36, 23, 39, 39, 20, 30, 34, 21, 23, 21, 33, 30, 33, 32, 36, 18, 31,
    ...        32, 25, 23, 23, 21, 34, 18, 40, 21, 29, 29, 21, 38, 35, 38, 32, 38, 27, 23, 33, 29, 19, 20, 35,
    ...        29, 27, 28, 20, 40, 35, 40, 40, 20, 36, 38, 28, 30, 30, 36, 29, 27, 25, 33, 19, 27, 28, 34, 36,
    ...        27, 40, 38, 37, 31, 33, 38, 36, 25, 23, 22, 23, 34, 26, 24, 28, 32, 22, 18, 29, 19, 21, 27, 28,
    ...        35, 30, 40, 28, 37, 34, 24, 40, 33, 29, 30, 36, 25, 26, 26, 28, 34, 39, 34, 26, 24, 33, 38, 37,
    ...        36, 34, 37, 33, 25, 27, 30, 26, 21, 40, 26, 25, 25, 40, 28, 35, 36, 39, 33, 36, 40, 32, 36, 26,
    ...        24, 36, 27, 28, 26, 37, 36, 37, 36, 20, 34, 30, 32, 40, 20, 31, 23, 27, 19, 24, 23, 24, 25, 36,
    ...        26, 33, 30, 27, 26, 28, 28, 21, 31, 24, 27, 24, 29, 29, 28, 22, 20, 23, 35, 30, 37, 31, 31, 21,
    ...        32, 29, 27, 27, 30, 39, 34, 23, 35, 39, 27, 40, 28, 36, 35, 38, 21, 18, 21, 38, 37, 24, 21, 25,
    ...        35, 27, 35, 24, 36, 32, 20]
    >>> wage = [17000, 13000, 28000, 45000, 28000, 1200, 15500, 26400, 14000, 35000, 16400, 50000, 2600, 9000,
    ...        27000, 150000, 32000, 22000, 65000, 56000, 6500, 30000, 70000, 9000, 6000, 34000, 40000, 30000,
    ...        6400, 87000, 20000, 45000, 4800, 34000, 75000, 26000, 4000, 50000, 63000, 14700, 45000, 42000,
    ...        10000, 40000, 70000, 14000, 54000, 14000, 23000, 24400, 27900, 4700, 8000, 19000, 17300, 45000,
    ...        3900, 2900, 138000, 2100, 60000, 55000, 45000, 40000, 45700, 90000, 40000, 13000, 30000, 2000,
    ...        75000, 60000, 70000, 41000, 42000, 31000, 39000, 104000, 52000, 20000, 59000, 66000, 63000, 32000,
    ...        11000, 16000, 6400, 17000, 47700, 5000, 25000, 35000, 20000, 14000, 29000, 267000, 31000, 27000,
    ...        64000, 39600, 267000, 7100, 33000, 31500, 40000, 23000, 3000, 14000, 44000, 15100, 2600, 6200,
    ...        50000, 3000, 25000, 2000, 38000, 22000, 20000, 2500, 1500, 42000, 30000, 27000, 7000, 11900, 27000,
    ...        24000, 4300, 30200, 2500, 30000, 70000, 38700, 8000, 36000, 66000, 24000, 95000, 39000, 20000, 23000,
    ...        56000, 25200, 62000, 12000, 13000, 35000, 35000, 14000, 24000, 12000, 14000, 31000, 40000, 22900, 12000,
    ...        14000, 1600, 12000, 80000, 90000, 126000, 1600, 100000, 8000, 71000, 40000, 42000, 40000, 120000, 35000,
    ...        1200, 4000, 32000, 8000, 14500, 65000, 15000, 3000, 2000, 23900, 1000, 22000, 18200, 8000, 30000, 23000,
    ...        30000, 27000, 70000, 40000, 18000, 3100, 57000, 25000, 32000, 10000, 4000, 49000, 93000, 35000, 49000,
    ...        40000, 5500, 30000, 25000, 5700, 6000, 30000, 42900, 8000, 5300, 90000, 85000, 15000, 17000, 5600,
    ...        11500, 52000, 1000, 42000, 2100, 50000, 1500, 40000, 28000, 5300, 149000, 3200, 12000, 83000, 45000,
    ...        31200, 25000, 72000, 70000, 7000, 23000, 40000, 40000, 28000, 10000, 48000, 20000, 60000, 19000, 25000,
    ...        39000, 68000, 2300, 23900, 5000, 16300, 80000, 45000, 12000, 9000, 1300, 35000, 35000, 47000, 32000,
    ...        18000, 20000, 20000, 23400, 48000, 8000, 5200, 33500, 22000, 22000, 52000, 104000, 28000, 13000, 12000,
    ...        15000, 53000, 27000, 50000, 13900, 23000, 28100, 23000, 12000, 55000, 83000, 31000, 33200, 45000, 3000,
    ...        18000, 11000, 41000, 36000, 33600, 38000, 45000, 53000, 24000, 3000, 37500, 7700, 4800, 29000, 6600,
    ...        12400, 20000, 2000, 1100, 55000, 13400, 10000, 6000, 6000, 16000, 19000, 8300, 52000, 58000, 27000,
    ...        25000, 80000, 10000, 22000, 18000, 21000, 8000, 15200, 15000, 5000, 50000, 89000, 7000, 65000, 58000,
    ...        42000, 55000, 40000, 14000, 36000, 30000, 7900, 6000, 1200, 10000, 54000, 12800, 35000, 34000, 40000,
    ...        45000, 9600, 3300, 39000, 22000, 40000, 68000, 24400, 1000, 10800, 8400, 50000, 22000, 20000, 20000,
    ...        1300, 9000, 14200, 32000, 65000, 18000, 18000, 3000, 16700, 1500, 1400, 15000, 55000, 42000, 70000,
    ...        35000, 21600, 5800, 35000, 5700, 1700, 40000, 40000, 45000, 25000, 13000, 6400, 11000, 4200, 30000,
    ...        32000, 120000, 10000, 19000, 12000, 13000, 37000, 40000, 38000, 60000, 3100, 16000, 18000, 130000,
    ...        5000, 5000, 35000, 1000, 14300, 100000, 20000, 33000, 8000, 9400, 87000, 2500, 12000, 12000, 33000,
    ...        16500, 25500, 7200, 2300, 3100, 2100, 3200, 45000, 40000, 3800, 30000, 12000, 62000, 45000, 46000,
    ...        50000, 40000, 13000, 50000, 23000, 4000, 40000, 25000, 16000, 3000, 80000, 27000, 68000, 3500,
    ...        1300, 10000, 46000, 5800, 24000, 12500, 50000, 48000, 29000, 19000, 26000, 30000, 10000, 10000,
    ...        20000, 43000, 105000, 55000, 5000, 65000, 68000, 38000, 47000, 48700, 6100, 55000, 30000, 5000, 3500,
    ...        23400, 11400, 7000, 1300, 80000, 65000, 45000, 19000, 3000, 17100, 22900, 31200, 35000, 3000, 5000,
    ...        1000, 36000, 4800, 60000, 9800, 30000, 85000, 18000, 24000, 60000, 30000, 2000, 39000, 12000, 10500,
    ...        60000, 36000, 10500, 3600, 1200, 28600, 48000, 20800, 5400, 9600, 30000, 30000, 20000, 6700, 30000,
    ...        3200, 42000, 37000, 5000, 18000, 20000, 14000, 12000, 18000, 3000, 13500, 35000, 38000, 30000, 36000,
    ...        66000, 45000, 32000, 46000, 80000, 27000, 4000, 21000, 7600, 16000, 10300, 27000, 19000, 14000, 19000,
    ...        3100, 20000, 2700, 27000, 7000, 13600, 75000, 35000, 36000, 25000, 6000, 36000, 50000, 46000, 3000,
    ...        37000, 40000, 30000, 48800, 19700, 16000, 14000, 12000, 25000, 25000, 28600, 17000, 31200, 57000,
    ...        23000, 23500, 46000, 18700, 26700, 9900, 16000, 3000, 52000, 51000, 14000, 14400, 27000, 26000, 60000,
    ...        25000, 6000, 20000, 3000, 69000, 24800, 12000, 3100, 18000, 20000, 267000, 28000, 9800, 18200, 80000,
    ...        6800, 21100, 20000, 68000, 20000, 45000, 8000, 40000, 31900, 28000, 24000, 2000, 32000, 11000, 20000,
    ...        5900, 16100, 23900, 40000, 37500, 11000, 55000, 37500, 60000, 23000, 9500, 34500, 4000, 9000, 11200,
    ...        35200, 30000, 18000, 21800, 19700, 16700, 12500, 11300, 4000, 39000, 32000, 14000, 65000, 50000,
    ...        2000, 30400, 22000, 1600, 56000, 40000, 85000, 9000, 10000, 19000, 5300, 5200, 43000, 60000, 50000,
    ...        38000, 267000, 15600, 1800, 17000, 45000, 31000, 5000, 8000, 43000, 103000, 45000, 8800, 26000, 47000,
    ...        40000, 8000]
    >>> # Udacity data shows that people earn $1.8K more for each year of age and start with a $21K deficit
    >>> regress(age, wage)   # doctest: +ELLIPSIS, +NORMALIZE_WHITESPACE
    array([22214.93338944, ...)

    >> # Gainseville, FL census data shows 14 more new homes are built each year, starting with 517 completed in 1991
    >> poly = regress([483, 576, 529, 551, 529, 551, 663, 639, 704, 675, 601, 621, 630, 778, 831, 610])
    """
    if y is None:
        y = x
        x = range(len(x))
    if not isinstance(x[0], (float, int, np.float64, np.float32)):
        x = [row[0] for row in x]
    A = np.vstack([np.array(x), np.ones(len(x))]).T
    fit = np.linalg.lstsq(A, y, rcond=None)
    # if fit is None:
    #     fit = [(1, 0), None, None, None]
    poly = fit[0][0], fit[0][-1]
    poly = regressionplot(x, y, poly)
    return poly


def regressionplot(x, y, poly=None):
    """
    Plot a 2-D linear regression (y = slope * x + offset) overlayed over the raw data samples
    """
    if not isinstance(x[0], (float, int, np.float64, np.float32)):
        x = [row[0] for row in x]
    y_regression = poly[0] * np.array(x) + poly[-1]
    try:
        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        plt.plot(x, y_regression, "r-", x, y, "o", markersize=5)
        plt.legend(["%+.2g * x + %.2g" % poly, "Samples"])
        ax.grid(True)
        plt.draw()
    except:
        logger.warn("No display available")
    return y_regression


class ColorMap(object):
    def __init__(self, mat, **kwargs):
        """Render a color map (image) of a matrix or sequence of Matrix objects

        A color map is like a contour map except the "height" or "value" of each matrix element
        is used to select a color from a continuous spectrum of colors (for heatmap white is max and red is medium)

        Arguments:
            mat (np.matrix or np.array or list of list): the matrix to be rendered as a color map

        """
        # try:
        #     self.colormaps = [ColorMap(m, cmap=cmap, pixelspervalue=pixelspervalue,
        #                       minvalue=minvalue, maxvalue=maxvalue) for m in mat]
        # except:
        #     pass
        #     # raise ValueError("Don't know how to display ColorMaps for a sequence of type {}".format(type(mat)))

        try:
            mat = np.array(mat.values)
        except AttributeError:
            try:
                mat = np.array(mat)
            except ValueError:
                pass

        if not isinstance(mat, np.ndarray):
            raise ValueError(
                "Don't know how to display a ColorMap for a matrix of type {}".format(
                    type(mat)
                )
            )

        kwargs["vmin"] = kwargs.get("vmin", np.amin(mat))
        kwargs["vmax"] = kwargs.get("vmax", np.amax(mat))
        kwargs["cmap"] = kwargs.get("cmap", "bone")  # 'hot', 'greens', 'blues'
        kwargs["linewidths"] = kwargs.get("linewidths", 0.25)
        kwargs["square"] = kwargs.get("square", True)
        sb.heatmap(mat, **kwargs)

    def show(self, block=False):
        """Display the last image drawn"""
        try:
            plt.show(block=block)
        except ValueError:
            plt.show()

    def save(self, filename):
        """save colormap to file"""
        plt.savefig(filename, fig=self.fig, facecolor="black", edgecolor="black")


def scatmat(
    df,
    category=None,
    colors="rgob",
    num_plots=4,
    num_topics=100,
    num_columns=4,
    show=False,
    block=False,
    data_path=DATA_PATH,
    save=False,
    verbose=1,
):
    """Scatter plot with colored markers depending on the discrete values in a "category" column

    FIXME: empty plots that dont go away, Plot and/save scatter matrix in groups of num_columns topics
    """
    if category is None:
        category = list(df.columns)[-1]
    if isinstance(category, (str, bytes, int)) and category in df.columns:
        category = df[category]
    else:
        category = pd.Series(category)

    suffix = "{}x{}".format(*list(df.shape))
    # suffix = compose_suffix(len(df), num_topics, save)
    # save = bool(save)
    for i in range(min(num_plots * num_columns, num_topics) / num_plots):
        scatter_matrix(
            df[df.columns[i * num_columns : (i + 1) * num_columns]],
            marker="+",
            c=[colors[int(x) % len(colors)] for x in category.values],
            figsize=(18, 12),
        )
    if save:
        name = (
            "scatmat_topics_{}-{}.jpg".format(i * num_columns, (i + 1) * num_columns)
            + suffix
        )
        plt.savefig(os.path.join(data_path, name + ".jpg"))
    if show:
        if block:
            plt.show()
        else:
            plt.show(block=False)


def point_cloud(df, columns=[0, 1, 2]):
    """3-D Point cloud for plotting things like mesh models of horses ;)"""
    df = df if isinstance(df, pd.DataFrame) else pd.DataFrame(df)
    if not all(c in df.columns for c in columns):
        columns = list(df.columns)[:3]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection="3d")  # noqa
    Axes3D.scatter(
        *[df[columns[i]] for i in range(3)], zdir="z", s=20, c=None, depthshade=True
    )
    return ax


def plotly_scatter(df):
    trace1 = go.Scatter(
        x=[0, 1, 2],
        y=[1, 1, 1],
        mode="lines+markers+text",
        name="Lines, Markers and Text",
        text=["Text A", "Text B", "Text C"],
        textposition="top",
    )
    trace2 = go.Scatter(
        x=[0, 1, 2],
        y=[2, 2, 2],
        mode="markers+text",
        name="Markers and Text",
        text=["Text D", "Text E", "Text F"],
        textposition="bottom",
    )
    trace3 = go.Scatter(
        x=[0, 1, 2],
        y=[3, 3, 3],
        mode="lines+text",
        name="Lines and Text",
        text=["Text G", "Text H", "Text I"],
        textposition="bottom",
    )
    data = [trace1, trace2, trace3]
    layout = go.Layout(showlegend=False)
    fig = go.Figure(data=data, layout=layout)
    plot_url = plt.plot(fig, filename="text-chart-basic")
    return plot_url


def join_spans(spans):
    spans = list(spans)
    joined_spans = [list(spans[0])]
    for i, (start, stop) in enumerate(spans[1:]):
        if start > joined_spans[i][1]:
            joined_spans += [[start, stop]]
        else:
            joined_spans[i - 1][1] = stop
    return joined_spans


def mask2spans(mask, index=None):
    """Convert a sequence of bools (True/False) into a list of the start and stop of the True "sections" or spans"""
    index = list(range(len(mask))) if index is None else index

    mask = pd.Series(mask)
    mask = mask.astype(int).fillna(0).diff().fillna(0)
    starts = list(index[mask > 0])
    stops = list(index[mask < 0])
    if len(stops) == len(starts) - 1:
        stops += [index.values[-1]]
    spans = join_spans(join_spans(zip(starts, stops)))
    return spans


def plotly_timeseries(df, mask=None, filename="plotly_timeseries.html"):
    spans = mask2spans(mask)
    offline.plot(
        df.iplot(
            asFigure=True,
            xTitle="Date-Time",
            yTitle="Monitor Value",
            kind="scatter",
            logy=True,
            vspan=spans,
        ),
        filename=filename,
    )
    return df
