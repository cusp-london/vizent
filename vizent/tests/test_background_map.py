# background_map.py functions
# ===========================
# get_basemap()

import warnings
import matplotlib.pyplot as plt
import os
from matplotlib.testing.compare import compare_images
from matplotlib import gridspec
import matplotlib

def test_get_basemap():

    try: 
        matplotlib.use('agg')
    except ImportError:
        warnings.warn("The default images for this test have been created "
                      "using the agg backend for matplotlib. This backend is"
                      " unavailable in your current python distribution. This "
                      " test may therefore fail")


    try: 
        from cartopy.mpl.geoaxes import GeoAxes
        
    except ImportError:
        warnings.warn("Pytest unable to import cartopy."
                      " Basemap functionality not tested")
    else:
        from vizent.background_map import get_basemap
        gs = gridspec.GridSpec(1, 3, width_ratios=[1,0,0])
        extent = [-8, 2, 50, 60]
        ax = get_basemap(gs, extent, show_axes=False, projection=None)
        
        tmp_file_map = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    'tmp_basemap_test.png')
        # save to a temporary file
        plt.savefig(tmp_file_map)

        assert type(ax) == GeoAxes
        expected = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                    'default_images', 'UK_basemap.png')
        actual = tmp_file_map
        
        assert compare_images(expected=expected, \
                                actual=actual, \
                                tol=12) is None
        
        os.remove(tmp_file_map)
