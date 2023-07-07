# background image functions
# ==========================
# get_image_size()
# get_image()
# add_image_background()

import os
import warnings
import uuid
import matplotlib
from matplotlib import gridspec
import matplotlib.pyplot as plt
from matplotlib import axes
from matplotlib.testing.compare import compare_images


def test_get_image_size():

    try:
        from vizent.background_image import get_image_size
        image_file = os.path.join('tests', 'default_images', 'UK_basemap.png')
        aspx, aspy = get_image_size(image_file)
        assert (aspx, aspy) == (640, 480)
    except ImportError:
        warnings.warn("Pytest unable to import PIL."
                      " Background image functionality not tested.")


def test_get_image():
    try: 
        from vizent.background_image import get_image
        
        image_type = 'newcastle'
        x = [425675, 425320]
        y = [562325, 562800]
        image, extent = get_image(x,y,image_type,None)
        assert image == "{0}\\images\\{1}".format(
                                        os.path.dirname(os.path.split(
                                        os.path.abspath(__file__))[0]),
                                        '425562.png')
        assert extent == [425000, 426000, 562000, 563000]

        image_type = 'newcastle'
        x = [423700, 426000]
        y = [562325, 565000]
        image, extent = get_image(x,y,image_type,None)
        assert image ==  "{0}\\images\\{1}".format(
                                         os.path.dirname(os.path.split(
                                        os.path.abspath(__file__))[0]),
                                        'all.png')
        assert extent == []
        
        image_type = 'newcastle'
        x = [421000]
        y = [562000]
        image, extent = get_image(x,y,image_type,None)
        assert image ==  "{0}\\images\\{1}".format(
                                        os.path.dirname(os.path.split(
                                        os.path.abspath(__file__))[0]),
                                        'no_map.png')
        assert extent == []

        image_type = "england"
        x = [-1, 1]
        y = [50, 54]
        image, extent = get_image(x,y,image_type,None)
        assert image == "{0}\\images\\{1}".format(
                                        os.path.dirname(os.path.split(
                                        os.path.abspath(__file__))[0]),
                                        'england_map.png')
        assert extent == [-6,2,49.9,56]
    
        image_type = None
        image_file = "default_images\\UK_basemap.png"
        x = [-1, 1]
        y = [50, 54]
        image, extent = get_image(x,y,image_type,image_file)
        assert image == image_file
        assert extent == []

    except ImportError:
        warnings.warn("Pytest unable to import PIL. "
                      "Background image functionality not tested.")


def test_add_image_background(): 
    try: 
        matplotlib.use('qtagg')
    except ImportError:
        warnings.warn("The default images for this test have been created "
                      "using the qtagg backend for matplotlib. This backend is"
                      " unavailable in your current python distribution. This "
                      " test may therefore fail")

    try:
        from vizent.background_image import add_image_background
        fig = plt.figure(figsize=(6.4,4.8))
        ax1 = fig.add_subplot()
        image_file = os.path.join('tests', 'default_images', 
                                  'UK_basemap.png')
        extent = [0,1,0,1]
        add_image_background(image_file, ax1, extent)
        
        tmp_file = 'tmp_background_images_test.png' #%s.png' % uuid.uuid1()
        # save to a temporary file
        plt.savefig(os.path.join('tests', tmp_file))

        assert type(ax1) == axes.Axes
        expected = os.path.join('tests', 'default_images', 
                                'Background_image_test.png')
        actual = os.path.join('tests', tmp_file)
        
        assert compare_images(expected=expected,
                    actual=actual, 
                    tol=0) is None

        os.remove(os.path.join('tests', tmp_file))
    
    except ImportError:
        warnings.warn("Pytest unable to import PIL. "
                      "Background image functionality not tested.")
