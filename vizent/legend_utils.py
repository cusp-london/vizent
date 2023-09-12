import matplotlib.pyplot as plt
import numpy as np

def add_colorbar(ax, color_mapping, label_size):


    # Get position of axis in figure coords
    ax_bbox = ax.get_position()

    
    # Coordinates of ax are: 
    # ax_bbox.x0
    # ax_bbox.x1
    # ax_bbox.y0
    # ax_bbox.y1


    # if the axis data lim is small, then the colorbar should not be plotted
    if np.abs(ax_bbox.x1 - ax_bbox.x0) < 10e-5:
        return

    # Define axes in which to place colorbar
    cax_x0 = 1. / 8.
    cax_y0 = 0.05
    cax = ax.inset_axes([cax_x0, cax_y0, 0.08, 0.78])
    cbar = plt.colorbar(color_mapping, cax=cax)
    cbar.ax.tick_params(labelsize=label_size)



def format_legend(ax, lhs_values, rhs_values, scale_y, title, lhs_heading, rhs_heading, label_fontsize, lines=False):

    # Fixed positions and limits
    x_positions = [0.75, 3.25]
    y_title = 9.5
    y_subtitle = 8.9
    ymax = 10
    ymax_glyphs = 8.75
    ymin = 0

    # Calculated positions
    lhs_y_positions = [(x-0.5) * (ymax_glyphs/(len(lhs_values))) 
                          for x in range(1, len(lhs_values) + 1)]
    rhs_y_positions = [(x-0.5) * (ymax_glyphs/len(rhs_values)) 
                         for x in range(1, len(rhs_values) + 1)]

    # Axis formatting
    ax.set_xlim(0, 5)
    ax.set_ylim(ymin, ymax)
    ax.axes.xaxis.set_visible(False)
    ax.axes.yaxis.set_visible(False)

    if lines==False:
        # Size calculations for glyphs
        n_glyphs = max(len(lhs_values), len(rhs_values))
        y_size = (1 / (3*n_glyphs)) * scale_y
        x_size = scale_y / 12
        calculated_size = (min(x_size, y_size) / 0.014) # 0.014 is the size in inches of an object one point wide. I.e. inches per point.
        color_length=None
        shape_length=None
    else:
        # Size calculations for lines and text
        color_length = ((ymax_glyphs-ymin) / len(lhs_values))*0.7
        shape_length = ((ymax_glyphs-ymin) / len(rhs_values))*0.7
        y_size = (1 / (2*ymax)) * scale_y
        x_size = scale_y / 12
        
        calculated_size = 0.5 * (min(x_size, y_size)/0.014)

    if label_fontsize is None:
        title_length = max([len(i) for i in title.split('\n')])
        title_size = min((1.5 * (scale_y/3) / (len(str(title_length))*0.014)), 25)

        heading_length = max([len(i) for i in lhs_heading.split('\n')] + \
                             [len(i) for i in rhs_heading.split('\n')])
        heading_size = 0.55 * ((scale_y/3) / (heading_length*0.014))

    else:
        heading_size = label_fontsize
        title_size = label_fontsize + 2

    # Add legend title
    ax.annotate(title, ((x_positions[0]+x_positions[1]+1) / 2, y_title), 
                ha='center', va='center', size=title_size)

    # Add color title
    ax.annotate(lhs_heading, (x_positions[0] + 0.5, y_subtitle), ha='center', 
                va='center', size=heading_size)

    # Add shape title
    ax.annotate(rhs_heading, (x_positions[1] + 0.5, y_subtitle), ha='center', 
                va='center', size=heading_size)
    
    return x_positions, lhs_y_positions, rhs_y_positions, calculated_size, \
        color_length, shape_length