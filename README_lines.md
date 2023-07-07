The module 'vizent_lines.py' contains the user accessible functions of the 
vizent library. These functions can be used to create a plot in up to four 
steps: preparing the plot area, adding glyphs, adding lines, and 
returning the completed plot. 

Functions:
    create_plot(glyphs=True, lines=True, show_legend=True, 
                show_axes=True, use_cartopy=False, use_image=False, 
                image_type=None, image_file=None, extent=None, 
                scale_x=None, scale_y=None)
    add_glyphs(ax, x_values, y_values, color_values, shape_values, 
               size_values, colormap="viridis", scale_diverges=None, 
               shape="sine", shape_pos="sine", shape_neg="square", 
               color_max=None, color_min=None, color_n=None, 
               color_spread=None, shape_max=None, shape_min=None, 
               shape_n=None, shape_spread=None, color_label="color", 
               shape_label="shape", legend_title="glyphs", scale_dp=2, 
               interval_type="closest", legend_marker_size="auto")
    add_lines(ax, x_starts, y_starts, x_ends, y_ends, color_values,
              freq_values, width_values, striped_length=1, 
              length_type="units", colormap="viridis", style="middle", 
              color_max=None, color_min=None, color_n=4, 
              color_spread=None, freq_max=None, freq_min=None, 
              freq_n=4, freq_spread=None, color_label="color", 
              shape_label="shape", legend_title="lines", scale_dp=2, 
              interval_type="closest", legend_marker_size="auto")
    return_figure(fig, return_type, file_name="vizent_plot_save")


Usage example:

    # This library requires several functions to be called sequentially.
    # First the plot area is prepared. This includes specifications
    # relating to the axes, plot area background and legends.

    axes=create_plot(use_image=True, image_file="england_map.png", 
                     extent=[0,6,0,6])

    # Next any glyphs and lines are added. This can be done in any 
    # order, glyphs will always be placed on top of lines.

    x_values = [1,4,2,3]
    y_values = [1,5,2,5]
    color_values = [1,2,3,4]
    shape_values = [1,2,3,4] 
    size_values = [30,30,30,30]

    add_glyphs(axes, x_values, y_values, color_values, shape_values, 
               size_values)

    x_starts = [2,1]
    y_starts = [2,1]
    x_ends = [4,3]
    y_ends = [5,5]
    color_values = [4,1]
    shape_values = [4,1] 
    width_values = [15,15]

    add_lines(axes, x_starts, y_starts, x_ends, y_ends, color_values, 
              shape_values, width_values)

    # Finally, the created figure is returned in the required manner.
              
    return_figure(axes, "display")


create_plot()

    Create the figure used to plot glyphs and/or lines. This function
    must be executed first, and the output is used as an input to all
    other functions.

    Parameters:
        glyphs (Boolean, default: True):
            Set True if glyphs are to be plotted.
        lines (Boolean, default: True):
            Set True if lines are to be plotted.
        show_legend (Boolean, default: True):
            If True, show legends for glyphs/lines as included. 
        show_axes (Boolean, default: True):
            If True, show axis labels.
        use_cartopy (Boolean, default: False):
            If True, use Cartopy to generate a map background. Must
            specify extent if used.
        use_image (Boolean, default: False):
            If True, use an image as a background. Must specify extent
            if used.
        image_type (str, optional):
            "newcastle": detailed 3D rendered image of Newcastle Upon
                Tyne (available for limited coordinates)
            "england": OpenStreetMap England map
            otherwise: the specified image file is used
        image_file (str, optional):
            Path to the image file to use as the background.
        extent (list of int, optional):
            Axis limits or extent of coordinates for Cartopy. A list of
            four values in the form: [xmin, xmax, ymin, ymax].  
        scale_x (int, optional):
            Width of plot window in inches.
        scale_y (int, optional):
            Height of plot window in inches.

    Returns:
        fig (matplotlib.figure):
            The matplotlib figure object which will contain the axes.
        ax1 (matplotlib.axes.SubplotBase):
            The matplotlib axes object for the main plot.
        ax2 (matplotlib.axes.SubplotBase):
            The matplotlib axes object used for the glyph legend.
        ax3 (matplotlib.axes.SubplotBase):
            The matplotlib axes object used for the line legend.
        asp (Numerical):
            The aspect ratio of the main plot area (necessary to ensure
            the legends display correctly when using image or map
            backgrounds).


add_glyphs()

    Add glyphs/nodes to the plot.

    Parameters:
        ax (tuple (matplotlib.figure, matplotlib.axes.SubplotBase, 
            matplotlib.axes.SubplotBase, matplotlib.axes.SubplotBase, 
            Numerical)): 
            This must be the tuple returned by create_plot().
        x_values (list of float): 
            The x coordinate of each glyph.
        y_values (list of float): 
            The y coordinate of each glyph.
        color_values (list of float): 
            The values to be represented by the color of each
            glyph.
        shape_values (list of float): 
            the list of values to be represented by the outer shape of
            each glyph.
        size_values (list of float): 
            the list of values in points for the diameter of each glyph.
        colormap (matplotlib.colors.Colormap, default: "viridis"): 
            the matplotlib colormap to be used.
        scale_diverges (boolean, optional):
            If True, diverging sets of glyphs are used for positive and
            negative values. If not specified, your scale will diverge
            if both positive and negative values are included for the
            shape variable.
        shape (str, default: "sine"):
            Glyph shape design to use for non-divergent scales.
                "sine"
                "saw"
                "reverse_saw"
                "square"
                "triangular"
                "concave"
                "star"
        shape_pos (str, default: "sine"):
            When using divergent scale, glyph shape design to use for 
            positive values. Options as for shape.
        shape_neg (str, default: "square"):
            When using divergent scale, glyph shape design to use for 
            negative values. Options as for shape.
        color_max (float), optional: 
            The maximum color value in the legend.
        color_min (float), optional: 
            The minimum color value in the legend.
        color_n (int), optional: 
            The number of color values to show in the legend.
        color_spread (float), optional: 
            Range of color values in key. Only used if not specifying
            both max and min.
        shape_max (float), optional: 
            The maximum shape value in the legend.
        shape_min (int), optional: 
            The minimum shape value in the legend.
        shape_n (int), optional: 
            The number of shape values to show in the legend. 
        shape_spread (float), optional:
            Range of shape values in key. Only used if not 
            specifying both max and min. 
        color_label (str, default: "color"):
            The heading for the color component of the legend.
        shape_label (str, default: "shape"):
            The heading for the shape component of the legend.
        legend_title (str, default: "glyphs"):
            The main title for the glyph legend.
        scale_dp (int, default: 2):
            The number of decimal places to round to for legend values.
        interval_type (str, default: "closest"):
            This defines how the shape of each glyph is determined:
                "closest": use the closest scale value.
                "limit": use the highest scale value that the glyph 
                    value is greater than or equal to (based on modulus
                    for negative values).
        legend_marker_size (str, default: "auto"):
            This controls the diameter of the legend glyph markers.
                "auto": diameter is calculated automatically to fit.
                "mean": use the mean diameter/size value of the plotted
                    glyphs.


add_lines()

    Add lines/edges to the plot.

    Parameters:
        ax (tuple (matplotlib.figure, matplotlib.axes.SubplotBase, 
            matplotlib.axes.SubplotBase, matplotlib.axes.SubplotBase, 
            Numerical)): 
            This must be the tuple returned by create_plot().
        x_starts (list of float): 
            The x coordinates of the origin points of each line.
        y_starts (list of float): 
            The y coordinates of the origin points of each line.
        x_ends(list of float): 
            The x coordinates of the end points of each line.
        y_ends(list of float): 
            The y coordinates of the end points of each line.
        color_values (list of float): 
            The values to be represented by the color of each
            line.
        freq_values (list of float): 
            the list of values to be represented by the central stripe
            frequency.
        width_values (list of float): 
            the list of values in points for the width of each line.
        striped_length (float, default: 1): 
            if using the style "set_length", the length of the central
            stripe. Units determined by length_type.
        length_type (str, default: "units"): 
            the units to be used for stripe length.
                "units": number of units on the axes.
                "pixels": number of pixels.
        colormap (matplotlib.colors.Colormap, default: "viridis"): 
            the matplotlib colormap to be used.
        style (str, default: "middle"): 
            the length and positioning style of the striped area.
                "middle": striped area centred on line/edge, length is
                    1/3 edge length.
                "ends": one striped area at each end of the line/edge,
                    each 1/4 edge length.
                "source": striped area at line source, 1/2 edge length.
                "destination": striped area at line destination, 1/2 
                    edge length.
                "set_length": striped area at line centre, length 
                    specified by user.
                "frequency": striped area at line centre, 1/3 edge 
                    length. Instead of a set number of stripes, this 
                    uses number of stripes per unit length, matched to
                    the legend.
        color_max (float), optional: 
            The maximum color value in the legend.
        color_min (float), optional: 
            The minimum color value in the legend.
        color_n (int), optional: 
            The number of color values to show in the legend.
        color_spread (float), optional: 
            Range of color values in key. Only used if not specifying
            both max and min.
        freq_max (float), optional: 
            The maximum frequency value in the legend.
        freq_min (int), optional: 
            The minimum frequency value in the legend.
        freq_n (int), optional: 
            The number of frequency values to show in the legend. 
        freq_spread (float), optional:
            Range of frequency values in key. Only used if not 
            specifying both max and min. 
        color_label (str, default: "color"):
            The heading for the color component of the legend.
        shape_label (str, default: "shape"):
            The heading for the shape/frequency component of the legend.
        legend_title (str, default: "lines"):
            The main title for the line legend.
        scale_dp (int, default: 2):
            The number of decimal places to round to for legend values.
        interval_type (str, default: "closest"):
            This defines how the frequency of each line is determined:
                "closest": use the closest scale value.
                "limit": use the highest scale value that the frequency 
                    value is greater than or equal to (based on modulus
                    for negative values).
        legend_marker_size (str, default: "auto"):
            This controls the width of the legend line markers.
                "auto": width is calculated automatically to fit.
                "mean": use the mean width value of the plotted lines.


return_figure()

    Return the created figure by your chosen method 

    Parameters:
        fig (tuple (matplotlib.figure, matplotlib.axes.SubplotBase, 
            matplotlib.axes.SubplotBase, matplotlib.axes.SubplotBase, 
            Numerical)): 
            This must be the tuple returned by create_plot().
        return_type (str): 
            The method for returning the created plot:
                "show": display the figure immediately
                "save": save figure without displaying
                "return": return axes for use with Matplotlib
        file_name (str, default: "vizent_plot_save"): 
            if return_type is "save", the file name for your saved file.
            This can be any format supported by Matplotlib. If no file 
            extension is included, .png is used by default.