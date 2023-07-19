from .vizent_plot import add_glyphs, add_lines, return_figure, vizent_plot, \
    create_plot

# This line determines what is imported when running from vizent import *
# It's used by sphinx when building the API reference docs to determine which 
# functions to include
__all__ = ['create_plot', 'add_glyphs', 'add_lines', 'return_figure', 
           'vizent_plot']