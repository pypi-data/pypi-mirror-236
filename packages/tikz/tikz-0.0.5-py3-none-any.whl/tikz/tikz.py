"""
--------------------------------------------------------------------------------
Copyright 2022 David Woodburn

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
--------------------------------------------------------------------------------
"""

__author__ = "David Woodburn"
__license__ = "MIT"
__date__ = "2023-10-21"
__maintainer__ = "David Woodburn"
__email__ = "david.woodburn@icloud.com"
__status__ = "Development"

import os
import warnings
import math
import numpy as np
# The math library is also used because for scalar values it is about 5 to 10
# times faster than the NumPy library.

# TODO Add scatter plots.
# TODO Add NaN immunity.
# TODO Add cropping of data points outside the box.

TIKZ_WIDTH = 8.636                  # (cm) 3.4 in
TIKZ_FONTSIZE = 9                   # (pt)
TIKZ_FONTSIZENAME = "normalsize"    # name of normal font size
TIKZ_COLOR = -1                     # hex value
TIKZ_OPACITY = 1.0                  # [0, 1]
TIKZ_THIN = 0.4                     # (pt)
TIKZ_THICK = 0.8                    # (pt)
TIKZ_SOLID = '--'                   # solid line style
TIKZ_DASHED = '- '                  # dashed line style
TIKZ_DOTTED = '..'                  # dotted line style
TIKZ_DASH_DOTTED = '-.'             # dash-dotted line style
TIKZ_TOL = 1e-45                    # tolerance
TIKZ_PT_PER_CM = 28.45274           # points per centimeter
TIKZ_GOLDEN_RATIO = 1.61803398875   # golden ratio
TIKZ_PAD_RATIO = 0.1                # padding ratio of figure width
TIKZ_TICK_SIZE = 0.1                # size of tick marks (cm)
TIKZ_LEGEND_RATIO = 0.03            # (cm/cm) of figure width
TIKZ_TICK_OFFSET_RATIO = 0.25       # fraction of tick length to offset label
TIKZ_R_DIGIT = 0.5                  # digit width as ratio of font size
TIKZ_R_SIGN = 0.75                  # sign width as ratio of font size
TIKZ_R_DECIMAL = 0.28               # decimal width as ratio of font size
TIKZ_R_TIMES = 0.89                 # times width as ratio of font size
TIKZ_R_POWER = 0.85                 # scaling factor for widths in powers


class Path:
    def __init__(self, x, y, color=TIKZ_COLOR, opacity=TIKZ_OPACITY,
            thickness=TIKZ_THICK, dash=TIKZ_SOLID, mark=None, label=None,
            fmt=None):
        self.x = x                  # array of x-axis values
        self.y = y                  # array of y-axis values
        self.color = color          # scalar color integer (0xRRGGBB)
        self.opacity = opacity      # scalar opacity float [0, 1]
        self.thickness = thickness  # line thickness (pt) (0 means fill)
        self.dash = dash            # line style ("solid", "dashed", ...)
        self.mark = mark            # marker string ("*", "o", "square", ...)
        self.label = label          # path string label
        self.fmt = fmt              # additional format string


class Layout:
    def __init__(self):
        self.width = 0.0            # width of figure (cm)
        self.height = 0.0           # height of figure (cm)
        self.font_size = 0.0        # font size (pt)
        self.font_size_name = ""    # font size name ("tiny", "large", ...)
        self.x_min = 0.0            # x-axis min (units)
        self.x_max = 0.0            # x-axis max (units)
        self.y_min = 0.0            # y-axis min (units)
        self.y_max = 0.0            # y-axis max (units)
        self.x_scale = 0.0          # x-axis scaling factor (cm/units)
        self.y_scale = 0.0          # y-axis scaling factor (cm/units)
        self.W_box = 0.0            # width of plotting box (cm)
        self.H_box = 0.0            # height of plotting box (cm)
        self.L_text = 0.0           # height of text (cm)
        self.X_axes = 0.0           # x position of axis origin (cm)
        self.Y_axes = 0.0           # y position of axis origin (cm)
        self.L_margin = 0.0         # left tick label margin (cm)
        self.R_margin = 0.0         # right tick label margin (cm)
        self.B_margin = 0.0         # bottom tick label margin (cm)
        self.T_margin = 0.0         # top tick label margin (cm)
        self.L_x_tick = 0.0         # estimated left x-axis tick width
        self.R_x_tick = 0.0         # estimated right x-axis tick width
        self.H_x_tick = 0.0         # estimated x-axis tick height
        self.W_y_tick = 0.0         # estimated y-axis tick width
        self.H_y_tick = 0.0         # estimated y-axis tick height
        self.x_tick_fmt = ""        # format string of x-axis tick labels
        self.y_tick_fmt = ""        # format string of y-axis tick labels
        self.L_tick_shift = 0.0     # the axis tick label shift magnitude (cm)
        self.x_tick_shift = 0.0     # x-axis tick label vertical shift (cm)
        self.y_tick_shift = 0.0     # y-axis tick label horizontal shift (cm)
        self.legend_cols = 0        # number of legend columns
        self.legend_rows = 0        # number of legend rows
        self.H_legend_row = 0.0     # height of a legend row (cm)
        self.H_legend = 0.0         # height of the entire legend (cm)
        self.invisibles = False     # flag to show invisible boundaries


class Fig:
    # Class-wide attributes
    skip = False                    # flag to skip all subsequent plotting
    silent = True                   # flag to silence pdflatex output
    directory = None                # directory for all figures

    def __init__(self, filename='fig', width=None, height=None, paths=None,
            xmin=None, xmax=None, ymin=None, ymax=None, xpad=False, ypad=True,
            xlog=False, ylog=False, equal=False, fontsize=TIKZ_FONTSIZE,
            xlabel=None, ylabel=None, xaxis=True, yaxis=True, xgrid=True,
            ygrid=True, xsubgrid=True, ysubgrid=True, xtick=True,
            ytick=True, ticksize=TIKZ_TICK_SIZE, xout=False, yout=False,
            rowmajor=False, columns=None, simp=True, preamble=None,
            standalone=True, silent=None, skip=None, directory=None):
        # Assign the settings.
        self.filename = filename    # string of file without extension
        self.width = width          # width of pdf image in centimeters
        self.height = height        # height of pdf image in centimeters
        self.xmin = xmin            # x-axis minimum
        self.xmax = xmax            # x-axis maximum
        self.ymin = ymin            # y-axis minimum
        self.ymax = ymax            # y-axis maximum
        self.xpad = xpad            # use padding on x axis
        self.ypad = ypad            # use padding on y axis
        self.xlog = xlog            # flag to use log scaling on x axis
        self.ylog = ylog            # flag to use log scaling on y axis
        self.equal = equal          # flag to use equal scaling
        self.fontsize = fontsize    # font size in points
        self.xlabel = xlabel        # x-axis label
        self.ylabel = ylabel        # y-axis label
        self.xaxis = xaxis          # flag to show x axis
        self.yaxis = yaxis          # flag to show y axis
        self.xgrid = xgrid          # flag to show x grid
        self.ygrid = ygrid          # flag to show y grid
        self.xsubgrid = xsubgrid    # flag to show x sub-grid
        self.ysubgrid = ysubgrid    # flag to show y sub-grid
        self.xtick = xtick          # flag to show x ticks
        self.ytick = ytick          # flag to show y ticks
        self.ticksize = ticksize    # size of tick marks (cm)
        self.xout = xout            # flag to put x-axis ticks outside
        self.yout = yout            # flag to put y-axis ticks outside
        self.rowmajor = rowmajor    # flag to layout legend row major
        self.columns = columns      # number of legend columns
        self.simp = simp            # flag to simplify curve
        self.preamble = preamble    # added string of LaTeX code in preamble
        self.standalone = standalone# flag to create standalone LaTeX file

        # Initialize the paths list.
        if paths is None:
            self.paths = []         # list of path objects
        else:
            if isinstance(paths, tuple):
                self.paths = list(paths)
            elif isinstance(paths, Path):
                self.paths = [paths]

        # Assign class-wide attributes.
        if skip == False or skip == True:
            Fig.skip = skip
        if silent == False or silent == True:
            Fig.silent = silent
        if directory is not None:
            Fig.directory = directory

    def path(self, x, y, color=TIKZ_COLOR, opacity=TIKZ_OPACITY,
            thickness=TIKZ_THICK, dash=TIKZ_SOLID, mark=None, label=None,
            fmt=None):
        # Make Path object.
        p = Path(x=x, y=y, color=color, opacity=opacity, thickness=thickness,
                dash=dash, mark=mark, label=label, fmt=fmt)

        # Link Path object to this Fig object.
        self.paths.append(p)

        # Return the Path object.
        return p

    def render(self, paths=None):
        # Skip all the plotting code if the flag is set.
        if Fig.skip:
            return

        # Append additional paths to the list of paths.
        if paths is not None:
            # Ensure paths is a list.
            if isinstance(paths, tuple):
                paths = list(paths)
            elif isinstance(paths, Path):
                paths = [paths]
            # Append to the list.
            self.paths = self.paths + paths

        # --------------------
        # Plan out the figure.
        # --------------------

        # Initialize the layout.
        lay = Layout()

        # Get the viewing region. Find the mins and maxs and adjust for required
        # padding.
        get_view(self, self.paths, lay)

        # Get the size of the box and margins.
        get_layout(self, self.paths, lay)

        # Get the scaling factors and conditionally apply equal scaling. Equal
        # scaling will alter the mins and maxs.
        get_scaling(self, lay)

        # Get grid line locations (in linear scaling).
        if self.xlog:
            x_grids, x_sub_grids = grid_logarithmic(lay.x_min, lay.x_max)
        else:
            x_grids, x_sub_grids = grid_linear(lay.x_min, lay.x_max, lay.W_box,
                    max(lay.L_x_tick, lay.R_x_tick, lay.W_box/10))
        if self.ylog:
            y_grids, y_sub_grids = grid_logarithmic(lay.y_min, lay.y_max)
        else:
            y_grids, y_sub_grids = grid_linear(lay.y_min, lay.y_max, lay.H_box,
                    2*lay.font_size/TIKZ_PT_PER_CM)

        # Determine where the x and y axes would be.
        if self.yout or self.xlog:
            lay.X_axes = 0.0
        else:
            lay.X_axes = to_scale(0, lay.x_min, lay.x_scale, self.xlog)
            lay.X_axes = max(0, min(lay.X_axes, lay.W_box))
        if self.xout or self.ylog:
            lay.Y_axes = 0.0
        else:
            lay.Y_axes = to_scale(0, lay.y_min, lay.y_scale, self.ylog)
            lay.Y_axes = max(0, min(lay.Y_axes, lay.H_box))

        # Determine what the tick format would be.
        if self.xout or lay.Y_axes > lay.L_text:
            lay.x_tick_fmt = "below"
            lay.x_tick_shift = -lay.L_tick_shift
        else:
            lay.x_tick_fmt = "above"
            lay.x_tick_shift = lay.L_tick_shift
        if not self.xout:
            lay.x_tick_fmt += ", draw opacity=0.8"
        if self.yout or lay.X_axes > lay.W_box/2:
            lay.y_tick_fmt = "left"
            lay.y_tick_shift = -lay.L_tick_shift
        else:
            lay.y_tick_fmt = "right"
            lay.y_tick_shift = lay.L_tick_shift
        if not self.yout:
            lay.y_tick_fmt += ", draw opacity=0.8"

        # -----------------------
        # Write the data to file.
        # -----------------------

        # Open the output file.
        if Fig.directory is None:
            fid = open(self.filename + ".tex", "w")
        else:
            fid = open(Fig.directory + "/" + self.filename + ".tex", "w")

        # Open the standalone TikZ script.
        if self.standalone:
            tikz_open(fid, self.preamble)
        elif self.preamble is not None:
            print("Because this plot is not standalone, the additional "
                    + "preamble will not be used.")

        # Define the font size.
        tikz_textstyle(fid, lay.font_size_name)

        # Define the colors.
        tikz_colors(fid, self.paths)

        # Reserve the full figure space: the box and margins.
        tikz_reserve(fid, lay)

        # Draw the sub-grids and grids.
        if self.xsubgrid:
            grids = to_scale(x_sub_grids, lay.x_min, lay.x_scale, self.xlog)
            tikz_xgrid(fid, grids, lay.H_box, sub=True)
        if self.ysubgrid:
            grids = to_scale(y_sub_grids, lay.y_min, lay.y_scale, self.ylog)
            tikz_ygrid(fid, grids, lay.W_box, sub=True)
        if self.xgrid:
            grids = to_scale(x_grids, lay.x_min, lay.x_scale, self.xlog)
            tikz_xgrid(fid, grids, lay.H_box)
        if self.ygrid:
            grids = to_scale(y_grids, lay.y_min, lay.y_scale, self.ylog)
            tikz_ygrid(fid, grids, lay.W_box)

        # Start a clip environment to contain the drawing.
        tikz_begin_clip(fid, lay.W_box, lay.H_box)

        # Set path style to rounded.
        tikz_rounded(fid)

        # Draw the paths.
        points = 0
        for j in range(len(self.paths)):
            # Get the data set.
            X = to_scale(self.paths[j].x, lay.x_min, lay.x_scale, self.xlog)
            Y = to_scale(self.paths[j].y, lay.y_min, lay.y_scale, self.ylog)
            opacity = self.paths[j].opacity
            thickness = self.paths[j].thickness
            dash = self.paths[j].dash
            mark = self.paths[j].mark

            # Build the format specifications.
            fmt = f"C{j}" # pre-defined color
            if opacity != TIKZ_OPACITY:
                fmt += f", opacity={opacity:0.3g}"
            if thickness > 0:
                if thickness != TIKZ_THIN:
                    fmt += f", line width={thickness:0.3g}pt"
                if dash != TIKZ_SOLID:
                    if dash == TIKZ_DASHED:
                        fmt += ", dashed"
                    elif dash == TIKZ_DOTTED:
                        fmt += ", dotted"
                    elif dash == TIKZ_DASH_DOTTED:
                        fmt += ", dashdotted"
                if mark is not None:
                    fmt += f", mark={mark}"

            # Plot the path.
            if thickness > 0:
                points += tikz_draw_set(fid, X, Y, j,
                        self.simp, lay.W_box, lay.H_box, thickness, fmt)
            else:
                points += tikz_fill_set(fid, X, Y, j,
                        self.simp, lay.W_box, lay.H_box, thickness, fmt)
        # FIXME Do something with `points`.

        # End the clip environment.
        tikz_end_clip(fid)

        # Draw the axes.
        tikz_comment(fid, "Draw axes.")
        if self.xaxis:
            tikz_line(fid, -self.ticksize/2, lay.Y_axes,
                    lay.W_box + self.ticksize, lay.Y_axes, "->")
        if self.yaxis:
            tikz_line(fid, lay.X_axes, -self.ticksize/2,
                    lay.X_axes, lay.H_box + self.ticksize, "->")

        # Write the x-axis ticks and labels.
        if self.xtick and self.xaxis: # Ticks without an axis look weird.
            # Comment.
            tikz_comment(fid, "Draw x-axis ticks and labels.")

            # Scale the grid lines to paper dimensions.
            X = to_scale(x_grids, lay.x_min, lay.x_scale, self.xlog)

            # Determine the form for the tick labels and their precision.
            format_func, precision = get_num_format(self.xlog, x_grids)

            for n in range(len(X)):
                # Get the label string and its width.
                txt, w_txt = format_func(x_grids[n], precision, lay.font_size)
                W_txt = w_txt/TIKZ_PT_PER_CM

                # Skip the tick labels too close to the axis.
                if not self.xout:
                    dist_to_axis = math.fabs(X[n] - lay.X_axes)
                    if self.yaxis and dist_to_axis < W_txt/2:
                        continue
                    dist_to_edge = min(math.fabs(X[n]),
                            math.fabs(lay.W_box - X[n]))
                    if dist_to_edge < W_txt/2:
                        continue

                # Draw the tick line.
                tikz_line(fid, X[n], lay.Y_axes - self.ticksize/2,
                        X[n], lay.Y_axes + self.ticksize/2)

                # Wrap the text string in math mode.
                txt = "$" + txt + "$"

                # Add a white contour.
                if not self.xout:
                    txt = f"\\contour{{white}}{{{txt}}}"

                # Write the tick label.
                tikz_text(fid, X[n], lay.Y_axes + lay.x_tick_shift,
                        txt + "\\strut", lay.x_tick_fmt)

        # Write the y-axis ticks and labels.
        if self.ytick and self.yaxis: # Ticks without an axis look weird.
            # Comment.
            tikz_comment(fid, "Draw y-axis ticks and labels.")

            # Scale the grid lines to paper dimensions.
            Y = to_scale(y_grids, lay.y_min, lay.y_scale, self.ylog)

            # Determine the form for the tick labels and their precision.
            format_func, precision = get_num_format(self.ylog, y_grids)

            tol_to_axis = lay.font_size/(2*TIKZ_PT_PER_CM)
            for n in range(len(Y)):
                # Get the label string.
                txt, _ = format_func(y_grids[n], precision, lay.font_size)

                # Skip the tick on the axis.
                if not self.yout:
                    dist_to_axis = math.fabs(Y[n] - lay.Y_axes)
                    if self.xaxis and dist_to_axis < tol_to_axis:
                        continue
                    dist_to_edge = min(math.fabs(Y[n]),
                            math.fabs(lay.H_box - Y[n]))
                    if dist_to_edge < tol_to_axis:
                        continue

                # Draw the tick line.
                tikz_line(fid, lay.X_axes - self.ticksize/2, Y[n],
                        lay.X_axes + self.ticksize/2, Y[n])

                # Wrap the text string in math mode.
                txt = "$" + txt + "$"

                # Add a white contour.
                if not self.yout:
                    txt = f"\\contour{{white}}{{{txt}}}"

                # Write the tick text.
                tikz_text(fid, lay.X_axes + lay.y_tick_shift, Y[n],
                        txt + "\\strut", lay.y_tick_fmt)

        # Write the axis labels (inside the figure space).
        if self.xlabel is not None:
            tikz_comment(fid, "Write x-axis label.")
            tikz_text(fid, lay.W_box/2, -lay.B_margin,
                    self.xlabel + "\\strut", "above")
        if self.ylabel is not None:
            tikz_comment(fid, "Write y-axis label.")
            tikz_text(fid, -lay.L_margin, lay.H_box/2,
                    self.ylabel + "\\strut", "below, rotate=90")

        # Write the legend labels.
        if lay.legend_cols > 0:
            # Comment.
            tikz_comment(fid, "Write legend.")

            row = 0
            col = 0
            for j in range(len(self.paths)):
                # Skip unlabled paths.
                label = self.paths[j].label
                if label is None:
                    continue

                # Draw the legend line.
                x = col*(lay.W_box/lay.legend_cols)
                y = -lay.B_margin - lay.H_legend \
                        + (lay.H_legend_row)*(lay.legend_rows - 0.5 - row)
                tikz_line(fid, x, y, x + lay.width*TIKZ_LEGEND_RATIO, y,
                        fmt=f"line width=3pt, C{j}")
                tikz_text(fid, x + lay.width*TIKZ_LEGEND_RATIO
                        + TIKZ_TICK_SIZE, y, label + "\\strut", fmt="right")

                # Increment the column number.
                if self.rowmajor:
                    row += 1
                    if row >= lay.legend_rows:
                        col += 1
                        row = 0
                else:
                    col += 1
                    if col >= lay.legend_cols:
                        row += 1
                        col = 0

        # Close the standalone TikZ script.
        if self.standalone:
            tikz_close(fid)

        # Close the output file.
        fid.close()

        # -----------------
        # Compile the file.
        # -----------------

        # Compile the LaTeX file.
        if self.standalone:
            cmd = 'pdflatex'
            if Fig.silent:
                cmd = cmd + ' --interaction=batchmode'
            if Fig.directory is None:
                os.system(f'{cmd} {self.filename}.tex')
                os.system(f'rm {self.filename}.aux')
                os.system(f'rm {self.filename}.log')
            else:
                pwd = os.getcwd()
                cmd = f'{cmd} -output-directory="{pwd}/{Fig.directory}"'
                os.system(f'{cmd} "{Fig.directory}/{self.filename}.tex"')
                os.system(f'rm {Fig.directory}/{self.filename}.aux')
                os.system(f'rm {Fig.directory}/{self.filename}.log')


def get_view(fig, paths, lay):
    # Initialize the minimums and maximums.
    lay.x_min = math.inf
    lay.x_max = -math.inf
    lay.y_min = math.inf
    lay.y_max = -math.inf

    # Check each path.
    for j in range(len(paths)):
        # Parse the x and y fields.
        x = paths[j].x
        y = paths[j].y

        # Convert x and y to ndarrays.
        if isinstance(x, (int, float)):
            x = np.array([x], dtype=float)
            paths[j].x = x
        elif isinstance(x, (list, tuple)):
            x = np.array(x)
            paths[j].x = x
        if isinstance(y, (int, float)):
            y = np.array([y], dtype=float)
            paths[j].y = y
        elif isinstance(y, (list, tuple)):
            y = np.array(y)
            paths[j].y = y

        # Check the dimensions.
        if x.shape[-1] != y.shape[-1]:
            raise ValueError("x and y do not have the same lengths "
                    + f"in their last dimensions for path {j}.")

        # Get extrema of this path, ignoring NaNs.
        x_min = np.nanmin(x)
        x_max = np.nanmax(x)
        y_min = np.nanmin(y)
        y_max = np.nanmax(y)

        # Enlarge minimums and maximums.
        if x_min < lay.x_min:
            lay.x_min = x_min
        if x_max > lay.x_max:
            lay.x_max = x_max
        if y_min < lay.y_min:
            lay.y_min = y_min
        if y_max > lay.y_max:
            lay.y_max = y_max

    # Adjust for log scaling.
    if fig.xlog and lay.x_min <= 0.0:
        print("Negative values cannot be plotted in a log-scale x axis.")
        lay.x_min = TIKZ_TOL
    if fig.ylog and lay.y_min <= 0.0:
        print("Negative values cannot be plotted in a log-scale y axis.")
        lay.y_min = TIKZ_TOL

    # Adjust for requested limits.
    if fig.xmin is not None:
        lay.x_min = fig.xmin
    if fig.xmax is not None:
        lay.x_max = fig.xmax
    if fig.ymin is not None:
        lay.y_min = fig.ymin
    if fig.ymax is not None:
        lay.y_max = fig.ymax

    # Ensure there is something to plot.
    if lay.x_max < lay.x_min or lay.y_max < lay.y_min:
        raise ValueError("Invalid range of values! "
                + f"x: ({lay.x_min},{lay.x_max}), "
                + f"y: ({lay.y_min}, {lay.y_max})")

    # Add padding if requested or needed.
    if lay.x_max == lay.x_min:
        # Add a very small padding.
        lay.x_min -= TIKZ_TOL
        lay.x_max += TIKZ_TOL
    elif fig.xpad:
        # Convert to logarithmic scaling.
        if fig.xlog:
            lay.x_min = math.log10(lay.x_min)
            lay.x_max = math.log10(lay.x_max)

        # Add padding
        w = lay.x_max - lay.x_min
        lay.x_min -= w*TIKZ_PAD_RATIO/2
        lay.x_max += w*TIKZ_PAD_RATIO/2

        # Convert back to linear scaling.
        if fig.xlog:
            lay.x_min = 10.0**lay.x_min
            lay.x_max = 10.0**lay.x_max

    if lay.y_max == lay.y_min:
        # Add a very small padding.
        lay.y_min -= TIKZ_TOL
        lay.y_max += TIKZ_TOL
    elif fig.ypad:
        # Convert to logarithmic scaling.
        if fig.ylog:
            lay.y_min = math.log10(lay.y_min)
            lay.y_max = math.log10(lay.y_max)

        # Add padding
        h = lay.y_max - lay.y_min
        lay.y_min -= h*TIKZ_PAD_RATIO/2
        lay.y_max += h*TIKZ_PAD_RATIO/2

        # Convert back to linear scaling.
        if fig.ylog:
            lay.y_min = 10.0**lay.y_min
            lay.y_max = 10.0**lay.y_max


def get_base_exp(x):
    if x == 0:
        base_exp = 0
    else:
        base_exp = int(math.floor(math.log10(math.fabs(x)) + 1e-3))
    return base_exp


def get_num_format(is_log, grids):
    # Determine the form for the tick labels and their precision.
    if is_log:
        precision = 0
        format_func = lstr
    else:
        # The decision to use scientific notation (3.14x10^1) versus
        # floating-point notation (31.4) depends on the extrema grid
        # values being larger than 999 or smaller than 0.01. The
        # 'precision' is of the whole number, not just the mantissa,
        # and depends on the grid step size.
        e_min = get_base_exp(grids[0])
        e_max = get_base_exp(grids[-1])
        precision = -get_base_exp(grids[1] - grids[0])
        if math.fabs(e_min) > 3 or math.fabs(e_max) > 3:
            format_func = gstr
        else:
            if precision < 0: # integer step size
                format_func = dstr
            else: # decimal values required for step size
                format_func = fstr
    return format_func, precision


def get_layout(fig, paths, lay):
    # Set the figure dimensions.
    lay.width = fig.width
    lay.height = fig.height
    if lay.width is None and lay.height is None:
        lay.width = TIKZ_WIDTH
        lay.height = TIKZ_WIDTH/TIKZ_GOLDEN_RATIO
    elif lay.width is None:
        lay.width = lay.height*TIKZ_GOLDEN_RATIO
    elif lay.height is None:
        lay.height = lay.width/TIKZ_GOLDEN_RATIO

    # Force fontsize to be a regular value.
    font_sizes = np.array([5, 7, 8, 9, 10, 12, 14.4, 17.28, 20.74, 24.88])
    font_size_names = ["tiny", "scriptsize", "footnotesize", "small",
            "normalsize", "large", "Large", "LARGE", "huge", "Huge"]
    n = (np.abs(font_sizes - fig.fontsize)).argmin()
    if fig.fontsize != font_sizes[n]:
        print("The requested font size is adjusted to a standard value: "
                + f"{font_size[n]} pt.")
    lay.font_size = font_sizes[n]
    lay.font_size_name = font_size_names[n]

    # Define text-based lengths.
    lay.L_text = 1.3*lay.font_size/TIKZ_PT_PER_CM # (cm)

    # Get the tick shift.
    lay.L_tick_shift = fig.ticksize*(0.5 + TIKZ_TICK_OFFSET_RATIO)

    # Get impact of axis labels on the margins.
    H_x_label = lay.L_text*(fig.xlabel is not None) + fig.ticksize/4
    W_y_label = lay.L_text*(fig.ylabel is not None) + fig.ticksize/4

    # -----------------------------
    # Get dimensions of the legend.
    # -----------------------------

    # Count the number of labeled paths and the required number of rows and
    # columns for the legend, and define the height of a legend row.
    labeled = 0
    legend_buff = 0
    lay.legend_cols = 0
    lay.legend_rows = 0
    for j in range(len(paths)):
        if paths[j].label is not None:
            labeled += 1
    if labeled > 0:
        if fig.columns is None:
            lay.legend_cols = round(lay.width/2.54)
            if lay.legend_cols + 1 >= labeled:
                lay.legend_cols = labeled
        else:
            lay.legend_cols = fig.columns
        lay.legend_rows = int(math.ceil(labeled/lay.legend_cols))
        if fig.xlabel:
            legend_buff = 0.5*lay.L_text
    lay.H_legend_row = 1.5*lay.L_text

    # Get the height of the legend.
    lay.H_legend = legend_buff + lay.legend_rows*lay.H_legend_row

    # --------------------------
    # Estimate the grid numbers.
    # --------------------------

    # Copy the layout limits and size.
    x_min = lay.x_min
    x_max = lay.x_max
    y_min = lay.y_min
    y_max = lay.y_max

    # Get the tick-label dimensions, assuming the worst-case label widths.
    # This width is based on a number of the form "-m.mm x 10^(-eee)".
    if fig.xtick and fig.xaxis and fig.xout:
        if fig.xlog:
            W_x_tick = 2.5*lay.font_size/TIKZ_PT_PER_CM
        else:
            W_x_tick = 6.0*lay.font_size/TIKZ_PT_PER_CM
    else:
        W_x_tick = 0.0
    if fig.ytick and fig.yaxis and fig.yout:
        if fig.ylog:
            W_y_tick = 2.5*lay.font_size/TIKZ_PT_PER_CM
        else:
            W_y_tick = 6.0*lay.font_size/TIKZ_PT_PER_CM
    else:
        W_y_tick = 0.0
    H_y_tick = lay.L_text if fig.ytick and fig.yaxis else 0.0
    H_x_tick = lay.L_text + lay.L_tick_shift if fig.xout else 0.0

    # Get the dimensions of the margins around the box.
    L_margin = max(W_y_label + W_y_tick + fig.ticksize/2, W_x_tick/2)
    R_margin = max(fig.ticksize, W_x_tick/2)
    B_margin = max(H_x_label + H_x_tick + fig.ticksize/2, H_y_tick/2)
    T_margin = max(fig.ticksize, H_y_tick/2)

    # Initialize the box size.
    W_box = lay.width - L_margin - R_margin
    H_box = lay.height - B_margin - T_margin - lay.H_legend

    # Adjust the limits for equal axis scaling. For equal axis scaling to affect
    # anything, xlog must equal ylog.
    if fig.equal and fig.xlog == fig.ylog:
        # Convert to logarithmic scaling.
        if fig.xlog and fig.ylog:
            x_min = math.log10(x_min)
            x_max = math.log10(x_max)
            y_min = math.log10(y_min)
            y_max = math.log10(y_max)

        # Get the data scaling factors. This is needed later regardless of
        # whether equal-axis scaling is required.
        x_scale = W_box/(x_max - x_min)
        y_scale = H_box/(y_max - y_min)

        # Increase the span of the axis with a larger scale (zoom out).
        if x_scale < y_scale:
            y_span = H_box/x_scale
            y_mid = (y_max + y_min)*0.5
            y_min = y_mid - y_span*0.5
            y_max = y_mid + y_span*0.5
        elif y_scale < x_scale:
            x_span = W_box/y_scale
            x_mid = (x_max + x_min)*0.5
            x_min = x_mid - x_span*0.5
            x_max = x_mid + x_span*0.5

        # Convert back to linear scaling.
        if fig.xlog and fig.ylog:
            x_min = 10.0**x_min
            x_max = 10.0**x_max
            y_min = 10.0**y_min
            y_max = 10.0**y_max

    # Get the estimated grid values so we can estimate the tick label widths.
    if fig.xlog:
        x_grids, _ = grid_logarithmic(x_min, x_max)
    else:
        x_grids, _ = grid_linear(x_min, x_max, W_box,
                5*lay.font_size/TIKZ_PT_PER_CM)
    if fig.ylog:
        y_grids, _ = grid_logarithmic(y_min, y_max)
    else:
        y_grids, _ = grid_linear(y_min, y_max, H_box,
                2*lay.font_size/TIKZ_PT_PER_CM)

    # -------------------------------------
    # Get the dimensions of the components.
    # -------------------------------------

    # Get x-axis, tick-label margins.
    lay.L_x_tick = 0.0
    lay.R_x_tick = 0.0
    lay.H_x_tick = 0.0
    if fig.xtick and fig.xaxis: # Ticks without an axis look weird.
        # Height of tick label.
        lay.H_x_tick = lay.L_text + fig.ticksize/4

        # Determine the form for the tick labels and their precision.
        format_func, precision = get_num_format(fig.xlog, x_grids)

        # Get the left and right tick label widths in points.
        _, w_left = format_func(x_grids[0], precision, lay.font_size)
        _, w_right = format_func(x_grids[-1], precision, lay.font_size)
        lay.L_x_tick = w_left/TIKZ_PT_PER_CM + fig.ticksize
        lay.R_x_tick = w_right/TIKZ_PT_PER_CM + fig.ticksize

    # Get y-axis, tick-label margins.
    lay.W_y_tick = 0.0
    lay.H_y_tick = 0.0
    if fig.ytick and fig.yaxis: # Ticks without an axis look weird.
        # Determine the form for the tick labels and their precision.
        format_func, precision = get_num_format(fig.ylog, y_grids)

        # Get the left and right tick label widths in points.
        _, w_bot = format_func(y_grids[0], precision, lay.font_size)
        _, w_top = format_func(y_grids[-1], precision, lay.font_size)
        lay.W_y_tick = max(w_bot, w_top)/TIKZ_PT_PER_CM + fig.ticksize

        # Top and bottom of tick labels
        lay.H_y_tick = lay.L_text

    # --------------------------------------------------------
    # Get the margins, size of the box, and positions of text.
    # --------------------------------------------------------

    # Get the dimensions of the margins around the box.
    lay.L_margin = max(W_y_label + lay.W_y_tick*fig.yout + fig.ticksize/2,
            W_y_label + lay.L_x_tick/2*fig.xout)
    lay.R_margin = max(fig.ticksize, lay.R_x_tick/2*fig.xout)
    lay.B_margin = max(H_x_label + lay.H_x_tick*fig.xout + fig.ticksize/2,
            lay.H_y_tick/2*fig.yout)
    lay.T_margin = max(fig.ticksize, lay.H_y_tick/2*fig.yout)

    # Get the height of the legend.
    lay.H_legend = legend_buff + lay.legend_rows*lay.H_legend_row

    # Initialize the box size.
    lay.W_box = lay.width - lay.L_margin - lay.R_margin
    lay.H_box = lay.height - lay.B_margin - lay.T_margin - lay.H_legend


def get_scaling(fig, lay):
    # Convert to logarithmic scaling.
    if fig.xlog:
        lay.x_min = math.log10(lay.x_min)
        lay.x_max = math.log10(lay.x_max)
    if fig.ylog:
        lay.y_min = math.log10(lay.y_min)
        lay.y_max = math.log10(lay.y_max)

    # Get the data scaling factors. This is needed later regardless of
    # whether equal-axis scaling is required.
    lay.x_scale = lay.W_box/(lay.x_max - lay.x_min)
    lay.y_scale = lay.H_box/(lay.y_max - lay.y_min)

    # Increase the span of the axis with a larger scale (zoom out).
    if fig.equal:
        if fig.xlog == fig.ylog:
            if lay.x_scale < lay.y_scale:
                lay.y_scale = lay.x_scale
                y_span = lay.H_box/lay.y_scale
                y_mid = (lay.y_max + lay.y_min)*0.5
                lay.y_min = y_mid - y_span*0.5
                lay.y_max = y_mid + y_span*0.5
            elif lay.y_scale < lay.x_scale:
                lay.x_scale = lay.y_scale
                x_span = lay.W_box/lay.x_scale
                x_mid = (lay.x_max + lay.x_min)*0.5
                lay.x_min = x_mid - x_span*0.5
                lay.x_max = x_mid + x_span*0.5
        else:
            print("Semi-log scaling does not make sense with equal axes. "
                    + "The equal-axis setting will be ignored.")

    # Convert back to linear scaling.
    if fig.xlog:
        lay.x_min = 10.0**lay.x_min
        lay.x_max = 10.0**lay.x_max
    if fig.ylog:
        lay.y_min = 10.0**lay.y_min
        lay.y_max = 10.0**lay.y_max

def dstr(x, p=0, f=10):
    """
    Given a floating-point number `x`, the precision `p`, and  the font size `f`
    in points, return a LaTeX string `s` of the number as an integer and the
    estimated width `w` in points. 'p' is unused.
    """
    x = int(round(x))
    s = "%d" % x
    if x >= 0:
        w = (len(s)*TIKZ_R_DIGIT)*f
    else:
        w = (TIKZ_R_SIGN + (len(s) - 1)*TIKZ_R_DIGIT)*f
    return s, w


def fstr(x, p=4, f=10):
    """
    Given a floating-point number `x`, the precision `p`, and  the font size `f`
    in points, return a LaTeX string `s` of the number as a floating-point value
    and the estimated width `w` in points.
    """
    s = "%.*f" % (p, x)
    if x > 0:
        w = (TIKZ_R_DECIMAL + (len(s) - 1)*TIKZ_R_DIGIT)*f
    else:
        w = (TIKZ_R_SIGN + TIKZ_R_DECIMAL + (len(s) - 2)*TIKZ_R_DIGIT)*f
    return s, w


def gstr(x, p=6, f=10):
    """
    Given a floating-point number `x`, the precision `p`, and  the font size `f`
    in points, return a LaTeX string `s` of the number in the format `m x 10^e`
    and the estimated width `w` in points. 'p' is the precision of the whole
    number, not of the mantissa alone.
    """

    # Simplify for zero.
    if x == 0:
        return "0", (TIKZ_R_DIGIT*f)

    # Get the base exponent.
    e = get_base_exp(x)

    # Get the mantissa string and width.
    mt = x*10.0**(-e) # mantissa value
    if p > -e: # More precision than the units place is required.
        sm, wm = fstr(mt, p + e, f)
    else: # An integer will satisfy the precision requirement.
        sm, wm = dstr(mt, 0, f)

    # Get the times string and width.
    st = "\\!\\times\\!10^{{"
    wt = (TIKZ_R_TIMES + 2*TIKZ_R_DIGIT)*f

    # Get the exponent string and width.
    se = "%d" % (e)
    if e > 0:
        we = (TIKZ_R_POWER*(len(se)*TIKZ_R_DIGIT))*f
    else:
        we = (TIKZ_R_POWER*(TIKZ_R_SIGN + (len(se) - 1)*TIKZ_R_DIGIT))*f

    # Assemble the full string and width.
    s = sm + st + se + "}}"
    w = wm + wt + we

    return s, w


def lstr(x, p=6, f=10):
    """
    Given a floating-point number `x`, the precision `p`, and  the font size `f`
    in points, return a LaTeX string `s` of the number and the estimated width
    `w` in points. `p` is unused.
    """
    e = get_base_exp(x)
    se = "%d" % (e)
    s = "10^{{" + se + "}}"
    if e > 0:
        we = (len(se)*TIKZ_R_DIGIT)*f
    else:
        we = (TIKZ_R_SIGN + (len(se) - 1)*TIKZ_R_DIGIT)*f
    w = (2*TIKZ_R_DIGIT)*f + TIKZ_R_POWER*(we)
    return s, w


def grid_linear(u_min, u_max, L_box, L_tick):
    # Get the normalized span. Every span will map to [1,10).
    u_span = u_max - u_min # guaranteed to be positive
    base = 10.0**get_base_exp(u_span)
    u_span_normalized = u_span/base # [1, 10)

    # Choose a nice step and sub-step based on the normalized span.
    u_cnt_preferred = math.floor(L_box/L_tick)
    step_sizes = \
            np.array([5.0, 2.5, 2.0, 1.0, 0.5, 0.25, 0.2,  0.1,  0.05, 0.02])
    sub_step_sizes = \
            np.array([1.0, 0.5, 0.5, 0.2, 0.1, 0.05, 0.05, 0.02, 0.01, 0.005])
    grid_cnts = np.round(u_span_normalized/step_sizes)
    n_min = np.argmax(grid_cnts >= 2) # first count to satisfy
    n_pref = np.argmax(grid_cnts > u_cnt_preferred) - 1
    n = max(n_pref, n_min)
    step_size = step_sizes[n]*base
    sub_step_size = sub_step_sizes[n]*base

    # Get the nice extrema. The major grid lines may go to the very edge.
    # The minor grid lines may not.
    grid_min = u_min if math.fmod(u_min, step_size) == 0 else \
            (math.floor(u_min/step_size) + 1)*step_size
    grid_max = u_max if math.fmod(u_max, step_size) == 0 else \
            (math.ceil(u_max/step_size) - 1)*step_size
    sub_grid_min = (math.floor(u_min/sub_step_size) + 1)*sub_step_size
    sub_grid_max =  (math.ceil(u_max/sub_step_size) - 1)*sub_step_size

    # Build the grids arrays.
    N_grids = round((grid_max - grid_min)/step_size) + 1
    N_sub_grids = round((sub_grid_max - sub_grid_min)/sub_step_size) + 1
    grids = np.linspace(grid_min, grid_max, N_grids)
    sub_grids = np.linspace(sub_grid_min, sub_grid_max, N_sub_grids)

    # Remove the major grid lines from the minor set.
    sub_grids = np.array([u for u in sub_grids if u not in grids])

    return grids, sub_grids


def grid_logarithmic(u_min, u_max):
    # Convert to log scale.
    e_min = math.log10(u_min)
    e_max = math.log10(u_max)

    # Build the grids array.
    e_min_base = int(math.floor(e_min))
    e_max_base = int(math.floor(e_max))
    if e_min_base == e_min:
        e_grids = np.arange(e_min_base, e_max_base + 1)
    else:
        e_grids = np.arange(e_min_base + 1, e_max_base + 1)
    grids = 10.0**e_grids

    # Get the normalized limits of the sub-grids.
    u_min_mod = math.ceil(10.0**math.fmod(e_min, 1)) # [1, 10]
    if u_min_mod == 1:
        u_min_mod = 2
    u_max_mod = math.floor(10.0**math.fmod(e_max, 1)) # [0, 9]

    # Build the first, middle, and end parts of the sub_grids.
    e_sub_grids = np.log10(np.arange(u_min_mod, 10)) + e_min_base
    for e_base in range(e_min_base + 1, e_max_base):
        e_set = np.log10(np.arange(2, 10)) + e_base
        e_sub_grids = np.append(e_sub_grids, e_set)
    if u_max_mod > 1:
        e_set = np.log10(np.arange(2, u_max_mod + 1)) + e_max_base
        e_sub_grids = np.append(e_sub_grids, e_set)
    sub_grids = 10.0**e_sub_grids

    return grids, sub_grids


def to_scale(u, u_min, u_scale, u_log):
    if u_log:
        U = np.log10(u/u_min)*u_scale
    else:
        U = (u - u_min)*u_scale
    return U


def simp_chunks(u, v, chunks):
    """
    Simplify the u and v data path by uniform index chunking along the u axis.
    """

    # Get the number of points.
    K = len(u)

    # Get the number of chunks.
    if K <= chunks:
        return u, v

    # Get the array of chunking indices: [0, K].
    nn = np.round(np.arange(chunks + 1)/chunks*K).astype(int)

    # Allocate memory for the new path.
    uc = np.zeros(2*chunks)
    vc = np.zeros(2*chunks)

    # For each chunk, store the min and max.
    for n_chunk in range(chunks):
        na = nn[n_chunk]
        nb = nn[n_chunk + 1]
        n_min = np.argmin(v[na:nb]) + na
        n_max = np.argmax(v[na:nb]) + na
        if n_min < n_max:
            uc[2*n_chunk] = u[n_min]
            vc[2*n_chunk] = v[n_min]
            uc[2*n_chunk + 1] = u[n_max]
            vc[2*n_chunk + 1] = v[n_max]
        else:
            uc[2*n_chunk] = u[n_max]
            vc[2*n_chunk] = v[n_max]
            uc[2*n_chunk + 1] = u[n_min]
            vc[2*n_chunk + 1] = v[n_min]

    return uc, vc


def simp_map(u, v, tol):
    """
    Simplify the u and v data path by replacement with a line that breaks when
    points are too far from the line. This algorithm works by setting a range of
    angles of tangent lines to a circle about the last pinned point. All future
    points must be between those tangent lines. This algorithm achieves a
    similar result to the Ramer-Douglas-Peucker algorithm, but with far fewer
    calculations.
    """

    # Get the circle radius.
    h = tol/2

    # Initialize the pin index and array.
    N = len(u)
    n_pin = 0
    nn = np.zeros(N, dtype=np.int32)
    nn[0] = 0
    m = 1 # index into nn

    # Clear the bounding angles, A and B. A is also used as a state. It is None
    # when we are searching for a new point outside the radius of the last
    # pinned point.
    A = None # lower angle
    B = None # upper angle

    # Clear the maximum distance down the tube.
    d_max = 0.0
    n_max = 0

    # For each point,
    n = 1
    while (n < N):
        # Get the displacement from the pin.
        du = u[n] - u[n_pin]
        dv = v[n] - v[n_pin]
        d = math.sqrt(du**2 + dv**2)

        # Skip all points within radius h of p.
        if d <= h:
            n += 1
            continue

        # Initialize angles.
        if A is None:
            C = math.atan2(dv, du)
            dC = math.pi - math.acos(h/d)
            A = (C - dC + math.pi) % math.tau - math.pi
            B = (C + dC + math.pi) % math.tau - math.pi
            d_max = d
            n_max = n
            n += 1
            continue

        # Get the circle-edge points.
        uA = h*math.cos(A) + u[n_pin]
        vA = h*math.sin(A) + v[n_pin]
        uB = h*math.cos(B) + u[n_pin]
        vB = h*math.sin(B) + v[n_pin]

        # Get the angles relative to the circle-edge points.
        CA = math.atan2(v[n] - vA, u[n] - uA)
        CB = math.atan2(v[n] - vB, u[n] - uB)

        # Get the angle margins to the edge lines.
        dA = (CA - (A + math.pi/2) + math.pi) % math.tau - math.pi
        dB = ((B - math.pi/2) - CB + math.pi) % math.tau - math.pi

        # Check if this point is out of bounds.
        if dA < 0 or dB < 0:
            # Pin previous point.
            n_pin = n_max
            nn[m] = n_pin
            m += 1
            # Clear the bounding angles.
            A = None
            B = None
            d_max = 0.0
            continue # without incrementing n

        # Remember this point if it is furthest down the tube.
        if d > d_max:
            d_max = d
            n_max = n

        # Get new potential a and b bounding angles.
        C = math.atan2(dv, du)
        dC = math.pi - math.acos(h/d)
        a = (C - dC + math.pi) % math.tau - math.pi
        b = (C + dC + math.pi) % math.tau - math.pi

        # Get the margins between the old and new bounding angles.
        dA = (a - A + math.pi) % math.tau - math.pi
        dB = (B - b + math.pi) % math.tau - math.pi

        # Check if the new bounds are more restrictive.
        if dA > 0: # a more so than A
            A = a
        if dB > 0: # b more so than B
            B = b
        n += 1

    # Add end point to list and crop.
    if m >= N:
        m = N - 1
    nn[m] = N - 1
    nn = nn[:m + 1]

    # Return just the pinned points.
    return u[nn], v[nn]


def hex_to_rgb(color):
    """
    Convert 24-bit color values to red, green, blue values on the scale of 0
    to 255.  This function can take an ndarray of colors.
    """

    B = np.bitwise_and(color, 0xFF)
    RG = np.right_shift(color, 8)
    G = np.bitwise_and(RG, 0xFF)
    R = np.right_shift(RG, 8)
    return R, G, B


def mix_colors(R0, G0, B0, R1, G1, B1, w):
    """
    Mix colors `C0` and `C1` using weight `w`.  A weight of 0 makes the
    output equal to `C0`, and a weight of 1 makes the output equal to `C1`.
    The colors are treated as 6-character hexadecimal values.
    """

    R = int(math.sqrt(w*R1**2 + (1 - w)*R0**2))
    G = int(math.sqrt(w*G1**2 + (1 - w)*G0**2))
    B = int(math.sqrt(w*B1**2 + (1 - w)*B0**2))
    return R, G, B


def tikz_open(fid, preamble=None):
    fid.write("% Preamble")
    fid.write("\n\\documentclass{standalone}")
    fid.write("\n\\usepackage{tikz}")
    fid.write("\n\\usepackage[pdftex, outline]{contour}")
    fid.write("\n\\usetikzlibrary{plotmarks}")
    fid.write("\n\\contourlength{0.8pt}")
    fid.write("\n\\newcommand{\\ul}[1] % vectors")
    fid.write("\n    {{}\\mkern1mu\\underline")
    fid.write("{\\mkern-1mu#1\\mkern-1mu}\\mkern1mu}")
    fid.write("\n\\newcommand{\\micro}")
    fid.write("\n    {{\\fontencoding{U}\\fontfamily{eur}")
    fid.write("\\selectfont\\char22}}")
    fid.write("\n\\DeclareSymbolFont{euler}{U}{eur}{m}{n}")
    fid.write("\n\\DeclareMathSymbol{\\PI}{\\mathord}{euler}{25}")
    if preamble is not None:
        fid.write("\n%s" % preamble)
    fid.write("\n% Document contents")
    fid.write("\n\\begin{document}")
    fid.write("\n\\begin{tikzpicture}")


def tikz_textstyle(fid, fsname):
    txt = "\n% Set the style of all text."
    txt += "\n\\tikzset{every node/.style={inner sep=0pt"
    if fsname != TIKZ_FONTSIZENAME:
        txt += ", font=\\" + fsname
    txt += "}}"
    fid.write(txt)


def tikz_colors(fid, paths):
    color_map = [0x0000ff, 0x0080ff, 0x00d1d1, 0x0fb400, 0xa9cb00,
            0xffbf00, 0xff8000, 0xff0000, 0xff00ff, 0x8000ff]
    J = len(paths)
    fid.write("\n% Define the plot colors.")
    for j in range(J):
        if paths[j].color < 0:
            if J < 5:
                R, G, B = hex_to_rgb(color_map[3*j])
            elif J == 5:
                R, G, B = hex_to_rgb(color_map[2*j])
            elif J <= 10:
                R, G, B = hex_to_rgb(color_map[j])
            else:
                r = (10 - 1.0)*(j/(J - 1.0))
                n = int(r)
                w = r - n
                C0 = color_map[n]
                C1 = color_map[n + 1]
                R0, G0, B0 = hex_to_rgb(C0)
                R1, G1, B1 = hex_to_rgb(C1)
                R, G, B = mix_colors(R0, G0, B0, R1, G1, B1, w)
        else:
            C = int(paths[j].color)
            R = ((C & 0xff0000) >> 16)
            G = ((C & 0x00ff00) >> 8)
            B = (C & 0x0000ff)
        fid.write(f"\n\definecolor{{C{j}}}{{RGB}}{{{R},{G},{B}}}")


def tikz_reserve(fid, lay):
    # Calculate dimensions.
    xa = lay.W_box + lay.R_margin - lay.width
    ya = lay.H_box + lay.T_margin - lay.height
    xb = lay.W_box + lay.R_margin
    yb = lay.H_box + lay.T_margin

    # Comment.
    fid.write("\n% Reserve the full figure space.")

    # Draw the paths.
    if lay.invisibles:
        # Outer figure box
        fid.write(f"\n\\draw[ultra thin, red] ({xa:0.3f},{ya:0.3f}) rectangle "
                + f"({xb:0.3f},{yb:0.3f});")
        # Margins
        xc = -lay.L_margin
        yc = -lay.B_margin
        fid.write(f"\n\draw[ultra thin, red] ({xc:0.3f},{yc:0.3f}) rectangle "
                + f"({xb:0.3f},{yb:0.3f});")
        # Legend
        yd = -lay.H_legend - lay.B_margin
        for row in range(lay.legend_rows):
            yd += lay.H_legend_row
            fid.write(f"\n\\draw[ultra thin, red] "
                    + f"({xa:0.3f},{yd:0.3f}) -- ({xb:0.3f},{yd:0.3f});")
    else:
        fid.write(f"\n\\path ({xa:0.3f},{ya:0.3f}) rectangle "
                + f"({xb:0.3f},{yb:0.3f});")


def tikz_begin_clip(fid, W_box, H_box):
    fid.write("\n% Draw the plot contents, clipping it to the box area.")
    fid.write("\n\\begin{scope}")
    fid.write(f"\n\\clip (0,0) rectangle ({W_box:0.3f},{H_box:0.3f});")


def tikz_end_clip(fid):
    fid.write("\n\\end{scope}")


def tikz_comment(fid, txt):
    fid.write(f"\n% {txt}")


def tikz_xgrid(fid, X_list, Y_max, sub=False):
    if sub:
        fid.write("\n% Draw x-axis minor grid.")
        fid.write("\n\\draw[very thin, lightgray!20]")
    else:
        fid.write("\n% Draw x-axis major grid.")
        fid.write("\n\\draw[very thin, lightgray!60]")
    for n, X in enumerate(X_list):
        if n % 2 == 0:
            fid.write("\n    ")
        else:
            fid.write("  ")
        fid.write(f"({X:0.3f},0) -- ({X:0.3f},{Y_max:0.3f})")
    fid.write(";")


def tikz_ygrid(fid, Y_list, X_max, sub=False):
    if sub:
        fid.write("\n% Draw y-axis minor grid.")
        fid.write("\n\\draw[very thin, lightgray!20]")
    else:
        fid.write("\n% Draw y-axis major grid.")
        fid.write("\n\\draw[very thin, lightgray!60]")
    for n, Y in enumerate(Y_list):
        if n % 2 == 0:
            fid.write("\n    ")
        else:
            fid.write("  ")
        fid.write(f"(0,{Y:0.3f}) -- ({X_max:0.3f},{Y:0.3f})")
    fid.write(";")


def tikz_rounded(fid):
    fid.write("\n% Round every subsequent path until the end of the clip.")
    fid.write("\n\\tikzset{every path/.style="
            + "{line cap=round, line join=round}}")


def tikz_coordinates(fid, X, Y, simp, W_box, H_box, thickness, fmt=None):
    # Simplify the data path.
    if simp:
        Xs, Ys = simp_map(X, Y, 0.001)
        tol = max(thickness, TIKZ_THIN)/TIKZ_PT_PER_CM
        x_chunks = round(W_box/(tol/2))
        y_chunks = round(H_box/(tol/2))
        if len(Xs) > 2*max(x_chunks, y_chunks):
            dX = np.diff(X)
            dY = np.diff(Y)
            if np.all(dX >= 0) or np.all(dX <= 0): # X is monotonic
                Xs, Ys = simp_chunks(X, Y, x_chunks)
            elif np.all(dY >= 0) or np.all(dY <= 0): # Y is monotonic
                Ys, Xs = simp_chunks(Y, X, y_chunks)
        X = Xs
        Y = Ys

    # Write the path.
    points = 0
    is_start = True
    for n in range(len(X)):
        if math.isnan(X[n]) or math.isnan(Y[n]):
            is_start = True
            continue
        if points % 4 == 0:
            fid.write("\n   ")
        if is_start:
            fid.write(f" ({X[n]:0.3f},{Y[n]:0.3f})")
            is_start = False
        else:
            fid.write(f" ({X[n]:0.3f},{Y[n]:0.3f})")
        points += 1
    return points


def tikz_draw_set(fid, X, Y, j, simp, W_box, H_box, thickness, fmt=None):
    # Comment on the path.
    fid.write(f"\n% Draw path {j}")

    # Begin the drawing command.
    fid.write("\n\\draw")
    if fmt is not None:
        fid.write(f"[{fmt}]")
    fid.write(" plot coordinates {")

    # Draw each row as a separate path.
    points = 0
    if X.ndim == 1 and Y.ndim == 1:
        points = tikz_coordinates(fid, X, Y,
                simp, W_box, H_box, thickness, fmt)
    elif X.ndim == 1 and Y.ndim == 2:
        for row in range(Y.shape[0]):
            points += tikz_coordinates(fid, X, Y[row, :],
                simp, W_box, H_box, thickness, fmt)
    elif X.ndim == 2 and Y.ndim == 1:
        for row in range(X.shape[0]):
            points += tikz_coordinates(fid, X[row, :], Y,
                simp, W_box, H_box, thickness, fmt)
    elif X.ndim == 2 and Y.ndim == 2:
        for row in range(X.shape[0]):
            points += tikz_coordinates(fid, X[row, :], Y[row, :],
                simp, W_box, H_box, thickness, fmt)
    else:
        print("x and y for path {j} are not 1 or 2D arrays.")

    # End the drawing command.
    fid.write("};")

    return points


def tikz_fill_set(fid, X, Y, j, simp, W_box, H_box, thickness, fmt=None):
    # Comment on the path.
    fid.write(f"\n% Fill path {j}")

    # Begin the drawing command.
    fid.write("\n\\fill")
    if fmt is not None:
        fid.write(f"[{fmt}]")
    fid.write(" plot coordinates {")

    # Draw each row as a separate path.
    points = 0
    if X.ndim == 1 and Y.ndim == 1:
        points = tikz_coordinates(fid, X, Y,
                simp, W_box, H_box, thickness, fmt)
    elif X.ndim == 1 and Y.ndim == 2:
        for row in range(1, Y.shape[0], 2):
            x = np.concatenate((X, X[::-1]))
            y = np.concatenate((Y[row - 1, :], Y[row, ::-1]))
            points += tikz_coordinates(fid, x, y,
                    simp, W_box, H_box, thickness, fmt)
        if row < Y.shape[0] - 1:
            points += tikz_coordinates(fid, X, Y[row + 1, :],
                    simp, W_box, H_box, thickness, fmt)
    elif X.ndim == 2 and Y.ndim == 1:
        for row in range(1, X.shape[0], 2):
            x = np.concatenate((X[row - 1, :], X[row, ::-1]))
            y = np.concatenate((Y, Y[::-1]))
            points += tikz_coordinates(fid, x, y,
                    simp, W_box, H_box, thickness, fmt)
        if row < X.shape[0] - 1:
            points += tikz_coordinates(fid, X[row + 1, :], Y,
                    simp, W_box, H_box, thickness, fmt)
    elif X.ndim == 2 and Y.ndim == 2:
        for row in range(1, X.shape[0], 2):
            x = np.concatenate((X[row - 1, :], X[row, ::-1]))
            y = np.concatenate((Y[row - 1, :], Y[row, ::-1]))
            points += tikz_coordinates(fid, x, y,
                    simp, W_box, H_box, thickness, fmt)
        if row < X.shape[0] - 1:
            points += tikz_coordinates(fid, X[row + 1, :], Y[row + 1, :],
                    simp, W_box, H_box, thickness, fmt)
    else:
        print("x and y for path {j} are not 1 or 2D arrays.")

    # End the drawing command.
    fid.write("};")

    return points


def tikz_line(fid, xa, ya, xb, yb, fmt=None):
    # Draw the line.
    fid.write("\n\\draw")
    if fmt is not None:
        fid.write(f"[{fmt}]")
    fid.write(f" ({xa:0.3f},{ya:0.3f}) -- ({xb:0.3f},{yb:0.3f});")


def tikz_text(fid, x, y, txt, fmt=None):
    if fmt is None:
        fid.write(f"\n\\node at ({x:0.3f},{y:0.3f})\n    {{{txt}}};")
    else:
        fid.write(f"\n\\node[{fmt}] at ({x:0.3f},{y:0.3f})\n    {{{txt}}};")


def tikz_close(fid):
    fid.write("\n\\end{tikzpicture}")
    fid.write("\n\\end{document}")
