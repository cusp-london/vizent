Gallery
=======

TO DO.

.. ## Examples

.. ### Create a basic scatterplot:

.. ```python
.. from vizent import vizent_plot

.. x_values = [1,2,3,4,5,6,7]
.. y_values = [6,3,7,1,4,2,5]
.. color_values = [0,3,6,9,12,15,18]
.. shape_values= [0,1,2,3,4,5,6]
.. size_values = [30,60,30,45,60,30,45]

.. vizent_plot(x_values, y_values, color_values, shape_values, size_values,
..             color_label="color", shape_label="shape",
..             title="A plot with a title", x_label="This is the x axis",
..             y_label="This is the y axis")
.. ```
.. ![scatterplot image](https://github.com/luyc12/vizent/raw/main/vizent/example_images/basic_example.png "scatterplot image")

.. ### Create a map using Cartopy:

.. ```python
.. from vizent import vizent_plot
.. import pandas as pd

.. data = pd.read_csv("englandRegions.csv")
.. x = data['long'].tolist()
.. y = data['lat'].tolist()
.. cases = data['dailyCases'].tolist()
.. accel = data['accel'].tolist()

.. size = [30]*len(x)
.. extent = [-6, 2, 49.9, 56]

.. vizent_plot(x, y, cases, accel, size, shape_label="Acceleration", 
..             color_label="Daily cases", use_cartopy=True, extent=extent, 
..             title='COVID19 daily case count and one day acceleration \n'
..             'English regions, 30th October 2020') 
.. ```
.. ![cartopy image](https://github.com/luyc12/vizent/raw/main/vizent/example_images/cartopy_example.png "cartopy image")

.. ### Create a map of england using an image background:

.. ```python
.. from vizent import vizent_plot
.. import pandas as pd

.. data = pd.read_csv("englandRegions.csv")
.. x = data['long'].tolist()
.. y = data['lat'].tolist()
.. cases = data['dailyCases'].tolist()
.. accel = data['accel'].tolist()

.. size = [30]*len(x)

.. vizent_plot(x, y, cases, accel, size, shape_label="Acceleration",
..             color_label="Daily cases", use_image=True,
..             image_type="england", title="COVID19 daily case count and one "
..             "day acceleration \n English regions, 30th October 2020")
.. ```

.. ![map image](https://github.com/luyc12/vizent/raw/main/vizent/example_images/england_example.png "map image")

.. Map © [OpenStreetMap](https://www.openstreetmap.org/) contributors

.. ### Use detailed background images of Newcastle Upon Tyne:

.. ```python
.. from vizent import vizent_plot
.. import pandas as pd

.. data = pd.read_csv("cleaned_temp_data.csv")
.. eastings = data['easting'].tolist()
.. northings = data['northing'].tolist()
.. average = data['Average of Value'].tolist()
.. variance = data['Variance of Value'].tolist()

.. size = [20]*len(eastings)

.. vizent_plot(eastings, northings, average, variance, size, 
..             "metoffice", shape_label="variance", 
..             color_label="temperature", use_image=True, 
..             image_type="newcastle", color_spread=20,
..             title="Newcastle Upon Tyne Temperature Data",
..             show_axes=False)
.. ```
.. ![newcastle image](https://github.com/luyc12/vizent/raw/main/vizent/example_images/newcastle_example.png "newcastle image")

.. ### Add your own MatPlotLib elements to the plot:

.. ```python
.. from vizent import vizent_plot
.. import numpy as np

.. # Let's take an example of a vizent plot and add to it

.. x = [0.05,0.35,0.75,0.9,1.35,1.55,1.85]
.. y = [(1 + np.sin(2 * np.pi * i)) for i in x]
.. color_values = [0,3,7,2,-1,10,6]
.. shape_values = [1,2,3,2.3,0,3,2]
.. size = [30,30,30,30,30,30,30]

.. # Assign the output of the function to fig, ax as shown

.. fig, ax = vizent_plot(x, y, color_values, shape_values, size, 
..                       colormap="rainbow", shape_label="shape", 
..                       color_label="color", return_axes=True, 
..                       title="An example of adding to your plot")

.. # Let's add a line to the plot

.. t = np.arange(0.0, 2.0, 0.01)
.. s = 1 + np.sin(2 * np.pi * t)

.. # Adjust zorder to control whether line is behind or in front of points, 
.. # background image etc. In this case, zorder=0 places the line behind the 
.. # points while zorder=1 would place it in front. If using a background
.. # image, zorder=0.5 places the line in front of the background image, 
.. # but behind the points.

.. ax.plot(t, s, zorder=0)

.. # Let's also add a text box with some additional information, such as the 
.. # data source

.. props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
.. text = "Source: Some Official Data Source"

.. # Text box position can be adjusted

.. ax.text(0.05, -0.1, text, transform=ax.transAxes, fontsize=14,
..         verticalalignment='top', bbox=props)

.. # And you can adjust the space around the subplot to ensure the text box
.. # is shown if it is outside of the axes

.. plt.subplots_adjust(bottom=0.15)

.. plt.show()
.. plt.close()  
.. ```

.. ![custom plot example](https://github.com/luyc12/vizent/raw/main/vizent/example_images/custom_example.png "custom plot example")
  