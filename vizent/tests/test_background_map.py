# background_map.py functions
# ===========================
# get_basemap()

import warnings
import matplotlib.pyplot as plt
import uuid
import os
from matplotlib.testing.compare import compare_images
from matplotlib import gridspec
import matplotlib

def test_get_basemap():

    try: 
        matplotlib.use('qtagg')
    except ImportError:
        warnings.warn("The default images for this test have been created "
                      "using the qtagg backend for matplotlib. This backend is"
                      " unavailable in your current python distribution. This "
                      " test may therefore fail")


    try: 
        from cartopy.mpl.geoaxes import GeoAxes
        from vizent.background_map import get_basemap

        gs = gridspec.GridSpec(1, 3, width_ratios=[1,0,0])
        extent = [-8, 2, 50, 60]
        ax = get_basemap(gs, extent, show_axes=False)
        
        tmp_file_map = 'tmp_basemap_test.png' #% uuid.uuid1()
        # save to a temporary file
        plt.savefig(os.path.join('tests',tmp_file_map))

        assert type(ax) == GeoAxes
        expected = os.path.join('tests', 'default_images', 'UK_basemap.png')
        actual = os.path.join('tests', tmp_file_map)
        
        assert compare_images(expected=expected, \
                              actual=actual, \
                              tol=0) is None
        
        os.remove(os.path.join('tests', tmp_file_map))
        
    
    except ImportError:
        warnings.warn("Pytest unable to import cartopy."
                      " Basemap functionality not tested")

